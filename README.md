# Felucca S49 Edition

Full MIDI remote-control patch for **Native Instruments Kontrol S49 MK3 + M-VAVE FM-1 running Felucca 1.0.2**.

The purpose of this build is to use the S49 as the main performance and editing surface for Felucca:

- play Felucca tracks from the S49 keyboard
- edit the selected track from 24 absolute parameter controls
- reproduce the FM-1's digital panel buttons over MIDI
- reproduce the FM-1's seven digital encoders over MIDI
- keep Felucca's original MIDI behaviour, including sustain, pitch bend, aftertouch and modulation

The repository stores the firmware patch, build workflow and ready-to-import S49 MIDI template. GitHub Actions downloads the exact upstream Felucca 1.0.2 commit, applies the patch, runs the host tests and produces an installable `.fwsc`.

The custom build also identifies itself visually at boot with **S49 EDITION** under the original Felucca splash screen. The technical package identity used by the installer is left unchanged.

---

## 1. MIDI architecture

### Musical tracks

Felucca's normal routing is preserved:

| MIDI channel | Felucca destination |
|---:|---|
| CH1 | Track 1 |
| CH2 | Track 2 |
| CH3 | Track 3 |
| CH4 | Track 4 |
| CH5..CH16 | Selected track |

For the included template, set **`ROUT=SEL` on Felucca** and leave the S49 keybed on **CH1**. The full keyboard then plays the currently selected track. Turn the **TRACK** knob (CC71 on CH16) to change tracks without editing the template or splitting the keyboard.

The channel-to-track table above applies to `ROUT=CH1-4`.

This means an S49 split / zone setup can use CH1..CH4 to play the four Felucca tracks directly.

### Dedicated remote-control channel

**MIDI CH16 is the S49 Edition panel-control channel.**

Use CH16 for:

- the 24 absolute S49 parameter controls
- the virtual FM-1 panel buttons
- the virtual FM-1 panel encoders

The panel commands themselves are consumed by the S49 Edition firmware and do not become ordinary Felucca parameter CCs.

---

## 2. Recommended S49 control modes

| Control type | S49 mode | MIDI channel |
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

# 3. S49 parameter pages

These controls are **absolute 0..127 CCs**.

Putting them on **CH16** makes them edit the currently selected Felucca track.

## Page 1 — MAIN

| S49 knob | CC | Felucca parameter |
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

| S49 knob | CC | Felucca parameter |
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

| S49 knob | CC | Felucca parameter |
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

CC32..63 are intentionally avoided for the S49 Edition absolute parameter pages because they are the LSB half of standard 14-bit MIDI controller pairs.

In particular:

- CC6 = Data Entry MSB
- CC38 = Data Entry LSB

Felucca uses these for RPN pitch-bend sensitivity, so using CC38 as an ordinary synth parameter would break standard MIDI behaviour.

---

# 4. Virtual FM-1 panel buttons

These controls reproduce the **digital buttons on the physical FM-1 panel**.

Configure every S49 button as:

- Type: **Control Change**
- Mode: **Gate**
- Off Value: **0**
- On Value: **127**
- MIDI Channel: **16**

The firmware keeps the button held for as long as the S49 sends the Gate-on state, and releases it when the S49 sends 0.

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

Felucca's hold threshold and state machine remain the upstream implementation; the S49 Edition does not duplicate that logic.

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

| S49 knob | CC | Virtual FM-1 encoder | Main Felucca function |
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

The S49 virtual buttons call the same Felucca page logic as the FM-1 controls.

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

Felucca 1.0.2 has four hold layers.

The virtual S49 buttons preserve the **button-hold state** required to open them.

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

The S49 Edition currently virtualizes the **panel buttons and encoders**, not the FM-1's local 27-key hardware matrix.

Therefore the hold layer itself can be opened remotely, and its encoder functions can be controlled remotely, but **key-combination shortcuts that specifically depend on the FM-1's own local keys are not currently generated from ordinary external MIDI notes**.

External S49 notes remain musical MIDI input.

---

# 10. Keyboard and performance MIDI

The S49 keyboard uses Felucca's normal MIDI note implementation.

### Note routing

With normal `ROUT=CH1-4`:

| S49 MIDI channel | Destination |
|---:|---|
| 1 | Track 1 |
| 2 | Track 2 |
| 3 | Track 3 |
| 4 | Track 4 |

Channels 5..16 play the currently selected track.

This allows S49 keyboard zones / splits to address several Felucca tracks.

### Note On / Note Off

Standard Note On / Note Off messages are retained.

Velocity is passed into Felucca's existing note path.

### Chord / scale behaviour

MIDI notes pass through Felucca's existing track note logic, including the active chord / scale behaviour implemented by the upstream firmware.

---

# 11. Existing MIDI CC and performance controls retained

The S49 Edition leaves upstream MIDI controls intact.

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

Therefore the S49 Edition mappings work through:

- **USB MIDI**
- **TRS MIDI IN**

The custom mapping is not USB-only.

---

# 13. Included S49 MIDI template

Download [FM-01.kmt](templates/FM-01.kmt) (use GitHub's **Download raw file** button).

This is the two-page template configured for the S49 Edition firmware. It includes the custom **Felucca S49 Edition** black/red banner. Every display knob and button sends on **CH16**; the single full-range keyzone remains on **CH1**. MIDI output preference is **DIN priority**.

![Felucca S49 Edition display banner](templates/Felucca-S49-Edition.jpg)

*Embedded display artwork; the S49's button labels and knob indicators appear above and below this banner.*

### Import and play

1. Connect the S49 to a computer by USB with **NI Hardware Connection Service** installed and running.
2. Open the MIDI Template browser and choose **Import**. Select the downloaded `FM-01.kmt` in the computer's import window and send it to the keyboard.
3. Load the **FM-01** template.
4. Connect S49 **MIDI OUT** to FM-1 **MIDI IN** through the appropriate DIN/TRS connection.
5. Set **`ROUT=SEL` on Felucca**. Leave the S49 keybed on CH1.
6. Use **TRACK** on page 1 to select a track. All 49 keys now play that selected track.

Import/export requires a computer; the imported template can then be used standalone. Use the S49 Page arrow buttons to switch between its two control pages. The custom artwork requires S49 firmware with MIDI-template artwork support (introduced in version 1.8).

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

All buttons use **Gate, Off 0 / On 127**, CH16. OCT - / OCT + reproduce the FM-1's contextual octave / back / cancel / enter / confirm buttons. To transpose notes sent by the S49 itself, use its native octave controls.

### Artwork and display behaviour

The template embeds a **1280 × 212 JPEG banner** in `image_data` as a complete Base64 data URL beginning with `data:image/jpeg;base64,`. `hide_template_name=true` prevents the ordinary template title from overlaying the artwork.

The banner occupies the center display area; it does not mirror the FM-1 screen. Control labels stay those defined in the template, so KNOB1..4 and HOME 1..4 do not automatically acquire the current engine's parameter names.

The S49's on-screen knob indicator can reach its visual endpoint while a **Relative Offset** knob continues sending increments. Preset browsing was confirmed to continue beyond that visual endpoint.

### Firmware controls beyond this template

Sections 3 and 14 list the complete firmware CC map. The included template has two pages; the SHAPE / MIX and ENGINE groups in section 3 are optional direct-CC assignments, not additional pages inside this file. Those parameters can also be edited through the contextual panel controls where Felucca exposes them.

### Hardware checks

The flashed S49 Edition firmware was checked through the S49's MIDI OUT → FM-1 TRS MIDI IN: note playback, direct Attack control, HOME tap and hold, track selection, preset browsing and `ROUT=SEL` selected-track playback. The template's assignments and embedded image data URL have been validated as JSON; loading and rendering the artwork must be checked on the S49.

NI reference: [How to use MIDI Templates with the Kontrol S-Series MK3](https://support.native-instruments.com/support/solutions/articles/69000879639-how-to-use-midi-templates-with-the-kontrol-s-series-mk3).

---

# 14. Complete S49 Edition CC map

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

The S49 Edition currently virtualizes Felucca's **digital panel buttons and seven digital encoders**, plus the additional parameter CC pages.

Two FM-1 hardware-specific areas are not yet virtualized:

1. **MASTER physical volume control**  
   The FM-1 MASTER control is an analog ADC control, not one of the seven digital encoders. It remains controlled by the FM-1 hardware.

2. **FM-1 local key-matrix UI gestures**  
   Ordinary external MIDI notes are musical input. They do not currently impersonate the FM-1's local 27-key matrix for functions such as naming or key-based quick-layer shortcuts.

Everything listed in the CC tables above is implemented in the custom firmware.

---

# 16. Build

Open:

**Actions → Build Felucca S49 Edition → Run workflow**

When the job is green, download the artifact:

`felucca-1.0.2-s49`

Inside it is:

`felucca-1.0.2-s49.fwsc`

The workflow:

1. clones the pinned Felucca 1.0.2 source
2. applies the S49 Edition patch
3. builds the firmware
4. runs Felucca host tests, including S49 control tests
5. builds the release package
6. uploads the installable `.fwsc`

---

# 17. Install the S49 Edition firmware

The firmware package (`.fwsc`) is installed on the **FM-1**. The MIDI template (`.kmt`) is imported separately on the **S49**, as described in section 13.

### 1. Download the custom firmware

1. Open this repository's [Actions](https://github.com/1bitfromdend/felucca_1.0.1_S49V0.1/actions).
2. Select a successful **Build Felucca S49 Edition** run. Choose a firmware build, not a documentation-only commit.
3. Under **Artifacts**, download **`felucca-1.0.2-s49`**. GitHub may require you to sign in.
4. Extract the ZIP. The file to install is **`felucca-1.0.2-s49.fwsc`**.
5. Download the [official Python installer matching the pinned Felucca source](https://raw.githubusercontent.com/hugelton/Felucca/db70550344f36cb10657d1652f567b5932ac4b2b/tools/fm1_install.py) and save it as **`fm1_install.py`**.
6. Put both files in the same folder, for example a folder named **`Felucca-S49`** on your Desktop.

Use the artifact from **this repository** to install S49 Edition. Installing the ordinary upstream Felucca release instead does not include this project's remote-control patch.

### 2. Connect the FM-1

- Install Python 3 if it is not already available.
- Close DAWs, MIDI monitors, browser MIDI editors and other applications that may hold the FM-1 MIDI ports.
- Connect the **FM-1 directly to the computer with a USB data cable** and power it on.
- Firmware installation uses **USB-MIDI**, not the S49 → FM-1 DIN/TRS performance connection.
- Keep USB and power connected throughout the write and automatic restart.

### 3. macOS / Linux terminal commands

Open Terminal, enter the folder containing the two downloaded files, and create a local Python environment. This example uses the Desktop folder above; adjust the path if needed:

```bash
cd "$HOME/Desktop/Felucca-S49"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install mido python-rtmidi
```

Check that the installer can identify the connected FM-1:

```bash
python fm1_install.py --info
```

Install the custom firmware:

```bash
python fm1_install.py felucca-1.0.2-s49.fwsc
```

Read the installer prompt and confirm when asked. Wait for the package transfer, flash write, automatic restart and identity check to finish.

### 4. Windows PowerShell commands

Open PowerShell and enter the folder containing the two downloaded files. This example uses the same Desktop folder:

```powershell
cd "$env:USERPROFILE\Desktop\Felucca-S49"
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install mido python-rtmidi
.\.venv\Scripts\python.exe fm1_install.py --info
.\.venv\Scripts\python.exe fm1_install.py felucca-1.0.2-s49.fwsc
```

No PowerShell environment activation is needed for these commands. If your Desktop is redirected, use its actual folder path. Confirm at the installer prompt and wait until installation finishes.

### 5. Verify and start playing

1. The FM-1 should restart and show **S49 EDITION in red** under the original Felucca splash.
2. If needed, check its identity again with `python fm1_install.py --info` (or the Windows interpreter command above). The installer's technical package identity remains the upstream identity; the splash and custom control behaviour distinguish S49 Edition.
3. Load the included **FM-01** template on the S49.
4. Reconnect the S49 MIDI OUT → FM-1 MIDI IN performance connection and set **`ROUT=SEL`** on Felucca.
5. Test HOME, TRACK and PRESET from S49 page 1, then PLAY / REC and the direct controls on page 2.

### Port selection and troubleshooting

The installer normally detects eligible FM-1 ports automatically. If necessary, select one explicitly using a distinctive part of its MIDI port name:

```bash
python fm1_install.py --info --port "Felucca"
python fm1_install.py felucca-1.0.2-s49.fwsc --port "Felucca"
```

Replace `Felucca` with a name actually shown by your system. On Windows use `.\.venv\Scripts\python.exe` in place of `python`.

- **Missing mido / python-rtmidi:** run the dependency-install command using the same Python interpreter you use to launch the installer.
- **FM-1 not found / port busy:** close other MIDI applications, check the USB data cable and reconnect the device.
- **Interrupted install with the FM-1 still in update mode:** rerun the same install command to finish the write; the installer supports resuming from update mode.
- **Package rejected:** check that you extracted the correct `.fwsc`. `--force` is not needed for this custom Felucca package.

### Return to stock / recovery

The installer also accepts the original M-VAVE **V15 `FM-1.fwsc`** package:

```bash
python fm1_install.py FM-1.fwsc
```

Use the authentic official V15 file. The [upstream web installer](https://hugelton.github.io/Felucca/) also offers **Return to official V15**.

If the FM-1 cannot start and appears as **WL80UBOOT**, see the [upstream recovery instructions](https://github.com/hugelton/Felucca#if-the-fm-1-does-not-start) and [FM-1 Transporter](https://github.com/kurogedelic/FM-1-transporter). Transporter recovery is a separate hardware procedure, not the normal USB-MIDI installation.

---

# 18. Upstream

Felucca S49 Edition is based on the upstream **Felucca 1.0.2** firmware by Hügelton Instruments.

- Upstream repository: https://github.com/hugelton/Felucca
- Upstream version: `1.0.2`
- Upstream commit: `db70550344f36cb10657d1652f567b5932ac4b2b`

The build workflow always downloads this exact upstream commit before applying the S49 Edition patch, so builds remain reproducible and independent from later upstream changes.

This project is an independent community modification and is **not officially affiliated with, endorsed by, or supported by Hügelton Instruments, Native Instruments, or M-VAVE**.

Felucca remains the work of its original authors. This repository adds the S49-specific MIDI-control modifications, tests and build automation.
