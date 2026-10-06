@echo off
echo ============================================================
echo  PV SOILING ANALYZER - EXE BUILDER
echo  Department of Materials and Metallurgical Engineering
echo  Federal University of Technology, Minna
echo ============================================================
echo.

echo [1/4] Installing PyInstaller...
python -m pip install pyinstaller --quiet
echo ✅ PyInstaller ready!
echo.

echo [2/4] Building EXE...
echo This may take 3-5 minutes...
python -m PyInstaller --onefile --windowed --name PVSoilingAnalyzer --add-data "reports;reports" --add-data "data;data" --hidden-import PyQt5 --hidden-import PyQt5.QtWidgets --hidden-import PyQt5.QtCore --hidden-import PyQt5.QtGui --hidden-import matplotlib --hidden-import matplotlib.backends.backend_qt5agg --hidden-import pandas --hidden-import numpy --hidden-import sqlalchemy --hidden-import reportlab --hidden-import openpyxl --hidden-import plotly --hidden-import seaborn --collect-all matplotlib --collect-all pyqt5 --exclude-module tkinter main.py

if errorlevel 1 (
    echo ❌ Build failed!
    pause
    exit /b 1
)
echo ✅ Build complete!
echo.

echo [3/4] Creating cla folder on Desktop...
set CLA_DIR=%USERPROFILE%\Desktop\cla
if not exist "%CLA_DIR%" mkdir "%CLA_DIR%"
echo ✅ Created: %CLA_DIR%
echo.

echo [4/4] Copying files...
copy "dist\PVSoilingAnalyzer.exe" "%CLA_DIR%\"
xcopy "data" "%CLA_DIR%\data\" /E /I /Y >nul
xcopy "reports" "%CLA_DIR%\reports\" /E /I /Y >nul

echo.
echo ============================================================
echo  ✅ BUILD COMPLETE!
echo ============================================================
echo.
echo 📁 Location: %USERPROFILE%\Desktop\cla
echo 📄 File: PVSoilingAnalyzer.exe
echo.
echo To run:
echo   Double-click PVSoilingAnalyzer.exe in the cla folder
echo.
pause