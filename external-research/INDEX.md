# Research index

**Last `/gr` pass: 2026-11-25 — CHECK-IN.** Inbox empty. FNVVR Reborn reached v1.0.0 (11-24) with an OpenXR backend and named TTW lists in v0.21's scope fix; its known-issue list doubles as a checklist for Begin Again. TTWVR (KeenGamer 11-18) already known.

_Previous: **Last `/gr` pass: 2026-11-21 — CHECK-IN.** FNVVR Reborn v0.18-v0.20 points lasers at a game menu (the companion wheel), fixed distant water again and found the water timer and several fades running once per eye (double-speed water, different in each eye); KeenGamer reports TTWVR publicly released on 2026-11-17 (no version named); one topic._

_Previous: **Last `/gr` pass: 2026-11-14 — FULL.** Folder set up this pass (index, credits, topics, inbox); found FNVVR Reborn, a second New Vegas VR mod whose public notes already met our sky/far-view, water and Stewie's Tweaks faults (the sky dome must be centred on each eye), and the Stewie's Tweaks INI switch behind the grabbed-weight crash hook; two pointers in `engine-research/inbox/`._

Status tags: 🆕 new · 👀 being looked at · ✅ used / confirmed · ❌ dead end.

| Date | Topic | Status | Summary |
| --- | --- | --- | --- |
| 2026-11-25 | [FNVVR Reborn v0.21 and v1.0.0: an OpenXR route, and TTW lists named](topics/2026-11-25-fnvvr-reborn-v021-v100-openxr-and-ttw.md) | 🆕 | v1.0.0 plays on OpenXR without SteamVR (Touch only), drops v0.21's performance mode, fixes TTW-list scope reticles; its known issues (UI Organizer HUD, JohnnyGuitar overlays, NVAC, three lStewieAl settings) are worth checking in Begin Again. |
| 2026-11-21 | [FNVVR Reborn v0.18.0 to v0.20.0: lasers in a game menu, distant water, effects run once per eye; TTWVR's public release reported](topics/2026-11-21-fnvvr-reborn-v018-to-v020-lasers-water-once-per-frame.md) | 🆕 | The shape for pointing at menus (FO-017), a check for double-speed or per-eye water (FO-002, FO-004), and a nudge to look for a TTWVR build newer than 1.0.0 |
| 2026-11-14 | [FNVVR Reborn: a second New Vegas VR mod whose release notes already name our far-view, water and Stewie's Tweaks faults](topics/2026-11-14-fnvvr-reborn-already-met-our-sky-water-and-stewie-faults.md) | 🆕 | df4l's DXVK-based mod centred the sky dome on each eye (clouds stopped moving against the head), fixed distant water going grey and flat at the sides, gave each eye its own water reflection, and lists three Stewie's Tweaks settings to keep off in VR; a sideways-only head test separates a one-centre far pass from other causes of the swim. |
| 2026-11-14 | [The Stewie's Tweaks crash hook and the INI switch behind it](topics/2026-11-14-stewie-tweaks-grabbed-weight-switch.md) | 🆕 | `IsOverencumberedAddGrabbedWeightHook` matches `bEncumbranceIncludesGrabbedItems` ("include grabbed item weight"); check Begin Again's value, a VR-only 0 in our own MO2 mod would take the hook out. No public crash report, no public source. |
| 2026-11-12 | [TTWVR 1.0.0: setup and controls, from the author's pinned Discord messages](ttwvr/2026-11-12-ttwvr-1.0.0-controls-and-setup-from-the-discord-pins.md) | ✅ | Passed on by Tefa; install order, calibration, every control; the ReShade OpenXR layer fix does not apply here. Kept in `ttwvr/` where it was first filed. |

## How to add a topic

1. New file in `topics/`, named `YYYY-MM-DD-short-slug.md`.
2. One row added to the table above, newest at the top.
3. Status tags change only here, by the research session; the modding side sends its verdicts through [`inbox/`](inbox/).

Where the outside facts on TTWVR, Begin Again and TTW come from: [README.md](README.md). Every source: [CREDITS.md](CREDITS.md).
