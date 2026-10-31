# Felucca 1.8.0 KONTROL EDITION — hardware validation

**Result: PASS**  
**Test date: 2026-10-31**  
**Target: M-VAVE FM-1 + Native Instruments Kontrol S49 MK3**  
**Firmware: Felucca 1.8.0 KONTROL EDITION**

## Hardware test results

| Check | Result | Verification |
|---|---|---|
| FM-1 enumeration over Windows USB-MIDI | **PASS** | `py -3.12 fm1_install.py --info` identified the FM-1 in `[running]` mode |
| `.fwsc` firmware installation | **PASS** | `felucca-1.8.0-kontrol.fwsc` successfully installed |
| FM-1 operation following update | **PASS** | FM-1 operational after flashing |
| Kontrol S49 MK3 integration | **PASS** | Overall MIDI remote-control functionality operating correctly on the configured hardware |

**Test scope:** The complete S49 MK3 setup was assessed in normal operation, with a successful overall functional result. This record does not contain separate measured outcomes for every CC, page or possible parameter combination. S61 MK3 and S88 MK3 were not individually subjected to a physical test.

## Implemented S-Series MK3 functionality

The port retains the control map documented in [README.md](../README.md), including:

- Musical note routing and selected-track playing (recommended `ROUT=SEL`).
- Dedicated MIDI **CH16** for remote panel commands and direct parameter controls.
- Virtual FM-1 digital panel buttons (tap/hold/release) and seven relative encoders.
- Track and preset navigation, contextual page/parameter adjustments, and transport controls.
- Dedicated direct-CC mapping for the MAIN, SHAPE/MIX and ENGINE parameter groups.
- MIDI performance controls such as pitch bend, modulation, sustain, aftertouch, with Felucca 1.8's updated routing and MIDI Learn behaviour.

These are **implemented functions** covered by the project design and automated regression tests. The physical validation confirms overall operation of the connected S49 MK3 setup; a detailed CC-by-CC test record was not produced.

## Automated verification

The pinned Felucca v1.8.0 firmware with the KONTROL patch passed:

- Firmware compilation and release packaging.
- Splash-screen render/UI preflight.
- Felucca host regression suite, including MIDI/control-path tests.
- GitHub Actions artifact upload.

Evidence: [successful workflow run #41229560226](https://github.com/1bitfromdend/Felucca-KONTROL-MIDI/actions/runs/41229560226). Artifact name: `felucca-1.8.0-kontrol`; installed file: `felucca-1.8.0-kontrol.fwsc`.

Code was merged into `main` in [PR #2](https://github.com/1bitfromdend/Felucca-KONTROL-MIDI/pull/2). The historical Felucca 1.1.5.1 hardware-tested version remains available separately.

## Version-management note

This validation records a **successful installation and operational test**, not a new firmware revision. Documentation and workflow naming changes do not require another firmware installation. Further firmware builds are only needed when the underlying patch changes or a new release is requested.
