# Felucca S49 Edition

Custom MIDI-control patch for **Native Instruments Kontrol S49 MK3 + M-VAVE FM-1 running Felucca 1.0.1**.

The repository intentionally stores only the patch and build workflow. GitHub Actions downloads the exact upstream Felucca 1.0.1 commit, applies the patch, runs the host tests and produces an installable `.fwsc`.

## MIDI routing

Felucca's normal routing is preserved:

- MIDI CH1 → Track 1
- MIDI CH2 → Track 2
- MIDI CH3 → Track 3
- MIDI CH4 → Track 4
- with `ROUT=SEL`, Felucca's existing selected-track behaviour remains unchanged

All S49 knobs should use **CC / Absolute / 0..127**.

## S49 knob pages

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

CC32..63 are intentionally not used by the S49 Edition because they are the LSB range for standard 14-bit MIDI controllers. In particular, CC38 is Data Entry LSB used by RPN pitch-bend sensitivity.

## Existing MIDI controls retained

The patch does not change Felucca's existing MIDI behaviour:

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

This is a custom firmware build. Flashing third-party firmware always carries recovery risk; keep the official Felucca installer and FM-1-transporter recovery path available.
