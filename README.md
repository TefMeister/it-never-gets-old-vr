# IT NEVER GETS OLD WHEN SOMETHING BLOWS UP IN VR!

Tefa's own modlist for playing **Tale of Two Wastelands** (Fallout 3 and New Vegas as one game) in virtual reality,
with **Tale of Two Realities (TTWVR)** as the VR mod underneath. This is our own work: the list's VR setup, its
fixes, its look and every tool in this repository were made here.

**Built upon the work of others** (see Credits): the mod selection and the list's own patches come from
SpringHeelJon's Begin Again modlist, which this list builds upon with his permission. This list is **not
affiliated with or endorsed by Begin Again or its author**; please do not take questions or faults about this list
to him, or to KUPOkinz (TTWVR) or the TTW team. Open an issue here instead.

Earlier names of this project: `ba-ttr-vr-bridge` (2026-11-09), Atomic Fork VR (2026-11-19). Dated notes in this
repository keep the name that was current when they were written; the raw logs in `runs/` are left as recorded.

## How we work

- **The VR mod and the base list are never edited in place.** Whatever we change lives in our own small mods
  (`bridge-mods/`, the "Bridge" mods) placed on top, so every change can be seen and taken out again.
- **Fixed versions:** TTWVR 1.0.0 (the DLL of 2026-11-08) and the base list's V6.1.0. Since 2026-11-12 TTWVR may be
  changed by us where that is what makes the list work in VR, always as our own mod on top of the untouched original.
- **Every step is a recipe a script can repeat** (`tools/`), and each launch's logs are kept (`runs/`, scrubbed).
- **Tested as a ladder:** the list is switched back on group by group, each group as its own Mod Organizer profile,
  flat and in the headset (`tools/ladder.py`, `tools/ladder_groups.py`).

## Where it stands

- Work in progress: the list is being switched back on group by group on top of the VR mod, with our fixes (water,
  sky, menus, picture settings), tested on a Quest 3 through Virtual Desktop and on the desk with the OpenXR
  Simulator. `NOTEBOOK.md` says what has been tested where.
- **2026-11-20:** the list got its own name and look: a full copy under the new name, Tefa's poster behind Mod
  Organizer and on the main menu, an American poster font (Racing Sans One) on the manager and the menu.

## Files

- `NOTEBOOK.md`: the dated log of everything done and what came of it.
- `FAULTS.md`: the fault ledger, in the order faults must be sorted.
- `bridge-mods/`: our own MO2 mods and what each one does.
- `tools/`: the ladder, the run collector, the conflict report, the menu and font builders, the Mod Organizer look
  (`mo2_style_ingo.py`), the rename (`ingo_rename.py`), the water and sky tools.
- `modding-notes/`, `docs/`, `engine-research/`, `external-research/`: findings, plans and outside sources.
- `reports/`: which files the VR mod and the list both supply, and who wins.

## Credits

- **SpringHeelJon**: the Begin Again modlist, whose mod selection, patches, merges and settings this list builds
  upon. Thank you for allowing it.
- **KUPOkinz**: Tale of Two Realities (TTWVR), the VR conversion this whole list runs on.
- **The TTW team**: Tale of Two Wastelands.
- **Every author of every mod in the list**: the list is made of your work; each mod keeps its own page and credit
  on Nexus Mods.
- **Trosski**: the see-through Mod Organizer style our look is built on. **Mod Organizer 2**, **xNVSE**,
  **Wabbajack** and their teams.
- **momusdigital and the fnvdecomp.com contributors**: [fnv_decomp](https://github.com/momusdigital/fnv_decomp)
  (CC0), the decompiled New Vegas program we read to understand the game, and
  [f3_decomp](https://github.com/momusdigital/f3_decomp) (CC0) for comparing with Fallout 3.
- Fonts: Racing Sans One, Alfa Slab One and the other samples in `tools/fonts/` are under the SIL Open Font License
  (licences beside them).

If you should be credited here and are not, please open an issue.
