"""
build_exe.py - Build PV Soiling Analyzer as standalone EXE
Creates EXE in 'cla' folder at the root directory
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def clean_build():
    """Clean previous build files"""
    print("🧹 Cleaning previous builds...")
    dirs_to_remove = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  ✅ Removed {dir_name}/")
    
    # Remove .spec files
    for file in Path('.').glob('*.spec'):
        file.unlink()
        print(f"  ✅ Removed {file.name}")
    
    print("✅ Clean complete!\n")

def create_cla_folder():
    """Create cla folder on Desktop"""
    desktop = Path.home() / 'Desktop'
    cla_folder = desktop / 'cla'
    
    if not cla_folder.exists():
        cla_folder.mkdir(parents=True)
        print(f"✅ Created folder: {cla_folder}")
    else:
        print(f"✅ Folder exists: {cla_folder}")
    
    return cla_folder

def build_exe():
    """Build the EXE file"""
    print("=" * 60)
    print("  PV SOILING ANALYZER - EXE BUILDER")
    print("  Department of Materials and Metallurgical Engineering")
    print("  Federal University of Technology, Minna")
    print("=" * 60)
    print()
    
    # Clean previous builds
    clean_build()
    
    # Check if PyInstaller is installed
    print("📦 Checking PyInstaller...")
    try:
        import PyInstaller
        print("✅ PyInstaller is installed")
    except ImportError:
        print("⚠️  PyInstaller not found. Installing...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
        print("✅ PyInstaller installed")
    
    print()
    print("🔨 Building EXE...")
    print("   This may take 3-5 minutes...")
    print()
    
    # PyInstaller command
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--windowed',
        '--name', 'PVSoilingAnalyzer',
        '--add-data', f'reports{os.pathsep}reports',
        '--add-data', f'data{os.pathsep}data',
        '--hidden-import', 'PyQt5',
        '--hidden-import', 'PyQt5.QtWidgets',
        '--hidden-import', 'PyQt5.QtCore',
        '--hidden-import', 'PyQt5.QtGui',
        '--hidden-import', 'matplotlib',
        '--hidden-import', 'matplotlib.backends.backend_qt5agg',
        '--hidden-import', 'pandas',
        '--hidden-import', 'numpy',
        '--hidden-import', 'sqlalchemy',
        '--hidden-import', 'reportlab',
        '--hidden-import', 'openpyxl',
        '--hidden-import', 'plotly',
        '--hidden-import', 'seaborn',
        '--hidden-import', 'database',
        '--hidden-import', 'core',
        '--hidden-import', 'ui',
        '--hidden-import', 'visualization',
        '--hidden-import', 'reports',
        '--collect-all', 'matplotlib',
        '--collect-all', 'pyqt5',
        '--exclude-module', 'tkinter',
        '--exclude-module', 'tcl',
        'main.py'
    ]
    
    # Run PyInstaller
    result = subprocess.run(cmd)
    
    if result.returncode != 0:
        print("\n❌ Build failed!")
        print("   Check the error messages above.")
        return False
    
    print("\n✅ BUILD SUCCESSFUL!")
    return True

def copy_to_cla():
    """Copy the EXE to cla folder on Desktop"""
    print()
    print("📁 Copying to cla folder...")
    
    # Create cla folder on Desktop
    cla_folder = create_cla_folder()
    
    # Source and destination
    src_exe = Path('dist/PVSoilingAnalyzer.exe')
    dst_exe = cla_folder / 'PVSoilingAnalyzer.exe'
    
    if not src_exe.exists():
        print("❌ EXE not found in dist/")
        return False
    
    # Copy EXE
    shutil.copy2(src_exe, dst_exe)
    print(f"  ✅ Copied: {dst_exe}")
    
    # Copy data and reports folders
    for folder in ['data', 'reports']:
        src_folder = Path(folder)
        dst_folder = cla_folder / folder
        if src_folder.exists():
            if dst_folder.exists():
                shutil.rmtree(dst_folder)
            shutil.copytree(src_folder, dst_folder)
            print(f"  ✅ Copied: {dst_folder}/")
    
    # Create run script
    create_run_script(cla_folder)
    create_readme(cla_folder)
    
    print()
    print("=" * 60)
    print("  ✅ EXE READY FOR USE!")
    print("=" * 60)
    print(f"  📁 Location: {cla_folder}")
    print(f"  📄 File: {dst_exe.name}")
    print("=" * 60)
    
    return True

def create_run_script(cla_folder):
    """Create a batch file to run the EXE"""
    run_bat = cla_folder / 'run_app.bat'
    with open(run_bat, 'w') as f:
        f.write("""@echo off
title PV Soiling Analyzer
echo ============================================================
echo  PV SOILING ANALYZER
echo  Solar Panel Dust Effect Analysis
echo  Department of Materials and Metallurgical Engineering
echo  Federal University of Technology, Minna
echo ============================================================
echo.
echo Starting application...
echo.
start "" "PVSoilingAnalyzer.exe"
echo Application started!
echo.
pause
""")
    print(f"  ✅ Created: {run_bat}")

def create_readme(cla_folder):
    """Create a README file"""
    readme = cla_folder / 'README.txt'
    with open(readme, 'w') as f:
        f.write("""
============================================================
  PV SOILING ANALYZER - Standalone Application
  Department of Materials and Metallurgical Engineering
  Federal University of Technology, Minna
============================================================

📁 Location: Desktop/cla/

📄 Files:
  - PVSoilingAnalyzer.exe  (Main application)
  - run_app.bat            (Quick launch script)
  - data/                  (Database folder)
  - reports/               (Generated reports)
  - README.txt             (This file)

🚀 HOW TO RUN:
  Double-click PVSoilingAnalyzer.exe or run_app.bat

📋 FEATURES:
  - PV Soiling Analysis
  - Power Output Calculations
  - Soiling Loss and Ratio
  - Voltage and Current Drop Analysis
  - Regression Analysis
  - Dashboard and Graphs
  - PDF/Excel Report Generation

⚠️  REQUIREMENTS:
  - Windows 7 or later
  - No Python installation needed!

🔧 TROUBLESHOOTING:
  If the application doesn't start:
  1. Make sure all files are in the same folder
  2. Check that data/ and reports/ folders exist
  3. Try running as Administrator

============================================================
""")
    print(f"  ✅ Created: {readme}")

def main():
    """Main build function"""
    # Build the EXE
    if not build_exe():
        sys.exit(1)
    
    # Copy to cla folder
    if not copy_to_cla():
        sys.exit(1)
    
    print()
    print("🎉 Build complete! The EXE is ready in Desktop/cla/")
    print()

if __name__ == "__main__":
    main()