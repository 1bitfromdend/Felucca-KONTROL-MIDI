#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parents[1]
src = root / "upstream" / "firmware" / "src"
midi = src / "midi_control.c"
panel = src / "panel.c"
ui_input = src / "ui_input.c"
ui_layer = src / "ui_layer.c"
main = src / "main.c"
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
 * Felucca routes channels above CH4 to the selected track, so the absolute
 * parameter pages may also use CH16 to edit whichever track is selected.
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
midi.write_text(s)

# Merge the virtual S49 buttons/encoders with the real FM-1 panel at the
# panel abstraction boundary. This preserves Felucca's original page, layer,
# tap/hold, dialog, transport and contextual-knob behaviour.
p = panel.read_text()
panel_anchor = '''static uint32_t panel_btn_of(uint32_t matrix_id)        /* label of a matrix button, NB if none */
{
    uint32_t b;
    for (b = 0; b < NB; b++)
        if (panel.btn[b] == matrix_id)
            return b;
    return NB;
}

/* steps of a role, + = clockwise */
static int32_t panel_enc(uint32_t role)
{
    return fm1_enc_take(panel.enc[role]) * panel.dir[role];
}
'''
if panel_anchor not in p:
    raise SystemExit("panel.c anchor not found")

panel_replacement = '''static uint32_t panel_btn_of(uint32_t matrix_id)        /* label of a matrix button, NB if none */
{
    uint32_t b;
    for (b = 0; b < NB; b++)
        if (panel.btn[b] == matrix_id)
            return b;
    return NB;
}

#ifdef FELUCCA_S49_PANEL
/* S49 virtual-panel state uses logical button ids in the same order as B_FX..B_OCTUP.
 * Convert them through the calibrated physical-panel table only at this boundary, so a
 * calibrated FM-1 and the S49 still address the same printed controls. */
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

/* steps of a role, + = clockwise. The S49 uses Relative Offset: 65 = +1, 63 = -1. */
static int32_t panel_enc(uint32_t role)
{
    return fm1_enc_take(panel.enc[role]) * panel.dir[role] + s49_panel_enc_take(role);
}
#else
/* Standalone panel/settings host tests include panel.c without the MIDI engine. */
static int32_t panel_enc(uint32_t role)
{
    return fm1_enc_take(panel.enc[role]) * panel.dir[role];
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

m = main.read_text()
splash_anchor = '''    draw_text_box(0, 94, 240, &AF_L, "FELUCCA", T_THEME, 1);
    draw_text_box(0, 134, 240, &AF_S, "MULTI-ENGINE SYNTH", T_MID, 1);
'''
if splash_anchor not in m:
    raise SystemExit("main.c splash anchor not found")
m = m.replace(splash_anchor, '''    draw_text_box(0, 94, 240, &AF_L, "FELUCCA", T_THEME, 1);
    draw_text_box(0, 134, 240, &AF_S, "MULTI-ENGINE SYNTH", T_MID, 1);
    draw_text_box(0, 156, 240, &AF_S, "S49 EDITION", T_THEME, 1);
''', 1)
main.write_text(m)

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
test.write_text(t)

print("Applied Felucca S49 Edition full-panel patch")
