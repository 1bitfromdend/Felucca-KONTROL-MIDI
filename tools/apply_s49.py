#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parents[1]
src = root / "upstream" / "firmware" / "src"
midi = src / "midi_control.c"
panel = src / "panel.c"
ui_input = src / "ui_input.c"
ui_layer = src / "ui_layer.c"
main = src / "main.c"
ui_draw = src / "ui_draw.c"
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
 * Performance / parameter control:
 *   CC20..23 = current engine HOME knobs 1..4
 *   CC24 ATK, CC25 REL, CC26 DLY, CC27 REV
 *   CC102 DEC, CC103 SUS, CC104 DIST, CC105 CHOR
 *   CC106 LEVEL, CC107 PAN, CC108 LFO RATE, CC109 GLIDE
 *   CC110..117 = engine parameters E1..E8
 *
 * Full virtual FM-1 panel (MIDI channel 16 only):
 *   CC70..76 = SELECT, ALGORITHM, PRESETS, KNOB1..4
 *               Kontrol mode: Relative Offset (64 centre, 65 = +1, 63 = -1)
 *   CC80..93 = FX, SCL, ENV, LFO, EDIT, GLO, HOME, SAVE,
 *               ARP, SEQ, PLAY, REC, OCT-, OCT+
 *               Kontrol mode: Gate (127 while held, 0 on release)
 *
 * The panel channel is deliberately CH16: CH1..4 remain musical track channels.
 * Felucca 1.1.5.1 normally ignores CH5..16 in ROUT=CH1-4. The S49 Edition
 * exempts only its own CH16 CC map from that filter, so the remote panel and
 * direct parameter pages keep working in either ROUT mode while ordinary
 * CH16 notes/controllers retain upstream behaviour. CH16 S49 parameters edit
 * whichever track is selected.
 *
 * CC32..63 are intentionally avoided for the absolute parameter pages: they are
 * the LSB half of standard 14-bit MIDI controllers; CC38 in particular is RPN
 * Data Entry LSB.
 */
#define FELUCCA_S49_PANEL 1
#define S49_PANEL_CH 15u
#define S49_PANEL_ENC_FIRST 70u
#define S49_PANEL_BTN_FIRST 80u

enum {
    S49_B_FX, S49_B_SCL, S49_B_ENV, S49_B_LFO, S49_B_EDIT, S49_B_GLO, S49_B_HOME, S49_B_SAVE,
    S49_B_ARP, S49_B_SEQ, S49_B_PLAY, S49_B_REC, S49_B_OCTDN, S49_B_OCTUP, S49_NB
};
enum { S49_EN_SELECT, S49_EN_ALGO, S49_EN_PRESET, S49_EN_K1, S49_EN_K2, S49_EN_K3, S49_EN_K4, S49_NE };

static uint16_t s49_panel_down;
static uint16_t s49_panel_pressed;
static int16_t s49_panel_enc_delta[S49_NE];

static int s49_panel_control(uint32_t ch, uint32_t cc, uint32_t value)
{
    if (ch != S49_PANEL_CH)
        return 0;

    if (cc >= S49_PANEL_BTN_FIRST && cc < S49_PANEL_BTN_FIRST + S49_NB) {
        uint16_t bit = (uint16_t)(1u << (cc - S49_PANEL_BTN_FIRST));
        if (value >= 64u) {
            if (!(s49_panel_down & bit))
                s49_panel_pressed |= bit;
            s49_panel_down |= bit;
        } else {
            s49_panel_down &= (uint16_t)~bit;
        }
        return 1;
    }

    if (cc >= S49_PANEL_ENC_FIRST && cc < S49_PANEL_ENC_FIRST + S49_NE) {
        uint32_t e = cc - S49_PANEL_ENC_FIRST;
        int32_t d = value > 64u ? (int32_t)value - 64 : value < 64u ? -((int32_t)64 - (int32_t)value) : 0;
        int32_t v = (int32_t)s49_panel_enc_delta[e] + d;
        s49_panel_enc_delta[e] = (int16_t)clamp(v, -127, 127);
        return 1;
    }

    return 0;
}

static uint32_t s49_panel_take_pressed(void)
{
    uint32_t p = s49_panel_pressed;
    s49_panel_pressed = 0;
    return p;
}

static int32_t s49_panel_enc_take(uint32_t role)
{
    int32_t v;
    if (role >= S49_NE)
        return 0;
    v = s49_panel_enc_delta[role];
    s49_panel_enc_delta[role] = 0;
    return v;
}

static uint32_t s49_param_id(const track_t *t, uint32_t cc)
{
    static const uint8_t FIXED[] = {
        P_ATK, P_REL, P_DLY, P_REV,
        P_DEC, P_SUS, P_DIST, P_CHOR,
        P_LEVEL, P_PAN, P_LRATE, P_GLIDE
    };
    if (cc >= 20u && cc <= 23u)
        return ENGINES[eng_idx(t->eng_req)]->knob[cc - 20u];
    if (cc >= 24u && cc <= 27u)
        return FIXED[cc - 24u];
    if (cc >= 102u && cc <= 109u)
        return FIXED[4u + cc - 102u];
    if (cc >= 110u && cc <= 117u)
        return P_E0 + cc - 110u;
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
    "    uint32_t i, mask;\n    if (s49_panel_control(ch, cc, value))\n        return;\n    if (s49_control(ch, cc, value))\n        return;\n"
)
s = s.replace(insert_before, replacement, 1)

# Felucca 1.1.5.1 deliberately ignores CH5..16 while ROUT=CH1-4. Keep that
# upstream rule for ordinary MIDI, but allow the dedicated S49 CH16 CC map
# through so the existing template and wiring remain valid in both ROUT modes.
route_anchor = """static void __attribute__((noinline)) midi_event(uint32_t st, uint32_t ch, uint32_t d1, uint32_t d2)
{
    if (ch >= NPART && !song.g[G_ROUTE])
        return;
"""
if route_anchor not in s:
    raise SystemExit("midi_control.c ROUT anchor not found")

route_replacement = """static void __attribute__((noinline)) midi_event(uint32_t st, uint32_t ch, uint32_t d1, uint32_t d2)
{
    if (ch >= NPART && !song.g[G_ROUTE] &&
        !(st == 0xB0u && ch == S49_PANEL_CH &&
          ((d1 >= 20u && d1 <= 27u) || (d1 >= 70u && d1 <= 76u) ||
           (d1 >= 80u && d1 <= 93u) || (d1 >= 102u && d1 <= 117u))))
        return;
"""
s = s.replace(route_anchor, route_replacement, 1)
midi.write_text(s)

# Merge the virtual S49 buttons/encoders with the real FM-1 panel at the
# panel abstraction boundary. This preserves Felucca's original page, layer,
# tap/hold, dialog, transport and contextual-knob behaviour.
p = panel.read_text()
panel_anchor = '''/* steps of a role, + = clockwise */
static uint8_t panel_moved;                     /* a knob turned since ui.c scr_input last looked (SCREEN OFF) */
static int32_t panel_enc(uint32_t role)
{
    int32_t s = fm1_enc_take(panel.enc[role]) * panel.dir[role];
    if (s)
        panel_moved = 1;
    return s;
}
'''
if panel_anchor not in p:
    raise SystemExit("panel.c v1.1.5.1 encoder anchor not found")
panel_replacement = '''#ifdef FELUCCA_S49_PANEL
/* CH16 Kontrol virtual panel shares the physical panel's logical button mapping. */
static uint32_t s49_panel_matrix_bits(uint32_t logical)
{
    uint32_t b, m = 0;
    for (b = 0; b < NB; b++)
        if ((logical >> b) & 1u)
            m |= 1u << panel.btn[b];
    return m;
}
static uint32_t panel_buttons(void)
{
    return fm1_in.buttons | s49_panel_matrix_bits(s49_panel_down);
}
static uint32_t panel_pressed_take(void)
{
    return fm1_input_edges(0) | s49_panel_matrix_bits(s49_panel_take_pressed());
}
/* steps of a role, + = clockwise */
static uint8_t panel_moved;
static int32_t panel_enc(uint32_t role)
{
    int32_t s = fm1_enc_take(panel.enc[role]) * panel.dir[role] + s49_panel_enc_take(role);
    if (s)
        panel_moved = 1;
    return s;
}
#else
static uint8_t panel_moved;
/* Macro fallback: settings_test.c includes panel.c without declaring fm1_in.
 * Expand these only in UI code where fm1_in is available. */
#define panel_buttons() (fm1_in.buttons)
#define panel_pressed_take() fm1_input_edges(0)
static int32_t panel_enc(uint32_t role)
{
    int32_t s = fm1_enc_take(panel.enc[role]) * panel.dir[role];
    if (s)
        panel_moved = 1;
    return s;
}
#endif
'''
p = p.replace(panel_anchor, panel_replacement, 1)
panel.write_text(p)

u = ui_input.read_text()
if "uint32_t pressed = fm1_input_edges(0)" not in u:
    raise SystemExit("ui_input.c edge anchor not found")
u = u.replace("uint32_t pressed = fm1_input_edges(0)", "uint32_t pressed = panel_pressed_take()", 1)
u = u.replace("fm1_in.buttons", "panel_buttons()")
ui_input.write_text(u)

l = ui_layer.read_text()
if "fm1_in.buttons" not in l:
    raise SystemExit("ui_layer.c button anchor not found")
l = l.replace("fm1_in.buttons", "panel_buttons()")
ui_layer.write_text(l)

# Since 1.1.5 the boot splash lives in ui_draw.c. Preserve Felucca's
# credits and version, and add the KONTROL EDITION mark inside the 176px square.
d = ui_draw.read_text()
begin = d.find("static void draw_splash(void)")
end = d.find("/* UPDATE MODE countdown", begin)
if begin < 0 or end < 0:
    raise SystemExit("ui_draw.c Felucca 1.1.5.1 splash anchors not found")
segment = d[begin:end]
needle = "    lcd_sync();"
if segment.count(needle) != 1:
    raise SystemExit("ui_draw.c splash sync anchor not unique")
segment = segment.replace(needle, '    draw_text_box(SPL_X0, SPL_X0 + SPL_SQ / 2u - AF_S.h / 2u, SPL_SQ, &AF_S, "KONTROL EDITION", T_REC, 1);\n    lcd_sync();', 1)
d = d[:begin] + segment + d[end:]
ui_draw.write_text(d)

t = test.read_text()
reset_anchor = '''    fm1_in.notes = kb_prev = 0; fm1_ms = 0; song.sel = 0;
'''
if reset_anchor not in t:
    raise SystemExit("midi_control_test.c reset anchor not found")
t = t.replace(reset_anchor, '''    fm1_in.notes = kb_prev = 0; fm1_ms = 0; song.sel = 0;
    s49_panel_down = s49_panel_pressed = 0;
    memset(s49_panel_enc_delta, 0, sizeof s49_panel_enc_delta);
''', 1)

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

        queued(0xB0, 107, 64, 1);
        bad += check("S49 bipolar PAN maps MIDI centre to zero", t->p[P_PAN] == 0);

        queued(0xB0, 110, 127, 1);
        bad += check("S49 CC110 reaches engine parameter E1",
                     t->p[P_E0] == track_desc(t, P_E0)->max);

        song.sel = 0;
        queued(0xBF, 71, 65, 1); ui_input();
        bad += check("S49 CH16 virtual ALGORITHM encoder selects the next track", song.sel == 1u);
        queued(0xBF, 71, 63, 1); ui_input();
        bad += check("S49 CH16 virtual ALGORITHM encoder selects the previous track", song.sel == 0u);

        queued(0xBF, 80, 127, 1); ui_input();
        bad += check("S49 CH16 Gate button holds the virtual FX panel button",
                     (panel_buttons() & (1u << panel.btn[B_FX])) != 0u);
        queued(0xBF, 80, 0, 1); ui_input();
        bad += check("S49 CH16 FX release behaves like the physical panel tap", cur_fam() == FAM_FX);

        queued(0xBF, 86, 127, 1); ui_input();
        queued(0xBF, 86, 0, 1); ui_input();
        bad += check("S49 CH16 HOME press/release returns to HOME", ui.home != 0u);

        song.octave = 0;
        queued(0xBF, 93, 127, 1); ui_input();
        queued(0xBF, 93, 0, 1); ui_input();
        bad += check("S49 CH16 OCT+ behaves like the physical OCT+ button", song.octave == 1);
    }
'''
t = t.replace(test_anchor, test_block, 1)
# Upstream's "unknown CC" check uses CC20, now intentionally claimed by our
# HOME 1 mapping. Test genuinely unassigned CC54 instead.
unknown_cc = "queued(0xB0, 20, 99, 1); queued(0xB0, 76, 99, 1); queued(0xB0, 95, 99, 1);"
if unknown_cc not in t:
    raise SystemExit("midi_control_test.c unknown CC anchor not found")
t = t.replace(unknown_cc, "queued(0xB0, 54, 99, 1); queued(0xB0, 76, 99, 1); queued(0xB0, 95, 99, 1);", 1)
test.write_text(t)

print("Applied Felucca S49 Edition full-panel patch")
