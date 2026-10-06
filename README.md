# Felucca S49 Edition

Full MIDI remote-control patch for **Native Instruments Kontrol S49 MK3 + M-VAVE FM-1 running Felucca 1.0.1**.

The goal is to use the S49 as the main control surface for Felucca: play the four tracks from the keyboard, edit synth parameters from the S49 knobs, and operate Felucca's panel/navigation controls without reaching for the FM-1.

The repository intentionally stores only the patch and build workflow. GitHub Actions downloads the exact upstream Felucca 1.0.1 commit, applies the patch, runs the host tests and produces an installable `.fwsc`.

## MIDI architecture

Felucca's normal musical routing is preserved:

- MIDI CH1 → Track 1
- MIDI CH2 → Track 2
- MIDI CH3 → Track 3
- MIDI CH4 → Track 4
- with `ROUT=SEL`, Felucca's existing selected-track behaviour remains unchanged

For the S49 Edition, **MIDI CH16 is the dedicated control-panel channel**.

This keeps panel/navigation messages separate from the four performance channels. Felucca already routes channels above CH4 to the selected track, so the absolute parameter pages can also use CH16 to edit whichever Felucca track is currently selected.

## S49 parameter pages

Use **CC / Absolute / 0..127** for these knob pages.

Recommended setup: put all three pages on **MIDI CH16** so the knobs always edit the currently selected Felucca track.

### Page 1 — MAIN

| Knob | CC | Felucca |
|---|---:|---|
| 1 | 20 | Engine HOME knob 1 |
| 2 | 21 | Engine HOME knob 2 |
| 3 | 22 | Engine HOME knob 3 |
| 4 | 23 | Engine HOME knob 4 |
| 5 | 24 | Attack |
| 6 | 25 | Release |
| 7 | 26 | Delay send |
| 8 | 27 | Reverb send |

The first four controls are deliberately dynamic: they always address the four parameters that the current Felucca engine exposes on its HOME screen.

### Page 2 — SHAPE / MIX

| Knob | CC | Felucca |
|---|---:|---|
| 1 | 102 | Decay |
| 2 | 103 | Sustain |
| 3 | 104 | Distortion |
| 4 | 105 | Chorus send |
| 5 | 106 | Track level |
| 6 | 107 | Pan |
| 7 | 108 | LFO rate |
| 8 | 109 | Glide |

### Page 3 — ENGINE

| Knob | CC | Felucca |
|---|---:|---|
| 1..8 | 110..117 | Engine parameters E1..E8 |

E1..E8 mean different things on different engines, exactly like Felucca's EDIT parameters.

CC32..63 are intentionally not used by the absolute parameter pages because they are the LSB range for standard 14-bit MIDI controllers. In particular, CC38 is Data Entry LSB used by RPN pitch-bend sensitivity.

## Full virtual FM-1 panel

The S49 Edition also exposes the **physical FM-1 panel itself over MIDI**.

These controls use **MIDI CH16 only**.

### Virtual panel buttons

Configure S49 buttons as:

- Type: **Control Change**
- Mode: **Gate**
- Off Value: **0**
- On Value: **127**
- MIDI Channel: **16**

| CC | FM-1 / Felucca button |
|---:|---|
| 80 | FX |
| 81 | SCL |
| 82 | ENV |
| 83 | LFO |
| 84 | EDIT |
| 85 | GLO |
| 86 | HOME |
| 87 | SAVE |
| 88 | ARP |
| 89 | SEQ |
| 90 | PLAY |
| 91 | REC |
| 92 | OCT- |
| 93 | OCT+ |

The firmware preserves **press and release state**, so Felucca's existing tap/hold behaviour is retained instead of being reimplemented as one-shot commands. This matters for controls such as HOME, SAVE and SEQ.

### Virtual panel encoders

The seven FM-1 encoders are also available on MIDI CH16.

Configure these S49 knobs as:

- Type: **Control Change**
- Mode: **Relative Offset**
- MIDI Channel: **16**

Relative Offset is interpreted as **64 = no movement, 65 = +1, 63 = -1**.

| S49 knob | CC | FM-1 encoder |
|---|---:|---|
| 1 | 70 | SELECT |
| 2 | 71 | ALGORITHM |
| 3 | 72 | PRESETS |
| 4 | 73 | KNOB 1 |
| 5 | 74 | KNOB 2 |
| 6 | 75 | KNOB 3 |
| 7 | 76 | KNOB 4 |
| 8 | — | spare |

These virtual encoders enter Felucca at the same panel abstraction as the real hardware encoders. Their function therefore follows the current page exactly like the physical FM-1 controls: SELECT can edit tempo/menu values, ALGORITHM changes track, PRESETS browses sounds where allowed, and KNOB 1..4 operate the current Felucca page.

## Suggested S49 panel pages

The S49 MK3 supports multiple Buttons & Knobs pages, so a practical layout is:

### Page 4 — PANEL A

Buttons:

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|
| FX | SCL | ENV | LFO | EDIT | GLO | HOME | SAVE |
| CC80 | CC81 | CC82 | CC83 | CC84 | CC85 | CC86 | CC87 |

Knobs: CC70..76 as the seven virtual FM-1 encoders.

### Page 5 — PANEL B

Buttons:

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|
| ARP | SEQ | PLAY | REC | OCT- | OCT+ | HOME | SAVE |
| CC88 | CC89 | CC90 | CC91 | CC92 | CC93 | CC86 | CC87 |

Knobs: repeat CC70..76, so navigation remains available on both panel pages.

## Existing MIDI controls retained

The patch does not remove Felucca's existing MIDI behaviour:

- Note On / Note Off
- CC1 → Mod Wheel modulation source
- CC11 → Expression modulation source
- CC64 → Sustain
- Channel Pressure → Aftertouch modulation source
- Pitch Bend and RPN bend range
- CC120 / CC121 / CC123 panic/reset behaviour
- USB MIDI and TRS MIDI

## Build

Open **Actions → Build Felucca S49 Edition → Run workflow**.

When the job is green, download the artifact named `felucca-1.0.1-s49`. Inside it is:

`felucca-1.0.1-s49.fwsc`

## Upstream

Felucca S49 Edition is based on the upstream Felucca 1.0.1 firmware by Hügelton Instruments.

Upstream repository: https://github.com/hugelton/Felucca

Upstream version: `1.0.1`

Upstream commit: `20c275e39f75fa820978032efaceddfc5283c8cb`

The build workflow always downloads this exact upstream commit before applying the S49 Edition patch, so builds remain reproducible and independent from later upstream changes.

This project is an independent community modification and is **not officially affiliated with, endorsed by, or supported by Hügelton Instruments, Native Instruments, or M-VAVE**.

Felucca remains the work of its original authors. This repository only adds the S49-specific MIDI-control modifications and related build automation.

This is a custom firmware build. Flashing third-party firmware always carries recovery risk; keep the official Felucca installer and FM-1-transporter recovery path available.
