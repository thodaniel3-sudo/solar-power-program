"""
reports.py - PDF and Excel report generation for PV Soiling Analysis
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.linecharts import HorizontalLineChart

from database import Database
from core import PVSoilingAnalyzer


class ReportGenerator:
    """Generate PDF and Excel reports for PV soiling analysis"""
    
    def __init__(self, db: Database = None):
        self.db = db or Database()
        self.analyzer = PVSoilingAnalyzer()
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#2C3E50'),
            alignment=TA_CENTER,
            spaceAfter=30
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#34495E'),
            spaceAfter=12
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=6
        ))
    
    def generate_experiment_report(self, experiment_id: int = None) -> str:
        """Generate a PDF report for the experiment"""
        
        # Use the first experiment if none specified
        if experiment_id is None:
            experiments = self.db.get_all_experiments()
            if experiments:
                experiment_id = experiments[0]['id']
            else:
                raise ValueError("No experiments found")
        
        # Get data
        experiment = self.db.get_experiment(experiment_id) if hasattr(self.db, 'get_experiment') else None
        measurements = self.db.get_measurements(experiment_id)
        regression = self.db.get_regression_results(experiment_id)
        
        # Create output path
        output_dir = Path(__file__).parent / 'reports'
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / f"Soiling_Report_{datetime.now().strftime('%Y%m%d')}.pdf"
        
        # Create PDF
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        story = []
        
        # Title
        story.append(Paragraph(
            "PV Soiling Analysis Report",
            self.styles['CustomTitle']
        ))
        story.append(Spacer(1, 12))
        
        # Experiment Info
        story.append(Paragraph("Experiment Details", self.styles['CustomHeading']))
        if experiment:
            info_data = [
                ['Field', 'Value'],
                ['Experiment', experiment.get('name', 'N/A')],
                ['Location', experiment.get('location', 'N/A')],
                ['Tilt Angle', f"{experiment.get('tilt_angle', 'N/A')}°"],
                ['Date', experiment.get('created_at', 'N/A')[:10]]
            ]
        else:
            info_data = [['Field', 'Value'], ['Experiment', 'Minna Soiling Test 2026']]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#34495E')),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7')),
            ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#ECF0F1')),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 12))
        
        # Weekly Data Table
        story.append(Paragraph("Weekly Measurements", self.styles['CustomHeading']))
        
        table_data = [['Week', 'Temp (°C)', 'Clean P (W)', 'Dusty P (W)', 
                       'Soiling Ratio', 'Soiling Loss (%)']]
        
        for m in measurements:
            table_data.append([
                str(m['week_number']),
                str(m['temperature']),
                f"{m['clean_power']:.2f}",
                f"{m['dusty_power']:.2f}",
                f"{m['soiling_ratio']:.4f}",
                f"{m['soiling_loss']:.2f}"
            ])
        
        data_table = Table(table_data, colWidths=[0.8*inch, 0.8*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
        data_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495E')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7')),
        ]))
        story.append(data_table)
        story.append(Spacer(1, 12))
        
        # Regression Results
        if regression:
            story.append(Paragraph("Regression Analysis", self.styles['CustomHeading']))
            reg_data = [
                ['Parameter', 'Value'],
                ['Slope', f"{regression['slope']:.3f} % per week"],
                ['Intercept', f"{regression['intercept']:.3f}"],
                ['R² Value', f"{regression['r_squared']:.3f}"],
                ['Equation', regression['equation']]
            ]
            
            reg_table = Table(reg_data, colWidths=[2*inch, 4*inch])
            reg_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#34495E')),
                ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7')),
                ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#ECF0F1')),
            ]))
            story.append(reg_table)
            story.append(Spacer(1, 12))
        
        # Summary and Recommendation
        story.append(Paragraph("Summary and Recommendations", self.styles['CustomHeading']))
        
        if measurements:
            first_loss = measurements[0]['soiling_loss']
            last_loss = measurements[-1]['soiling_loss']
            total_increase = last_loss - first_loss
            
            summary_text = f"""
            <b>Key Findings:</b><br/>
            • Week 1 Soiling Loss: {first_loss:.2f}%<br/>
            • Week {len(measurements)} Soiling Loss: {last_loss:.2f}%<br/>
            • Total Increase: {total_increase:.2f}%<br/>
            • Average Soiling Rate: {total_increase/(len(measurements)-1):.2f}% per week<br/>
            <br/>
            <b>Recommendation:</b><br/>
            Based on the observed soiling trend, cleaning every 2-3 weeks is recommended.<br/>
            During Harmattan conditions, more frequent cleaning may be necessary.
            """
            
            story.append(Paragraph(summary_text, self.styles['CustomBody']))
        
        story.append(Spacer(1, 24))
        story.append(Paragraph(
            f"Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            self.styles['Normal']
        ))
        
        # Build PDF
        doc.build(story)
        return str(output_path)
    
    def generate_excel_report(self, experiment_id: int = None) -> str:
        """Generate an Excel report"""
        
        if experiment_id is None:
            experiments = self.db.get_all_experiments()
            if experiments:
                experiment_id = experiments[0]['id']
            else:
                raise ValueError("No experiments found")
        
        measurements = self.db.get_measurements(experiment_id)
        regression = self.db.get_regression_results(experiment_id)
        
        # Create output path
        output_dir = Path(__file__).parent / 'reports'
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / f"Soiling_Data_{datetime.now().strftime('%Y%m%d')}.xlsx"
        
        # Create DataFrames
        df_measurements = pd.DataFrame(measurements)
        df_regression = pd.DataFrame([regression]) if regression else pd.DataFrame()
        
        # Write to Excel
        with pd.ExcelWriter(str(output_path), engine='openpyxl') as writer:
            df_measurements.to_excel(writer, sheet_name='Measurements', index=False)
            if not df_regression.empty:
                df_regression.to_excel(writer, sheet_name='Regression', index=False)
        
        return str(output_path)