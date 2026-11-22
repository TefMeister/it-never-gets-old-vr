// ngo_menu_right.cpp -- Right = Down on the main menu's one-row layout (keyboard AND VR stick).  [ID FO-017]
//
// Why: our main menu shows its words in ONE ROW (tools/menu_row/). The list still moves by Up/Down. Left already works
// (each word's <xleft> names the word before it), but the menu file has no way to name the NEXT word, so Right did nothing.
//
// How (read off fnv_decomp, momusdigital, CC0; addresses checked on an unpacked FalloutNV.exe 1.4.0.525):
//   Keyboard and pad both end in InterfaceManager::HandleGamepadButton(0x0070F6E0, a direction number:
//   1 up, 2 down, 3 right, 4 left).
//   - keyboard: UpdateInterface calls HandleGamepadButton(itype) at 0x0070E52C;
//   - pad (TTWVR's fake pad in the headset): HandleGamepadButton reads the stick with
//     GetGamepadInput at 0x0070F838.
//   We re-point those two CALLs at small wrappers that change 3 into 2 ONLY while the chosen word's list carries our
//   menu trait _NeverGetsOldLeft = 1 (the main menu's top level; 0 in Load, Settings and the pause menu). Everything else
//   (edges, sounds, key repeat, Left, Settings sliders) stays the game's own.
// Chaining: each wrapper calls whatever the CALL pointed at before (TTWVR detours 0x0070F6E0's first bytes; that still
//   runs). A call site that is not a plain CALL is left alone and logged.
// Log: Documents\My Games\FalloutNV\ngo_menu_right.log (start-up, and the first remaps).
#include <windows.h>
#include <stdio.h>

// ---- settings table (game addresses, FalloutNV.exe 1.4.0.525) ----
static const DWORD CALL_KEY_DIRECTION = 0x0070E52C;  // call HandleGamepadButton(itype), keyboard path
static const DWORD CALL_PAD_DIRECTION = 0x0070F838;  // call GetGamepadInput(v, h, &up), pad path
static const DWORD EXPECT_KEY_TARGET  = 0x0070F6E0;  // HandleGamepadButton
static const DWORD EXPECT_PAD_TARGET  = 0x00710060;  // GetGamepadInput
static const DWORD INTERFACE_MANAGER  = 0x011D8A80;  // InterfaceManager* (global)
static const DWORD IM_ACTIVE_TILE     = 0xBC;        // InterfaceManager -> active tile (the game's own getter 0x0097AE90)
static const DWORD TILE_PARENT        = 0x28;        // Tile -> parent (fnv_decomp include/Tile.h)
static const DWORD TILE_TEXT_TO_TRAIT = 0x00A01860;  // int Tile::TextToTrait(const char*), cdecl
static const DWORD TILE_GET_FLOAT     = 0x00A011B0;  // float Tile::GetFloat(int trait), thiscall; 0 when absent
static const int   DIR_DOWN = 2, DIR_RIGHT = 3;
static const int   LOG_REMAPS = 20;                  // only the first few remaps are logged
static const char* ROW_TRAIT = "_NeverGetsOldLeft";

typedef int  (__thiscall* GetGamepadInput_t)(void*, bool, bool, bool*);
typedef void (__thiscall* HandleGamepadButton_t)(void*, int);
typedef int  (__cdecl*    TextToTrait_t)(const char*);
typedef float(__thiscall* GetFloat_t)(void*, int);

static GetGamepadInput_t     g_getPad;
static HandleGamepadButton_t g_handle;
static int  g_rowTrait = (int)0x80000000;
static int  g_logged;
static char g_logPath[MAX_PATH];

static void Log(const char* fmt, ...)
{
    if (!g_logPath[0]) return;
    FILE* f = nullptr;
    if (fopen_s(&f, g_logPath, "a") || !f) return;
    SYSTEMTIME t; GetLocalTime(&t);
    fprintf(f, "%02d:%02d:%02d ", t.wHour, t.wMinute, t.wSecond);
    va_list a; va_start(a, fmt); vfprintf(f, fmt, a); va_end(a);
    fputc('\n', f); fclose(f);
}

static bool OnTheRow()
{
    char* im = *(char**)INTERFACE_MANAGER;
    if (!im) return false;
    char* active = *(char**)(im + IM_ACTIVE_TILE);
    if (!active) return false;
    char* list = *(char**)(active + TILE_PARENT);
    if (!list) return false;
    if (g_rowTrait == (int)0x80000000) {             // known only once the menu file has been read
        g_rowTrait = ((TextToTrait_t)TILE_TEXT_TO_TRAIT)(ROW_TRAIT);
        if (g_rowTrait == (int)0x80000000) return false;
        Log("trait %s = %d", ROW_TRAIT, g_rowTrait);
    }
    return ((GetFloat_t)TILE_GET_FLOAT)(list, g_rowTrait) != 0.0f;
}

static int Remap(int dir, const char* from)
{
    if (dir != DIR_RIGHT || !OnTheRow()) return dir;
    if (g_logged < LOG_REMAPS) { ++g_logged; Log("%s: Right -> Down on the main menu row", from); }
    return DIR_DOWN;
}

// __fastcall with an unused EDX = __thiscall for the caller (this in ECX, arguments on the stack, callee cleans).
static int __fastcall PadDirection(void* im, void*, bool repeatV, bool repeatH, bool* isUp)
{
    return Remap(g_getPad(im, repeatV, repeatH, isUp), "pad");
}
static void __fastcall KeyDirection(void* im, void*, int dir)
{
    g_handle(im, Remap(dir, "key"));
}

static DWORD RepointCall(DWORD site, DWORD expect, void* wrapper, const char* what)
{
    BYTE* p = (BYTE*)site;
    if (p[0] != 0xE8) { Log("%s: 0x%08X is not a CALL (0x%02X), left alone", what, site, p[0]); return 0; }
    DWORD target = site + 5 + *(LONG*)(p + 1);
    if (target != expect) Log("%s: CALL at 0x%08X already points at 0x%08X (another mod?), chaining to it", what, site, target);
    DWORD old;
    if (!VirtualProtect(p, 5, PAGE_EXECUTE_READWRITE, &old)) { Log("%s: VirtualProtect failed", what); return 0; }
    *(LONG*)(p + 1) = (LONG)((DWORD)wrapper - (site + 5));
    VirtualProtect(p, 5, old, &old);
    FlushInstructionCache(GetCurrentProcess(), p, 5);
    Log("%s: CALL at 0x%08X now goes through us, then 0x%08X", what, site, target);
    return target;
}

// ---- NVSE plugin entry points (only the fields we read) ----
struct NVSEInterface { UINT32 nvseVersion, runtimeVersion, editorVersion, isEditor; };
struct PluginInfo { UINT32 infoVersion; const char* name; UINT32 version; };
static const UINT32 RUNTIME_1_4_0_525 = 0x040020D0;

extern "C" __declspec(dllexport) bool NVSEPlugin_Query(const NVSEInterface* nvse, PluginInfo* info)
{
    info->infoVersion = 1; info->name = "NeverGetsOldMenuRight"; info->version = 1;
    return !nvse->isEditor && nvse->runtimeVersion == RUNTIME_1_4_0_525;
}

extern "C" __declspec(dllexport) bool NVSEPlugin_Load(const NVSEInterface* nvse)
{
    if (nvse->isEditor) return true;
    char docs[MAX_PATH];
    if (GetEnvironmentVariableA("USERPROFILE", docs, MAX_PATH))
        sprintf_s(g_logPath, "%s/Documents/My Games/FalloutNV/ngo_menu_right.log", docs);
    Log("NeverGetsOldMenuRight 1 loading");
    g_handle = (HandleGamepadButton_t)RepointCall(CALL_KEY_DIRECTION, EXPECT_KEY_TARGET, (void*)&KeyDirection, "key");
    g_getPad = (GetGamepadInput_t)RepointCall(CALL_PAD_DIRECTION, EXPECT_PAD_TARGET, (void*)&PadDirection, "pad");
    return true;
}
