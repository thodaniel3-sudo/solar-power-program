"""
database.py - SQLite database for PV soiling data with real experimental results
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

class Database:
    """SQLite database handler for PV soiling analyzer"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            data_dir = Path(__file__).parent / 'data'
            data_dir.mkdir(exist_ok=True)
            db_path = data_dir / 'pv_soiling.db'
        
        self.db_path = str(db_path)
        self._init_database()
        self._load_sample_data()
    
    def _get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def _init_database(self):
        """Initialize database tables"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Experiments table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS experiments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    location TEXT,
                    start_date TEXT,
                    end_date TEXT,
                    tilt_angle REAL,
                    notes TEXT,
                    created_at TEXT NOT NULL
                )
            ''')
            
            # Weekly measurements table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS weekly_measurements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    experiment_id INTEGER,
                    week_number INTEGER,
                    temperature REAL,
                    clean_voltage REAL,
                    clean_current REAL,
                    clean_power REAL,
                    dusty_voltage REAL,
                    dusty_current REAL,
                    dusty_power REAL,
                    soiling_ratio REAL,
                    soiling_loss REAL,
                    voltage_drop REAL,
                    current_drop REAL,
                    power_loss REAL,
                    FOREIGN KEY (experiment_id) REFERENCES experiments (id)
                )
            ''')
            
            # Regression results table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS regression_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    experiment_id INTEGER,
                    slope REAL,
                    intercept REAL,
                    r_squared REAL,
                    equation TEXT,
                    FOREIGN KEY (experiment_id) REFERENCES experiments (id)
                )
            ''')
            
            conn.commit()
    
    def _load_sample_data(self):
        """Load Mohammed's real experimental data into the database"""
        # Check if data already exists
        experiments = self.get_all_experiments()
        if experiments:
            return  # Data already loaded
        
        # Create experiment
        exp_id = self.create_experiment(
            name="Minna_Soiling_Test_2026",
            location="Barako, Talba Road, Minna",
            tilt_angle=16.0,
            notes="Five-week soiling test with Jinko 650W panels. Clean control panel cleaned weekly, test panel left undisturbed."
        )
        
        # Real experimental data from the project
        data = [
            # week, temp, clean_v, clean_i, dusty_v, dusty_i
            (1, 29, 43.00, 13.45, 42.60, 13.45),
            (2, 29, 43.15, 13.41, 42.40, 13.24),
            (3, 29, 42.88, 13.48, 41.70, 13.20),
            (4, 29, 43.08, 13.42, 41.50, 13.00),
            (5, 29, 42.95, 13.46, 40.90, 12.96)
        ]
        
        for week, temp, cv, ci, dv, di in data:
            # Calculate values
            clean_power = cv * ci
            dusty_power = dv * di
            soiling_ratio = dusty_power / clean_power if clean_power > 0 else 0
            soiling_loss = ((clean_power - dusty_power) / clean_power) * 100 if clean_power > 0 else 0
            voltage_drop = ((cv - dv) / cv) * 100 if cv > 0 else 0
            current_drop = ((ci - di) / ci) * 100 if ci > 0 else 0
            power_loss = clean_power - dusty_power
            
            self.add_measurement(
                exp_id, week, temp,
                cv, ci, clean_power,
                dv, di, dusty_power,
                soiling_ratio, soiling_loss,
                voltage_drop, current_drop,
                power_loss
            )
        
        # Calculate and save regression results
        from core import PVSoilingAnalyzer
        analyzer = PVSoilingAnalyzer()
        data = analyzer.get_experimental_data()
        regression = analyzer.linear_regression(data['weeks'], data['soiling_loss'])
        
        self.save_regression_results(exp_id, regression)
    
    def create_experiment(self, name: str, location: str = None, 
                         tilt_angle: float = None, notes: str = None) -> int:
        """Create a new experiment"""
        now = datetime.now().isoformat()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO experiments (name, location, tilt_angle, notes, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, location, tilt_angle, notes, now))
            conn.commit()
            return cursor.lastrowid
    
    def add_measurement(self, experiment_id: int, week_number: int,
                       temperature: float, clean_voltage: float, clean_current: float,
                       clean_power: float, dusty_voltage: float, dusty_current: float,
                       dusty_power: float, soiling_ratio: float, soiling_loss: float,
                       voltage_drop: float, current_drop: float, power_loss: float):
        """Add a weekly measurement"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO weekly_measurements (
                    experiment_id, week_number, temperature,
                    clean_voltage, clean_current, clean_power,
                    dusty_voltage, dusty_current, dusty_power,
                    soiling_ratio, soiling_loss, voltage_drop, current_drop, power_loss
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (experiment_id, week_number, temperature,
                  clean_voltage, clean_current, clean_power,
                  dusty_voltage, dusty_current, dusty_power,
                  soiling_ratio, soiling_loss, voltage_drop, current_drop, power_loss))
            conn.commit()
    
    def save_regression_results(self, experiment_id: int, regression: Dict):
        """Save regression results"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO regression_results (experiment_id, slope, intercept, r_squared, equation)
                VALUES (?, ?, ?, ?, ?)
            ''', (experiment_id, regression['slope'], regression['intercept'],
                  regression['r_squared'], regression['equation']))
            conn.commit()
    
    def get_all_experiments(self) -> List[Dict]:
        """Get all experiments"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM experiments ORDER BY created_at DESC')
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
    
    def get_measurements(self, experiment_id: int) -> List[Dict]:
        """Get all measurements for an experiment"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM weekly_measurements WHERE experiment_id = ? ORDER BY week_number', 
                          (experiment_id,))
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
    
    def get_regression_results(self, experiment_id: int) -> Optional[Dict]:
        """Get regression results for an experiment"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM regression_results WHERE experiment_id = ?', (experiment_id,))
            row = cursor.fetchone()
            if row:
                columns = [description[0] for description in cursor.description]
                return dict(zip(columns, row))
            return None
    
    def get_summary_statistics(self) -> Dict:
        """Get summary statistics from the database"""
        experiments = self.get_all_experiments()
        if not experiments:
            return {'total_experiments': 0, 'total_measurements': 0}
        
        total_measurements = 0
        for exp in experiments:
            measurements = self.get_measurements(exp['id'])
            total_measurements += len(measurements)
        
        return {
            'total_experiments': len(experiments),
            'total_measurements': total_measurements,
            'latest_experiment': experiments[0]['name'] if experiments else 'N/A'
        }