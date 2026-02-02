@echo off
REM ============================================
REM Build script for Co Vay (Go Game) - Windows
REM ============================================

echo.
echo ========================================
echo   Building Co Vay (Go Game) executable
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.10 or later
    pause
    exit /b 1
)

REM Check if PyInstaller is installed
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo [ERROR] Failed to install PyInstaller
        pause
        exit /b 1
    )
)

REM Check if PySide6 is installed
pip show PySide6 >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing PySide6...
    pip install PySide6
    if errorlevel 1 (
        echo [ERROR] Failed to install PySide6
        pause
        exit /b 1
    )
)

REM Clean previous build
echo [INFO] Cleaning previous build...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

REM Build executable
echo [INFO] Building executable...
pyinstaller --clean GoGame.spec

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Build completed successfully!
echo ========================================
echo.
echo Output: dist\CoVay.exe
echo.
echo You can now run the game by double-clicking:
echo   dist\CoVay.exe
echo.

pause
