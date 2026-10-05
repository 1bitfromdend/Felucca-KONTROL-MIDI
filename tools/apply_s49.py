#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parents[1]
midi = root / "upstream" / "firmware" / "src" / "midi_control.c"
test = root / "upstream" / "tests" / "midi_control_test.c"

s = midi.read_text()

insert_before = """static void midi_control(uint32_t ch, uint32_t cc, uint32_t value)
{
    midi_channel_t *c = midi_channel(ch);
    uint32_t i, mask;
"""
if insert_before not in s:
    raise SystemExit("midi_control.c anchor not found")

s49_block = r'''/* Native Instruments Kontrol S49 MK3 direct-control map.
 *
 * The S49 template uses absolute CC values (0..127). Every message follows
 * Felucca's normal channel routing, so CH1..4 control tracks 1..4 with
 * ROUT=CH1-4; ROUT=SEL keeps the selected-track behaviour.
 *
 * Page 1: CC20..23 = current engine HOME knobs 1..4,
 *         CC24 ATK, CC25 REL, CC26 DLY, CC27 REV.
 * Page 2: CC28 DEC, CC29 SUS, CC30 DIST, CC31 CHOR,
 *         CC32 LEVEL, CC33 PAN, CC34 LFO RATE, CC35 GLIDE.
 * Page 3: CC36..43 = engine parameters E1..E8.
 */
static uint32_t s49_param_id(const track_t *t, uint32_t cc)
{
    static const uint8_t FIXED[] = {
        P_ATK, P_REL, P_DLY, P_REV,
        P_DEC, P_SUS, P_DIST, P_CHOR,
        P_LEVEL, P_PAN, P_LRATE, P_GLIDE
    };
    if (cc >= 20u && cc <= 23u)
        return ENGINES[eng_idx(t->eng_req)]->knob[cc - 20u];
    if (cc >= 24u && cc <= 35u)
        return FIXED[cc - 24u];
    if (cc >= 36u && cc <= 43u)
        return P_E0 + cc - 36u;
    return P_COUNT;
}

static int s49_control(uint32_t ch, uint32_t cc, uint32_t value)
{
    track_t *t = midi_track(ch);
    uint32_t id = s49_param_id(t, cc);
    const param_desc_t *d;
    int32_t v;

    if (id >= P_COUNT)
        return 0;

    d = track_desc(t, id);
    if (!d || d->max < d->min)
        return 1;

    v = d->min + ((int32_t)(d->max - d->min) * (int32_t)value + 63) / 127;
    if (d->fmt == F_ENUM)
        v = enum_orig(d, v);

    t->p[id] = (int16_t)clamp(v, d->min, d->max);
    return 1;
}

'''

replacement = s49_block + insert_before.replace(
    "    uint32_t i, mask;\n",
    "    uint32_t i, mask;\n    if (s49_control(ch, cc, value))\n        return;\n"
)
s = s.replace(insert_before, replacement, 1)
midi.write_text(s)

t = test.read_text()
test_anchor = '''    bad += check("existing modwheel/expression/aftertouch stay routed to the track", t->mw == 87 && t->ex_off == 104 && t->at == 90);
'''
if test_anchor not in t:
    raise SystemExit("midi_control_test.c anchor not found")

test_block = test_anchor + r'''    {
        uint32_t home = ENGINES[eng_idx(t->eng_req)]->knob[0];
        const param_desc_t *hd = track_desc(t, home);
        queued(0xB0, 20, 127, 1);
        bad += check("S49 CC20 controls the current engine's first HOME knob", t->p[home] == hd->max);

        queued(0xB0, 24, 0, 1);
        bad += check("S49 CC24 controls attack", t->p[P_ATK] == track_desc(t, P_ATK)->min);

        queued(0xB1, 27, 127, 1);
        bad += check("S49 CC routing follows MIDI channel to track 2",
                     trk[1].p[P_REV] == track_desc(&trk[1], P_REV)->max &&
                     t->p[P_REV] != track_desc(t, P_REV)->max);

        queued(0xB0, 33, 64, 1);
        bad += check("S49 bipolar PAN maps MIDI centre to zero", t->p[P_PAN] == 0);

        queued(0xB0, 36, 127, 1);
        bad += check("S49 CC36 reaches engine parameter E1",
                     t->p[P_E0] == track_desc(t, P_E0)->max);
    }
'''
t = t.replace(test_anchor, test_block, 1)
test.write_text(t)

print("Applied Felucca S49 Edition patch")
