@echo off
echo ========================================
echo Hospital Management System - Build Tool
echo ========================================
echo.
echo Cleaning previous build files...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__
echo.
echo Building executable with PyInstaller...
echo This may take a few minutes...
echo.
pyinstaller --onefile --windowed --name "HospitalManagementSystem" --add-data "hospital_management.db;." main.py
echo.
if exist "dist\HospitalManagementSystem.exe" (
    echo ========================================
    echo BUILD SUCCESSFUL!
    echo ========================================
    echo.
    echo Executable created: dist\HospitalManagementSystem.exe
    echo.
    echo You can now:
    echo 1. Run the executable from: dist\HospitalManagementSystem.exe
    echo 2. Copy it to any Windows computer and run it
    echo 3. The database file is included in the executable
    echo.
) else (
    echo ========================================
    echo BUILD FAILED!
    echo ========================================
    echo Please check the error messages above.
    echo.
)
pause
