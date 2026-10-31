# Felucca 1.8.0 KONTROL EDITION — hardware validation

**Status: PASSED — user-confirmed physical operation**  
**Date: 2026-10-31**  
**Hardware: M-VAVE FM-1 + Native Instruments Kontrol S49 MK3**  
**Software: Felucca 1.8.0 with KONTROL MIDI/virtual-panel patch**

## Physical results (reported by the device owner)

| Check | Result | Evidence / scope |
|---|---|---|
| Windows to FM-1 via USB-MIDI | PASS | The owner ran `py -3.12 fm1_install.py --info` and reported `[running]` |
| Installation of `felucca-1.8.0-kontrol.fwsc` | PASS | Owner completed the firmware update and stated that the FM-1 worked |
| FM-1 operation after update | PASS | Owner: “la fm 1 funziona” |
| Native Instruments Kontrol S49 MK3 integration | PASS | Owner: “funziona tutto perfettamente sulla kontrol” |

The S49 MK3 report confirms satisfactory **overall operation of the actual configured Kontrol setup**. It covers the complete functionality as reported by the owner, without claiming a separate logged measurement of every MIDI CC or every page/parameter combination. S61 MK3 and S88 MK3 use the same implementation but have **not** been individually tested in this report.

## Implemented S-Series MK3 functionality

The port retains the control map documented in [README.md](../README.md), including:

- Musical note routing and selected-track playing (recommended `ROUT=SEL`).
- Dedicated MIDI **CH16** for remote panel commands and direct parameter controls.
- Virtual FM-1 digital panel buttons (tap/hold/release) and seven relative encoders.
- Track and preset navigation, contextual page/parameter adjustments, and transport controls.
- Dedicated direct-CC mapping for the MAIN, SHAPE/MIX and ENGINE parameter groups.
- MIDI performance controls such as pitch bend, modulation, sustain, aftertouch, with Felucca 1.8's updated routing and MIDI Learn behaviour.

These describe **implemented capabilities**; the owner reported the overall Kontrol integration worked perfectly. The above list is not presented as an independent per-control test log.

## Automated verification

The pinned Felucca v1.8.0 firmware with the KONTROL patch passed:

- Firmware compilation and release packaging.
- Splash-screen render/UI preflight.
- Felucca host regression suite, including MIDI/control-path tests.
- GitHub Actions artifact upload.

Evidence: [successful workflow run #41229560226](https://github.com/1bitfromdend/Felucca-KONTROL-MIDI/actions/runs/41229560226). Artifact name: `felucca-1.8.0-kontrol`; installed file: `felucca-1.8.0-kontrol.fwsc`.

Code was merged into `main` in [PR #2](https://github.com/1bitfromdend/Felucca-KONTROL-MIDI/pull/2). The historical Felucca 1.1.5.1 hardware-tested version remains available separately.

## Version-management note

This validation records a **successful installation and operational test**, not a new firmware revision. Documentation and workflow naming changes do not require the owner to flash the FM-1 again. Further firmware builds are only needed when the underlying patch changes or a new release is requested.
