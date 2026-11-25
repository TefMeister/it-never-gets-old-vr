# FNVVR Reborn v0.21 and v1.0.0: an OpenXR route, and TTW lists named

**For:** the TTWVR + Begin Again fork. FNVVR Reborn (df4l) is the second New Vegas VR mod we track (topics of
2026-11-14 and 2026-11-21); KUPOkinz's TTWVR stays the VR mod this project builds on.

## What changed [reported 2026-11-25, the two release pages]

- **v1.0.0 (2026-11-24), "First release":** an **OpenXR backend** (`d3d9.vrBackend = openxr` in `dxvk.conf`): play
  without SteamVR on the system's OpenXR runtime, Touch controllers only; name entry then needs a real keyboard. The
  v0.21 performance mode is **removed** (every Steam Frame GPU crash of v0.21 came from sessions where it ran);
  occlusion culling per eye stays, on by default; the submission thread is an option again, off by default.
- **v0.21.0 (2026-11-22):** scope reticles fixed "with decompressed archives (TTW lists such as The Best of Times)":
  the game files were read a few bytes short. So FNVVR Reborn is being run on TTW modlists by its users.
- Known issues listed for v1.0.0 that touch big modlists: HUD elements added through UI Organizer stay at their
  flat position; JohnnyGuitar camera overlays do not work in VR; NVAC is not supported; three lStewieAl's Tweaks
  settings must stay off in VR (`bSmoothIronsightsCameraTransition`, `bScopeVisibilityDelay`,
  `bAlwaysShowWeaponAnimation`).

## Why it matters here

- Begin Again is a TTW list. FNVVR Reborn naming TTW lists, and fixing a TTW-only reading fault, means it is a live
  second route for a TTW list in VR, now on OpenXR (Virtual Desktop's runtime) as well as SteamVR. Not a reason to
  change the project's direction (Tefa chose TTWVR); a fallback worth knowing if a TTWVR blocker stays shut.
- Its known-issue list is a ready checklist for our list too: UI Organizer HUD items, JohnnyGuitar overlays, NVAC and
  the three lStewieAl settings are worth checking against Begin Again's own mod list, whichever VR mod runs it.
  [hypothesis: the same causes apply under TTWVR; not checked]

## Next step

Check Begin Again's list for NVAC, UI Organizer HUD mods, JohnnyGuitar overlays and the three lStewieAl settings, and
note which are present; that is the modding side's call.

## Sources

- df4l, FNVVR Reborn releases v0.21.0 (2026-11-22) and v1.0.0 (2026-11-24) — https://github.com/df4l/FNVVR/releases
