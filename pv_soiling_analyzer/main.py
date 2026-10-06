"""
main.py - Entry point for PV Soiling Analyzer
"""

import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    required = ['PyQt5', 'matplotlib', 'pandas', 'numpy', 'reportlab', 'openpyxl']
    missing = []
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    
    if missing:
        print("=" * 60)
        print("⚠️ Missing Dependencies Detected!")
        print("=" * 60)
        print("\nThe following packages are required but not installed:")
        for pkg in missing:
            print(f"  - {pkg}")
        print("\nPlease install them using:")
        print(f"  pip install {' '.join(missing)}")
        print("=" * 60)
        return False
    return True

def create_directories():
    """Create necessary directories"""
    for d in ['data', 'reports', 'logs']:
        path = Path(d)
        if not path.exists():
            path.mkdir(parents=True)
            print(f"✅ Created directory: {d}")

def show_splash():
    """Display splash screen"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║     ☀️ PV SOILING ANALYZER                                   ║
    ║     Solar Panel Dust Effect Analysis                        ║
    ║                                                              ║
    ║     Assessment of Dust Accumulation on                     ║
    ║     Photovoltaic Panel Performance                         ║
    ║                                                              ║
    ║     Federal University of Technology, Minna                 ║
    ║     Department of Materials and Metallurgical Engineering   ║
    ║                                                              ║
    ║     Version: 1.0.0                                          ║
    ║     Date: September, 2026                                   ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def main():
    show_splash()
    
    print("🔍 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    
    print("📁 Creating directories...")
    create_directories()
    
    print("🚀 Launching PV Soiling Analyzer...")
    print("   (Close the application window to exit)\n")
    
    from ui import run_app
    run_app()

if __name__ == "__main__":
    main()