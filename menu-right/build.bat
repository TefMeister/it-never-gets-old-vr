@echo off
rem Builds ngo_menu_right.dll (32-bit, like the game). Needs Visual Studio 2022's C++ tools (x86).
setlocal
set "VSWHERE=%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe"
for /f "usebackq delims=" %%i in (`"%VSWHERE%" -latest -products * -property installationPath`) do set "VS=%%i"
call "%VS%\VC\Auxiliary\Build\vcvarsall.bat" x86 >nul || exit /b 1
cd /d "%~dp0"
if not exist out mkdir out
cl /nologo /O2 /MT /W4 /LD ngo_menu_right.cpp /Fo:out\ /Fe:out\ngo_menu_right.dll /link /NOLOGO /NOIMPLIB /NOEXP /MACHINE:X86 user32.lib kernel32.lib || exit /b 1
echo built out\ngo_menu_right.dll
