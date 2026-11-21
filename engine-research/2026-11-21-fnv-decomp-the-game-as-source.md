# The game as source code: momusdigital's fnv_decomp (and f3_decomp)

2026-11-21, Build PC, ordinary session. Tefa: *"please look at this pile of gold and use it when we mod our version of
tales of two wastelands modlist"*.

## What it is

- **fnv_decomp** <https://github.com/momusdigital/fnv_decomp> (CC0, public domain): a **matching** decompilation of
  FalloutNV.exe **1.4.0.525** (Steam). 2,989 units, 68,657 functions, each rebuilt as C++ that compiles back to the
  same bytes at the same address `[reported, its README]`. Names come from RTTI, the console and script tables,
  byte-identical Gamebryo 2.6 / Havok 7.1 / VC2008 library functions, community projects (xNVSE, JIP LN: names only)
  and, most of all, **two Xbox 360 development PDBs** (retail and debug builds of August 2010), so many functions carry
  their original names, parameter names and even local variable names. Placeholders (`FUN_00xxxxxx`) and `GUESS`
  names are marked as such in the source. Coordinated on fnvdecomp.com. Contains no game files.
- **f3_decomp** <https://github.com/momusdigital/f3_decomp> (CC0): the same for Fallout3.exe 1.7.0.3, 63,681 of
  63,682 functions matching `[reported]`. **Not the program TTW runs** (TTW plays Fallout 3's content inside New
  Vegas's program); useful only to compare how Fallout 3 itself did something that TTW recreates.

## It fits our list exactly `[measured 2026-11-21]`

- The list's game program is 1.4.0.525 (the Steam folder's copy and the list's FNV4GB copy, both 16,549,704 bytes).
- The FNV4GB patch differs from the original in **188 bytes** (the header at 0x136-0x179 and a small stretch at file
  offsets 0xF57277-0xFC70EA, all inside the `.bind` section, Steam's start-up stub; `.text` ends at 0xBDDA00), so every code address in the decompilation is an address in our
  running game.
- Local copies (shallow clones, about 185 MB each): `D:\claude video game stuff\decomps\fnv_decomp` and `...\f3_decomp`.
  Update with `git pull` there.

## The tool: `tools/fnv_where.py`

- `addr <address...>`: the function each address falls in, with its offset, size, source file and line.
- `find <text>`: functions whose name contains the text.
- `src <address>`: prints the function's rebuilt source, with its PDB name, parameters and locals when known.
- `--game f3` for the Fallout 3 one.

First use, on addresses our own readers found by hand (`[verified-numerically 2026-11-21]`, the lookup itself):

| Address | Our note called it | The decompilation says |
|---|---|---|
| 0x00A24660 | (menu input, 2026-11-21 reader) | `InputManager::Controls_GetUserAction`, `src/fallout/interface/hotkeyswheel.cpp` |
| 0x0070F6E0 | (menu input) | `HandleGamepadButton` in `src/fallout/interface/interfacemanager.cpp` (2,419 bytes) |
| 0x0070CD63 | (menu input) | inside `UpdateInterface` (+0x8c3), same file |
| 0x00715BC0 | (menu input) | inside `InterfaceManager_SetCurrentFocusTarget` (+0x360) |
| 0x009F996E | | the game's `XInputGetState` import stub (the one TTWVR's fake pad answers; `[ID FO-017]`) |

## Where it helps the open rows first

- `[ID FO-016]` / `[ID FO-017]` menus: `StartMenu::*` (25 functions, `src/fallout/interface/menus/startmenu.cpp`:
  `HandleSelection`, `UpdateMouseover`, `HandleSliderTileInput`...), `HandleGamepadButton`, `Controls_GetUserAction`.
  The stick-right hook can be planned against named code instead of disassembly.
- `[ID FO-002]` the water line: `TESWaterSystem` (45 functions, `src/fallout_shared/teswater.cpp`), above all
  `TESWaterSystem::UpdateLODWater` (0x004E3320, the far water: per water reference, visible or forced, it binds the
  reflected or the plain water shader, and clears them under water), `UpdateWaterSystem` (0x004E1BC0), `UpdateShader`
  (0x004E3590), `TESWorldSpace::SetWaterLODHeight` (0x00584150).
- `[ID FO-012]` the sky: `Sky::*` (31) and `SkyShader` (33).
- `[ID FO-001]` distant land: `BSDistantTree*` (18), `LODLand*` (5).
- Any crash address from a crash log or x64dbg: `fnv_where.py addr <address>` before anything else.
- Still to do: map every game address TTWVR hooks to its named function (one list, one sitting), so each TTWVR
  behaviour reads as "it replaces X" (board row, `[PD]`).

## Rules for using it

- It is CC0, so names, structures and even code may be used; credit it anyway (README credits).
- It explains the program; it does not replace a live check: a reading from it is `[inferred-static]` until the game
  shows it.
