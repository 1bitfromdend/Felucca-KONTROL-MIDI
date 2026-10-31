# Felucca-KONTROL-MIDI

## Current release — Felucca 1.8.0 KONTROL EDITION (hardware verified 2026-10-31)

**Confirmed working on an actual M-VAVE FM-1 and Native Instruments Kontrol S49 MK3 on 31 October 2026.** After installing the custom `.fwsc` on Windows, the owner reported that the **FM-1 worked** and subsequently that **everything worked perfectly on the Kontrol**. The full KONTROL setup is therefore marked **hardware verified (user-confirmed)**, not experimental. This is the user's overall functional report; it is not an independently instrumented check of every CC, mode, or combination, and does not constitute a separate test on S61/S88.

**Automated validation also passed:** [GitHub Actions build #41229560226](https://github.com/1bitfromdend/Felucca-KONTROL-MIDI/actions/runs/41229560226) successfully compiled Felucca v1.8.0 with the KONTROL patch, ran the host/MIDI and UI regression suite and uploaded the installable firmware. The dedicated **CH16** virtual panel/encoder and direct parameter controls are included. The 1.8 source and workflow have been [merged into `main`](https://github.com/1bitfromdend/Felucca-KONTROL-MIDI/pull/2).

| Validation | Result | Evidence |
|---|---|---|
| Firmware build, host MIDI tests and UI checks | **PASS** | [Actions run #41229560226](https://github.com/1bitfromdend/Felucca-KONTROL-MIDI/actions/runs/41229560226) |
| FM-1 detected by the Windows USB-MIDI installer | **PASS** | Owner ran `py -3.12 fm1_install.py --info` and reported `[running]` |
| Felucca 1.8.0 KONTROL firmware installed; FM-1 running | **PASS** | Owner's physical test, 2026-10-31 |
| S49 MK3 KONTROL functionality | **PASS (owner-confirmed overall operation)** | Owner reported that all functions work perfectly |
| S61/S88 MK3 physical test | **Not separately tested** | Common S-Series MK3 MIDI template/protocol; no separate device report |

### Download the verified custom firmware

Open the [successful KONTROL 1.8 build](https://github.com/1bitfromdend/Felucca-KONTROL-MIDI/actions/runs/41229560226) and under **Artifacts** download **`felucca-1.8.0-kontrol`**. Unzip it to obtain **`felucca-1.8.0-kontrol.fwsc`**. GitHub may require sign-in and artifacts can expire. **Do not install the unmodified upstream Felucca build** if you want the S49 controller integration.

The official updater compatible with v1.8.0 is [`fm1_install.py` from Felucca v1.8.0](https://github.com/hugelton/Felucca/blob/v1.8.0/tools/fm1_install.py). Place it next to the `.fwsc` and, on Windows with the existing Python 3.12/mido setup, verify connectivity before flashing:

```powershell
py -3.12 fm1_install.py --info
```

The separate installation command is:

```powershell
py -3.12 fm1_install.py felucca-1.8.0-kontrol.fwsc
```

Confirm at the updater prompt; do not disconnect during flashing. The KONTROL MIDI template `FM-01.kmt` is imported on the S-Series MK3 separately.

### Older hardware-tested version — Felucca 1.1.5.1

The earlier **1.1.5.1 KONTROL EDITION** was also physically verified on 2026-10-08. Its source/history remains available on [`port-felucca-1.1.5.1`](https://github.com/1bitfromdend/Felucca-KONTROL-MIDI/tree/port-felucca-1.1.5.1) and in the repository history. The old firmware and 1.8 packages must not be confused.

---

Full MIDI remote-control patch for **Native Instruments Kontrol S-Series MK3 (S49 MK3 / S61 MK3 / S88 MK3) + M-VAVE FM-1 running Felucca 1.8.0**.

The purpose of this build is to use a Kontrol S-Series MK3 keyboard as the main performance and editing surface for Felucca:

- play Felucca tracks from the Kontrol keyboard
- edit the selected track from 24 absolute parameter controls
- reproduce the FM-1's digital panel buttons over MIDI
- reproduce the FM-1's seven digital encoders over MIDI
- keep Felucca's original MIDI behaviour, including sustain, pitch bend, aftertouch and modulation

The repository stores the firmware patch, build workflow and ready-to-import Kontrol S-Series MK3 MIDI template. The same MIDI control architecture applies to **S49 MK3, S61 MK3 and S88 MK3**; the number of keys does not affect the CC/button/encoder mapping. The active GitHub Actions workflow uses upstream tag **v1.8.0**, applies `tools/apply_s49_1_8.py`, runs host and UI tests, and produces the installable `.fwsc`. The 1.1.5.1 build pipeline is retained as legacy.

The custom build identifies itself at boot with **KONTROL EDITION** in red, inside the original centred 176 × 176-pixel Felucca splash on the FM-1's 240 × 240 display. The official Felucca/version/credits remain visible. The technical package identity used by the installer is unchanged.

## Previous 1.1.5.1 release — tested on hardware (2026-10-08)

**Felucca 1.1.5.1 KONTROL EDITION** was the previous version, tested on the physical FM-1 and S49 MK3. The [verified build #27](https://github.com/1bitfromdend/Felucca-KONTROL-MIDI/actions/runs/37806364726) completed all GitHub Actions checks, including firmware compilation, splash UI preflight, Felucca host tests, and upload of the installable artifact. [Build #26](https://github.com/1bitfromdend/Felucca-KONTROL-MIDI/actions/runs/37806346527) also passed.

**Physical test configuration:** M-VAVE FM-1, Native Instruments **Kontrol S49 MK3**, `FM-01.kmt` template, Kontrol MIDI OUT to FM-1 TRS MIDI IN, Felucca `ROUT=SEL`. The firmware was installed with the Python installer on Windows; `py -3.12 fm1_install.py --info` identified the device as `FM-1_910 [running]` on `Felucca 0` before flashing.

The following controls were tested on hardware and reported working:

| Area | Verified behaviour |
|---|---|
| Installation / boot | Firmware starts; red `KONTROL EDITION` splash appears |
| Keyboard and routing | S49 keys play the selected Felucca track with `ROUT=SEL` |
| Navigation | TRACK selects tracks 1–4; PRESET browses sounds |
| Contextual encoders | KNOB1–4 adjust the currently shown HOME parameters |
| Page navigation | ENV, FX, LFO, EDIT, GLO and HOME open/return to the expected pages |
| Hold | Holding HOME opens Felucca's menu |
| Sound editing | ATTACK and RELEASE respond from the S49 parameter page |
| Sequencer | PLAY and REC controls respond |
| Menu navigation | OCT− and OCT+ operate back/confirm where applicable |

**Scope of validation:** these are the functions actually checked with the S49 MK3. Other supported controller mappings and gestures are covered by source/host tests or documented as implemented but have not all been exercised on physical hardware. S61 MK3 and S88 MK3 use the same MIDI control protocol but were not physically tested. The previous Felucca 1.0.5.2 version remains available in the [archive/felucca-1.0.5.2-kontrol](https://github.com/1bitfromdend/Felucca-KONTROL-MIDI/tree/archive/felucca-1.0.5.2-kontrol) branch.

---

---

## 1. MIDI architecture

### Musical tracks

Felucca 1.8.0 offers multiple routing modes; common modes for the included S49 template are:

| ROUT mode | Musical MIDI routing |
|---|---|
| `CH1-4` | CH1 → Track 1, CH2 → Track 2, CH3 → Track 3, CH4 → Track 4; CH5..CH16 are ignored by upstream Felucca |
| `SEL` | CH1..CH16 play the currently selected track |
| `CH5-8`, `CH9-12`, `CH13-16` | Each block of four channels plays tracks 1..4 respectively |
| `TRACK` | MIDI channel per track can be configured individually; tracks can also use OMNI or OFF |

For the included template, set **`ROUT=SEL` on Felucca** and leave the Kontrol keybed on **CH1**. The full keyboard then plays the currently selected track. Turn the **TRACK** knob (CC71 on CH16) to change tracks without editing the template or splitting the keyboard.

The Kontrol S-Series MK3 Edition keeps its dedicated **CH16 custom CC map active independently of the selected ROUT mode**. Only the reserved S49 remote-control CCs bypass a musical routing filter; ordinary CH16 notes and controllers still follow upstream Felucca routing.

A Kontrol S-Series MK3 split / zone setup can therefore use CH1..CH4 for fixed-track playing in `ROUT=CH1-4`, while the S49 remote panel on CH16 remains available.

### Dedicated remote-control channel

**MIDI CH16 is the Kontrol S-Series MK3 Edition panel-control channel.**

Use CH16 for:

- the 24 absolute Kontrol parameter controls
- the virtual FM-1 panel buttons
- the virtual FM-1 panel encoders

The panel commands themselves are consumed by the Kontrol S-Series MK3 Edition firmware and do not become ordinary Felucca parameter CCs.

---

## 2. Recommended Kontrol S-Series MK3 control modes

| Control type | Kontrol mode | MIDI channel |
|---|---|---:|
| MAIN / SHAPE / ENGINE parameter knobs | CC, Absolute, 0..127 | 16 |
| Virtual FM-1 encoders | CC, Relative Offset | 16 |
| Virtual FM-1 buttons | CC, Gate, Off 0 / On 127 | 16 |
| Included template keybed (`ROUT=SEL`) | Note On / Note Off | 1 |
| Optional fixed-track keyboard zones (`ROUT=CH1-4`) | Note On / Note Off | 1..4 |
| Mod wheel | CC1 | track channel |
| Expression | CC11 | track channel |
| Sustain pedal | CC64 | track channel |
| Pitch bend | Pitch Bend | track channel |
| Aftertouch | Channel Pressure | track channel |

For Relative Offset controls, the firmware interprets:

- `64` = no movement
- `65` = +1
- `63` = -1
- values farther from 64 = larger relative moves

---

# 3. Kontrol parameter pages

These controls are **absolute 0..127 CCs**.

Putting them on **CH16** makes them edit the currently selected Felucca track.

## Page 1 — MAIN

| Kontrol knob | CC | Felucca parameter |
|---:|---:|---|
| 1 | 20 | Engine HOME knob 1 |
| 2 | 21 | Engine HOME knob 2 |
| 3 | 22 | Engine HOME knob 3 |
| 4 | 23 | Engine HOME knob 4 |
| 5 | 24 | Attack |
| 6 | 25 | Release |
| 7 | 26 | Delay send |
| 8 | 27 | Reverb send |

### Dynamic HOME controls

CC20..23 are deliberately dynamic.

They always control the four parameters exposed by the **currently loaded engine on Felucca's HOME page**.

Changing engine therefore changes what CC20..23 control, exactly as the four physical HOME knobs change function with the engine.

---

## Page 2 — SHAPE / MIX

| Kontrol knob | CC | Felucca parameter |
|---:|---:|---|
| 1 | 102 | Decay |
| 2 | 103 | Sustain |
| 3 | 104 | Distortion |
| 4 | 105 | Chorus send |
| 5 | 106 | Track level |
| 6 | 107 | Pan |
| 7 | 108 | LFO rate |
| 8 | 109 | Glide |

The firmware scales MIDI 0..127 to the real Felucca descriptor range, including bipolar parameters such as PAN.

---

## Page 3 — ENGINE

| Kontrol knob | CC | Felucca parameter |
|---:|---:|---|
| 1 | 110 | Engine E1 |
| 2 | 111 | Engine E2 |
| 3 | 112 | Engine E3 |
| 4 | 113 | Engine E4 |
| 5 | 114 | Engine E5 |
| 6 | 115 | Engine E6 |
| 7 | 116 | Engine E7 |
| 8 | 117 | Engine E8 |

E1..E8 are Felucca's engine-specific EDIT parameters.

Their meaning changes with the current engine.

Example: on FM6 the engine parameters include its FM-specific controls, including the algorithm parameter.

---

## Why CC32..63 are not used

CC32..63 are intentionally avoided for the Kontrol S-Series MK3 Edition absolute parameter pages because they are the LSB half of standard 14-bit MIDI controller pairs.

In particular:

- CC6 = Data Entry MSB
- CC38 = Data Entry LSB

Felucca uses these for RPN pitch-bend sensitivity, so using CC38 as an ordinary synth parameter would break standard MIDI behaviour.

---

# 4. Virtual FM-1 panel buttons

These controls reproduce the **digital buttons on the physical FM-1 panel**.

Configure every Kontrol button as:

- Type: **Control Change**
- Mode: **Gate**
- Off Value: **0**
- On Value: **127**
- MIDI Channel: **16**

The firmware keeps the button held for as long as the Kontrol sends the Gate-on state, and releases it when the Kontrol sends 0.

That means Felucca still sees real **press / hold / release** behaviour rather than a simplified one-shot command.

| CC | Virtual FM-1 button | Normal action |
|---:|---|---|
| 80 | FX | Open / advance FX pages |
| 81 | SCL | Open / advance Scale / Chord pages |
| 82 | ENV | Open / advance Envelope pages |
| 83 | LFO | Open / advance LFO pages |
| 84 | EDIT | Open / advance engine EDIT pages |
| 85 | GLO | Open / advance global / mixer-related pages |
| 86 | HOME | Return to HOME |
| 87 | SAVE | Open SAVE pages |
| 88 | ARP | Open / advance ARP pages |
| 89 | SEQ | Open / advance sequencer pages |
| 90 | PLAY | Start / stop transport |
| 91 | REC | Arm / disarm recording on selected track |
| 92 | OCT- | Octave down / back / cancel depending on context |
| 93 | OCT+ | Octave up / enter / confirm depending on context |

---

# 5. Tap and hold behaviour

Because the virtual buttons preserve Gate state, the following original Felucca gestures are retained.

| Button | Tap | Hold |
|---|---|---|
| HOME | Return HOME | Open / close menu |
| SAVE | Open SAVE | Undo last sound load / change where Felucca supports undo |
| SEQ | Open sequencer pages | Open SONG page |
| FX | Open FX page | Open FX quick layer |
| GLO | Open global / mixer pages | Open GLO quick layer |
| SCL | Open Scale / Chord pages | Open SCL quick layer |
| EDIT | Open EDIT pages | Open EDIT quick layer |
| REC | Arm / disarm selected track | No separate hold action |
| PLAY | Start / stop | Contextual with Felucca layers |
| ENV | Open / advance ENV pages | No quick layer |
| LFO | Open / advance LFO pages | No quick layer |
| ARP | Open / advance ARP pages | No quick layer |

Felucca's hold threshold and state machine remain the upstream implementation; the Kontrol S-Series MK3 Edition does not duplicate that logic.

---

# 6. OCT- / OCT+ behaviour

The two octave buttons remain contextual, just like the physical FM-1.

### Normal playing

- OCT- = shift keyboard down one octave
- OCT+ = shift keyboard up one octave
- OCT- + OCT+ together on the physical panel = reset octave to zero

### Dialogs / action pages / menu

- OCT- = back / cancel
- OCT+ = enter / confirm / execute

### SAVE workflow

The original Felucca workflow is preserved:

1. tap SAVE
2. choose a user slot
3. OCT+ to continue
4. OCT+ again to confirm / enter the naming step

---

# 7. Virtual FM-1 encoders

These reproduce the **seven digital encoders** from the physical FM-1 panel.

Configure them as:

- Type: **Control Change**
- Mode: **Relative Offset**
- MIDI Channel: **16**

| Kontrol knob | CC | Virtual FM-1 encoder | Main Felucca function |
|---:|---:|---|---|
| 1 | 70 | SELECT | BPM / contextual selection |
| 2 | 71 | ALGORITHM | Select Track 1..4 |
| 3 | 72 | PRESETS | Browse sounds / presets where allowed |
| 4 | 73 | KNOB 1 | Current page column 1 |
| 5 | 74 | KNOB 2 | Current page column 2 |
| 6 | 75 | KNOB 3 | Current page column 3 |
| 7 | 76 | KNOB 4 | Current page column 4 |
| 8 | — | Spare | Not assigned |

The virtual encoders are merged at the panel abstraction used by Felucca, so KNOB1..4 remain **context-sensitive**.

Examples:

- on HOME they edit the four engine HOME parameters
- on ENV they edit the current envelope page
- on LFO they edit the current LFO page
- on FX they edit the current FX page
- on SEQ they edit sequencer fields
- on SAVE / action screens they operate whatever the original Felucca page assigns to the physical knobs

### ALGORITHM

Despite the printed FM-1 label, in Felucca **ALGORITHM selects the active track**:

- turn right = next track
- turn left = previous track
- range = Track 1..4

FM6's actual 32-operator-routing algorithms are engine parameters, not this physical ALGORITHM encoder.

### PRESETS

PRESETS browses the selected track's sounds from HOME and the PRESETS browser, including factory engines / sounds and user presets according to Felucca's normal rules.

### SELECT

On the normal interface SELECT sets global BPM. In contextual Felucca screens it retains the original firmware behaviour of the physical SELECT encoder.

---

# 8. Original Felucca page-button behaviour

The Kontrol virtual buttons call the same Felucca page logic as the FM-1 controls.

The following physical-panel model is therefore retained:

- FX, SCL, ENV, LFO, EDIT, GLO, SAVE, ARP and SEQ open their page families
- pressing a page button again advances through that family's pages
- HOME returns to HOME
- PLAY starts / stops the four-track transport
- REC arms the selected track from any normal page
- ALGORITHM selects the current track
- PRESETS selects the sound
- KNOB1..4 edit the current page columns

---

# 9. Quick-layer reference

Felucca provides four quick layers that can be opened by holding the corresponding button, with the upstream double-tap lock gesture.

The virtual S49 buttons preserve press, hold and release state, so the same hold and double-tap layer behaviour is available from the S49.

## FX hold layer

Hold FX for Felucca's performance-effect layer.

Upstream Felucca includes performance actions such as:

- repeat
- reverse
- filter sweeps
- tape stop
- freeze
- harmonizer
- shimmer-related octave actions
- track mutes
- four FX macro knobs

## GLO hold layer

Upstream Felucca's GLO quick layer provides fast mixer / performance actions, including:

- track mute controls
- temporary solo controls
- unmute all
- tap tempo
- KNOB1..4 = Track 1..4 levels
- GLO + PLAY = restart from the top without the ordinary stop/start gesture

## SCL hold layer

The upstream SCL quick layer provides scale / chord setup:

- root selection
- scale selection
- chord mode
- voicing
- KNOB1..4 = ROOT / SCL / CHRD / VOIC

## EDIT hold layer

The upstream EDIT quick layer provides fast engine / sound selection:

- choose engine
- choose that engine's sound
- favourite control
- engine INIT action
- KNOB1 = engine
- KNOB2 = sound number
- KNOB3 = favourite

### Important quick-layer limitation

The Kontrol S-Series MK3 Edition currently virtualizes the **panel buttons and encoders**, not the FM-1's local 27-key hardware matrix.

Therefore the hold layer itself can be opened remotely, and its encoder functions can be controlled remotely, but **key-combination shortcuts that specifically depend on the FM-1's own local keys are not currently generated from ordinary external MIDI notes**.

External Kontrol notes remain musical MIDI input.

---

# 10. Keyboard and performance MIDI

The Kontrol keyboard uses Felucca's normal MIDI note implementation.

### Note routing

With `ROUT=CH1-4`:

| Kontrol MIDI channel | Destination |
|---:|---|
| 1 | Track 1 |
| 2 | Track 2 |
| 3 | Track 3 |
| 4 | Track 4 |
| 5..16 | Ignored for ordinary musical/control MIDI |

With `ROUT=SEL`, all MIDI channels play the currently selected track.

The Kontrol S-Series MK3 Edition's dedicated CH16 remote-control CCs are a deliberate exception to the `CH1-4` filter, so the existing Kontrol template keeps controlling the panel without changing its assignments.

### Note On / Note Off

Standard Note On / Note Off messages are retained.

Velocity is passed into Felucca's existing note path.

### Chord / scale behaviour

MIDI notes pass through Felucca's existing track note logic, including the active chord / scale behaviour implemented by the upstream firmware.

---

# 11. Existing MIDI CC and performance controls retained

The Kontrol S-Series MK3 Edition leaves upstream MIDI controls intact.

| MIDI message | Felucca behaviour |
|---|---|
| CC1 | Mod Wheel modulation source |
| CC11 | Expression modulation source |
| CC64 | Sustain pedal |
| Channel Pressure | Aftertouch modulation source |
| Pitch Bend | Track pitch bend |
| CC120 | All Sound Off |
| CC121 | Reset All Controllers |
| CC123 | All Notes Off |
| CC101 / CC100 | RPN select |
| CC6 | RPN Data Entry MSB |
| CC38 | RPN Data Entry LSB |
| CC99 / CC98 | NRPN select; cancels active RPN data entry |

### Pitch-bend range

Felucca uses **RPN 0** for pitch-bend sensitivity.

- CC101 = 0
- CC100 = 0
- CC6 = semitones, clamped to 0..24
- CC38 = cents, clamped to 0..99

The default bend range remains Felucca's normal **±2 semitones** until changed.

### Sustain

CC64 values:

- 64..127 = pedal down
- 0..63 = pedal up

Drum tracks ignore sustain and pitch bend according to upstream Felucca behaviour.

---

# 12. USB MIDI and TRS MIDI

The custom controls are processed by Felucca's shared MIDI control path.

Therefore the Kontrol S-Series MK3 Edition mappings work through:

- **USB MIDI**
- **TRS MIDI IN**

The custom mapping is not USB-only.

---

# 13. Included Kontrol S-Series MK3 MIDI template

Download [FM-01.kmt](templates/FM-01.kmt) (use GitHub's **Download raw file** button).

This is the two-page template configured for the Kontrol S-Series MK3 Edition firmware. It includes the custom black/red banner originally created on the S49 MK3; the template mapping itself is compatible with S49 MK3, S61 MK3 and S88 MK3. Every display knob and button sends on **CH16**; the single full-range keyzone remains on **CH1**. MIDI output preference is **DIN priority**.

![Felucca Kontrol S-Series MK3 Edition display banner](templates/Felucca-S49-Edition.jpg)

*Embedded display artwork; the Kontrol button labels and knob indicators appear above and below this banner.*

### Import and play

1. Connect the Kontrol to a computer by USB with **NI Hardware Connection Service** installed and running.
2. Open the MIDI Template browser and choose **Import**. Select the downloaded `FM-01.kmt` in the computer's import window and send it to the keyboard.
3. Load the **FM-01** template.
4. Connect the Kontrol **MIDI OUT** to FM-1 **MIDI IN** through the appropriate DIN/TRS connection.
5. Set **`ROUT=SEL` on Felucca**. Leave the Kontrol keybed on CH1.
6. Use **TRACK** on page 1 to select a track. All 49 keys now play that selected track.

Import/export requires a computer; the imported template can then be used standalone. Use the Kontrol Page arrow buttons to switch between its two control pages. The custom artwork requires Kontrol S-Series MK3 firmware with MIDI-template artwork support (introduced in version 1.8).

### Page 1 — panel controls

| Knob | Label | CC | Mode | Function |
|---:|---|---:|---|---|
| 1 | BPM | 70 | Relative Offset, step 1 | SELECT encoder: BPM / contextual selection |
| 2 | TRACK | 71 | Relative Offset, step 1 | Select Track 1..4 |
| 3 | PRESET | 72 | Relative Offset, step 1 | Browse selected track sounds / presets |
| 4 | KNOB1 | 73 | Relative Offset, step 1 | Current FM-1 page column 1 |
| 5 | KNOB2 | 74 | Relative Offset, step 1 | Current FM-1 page column 2 |
| 6 | KNOB3 | 75 | Relative Offset, step 1 | Current FM-1 page column 3 |
| 7 | KNOB4 | 76 | Relative Offset, step 1 | Current FM-1 page column 4 |
| 8 | LEVEL | 106 | Absolute, 0..127 | Selected track level |

KNOB1..4 follow the page open on the FM-1, including HOME, ENV, FX, LFO and EDIT. They provide contextual access beyond the direct controls on page 2.

| Button | Label | CC |
|---:|---|---:|
| 1 | FX | 80 |
| 2 | SCALE | 81 |
| 3 | ENV | 82 |
| 4 | LFO | 83 |
| 5 | EDIT | 84 |
| 6 | GLOBAL | 85 |
| 7 | HOME | 86 |
| 8 | SAVE | 87 |

All buttons use **Gate, Off 0 / On 127** on CH16, retaining tap / hold / release behaviour.

### Page 2 — direct sound controls and transport

| Knob | Label | CC |
|---:|---|---:|
| 1 | HOME 1 | 20 |
| 2 | HOME 2 | 21 |
| 3 | HOME 3 | 22 |
| 4 | HOME 4 | 23 |
| 5 | ATTACK | 24 |
| 6 | RELEASE | 25 |
| 7 | DELAY | 26 |
| 8 | REVERB | 27 |

All eight knobs use **Absolute, 0..127**, CH16. HOME 1..4 change function with the selected engine.

| Button | Label | CC |
|---:|---|---:|
| 1 | ARP | 88 |
| 2 | SEQ | 89 |
| 3 | PLAY | 90 |
| 4 | REC | 91 |
| 5 | OCT - | 92 |
| 6 | OCT + | 93 |
| 7 | HOME | 86 |
| 8 | SAVE | 87 |

All buttons use **Gate, Off 0 / On 127**, CH16. OCT - / OCT + reproduce the FM-1's contextual octave / back / cancel / enter / confirm buttons. To transpose notes sent by the Kontrol itself, use its native octave controls.

### Artwork and display behaviour

The template embeds a **1280 × 212 JPEG banner** in `image_data` as a complete Base64 data URL beginning with `data:image/jpeg;base64,`. `hide_template_name=true` prevents the ordinary template title from overlaying the artwork.

The banner occupies the center display area; it does not mirror the FM-1 screen. Control labels stay those defined in the template, so KNOB1..4 and HOME 1..4 do not automatically acquire the current engine's parameter names.

The Kontrol's on-screen knob indicator can reach its visual endpoint while a **Relative Offset** knob continues sending increments. Preset browsing was confirmed to continue beyond that visual endpoint.

### Firmware controls beyond this template

Sections 3 and 14 list the complete firmware CC map. The included template has two pages; the SHAPE / MIX and ENGINE groups in section 3 are optional direct-CC assignments, not additional pages inside this file. Those parameters can also be edited through the contextual panel controls where Felucca exposes them.

### Hardware checks

**Felucca 1.8.0 KONTROL EDITION was installed on the physical FM-1 and its overall operation with the S49 MK3 was confirmed successful by the owner on 2026-10-31.** See the validation summary at the top of this README. The earlier v1.1.5.1 test on 2026-10-08 documented the individual controls listed in the historical table above. S61/S88 compatibility is by shared S-Series MK3 MIDI protocol rather than separate physical tests.

NI reference: [How to use MIDI Templates with the Kontrol S-Series MK3](https://support.native-instruments.com/support/solutions/articles/69000879639-how-to-use-midi-templates-with-the-kontrol-s-series-mk3).

---

# 14. Complete Kontrol S-Series MK3 Edition CC map

| CC | Channel | Mode | Function |
|---:|---:|---|---|
| 20 | selected / track | Absolute | Engine HOME 1 |
| 21 | selected / track | Absolute | Engine HOME 2 |
| 22 | selected / track | Absolute | Engine HOME 3 |
| 23 | selected / track | Absolute | Engine HOME 4 |
| 24 | selected / track | Absolute | Attack |
| 25 | selected / track | Absolute | Release |
| 26 | selected / track | Absolute | Delay send |
| 27 | selected / track | Absolute | Reverb send |
| 70 | 16 | Relative Offset | SELECT encoder |
| 71 | 16 | Relative Offset | ALGORITHM / Track encoder |
| 72 | 16 | Relative Offset | PRESETS encoder |
| 73 | 16 | Relative Offset | FM-1 KNOB 1 |
| 74 | 16 | Relative Offset | FM-1 KNOB 2 |
| 75 | 16 | Relative Offset | FM-1 KNOB 3 |
| 76 | 16 | Relative Offset | FM-1 KNOB 4 |
| 80 | 16 | Gate | FX button |
| 81 | 16 | Gate | SCL button |
| 82 | 16 | Gate | ENV button |
| 83 | 16 | Gate | LFO button |
| 84 | 16 | Gate | EDIT button |
| 85 | 16 | Gate | GLO button |
| 86 | 16 | Gate | HOME button |
| 87 | 16 | Gate | SAVE button |
| 88 | 16 | Gate | ARP button |
| 89 | 16 | Gate | SEQ button |
| 90 | 16 | Gate | PLAY button |
| 91 | 16 | Gate | REC button |
| 92 | 16 | Gate | OCT- button |
| 93 | 16 | Gate | OCT+ button |
| 102 | selected / track | Absolute | Decay |
| 103 | selected / track | Absolute | Sustain |
| 104 | selected / track | Absolute | Distortion |
| 105 | selected / track | Absolute | Chorus send |
| 106 | selected / track | Absolute | Track level |
| 107 | selected / track | Absolute | Pan |
| 108 | selected / track | Absolute | LFO rate |
| 109 | selected / track | Absolute | Glide |
| 110 | selected / track | Absolute | Engine E1 |
| 111 | selected / track | Absolute | Engine E2 |
| 112 | selected / track | Absolute | Engine E3 |
| 113 | selected / track | Absolute | Engine E4 |
| 114 | selected / track | Absolute | Engine E5 |
| 115 | selected / track | Absolute | Engine E6 |
| 116 | selected / track | Absolute | Engine E7 |
| 117 | selected / track | Absolute | Engine E8 |

For the parameter rows, using **CH16** is recommended: Felucca routes it to the selected track.

---

# 15. Current limitations

The Kontrol S-Series MK3 Edition currently virtualizes Felucca's **digital panel buttons and seven digital encoders**, plus the additional parameter CC pages.

Two FM-1 hardware-specific areas are not yet virtualized:

1. **MASTER physical volume control**  
   The FM-1 MASTER control is an analog ADC control, not one of the seven digital encoders. It remains controlled by the FM-1 hardware.

2. **FM-1 local key-matrix UI gestures**  
   Ordinary external MIDI notes are musical input. They do not currently impersonate the FM-1's local 27-key matrix for functions such as naming or key-based quick-layer shortcuts.

Everything listed in the CC tables above is implemented in the custom firmware.

---

# 16. Build

**Current build: Felucca 1.8.0 KONTROL EDITION, verified on FM-1 + S49 MK3 (owner report, 2026-10-31).**

Open **[Actions → Build Felucca 1.8 KONTROL Edition](https://github.com/1bitfromdend/Felucca-KONTROL-MIDI/actions/workflows/build-s49-1_8.yml)** and select a successful run or choose *Run workflow*. The [hardware-verified build #41229560226](https://github.com/1bitfromdend/Felucca-KONTROL-MIDI/actions/runs/41229560226) produced the artifact `felucca-1.8.0-kontrol`, containing `felucca-1.8.0-kontrol.fwsc`.

The 1.8 workflow:
1. Checks out upstream Felucca **v1.8.0** and its submodules.
2. Applies `tools/apply_s49_1_8.py` (dedicated S49 MIDI controls and virtual FM-1 panel).
3. Compiles the firmware with the JieLi toolchain.
4. Runs splash/UI preflight and the Felucca host/MIDI test suite.
5. Creates and uploads the installable **`.fwsc`** package.

**Legacy:** The separate `build-s49.yml` workflow compiles the historical 1.1.5.1 patch and remains available for maintenance of that version.

---

# 17. Install the Kontrol S-Series MK3 Edition firmware

Install the **`.fwsc` package on the M-VAVE FM-1**; import the separate `FM-01.kmt` MIDI template on the **Kontrol**. The owner successfully installed and used version 1.8.0 on an FM-1 and S49 MK3 on 2026-10-31.

### Download

1. Download the `felucca-1.8.0-kontrol` artifact from [the successful v1.8.0 KONTROL build](https://github.com/1bitfromdend/Felucca-KONTROL-MIDI/actions/runs/41229560226).
2. Extract `felucca-1.8.0-kontrol.fwsc` from the ZIP.
3. Download [the upstream v1.8.0 Python installer](https://github.com/hugelton/Felucca/blob/v1.8.0/tools/fm1_install.py) using GitHub's *Download raw file* control; save it as `fm1_install.py`.
4. Put the `.fwsc` and `.py` files in the same folder (for example `Desktop/fm1-s49`).

### Connect and identify

Connect the FM-1 directly to the computer by USB data cable. Close DAWs, MIDI editors, and other software accessing the FM-1 MIDI ports. Do not disconnect during the write.

**Windows PowerShell** (the confirmed installation environment, with Python 3.12 and `mido`/`python-rtmidi` already available): open PowerShell from the folder containing the two files and run:

```powershell
py -3.12 fm1_install.py --info
```

A valid identity with `[running]` confirms that the updater sees the FM-1; this command does **not** install anything.

### Install

```powershell
py -3.12 fm1_install.py felucca-1.8.0-kontrol.fwsc
```

Confirm the installer prompt. Wait for the flash write and automatic restart; do not unplug the device. Afterwards, test the FM-1 and load the Kontrol template with `ROUT=SEL` (keyboard on CH1; custom remote controls on CH16).

### Other platforms and troubleshooting

The Python installer also runs on macOS/Linux **when a working Python environment and the `mido`/`python-rtmidi` dependencies are already installed**; there is no need to install Apple's full Xcode for this task. In that environment use `python3 fm1_install.py --info` and then `python3 fm1_install.py felucca-1.8.0-kontrol.fwsc`.

If the FM-1 is not found, check the USB data cable and close other MIDI software. If the updater reports an interrupted write and the device remains in update mode, follow the [upstream installer recovery instructions](https://github.com/hugelton/Felucca).

**Return to stock:** The official M-VAVE V15 `FM-1.fwsc` package is accepted by the installer, and the [upstream web installer](https://hugelton.github.io/Felucca/) offers a stock recovery option. Use an authentic stock package. Bootloader recovery through [FM-1 Transporter](https://github.com/kurogedelic/FM-1-transporter) is a separate hardware procedure, not the standard MIDI update.

---

# 18. Upstream

Felucca Kontrol S-Series MK3 Edition is based on the upstream **Felucca 1.8.0** firmware by Hügelton Instruments.

- Upstream repository: https://github.com/hugelton/Felucca
- Upstream version: **`v1.8.0`** (pinned tag and submodules)
- KONTROL patch: `tools/apply_s49_1_8.py`

The current build workflow checks out the upstream `v1.8.0` tag and its submodules before applying the KONTROL-specific patch. The legacy workflow retains the pinned Felucca 1.1.5.1 commit.

This project is an independent community modification and is **not officially affiliated with, endorsed by, or supported by Hügelton Instruments, Native Instruments, or M-VAVE**.

Felucca remains the work of its original authors. This repository adds the Kontrol S-Series MK3-specific MIDI-control modifications, tests and build automation.
