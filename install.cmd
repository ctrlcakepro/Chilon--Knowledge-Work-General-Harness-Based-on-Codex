@echo off
setlocal
set SCRIPT_DIR=%~dp0
powershell -ExecutionPolicy Bypass -File "%SCRIPT_DIR%install.ps1"
if errorlevel 1 (
  echo.
  echo 安装失败，请查看上方信息。
  pause
  exit /b 1
)
echo.
echo 安装完成。
pause
