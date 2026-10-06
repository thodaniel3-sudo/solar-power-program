"""
ui.py - Complete Professional GUI for PV Soiling Analyzer
Graphs and Calculations open in separate popup windows
"""

import sys
import os
from datetime import datetime
from typing import Dict, List

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
    QTabWidget, QGroupBox, QFormLayout, QMessageBox, QTextEdit,
    QDoubleSpinBox, QSpinBox, QHeaderView, QFileDialog, QSplitter,
    QScrollArea, QFrame, QComboBox, QTreeWidget, QTreeWidgetItem,
    QGridLayout, QDialog, QTabWidget as QTabWidget2
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPixmap

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from core import PVSoilingAnalyzer
from database import Database
from visualization import PVSoilingVisualizer
from reports import ReportGenerator


class GraphWindow(QDialog):
    """Separate window for displaying graphs - Professional styling"""
    def __init__(self, figure, title="Graph", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumSize(1000, 700)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a2e;
            }
            QLabel {
                color: #ccd6f6;
            }
        """)
        
        layout = QVBoxLayout(self)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title_label.setStyleSheet("color: #64ffda; padding: 10px;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        canvas = FigureCanvas(figure)
        canvas.setMinimumHeight(600)
        layout.addWidget(canvas)
        
        toolbar = NavigationToolbar(canvas, self)
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #0f0f23;
                border: none;
                padding: 4px;
            }
            QToolButton {
                background-color: transparent;
                color: #ccd6f6;
                border: none;
                padding: 4px;
            }
            QToolButton:hover {
                background-color: #2d2d44;
                border-radius: 4px;
            }
        """)
        layout.addWidget(toolbar)
        
        close_btn = QPushButton("Close Graph")
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #64ffda;
                color: #1a1a2e;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #4cd8b5;
            }
        """)
        layout.addWidget(close_btn)


class CalculatorWindow(QDialog):
    """Separate window for displaying detailed calculations"""
    def __init__(self, calculations, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Detailed Calculations - Step by Step")
        self.setMinimumSize(1000, 750)
        self.setMaximumSize(1200, 900)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a2e;
            }
            QLabel {
                color: #ccd6f6;
            }
            QTextEdit {
                background-color: #0a0a1a;
                color: #ccd6f6;
                border: 1px solid #2d2d44;
                border-radius: 4px;
                font-family: 'Consolas', monospace;
                font-size: 11px;
            }
            QTabWidget::pane {
                border: 1px solid #2d2d44;
                border-radius: 4px;
                background-color: #0f0f23;
            }
            QTabBar::tab {
                background-color: #1a1a2e;
                color: #a8b2d1;
                padding: 8px 16px;
                border: 1px solid #2d2d44;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #16213e;
                color: #64ffda;
                border-bottom: 2px solid #64ffda;
            }
            QGroupBox {
                font-weight: bold;
                color: #64ffda;
                border: 2px solid #2d2d44;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px;
                color: #64ffda;
            }
        """)
        
        self.calculations = calculations
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("📊 Detailed Calculations - Step by Step")
        header.setFont(QFont("Segoe UI", 18, QFont.Bold))
        header.setStyleSheet("color: #64ffda; padding: 10px;")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Tab widget for different calculation sections
        tabs = QTabWidget2()
        
        # Tab 1: Module Specifications
        tabs.addTab(self._create_module_specs_tab(), "Module Specs")
        
        # Tab 2: Module Calculations
        tabs.addTab(self._create_module_calculations_tab(), "Module Calculations")
        
        # Tab 3: Weekly Calculations
        tabs.addTab(self._create_weekly_calculations_tab(), "Weekly Calculations")
        
        # Tab 4: Regression Analysis
        tabs.addTab(self._create_regression_tab(), "Regression Analysis")
        
        # Tab 5: Summary
        tabs.addTab(self._create_summary_tab(), "Summary")
        
        layout.addWidget(tabs)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #64ffda;
                color: #1a1a2e;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #4cd8b5;
            }
        """)
        layout.addWidget(close_btn)
    
    def _create_module_specs_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        info_text = "Jinko Solar 650W Tiger Neo - Module Specifications\n"
        info_text += "=" * 60 + "\n\n"
        
        specs = self.calculations.get('module_specs', {})
        for key, value in specs.items():
            label = key.replace('_', ' ').title()
            info_text += f"{label:20} : {value}\n"
        
        text = QTextEdit()
        text.setPlainText(info_text)
        text.setReadOnly(True)
        text.setFont(QFont("Consolas", 11))
        layout.addWidget(text)
        
        return tab
    
    def _create_module_calculations_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        text = QTextEdit()
        text.setReadOnly(True)
        text.setFont(QFont("Consolas", 11))
        
        info = "🔬 MODULE CALCULATIONS\n"
        info += "=" * 60 + "\n\n"
        
        module_calc = self.calculations.get('module_calculations', {})
        
        # Area calculation
        if 'area' in module_calc:
            a = module_calc['area']
            info += "📐 1. MODULE SURFACE AREA\n"
            info += "   " + "-" * 40 + "\n"
            info += f"   Formula:     {a.get('formula', 'N/A')}\n"
            info += f"   Calculation: {a.get('calculation', 'N/A')}\n"
            info += f"   Result:      {a.get('result', 'N/A')}\n\n"
        
        # Efficiency calculation
        if 'efficiency' in module_calc:
            e = module_calc['efficiency']
            info += "⚡ 2. MODULE EFFICIENCY (STC)\n"
            info += "   " + "-" * 40 + "\n"
            info += f"   Formula:     {e.get('formula', 'N/A')}\n"
            info += f"   Calculation: {e.get('calculation', 'N/A')}\n"
            info += f"   Result:      {e.get('result', 'N/A')}\n\n"
        
        # Fill Factor calculation
        if 'fill_factor' in module_calc:
            ff = module_calc['fill_factor']
            info += "📊 3. FILL FACTOR\n"
            info += "   " + "-" * 40 + "\n"
            info += f"   Formula:     {ff.get('formula', 'N/A')}\n"
            info += f"   Calculation: {ff.get('calculation', 'N/A')}\n"
            info += f"   Result:      {ff.get('result', 'N/A')}\n"
            if 'details' in ff:
                for k, v in ff['details'].items():
                    info += f"   {k}: {v}\n"
        
        text.setPlainText(info)
        layout.addWidget(text)
        
        return tab
    
    def _create_weekly_calculations_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        text = QTextEdit()
        text.setReadOnly(True)
        text.setFont(QFont("Consolas", 11))
        
        info = "📊 WEEKLY CALCULATIONS\n"
        info += "=" * 60 + "\n\n"
        
        weekly = self.calculations.get('weekly_calculations', [])
        
        for week_data in weekly:
            week = week_data.get('week', 'N/A')
            info += f"📍 WEEK {week}\n"
            info += "   " + "-" * 40 + "\n"
            
            # Clean panel
            clean = week_data.get('clean_power', {})
            info += f"   Clean Panel:\n"
            info += f"      V = {week_data.get('clean_voltage', 'N/A'):.2f} V\n"
            info += f"      I = {week_data.get('clean_current', 'N/A'):.2f} A\n"
            if isinstance(clean, dict):
                info += f"      P = {clean.get('calculation', 'N/A')}\n"
                info += f"      Result: {clean.get('result', 'N/A')}\n"
            
            # Dusty panel
            dusty = week_data.get('dusty_power', {})
            info += f"   Dusty Panel:\n"
            info += f"      V = {week_data.get('dusty_voltage', 'N/A'):.2f} V\n"
            info += f"      I = {week_data.get('dusty_current', 'N/A'):.2f} A\n"
            if isinstance(dusty, dict):
                info += f"      P = {dusty.get('calculation', 'N/A')}\n"
                info += f"      Result: {dusty.get('result', 'N/A')}\n"
            
            # Soiling metrics
            sl = week_data.get('soiling_loss', {})
            if isinstance(sl, dict):
                info += f"\n   Soiling Loss:\n"
                info += f"      {sl.get('formula', 'N/A')}\n"
                info += f"      {sl.get('calculation', 'N/A')}\n"
                info += f"      Result: {sl.get('result', 'N/A')}\n"
            
            sr = week_data.get('soiling_ratio', {})
            if isinstance(sr, dict):
                info += f"\n   Soiling Ratio:\n"
                info += f"      {sr.get('formula', 'N/A')}\n"
                info += f"      {sr.get('calculation', 'N/A')}\n"
                info += f"      Result: {sr.get('result', 'N/A')}\n"
                if 'interpretation' in sr:
                    info += f"      Interpretation: {sr['interpretation']}\n"
            
            vd = week_data.get('voltage_drop', {})
            if isinstance(vd, dict):
                info += f"\n   Voltage Drop:\n"
                info += f"      {vd.get('formula', 'N/A')}\n"
                info += f"      {vd.get('calculation', 'N/A')}\n"
                info += f"      Result: {vd.get('result', 'N/A')}\n"
            
            cd = week_data.get('current_drop', {})
            if isinstance(cd, dict):
                info += f"\n   Current Drop:\n"
                info += f"      {cd.get('formula', 'N/A')}\n"
                info += f"      {cd.get('calculation', 'N/A')}\n"
                info += f"      Result: {cd.get('result', 'N/A')}\n"
            
            pl = week_data.get('power_loss', {})
            if isinstance(pl, dict):
                info += f"\n   Power Loss:\n"
                info += f"      {pl.get('formula', 'N/A')}\n"
                info += f"      {pl.get('calculation', 'N/A')}\n"
                info += f"      Result: {pl.get('result', 'N/A')}\n"
            
            info += "\n" + "-" * 40 + "\n\n"
        
        text.setPlainText(info)
        layout.addWidget(text)
        
        return tab
    
    def _create_regression_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        text = QTextEdit()
        text.setReadOnly(True)
        text.setFont(QFont("Consolas", 11))
        
        info = "📈 REGRESSION ANALYSIS\n"
        info += "=" * 60 + "\n\n"
        
        reg = self.calculations.get('regression', {})
        
        if reg:
            info += "🔍 Linear Regression: SL = a × Week + b\n"
            info += "   " + "-" * 40 + "\n\n"
            
            info += "📊 Data Points:\n"
            info += f"   Weeks (x): {reg.get('x_values', 'N/A')}\n"
            info += f"   Soiling Loss (y): {reg.get('y_values', 'N/A')}\n\n"
            
            info += "📐 Step-by-Step Calculation:\n"
            info += "   " + "-" * 40 + "\n"
            
            step_by_step = reg.get('step_by_step', {})
            for key, value in step_by_step.items():
                info += f"   {key}: {value}\n"
            
            info += "\n📊 Results:\n"
            info += "   " + "-" * 40 + "\n"
            info += f"   Slope (b):     {reg.get('slope', 0):.4f} % per week\n"
            info += f"   Intercept (a): {reg.get('intercept', 0):.4f}\n"
            info += f"   R² Value:      {reg.get('r_squared', 0):.4f}\n"
            info += f"   Equation:      {reg.get('equation', 'N/A')}\n"
            
            info += "\n📈 Interpretation:\n"
            info += "   " + "-" * 40 + "\n"
            info += f"   The soiling loss increases by {reg.get('slope', 0):.3f}% per week.\n"
            info += f"   The R² value of {reg.get('r_squared', 0):.4f} indicates a "
            if reg.get('r_squared', 0) > 0.95:
                info += "very strong"
            elif reg.get('r_squared', 0) > 0.85:
                info += "strong"
            else:
                info += "moderate"
            info += " linear relationship.\n"
        
        text.setPlainText(info)
        layout.addWidget(text)
        
        return tab
    
    def _create_summary_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        text = QTextEdit()
        text.setReadOnly(True)
        text.setFont(QFont("Consolas", 11))
        
        info = "📋 SUMMARY\n"
        info += "=" * 60 + "\n\n"
        
        summary = self.calculations.get('summary', {})
        
        for key, value in summary.items():
            label = key.replace('_', ' ').title()
            info += f"   {label:20}: {value}\n"
        
        text.setPlainText(info)
        layout.addWidget(text)
        
        return tab


class MatplotlibCanvas(FigureCanvas):
    """Canvas for displaying matplotlib figures in the main window"""
    def __init__(self, parent=None, width=14, height=8, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MatplotlibCanvas, self).__init__(self.fig)
        self.setParent(parent)
        self.fig.tight_layout()
        self.draw()


class MainWindow(QMainWindow):
    """Main application window - Professional Version"""
    
    def __init__(self):
        super().__init__()
        print("🔧 Initializing PV Soiling Analyzer...")
        
        self.db = Database()
        self.analyzer = PVSoilingAnalyzer()
        self.visualizer = PVSoilingVisualizer()
        self.report_gen = ReportGenerator(self.db)
        self.current_experiment_id = None
        self.all_calculations = None
        self.graph_window = None
        self.calc_window = None
        
        self.init_ui()
        self.load_data()
        self.run_full_calculation()
        print("✅ Application ready!")
    
    def init_ui(self):
        """Initialize the professional user interface"""
        self.setWindowTitle("☀️ PV Soiling Analyzer - Professional Edition")
        self.setGeometry(50, 50, 1200, 800)
        
        # Professional dark theme
        self.setStyleSheet("""
            QMainWindow { background-color: #1a1a2e; }
            QTabWidget::pane { 
                border: 1px solid #2d2d44; 
                border-radius: 8px; 
                background-color: #16213e; 
            }
            QTabBar::tab { 
                background-color: #1a1a2e; 
                color: #a8b2d1; 
                padding: 12px 24px; 
                border: 1px solid #2d2d44; 
                border-bottom: none; 
                border-top-left-radius: 6px; 
                border-top-right-radius: 6px; 
                font-weight: bold;
            }
            QTabBar::tab:selected { 
                background-color: #16213e; 
                color: #64ffda; 
                border-bottom: 2px solid #64ffda; 
            }
            QTabBar::tab:hover {
                background-color: #2d2d44;
                color: #ffffff;
            }
            QPushButton { 
                background-color: #64ffda; 
                color: #1a1a2e; 
                border: none; 
                padding: 10px 20px; 
                border-radius: 6px; 
                font-weight: bold; 
                font-size: 12px;
            }
            QPushButton:hover { background-color: #4cd8b5; }
            QPushButton:disabled { background-color: #2d2d44; color: #a8b2d1; }
            QGroupBox { 
                font-weight: bold; 
                color: #64ffda;
                border: 2px solid #2d2d44; 
                border-radius: 8px; 
                margin-top: 16px; 
                padding-top: 16px; 
            }
            QGroupBox::title { 
                subcontrol-origin: margin; 
                left: 10px; 
                padding: 0 10px; 
                color: #64ffda;
            }
            QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                border: 1px solid #2d2d44; 
                border-radius: 4px; 
                padding: 8px; 
                background-color: #0f0f23; 
                color: #ccd6f6;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border: 2px solid #64ffda;
            }
            QTableWidget {
                border: 1px solid #2d2d44; 
                border-radius: 4px; 
                background-color: #0f0f23;
                color: #ccd6f6;
                gridline-color: #2d2d44;
            }
            QTableWidget::item { padding: 6px; }
            QTableWidget::item:selected { background-color: #2d2d44; }
            QHeaderView::section {
                background-color: #1a1a2e; 
                color: #64ffda; 
                padding: 8px; 
                border: 1px solid #2d2d44;
                font-weight: bold;
            }
            QLabel {
                color: #ccd6f6;
            }
            QTextEdit {
                background-color: #0f0f23;
                color: #ccd6f6;
                border: 1px solid #2d2d44;
                border-radius: 4px;
            }
            QTreeWidget {
                background-color: #0f0f23;
                color: #ccd6f6;
                border: 1px solid #2d2d44;
                border-radius: 4px;
            }
            QTreeWidget::item { padding: 4px; }
            QTreeWidget::item:selected { background-color: #2d2d44; }
            QScrollBar::handle { background-color: #2d2d44; border-radius: 4px; }
        """)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Header
        header = self._create_header()
        layout.addWidget(header)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self._create_dashboard_tab(), "Dashboard")
        self.tabs.addTab(self._create_graph_tab(), "Graphs")
        self.tabs.addTab(self._create_calculator_tab(), "Calculator")
        self.tabs.addTab(self._create_data_tab(), "Data")
        self.tabs.addTab(self._create_results_tab(), "Results")
        self.tabs.addTab(self._create_report_tab(), "Reports")
        
        layout.addWidget(self.tabs)
        
        # Status bar
        self.statusBar().setStyleSheet("QStatusBar { background-color: #1a1a2e; color: #a8b2d1; padding: 4px; }")
        self.statusBar().showMessage("System Ready")
    
    def _create_header(self) -> QWidget:
        """Create professional header"""
        header = QWidget()
        header.setStyleSheet("""
            background-color: #0f0f23;
            border-radius: 8px;
            padding: 12px;
        """)
        layout = QHBoxLayout(header)
        
        title = QLabel("PV Soiling Analyzer")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color: #64ffda;")
        layout.addWidget(title)
        
        subtitle = QLabel("Professional Edition v2.0")
        subtitle.setFont(QFont("Segoe UI", 10))
        subtitle.setStyleSheet("color: #a8b2d1;")
        layout.addWidget(subtitle)
        
        layout.addStretch()
        
        info = QLabel("Minna Soiling Test 2026 | Jinko 650W Panels")
        info.setFont(QFont("Segoe UI", 10))
        info.setStyleSheet("color: #8892b0;")
        layout.addWidget(info)
        
        self.time_label = QLabel()
        self.time_label.setFont(QFont("Segoe UI", 10))
        self.time_label.setStyleSheet("color: #8892b0;")
        layout.addWidget(self.time_label)
        
        timer = QTimer()
        timer.timeout.connect(self._update_time)
        timer.start(1000)
        self._update_time()
        
        return header
    
    def _update_time(self):
        self.time_label.setText(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    def _create_dashboard_tab(self) -> QWidget:
        """Create professional dashboard tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Stats cards in a grid
        stats_widget = QWidget()
        stats_widget.setStyleSheet("background-color: #0f0f23; border-radius: 8px; padding: 10px;")
        stats_layout = QGridLayout(stats_widget)
        
        stats = [
            ("Weeks", "5"),
            ("Soiling Loss", "7.90%"),
            ("Avg / Week", "1.79%"),
            ("R² Value", "0.997"),
            ("Power Loss", "45.69W"),
            ("Recommendation", "Clean 2-3 weeks")
        ]
        
        for i, (label, value) in enumerate(stats):
            row = i // 3
            col = i % 3
            card = self._create_stat_card(label, value)
            stats_layout.addWidget(card, row, col)
        
        layout.addWidget(stats_widget)
        
        # Dashboard chart
        self.dashboard_canvas = MatplotlibCanvas(self, width=14, height=5)
        layout.addWidget(self.dashboard_canvas)
        
        # Info label
        info = QLabel("Real experimental data from Minna soiling test (5 weeks) | Harmattan period")
        info.setAlignment(Qt.AlignCenter)
        info.setStyleSheet("padding: 10px; background-color: #0f0f23; border-radius: 8px; color: #8892b0;")
        layout.addWidget(info)
        
        refresh_btn = QPushButton("Refresh Dashboard")
        refresh_btn.clicked.connect(self._update_dashboard)
        refresh_btn.setStyleSheet("background-color: #64ffda; color: #1a1a2e;")
        layout.addWidget(refresh_btn)
        
        return tab
    
    def _create_stat_card(self, label: str, value: str) -> QWidget:
        """Create a professional statistics card"""
        card = QWidget()
        card.setStyleSheet("""
            background-color: #1a1a2e;
            border-radius: 8px;
            padding: 12px;
            border: 1px solid #2d2d44;
        """)
        layout = QVBoxLayout(card)
        
        label_widget = QLabel(label)
        label_widget.setFont(QFont("Segoe UI", 10))
        label_widget.setStyleSheet("color: #8892b0;")
        layout.addWidget(label_widget)
        
        value_widget = QLabel(value)
        value_widget.setFont(QFont("Segoe UI", 20, QFont.Bold))
        value_widget.setStyleSheet("color: #64ffda;")
        value_widget.setObjectName("value_label")
        layout.addWidget(value_widget)
        
        return card
    
    def _create_graph_tab(self) -> QWidget:
        """Create graph tab - OPENS GRAPHS IN SEPARATE WINDOW"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        selector_widget = QWidget()
        selector_widget.setStyleSheet("background-color: #0f0f23; border-radius: 8px; padding: 20px;")
        selector_layout = QVBoxLayout(selector_widget)
        
        title_label = QLabel("📊 Graph Viewer")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title_label.setStyleSheet("color: #64ffda;")
        title_label.setAlignment(Qt.AlignCenter)
        selector_layout.addWidget(title_label)
        
        select_layout = QHBoxLayout()
        select_layout.addStretch()
        
        selector_label = QLabel("Select Graph:")
        selector_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        selector_label.setStyleSheet("color: #ccd6f6;")
        select_layout.addWidget(selector_label)
        
        self.graph_selector = QComboBox()
        self.graph_selector.addItems([
            "Dashboard (All Charts)",
            "Power Comparison",
            "Soiling Loss with Regression",
            "Voltage & Current Drop",
            "Soiling Ratio",
            "Power Loss Bar Chart"
        ])
        self.graph_selector.setStyleSheet("""
            QComboBox {
                background-color: #1a1a2e;
                color: #ccd6f6;
                border: 1px solid #2d2d44;
                border-radius: 4px;
                padding: 8px;
                min-width: 250px;
            }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView {
                background-color: #1a1a2e;
                color: #ccd6f6;
                selection-background-color: #2d2d44;
            }
        """)
        select_layout.addWidget(self.graph_selector)
        select_layout.addStretch()
        
        selector_layout.addLayout(select_layout)
        
        open_graph_btn = QPushButton("📈 Open Graph in New Window")
        open_graph_btn.clicked.connect(self._open_graph_window)
        open_graph_btn.setStyleSheet("""
            QPushButton {
                background-color: #64ffda;
                color: #1a1a2e;
                border: none;
                padding: 15px 30px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #4cd8b5;
            }
        """)
        selector_layout.addWidget(open_graph_btn)
        
        preview_label = QLabel("Click the button above to open the selected graph in a new window")
        preview_label.setAlignment(Qt.AlignCenter)
        preview_label.setStyleSheet("color: #8892b0; padding: 10px;")
        selector_layout.addWidget(preview_label)
        
        layout.addWidget(selector_widget)
        
        return tab
    
    def _open_graph_window(self):
        """Open the selected graph in a separate window"""
        try:
            print("Opening graph in new window...")
            
            data = self.analyzer.get_experimental_data()
            regression = self.analyzer.linear_regression(data['weeks'], data['soiling_loss'])
            data['regression'] = regression
            
            selection = self.graph_selector.currentIndex()
            selected_name = self.graph_selector.currentText()
            print(f"   Selected: {selected_name}")
            
            if selection == 0:
                fig = self.visualizer.create_dashboard(data)
                title = "PV Soiling Dashboard"
            elif selection == 1:
                fig = self.visualizer.plot_power_comparison(
                    data['weeks'], data['clean_power'], data['dusty_power']
                )
                title = "Power Comparison - Clean vs Dusty Panel"
            elif selection == 2:
                fig = self.visualizer.plot_soiling_loss(
                    data['weeks'], data['soiling_loss'], regression
                )
                title = "Soiling Loss with Regression"
            elif selection == 3:
                fig = self.visualizer.plot_voltage_current_drop(
                    data['weeks'], data['voltage_drop'], data['current_drop']
                )
                title = "Voltage & Current Drop"
            elif selection == 4:
                fig = self.visualizer.plot_soiling_ratio(
                    data['weeks'], data['soiling_ratio']
                )
                title = "Soiling Ratio Trend"
            elif selection == 5:
                fig = self.visualizer.plot_power_loss(
                    data['weeks'], data['power_loss']
                )
                title = "Power Loss Bar Chart"
            else:
                fig = self.visualizer.create_dashboard(data)
                title = "PV Soiling Dashboard"
            
            self.graph_window = GraphWindow(fig, title, self)
            self.graph_window.show()
            
            self.statusBar().showMessage(f"✅ Graph opened: {title}")
            print(f"✅ Graph window opened: {title}")
            
        except Exception as e:
            print(f"Error opening graph: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.warning(self, "Error", f"Error opening graph:\n{str(e)}")
    
    def _create_calculator_tab(self) -> QWidget:
        """Create calculator tab - OPENS CALCULATIONS IN SEPARATE WINDOW"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        calc_widget = QWidget()
        calc_widget.setStyleSheet("background-color: #0f0f23; border-radius: 8px; padding: 20px;")
        calc_layout = QVBoxLayout(calc_widget)
        
        title_label = QLabel("🧮 Detailed Calculator")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title_label.setStyleSheet("color: #64ffda;")
        title_label.setAlignment(Qt.AlignCenter)
        calc_layout.addWidget(title_label)
        
        info_text = QLabel(
            "This calculator shows all step-by-step calculations including:\n\n"
            "• Module Specifications (Jinko 650W Tiger Neo)\n"
            "• Module Calculations (Area, Efficiency, Fill Factor)\n"
            "• Weekly Calculations (Power, Soiling Loss, Ratio)\n"
            "• Regression Analysis (Slope, Intercept, R²)\n"
            "• Summary of Results\n\n"
            "Click the button below to view all detailed calculations."
        )
        info_text.setAlignment(Qt.AlignCenter)
        info_text.setStyleSheet("color: #8892b0; font-size: 12px; padding: 10px;")
        calc_layout.addWidget(info_text)
        
        open_calc_btn = QPushButton("🧮 Open Detailed Calculations")
        open_calc_btn.clicked.connect(self._open_calculations_window)
        open_calc_btn.setStyleSheet("""
            QPushButton {
                background-color: #64ffda;
                color: #1a1a2e;
                border: none;
                padding: 15px 30px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #4cd8b5;
            }
        """)
        calc_layout.addWidget(open_calc_btn)
        
        preview_label = QLabel("Click the button above to open detailed calculations in a new window")
        preview_label.setAlignment(Qt.AlignCenter)
        preview_label.setStyleSheet("color: #8892b0; padding: 10px;")
        calc_layout.addWidget(preview_label)
        
        layout.addWidget(calc_widget)
        
        return tab
    
    def _open_calculations_window(self):
        """Open the detailed calculations in a separate window"""
        try:
            print("Opening calculations in new window...")
            
            # Get all calculations
            if self.all_calculations is None:
                self.run_full_calculation()
            
            # Create and show calculator window
            self.calc_window = CalculatorWindow(self.all_calculations, self)
            self.calc_window.show()
            
            self.statusBar().showMessage("✅ Calculations opened")
            print("✅ Calculations window opened")
            
        except Exception as e:
            print(f"Error opening calculations: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.warning(self, "Error", f"Error opening calculations:\n{str(e)}")
    
    def _create_data_tab(self) -> QWidget:
        """Create data tab with real experimental data"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        table_group = QGroupBox("Weekly Measurements - Real Experimental Data")
        table_group.setStyleSheet("QGroupBox { color: #64ffda; }")
        table_layout = QVBoxLayout(table_group)
        
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(10)
        self.data_table.setHorizontalHeaderLabels([
            "Week", "Temp C", "Clean V", "Clean I", "Clean P",
            "Dusty V", "Dusty I", "Dusty P", 
            "Soiling Loss", "Soiling Ratio"
        ])
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.data_table.setFont(QFont("Segoe UI", 10))
        table_layout.addWidget(self.data_table)
        
        layout.addWidget(table_group)
        
        btn_layout = QHBoxLayout()
        
        load_btn = QPushButton("Load Real Data")
        load_btn.clicked.connect(self.load_data)
        load_btn.setStyleSheet("background-color: #64ffda; color: #1a1a2e;")
        btn_layout.addWidget(load_btn)
        
        analyze_btn = QPushButton("Run Full Analysis")
        analyze_btn.clicked.connect(self.run_full_calculation)
        analyze_btn.setStyleSheet("background-color: #64ffda; color: #1a1a2e;")
        btn_layout.addWidget(analyze_btn)
        
        layout.addLayout(btn_layout)
        
        return tab
    
    def _create_results_tab(self) -> QWidget:
        """Create results tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(6)
        self.results_table.setHorizontalHeaderLabels([
            "Week", "Soiling Ratio", "Soiling Loss", 
            "Voltage Drop", "Current Drop", "Power Loss"
        ])
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.results_table.setFont(QFont("Segoe UI", 10))
        layout.addWidget(self.results_table)
        
        return tab
    
    def _create_report_tab(self) -> QWidget:
        """Create report tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        info = QLabel("Generate Professional Reports")
        info.setFont(QFont("Segoe UI", 14, QFont.Bold))
        info.setStyleSheet("color: #64ffda;")
        layout.addWidget(info)
        
        btn_layout = QHBoxLayout()
        
        pdf_btn = QPushButton("Generate PDF Report")
        pdf_btn.clicked.connect(self._generate_pdf_report)
        pdf_btn.setStyleSheet("background-color: #64ffda; color: #1a1a2e; padding: 12px;")
        btn_layout.addWidget(pdf_btn)
        
        excel_btn = QPushButton("Generate Excel Report")
        excel_btn.clicked.connect(self._generate_excel_report)
        excel_btn.setStyleSheet("background-color: #64ffda; color: #1a1a2e; padding: 12px;")
        btn_layout.addWidget(excel_btn)
        
        layout.addLayout(btn_layout)
        
        self.report_preview = QTextEdit()
        self.report_preview.setReadOnly(True)
        self.report_preview.setPlaceholderText("Report preview will appear here...")
        self.report_preview.setFont(QFont("Consolas", 10))
        layout.addWidget(self.report_preview)
        
        return tab
    
    # ===================== DATA LOADING =====================
    
    def load_data(self):
        """Load real experimental data into the table"""
        print("Loading data into table...")
        data = self.analyzer.get_experimental_data()
        
        self.data_table.setRowCount(len(data['weeks']))
        
        for i in range(len(data['weeks'])):
            self.data_table.setItem(i, 0, QTableWidgetItem(str(data['weeks'][i])))
            self.data_table.setItem(i, 1, QTableWidgetItem(str(data['temperatures'][i])))
            self.data_table.setItem(i, 2, QTableWidgetItem(f"{data['clean_voltage'][i]:.2f}"))
            self.data_table.setItem(i, 3, QTableWidgetItem(f"{data['clean_current'][i]:.2f}"))
            self.data_table.setItem(i, 4, QTableWidgetItem(f"{data['clean_power'][i]:.2f}"))
            self.data_table.setItem(i, 5, QTableWidgetItem(f"{data['dusty_voltage'][i]:.2f}"))
            self.data_table.setItem(i, 6, QTableWidgetItem(f"{data['dusty_current'][i]:.2f}"))
            self.data_table.setItem(i, 7, QTableWidgetItem(f"{data['dusty_power'][i]:.2f}"))
            self.data_table.setItem(i, 8, QTableWidgetItem(f"{data['soiling_loss'][i]:.2f}"))
            self.data_table.setItem(i, 9, QTableWidgetItem(f"{data['soiling_ratio'][i]:.4f}"))
        
        self.statusBar().showMessage("Real experimental data loaded (5 weeks)")
        print("Data loaded successfully!")
    
    def run_full_calculation(self):
        """Run all calculations and update everything"""
        print("Running full calculations...")
        
        # Get all calculations
        self.all_calculations = self.analyzer.get_all_calculations()
        
        # Update dashboard
        self._update_dashboard()
        
        # Update results table
        self._populate_results()
        
        self.statusBar().showMessage("All calculations complete!")
        print("All calculations complete!")
    
    # ===================== DASHBOARD =====================
    
    def _update_dashboard(self):
        """Update the dashboard with analysis results"""
        try:
            print("Updating dashboard...")
            data = self.analyzer.get_experimental_data()
            regression = self.analyzer.linear_regression(data['weeks'], data['soiling_loss'])
            data['regression'] = regression
            
            self.dashboard_canvas.axes.clear()
            fig = self.visualizer.create_dashboard(data)
            self.dashboard_canvas.fig = fig
            self.dashboard_canvas.draw()
            print("Dashboard updated!")
            
        except Exception as e:
            print(f"Error updating dashboard: {e}")
            import traceback
            traceback.print_exc()
    
    # ===================== RESULTS =====================
    
    def _populate_results(self):
        """Populate results table with real data"""
        print("Populating results table...")
        data = self.analyzer.get_experimental_data()
        
        self.results_table.setRowCount(len(data['weeks']))
        
        for i in range(len(data['weeks'])):
            self.results_table.setItem(i, 0, QTableWidgetItem(str(data['weeks'][i])))
            self.results_table.setItem(i, 1, QTableWidgetItem(f"{data['soiling_ratio'][i]:.4f}"))
            self.results_table.setItem(i, 2, QTableWidgetItem(f"{data['soiling_loss'][i]:.2f}"))
            self.results_table.setItem(i, 3, QTableWidgetItem(f"{data['voltage_drop'][i]:.2f}"))
            self.results_table.setItem(i, 4, QTableWidgetItem(f"{data['current_drop'][i]:.2f}"))
            self.results_table.setItem(i, 5, QTableWidgetItem(f"{data['power_loss'][i]:.2f}"))
        
        print("Results table populated!")
    
    # ===================== REPORTS =====================
    
    def _generate_pdf_report(self):
        try:
            path = self.report_gen.generate_experiment_report()
            self.report_preview.setText(f"""
            PDF Report Generated Successfully!
            
            Location: {path}
            Format: PDF
            Includes: All measurements, regression analysis, and recommendations
            
            The report has been saved in the 'reports' folder.
            """)
            QMessageBox.information(self, "Report Generated", f"PDF Report saved at:\n{path}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error generating report: {str(e)}")
    
    def _generate_excel_report(self):
        try:
            path = self.report_gen.generate_excel_report()
            self.report_preview.setText(f"""
            Excel Report Generated Successfully!
            
            Location: {path}
            Format: Excel (.xlsx)
            Includes: All measurement data in spreadsheet format
            
            The report has been saved in the 'reports' folder.
            """)
            QMessageBox.information(self, "Report Generated", f"Excel Report saved at:\n{path}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error generating report: {str(e)}")


def run_app():
    """Run the application"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_app()