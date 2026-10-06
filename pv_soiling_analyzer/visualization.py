"""
visualization.py - Advanced Charts and Graphs for PV Soiling Analysis
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Optional

# Set professional style
plt.style.use('seaborn-v0_8-darkgrid')

class PVSoilingVisualizer:
    """Visualization tools for PV soiling analysis"""
    
    def __init__(self):
        self.figsize = (10, 6)
        self.dpi = 100
        self.colors = {
            'clean': '#2ECC71',
            'dusty': '#E74C3C',
            'soiling': '#F39C12',
            'voltage': '#3498DB',
            'current': '#9B59B6',
            'ratio': '#1ABC9C',
            'regression': '#2980B9',
            'power_loss': '#E67E22'
        }
    
    def plot_power_comparison(self, weeks: List, clean_power: List, dusty_power: List) -> plt.Figure:
        """Plot clean vs dusty panel power comparison"""
        fig, ax = plt.subplots(figsize=self.figsize, facecolor='#1a1a2e')
        ax.set_facecolor('#0f0f23')
        
        ax.plot(weeks, clean_power, 'o-', label='Clean Panel', 
                color=self.colors['clean'], linewidth=2, markersize=10)
        ax.plot(weeks, dusty_power, 's-', label='Dusty Panel', 
                color=self.colors['dusty'], linewidth=2, markersize=10)
        
        # Add value labels
        for i, (w, p) in enumerate(zip(weeks, clean_power)):
            ax.annotate(f'{p:.1f}W', (w, p), textcoords="offset points", 
                       xytext=(0, 10), ha='center', fontsize=9, color='white')
        
        for i, (w, p) in enumerate(zip(weeks, dusty_power)):
            ax.annotate(f'{p:.1f}W', (w, p), textcoords="offset points", 
                       xytext=(0, -15), ha='center', fontsize=9, color='white')
        
        ax.set_xlabel('Week', fontsize=12, color='white')
        ax.set_ylabel('Power Output (W)', fontsize=12, color='white')
        ax.set_title('Clean vs Dusty Panel Power Output', fontsize=14, fontweight='bold', color='#64ffda')
        ax.legend(fontsize=10, facecolor='#1a1a2e', edgecolor='#2d2d44', labelcolor='white')
        ax.grid(True, alpha=0.2, color='#2d2d44')
        ax.set_xticks(weeks)
        ax.tick_params(colors='white')
        
        plt.tight_layout()
        return fig
    
    def plot_soiling_loss(self, weeks: List, soiling_loss: List, 
                         regression: Optional[Dict] = None) -> plt.Figure:
        """Plot soiling loss over time with regression line"""
        fig, ax = plt.subplots(figsize=self.figsize, facecolor='#1a1a2e')
        ax.set_facecolor('#0f0f23')
        
        ax.plot(weeks, soiling_loss, 'o-', label='Soiling Loss', 
                color=self.colors['soiling'], linewidth=2, markersize=10)
        
        # Add value labels
        for i, (w, loss) in enumerate(zip(weeks, soiling_loss)):
            ax.annotate(f'{loss:.2f}%', (w, loss), textcoords="offset points", 
                       xytext=(0, 10), ha='center', fontsize=9, color='white')
        
        # Add regression line if provided
        if regression:
            x_pred = np.linspace(min(weeks), max(weeks), 100)
            y_pred = regression['slope'] * x_pred + regression['intercept']
            ax.plot(x_pred, y_pred, '--', color=self.colors['regression'], linewidth=2,
                    label=f'Linear Regression: R² = {regression["r_squared"]:.3f}')
            
            # Add equation text
            ax.text(0.05, 0.95, f'SL = {regression["slope"]:.3f} x Week + {regression["intercept"]:.3f}',
                   transform=ax.transAxes, fontsize=10, verticalalignment='top',
                   color='white',
                   bbox=dict(boxstyle="round", facecolor='#1a1a2e', edgecolor='#64ffda', alpha=0.8))
        
        ax.set_xlabel('Week', fontsize=12, color='white')
        ax.set_ylabel('Soiling Loss (%)', fontsize=12, color='white')
        ax.set_title('Soiling Loss Over Time with Regression', fontsize=14, fontweight='bold', color='#64ffda')
        ax.legend(fontsize=10, facecolor='#1a1a2e', edgecolor='#2d2d44', labelcolor='white')
        ax.grid(True, alpha=0.2, color='#2d2d44')
        ax.set_xticks(weeks)
        ax.tick_params(colors='white')
        
        plt.tight_layout()
        return fig
    
    def plot_voltage_current_drop(self, weeks: List, voltage_drop: List, 
                                  current_drop: List) -> plt.Figure:
        """Plot voltage and current drop comparison"""
        fig, ax = plt.subplots(figsize=self.figsize, facecolor='#1a1a2e')
        ax.set_facecolor('#0f0f23')
        
        ax.plot(weeks, voltage_drop, 'o-', label='Voltage Drop', 
                color=self.colors['voltage'], linewidth=2, markersize=10)
        ax.plot(weeks, current_drop, 's-', label='Current Drop', 
                color=self.colors['current'], linewidth=2, markersize=10)
        
        # Add value labels
        for i, (w, vd) in enumerate(zip(weeks, voltage_drop)):
            ax.annotate(f'{vd:.2f}%', (w, vd), textcoords="offset points", 
                       xytext=(0, 8), ha='center', fontsize=8, color='white')
        
        for i, (w, cd) in enumerate(zip(weeks, current_drop)):
            ax.annotate(f'{cd:.2f}%', (w, cd), textcoords="offset points", 
                       xytext=(0, -12), ha='center', fontsize=8, color='white')
        
        ax.set_xlabel('Week', fontsize=12, color='white')
        ax.set_ylabel('Drop (%)', fontsize=12, color='white')
        ax.set_title('Voltage and Current Drop Over Time', fontsize=14, fontweight='bold', color='#64ffda')
        ax.legend(fontsize=10, facecolor='#1a1a2e', edgecolor='#2d2d44', labelcolor='white')
        ax.grid(True, alpha=0.2, color='#2d2d44')
        ax.set_xticks(weeks)
        ax.tick_params(colors='white')
        
        plt.tight_layout()
        return fig
    
    def plot_soiling_ratio(self, weeks: List, soiling_ratio: List) -> plt.Figure:
        """Plot soiling ratio trend"""
        fig, ax = plt.subplots(figsize=self.figsize, facecolor='#1a1a2e')
        ax.set_facecolor('#0f0f23')
        
        ax.plot(weeks, soiling_ratio, 'o-', label='Soiling Ratio', 
                color=self.colors['ratio'], linewidth=2, markersize=10)
        ax.axhline(y=1.0, color='red', linestyle='--', linewidth=2, 
                   alpha=0.7, label='Clean (SR = 1.0)')
        
        # Add value labels
        for i, (w, sr) in enumerate(zip(weeks, soiling_ratio)):
            ax.annotate(f'{sr:.4f}', (w, sr), textcoords="offset points", 
                       xytext=(0, 8), ha='center', fontsize=8, color='white')
        
        ax.set_xlabel('Week', fontsize=12, color='white')
        ax.set_ylabel('Soiling Ratio', fontsize=12, color='white')
        ax.set_title('Soiling Ratio Over Time', fontsize=14, fontweight='bold', color='#64ffda')
        ax.legend(fontsize=10, facecolor='#1a1a2e', edgecolor='#2d2d44', labelcolor='white')
        ax.grid(True, alpha=0.2, color='#2d2d44')
        ax.set_xticks(weeks)
        ax.set_ylim(0.9, 1.05)
        ax.tick_params(colors='white')
        
        plt.tight_layout()
        return fig
    
    def plot_power_loss(self, weeks: List, power_loss: List) -> plt.Figure:
        """Plot power loss over time as bar chart"""
        fig, ax = plt.subplots(figsize=self.figsize, facecolor='#1a1a2e')
        ax.set_facecolor('#0f0f23')
        
        bars = ax.bar(weeks, power_loss, color='#E67E22', alpha=0.8, 
                     edgecolor='#64ffda', linewidth=1.5)
        
        # Add value labels on bars
        for bar, value in zip(bars, power_loss):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{value:.1f}W', ha='center', va='bottom', fontsize=10, 
                    fontweight='bold', color='white')
        
        ax.set_xlabel('Week', fontsize=12, color='white')
        ax.set_ylabel('Power Loss (W)', fontsize=12, color='white')
        ax.set_title('Weekly Power Loss Due to Soiling', fontsize=14, fontweight='bold', color='#64ffda')
        ax.grid(True, alpha=0.2, color='#2d2d44', axis='y')
        ax.set_xticks(weeks)
        ax.tick_params(colors='white')
        
        plt.tight_layout()
        return fig
    
    def create_dashboard(self, data: Dict) -> plt.Figure:
        """Create comprehensive dashboard with all plots"""
        fig, axes = plt.subplots(2, 3, figsize=(15, 10), facecolor='#1a1a2e')
        
        # Set background for all axes
        for ax in axes.flatten():
            ax.set_facecolor('#0f0f23')
        
        # 1. Power Comparison
        axes[0, 0].plot(data['weeks'], data['clean_power'], 'o-', 
                        label='Clean', color='#2ECC71', linewidth=2, markersize=8)
        axes[0, 0].plot(data['weeks'], data['dusty_power'], 's-', 
                        label='Dusty', color='#E74C3C', linewidth=2, markersize=8)
        axes[0, 0].set_xlabel('Week', color='white')
        axes[0, 0].set_ylabel('Power (W)', color='white')
        axes[0, 0].set_title('Power Comparison', color='#64ffda', fontweight='bold')
        axes[0, 0].legend(facecolor='#1a1a2e', edgecolor='#2d2d44', labelcolor='white')
        axes[0, 0].grid(True, alpha=0.2, color='#2d2d44')
        axes[0, 0].set_xticks(data['weeks'])
        axes[0, 0].tick_params(colors='white')
        
        # 2. Soiling Loss
        axes[0, 1].plot(data['weeks'], data['soiling_loss'], 'o-', 
                        color='#F39C12', linewidth=2, markersize=8)
        if 'regression' in data:
            x_pred = np.linspace(min(data['weeks']), max(data['weeks']), 100)
            y_pred = data['regression']['slope'] * x_pred + data['regression']['intercept']
            axes[0, 1].plot(x_pred, y_pred, '--', color='#2980B9',
                          label=f"R² = {data['regression']['r_squared']:.3f}")
        axes[0, 1].set_xlabel('Week', color='white')
        axes[0, 1].set_ylabel('Soiling Loss (%)', color='white')
        axes[0, 1].set_title('Soiling Loss', color='#64ffda', fontweight='bold')
        axes[0, 1].legend(facecolor='#1a1a2e', edgecolor='#2d2d44', labelcolor='white')
        axes[0, 1].grid(True, alpha=0.2, color='#2d2d44')
        axes[0, 1].set_xticks(data['weeks'])
        axes[0, 1].tick_params(colors='white')
        
        # 3. Voltage & Current Drop
        axes[0, 2].plot(data['weeks'], data['voltage_drop'], 'o-', 
                        label='Voltage', color='#3498DB')
        axes[0, 2].plot(data['weeks'], data['current_drop'], 's-', 
                        label='Current', color='#9B59B6')
        axes[0, 2].set_xlabel('Week', color='white')
        axes[0, 2].set_ylabel('Drop (%)', color='white')
        axes[0, 2].set_title('Voltage & Current Drop', color='#64ffda', fontweight='bold')
        axes[0, 2].legend(facecolor='#1a1a2e', edgecolor='#2d2d44', labelcolor='white')
        axes[0, 2].grid(True, alpha=0.2, color='#2d2d44')
        axes[0, 2].set_xticks(data['weeks'])
        axes[0, 2].tick_params(colors='white')
        
        # 4. Soiling Ratio
        axes[1, 0].plot(data['weeks'], data['soiling_ratio'], 'o-', 
                        color='#1ABC9C', linewidth=2)
        axes[1, 0].axhline(y=1.0, color='red', linestyle='--', alpha=0.5)
        axes[1, 0].set_xlabel('Week', color='white')
        axes[1, 0].set_ylabel('Soiling Ratio', color='white')
        axes[1, 0].set_title('Soiling Ratio', color='#64ffda', fontweight='bold')
        axes[1, 0].grid(True, alpha=0.2, color='#2d2d44')
        axes[1, 0].set_xticks(data['weeks'])
        axes[1, 0].tick_params(colors='white')
        
        # 5. Power Loss (Bar Chart)
        bars = axes[1, 1].bar(data['weeks'], data['power_loss'], 
                             color='#E67E22', alpha=0.7, edgecolor='#64ffda')
        for bar, value in zip(bars, data['power_loss']):
            height = bar.get_height()
            axes[1, 1].text(bar.get_x() + bar.get_width()/2., height + 1,
                          f'{value:.1f}W', ha='center', va='bottom', fontsize=8, color='white')
        axes[1, 1].set_xlabel('Week', color='white')
        axes[1, 1].set_ylabel('Power Loss (W)', color='white')
        axes[1, 1].set_title('Power Loss', color='#64ffda', fontweight='bold')
        axes[1, 1].grid(True, alpha=0.2, color='#2d2d44', axis='y')
        axes[1, 1].set_xticks(data['weeks'])
        axes[1, 1].tick_params(colors='white')
        
        # 6. Summary Stats
        axes[1, 2].axis('off')
        
        # Calculate stats
        total_loss = data['soiling_loss'][-1] - data['soiling_loss'][0]
        avg_loss = sum(data['soiling_loss']) / len(data['soiling_loss'])
        
        stats_text = f"""
        SOILING ANALYSIS SUMMARY
        
        -----------------------------
        Week 1 Loss:    {data['soiling_loss'][0]:.2f}%
        Week 5 Loss:    {data['soiling_loss'][-1]:.2f}%
        Total Increase: {total_loss:.2f}%
        Average Loss:   {avg_loss:.2f}%
        
        -----------------------------
        REGRESSION:
        Slope:  {data['regression']['slope']:.3f}% / week
        R²:     {data['regression']['r_squared']:.4f}
        Eq:     SL = {data['regression']['slope']:.3f}xWeek + {data['regression']['intercept']:.3f}
        
        -----------------------------
        RECOMMENDATION:
        Clean every 2-3 weeks
        More frequent during Harmattan
        """
        axes[1, 2].text(0.1, 0.5, stats_text, transform=axes[1, 2].transAxes,
                       fontsize=11, verticalalignment='center', color='#ccd6f6',
                       bbox=dict(boxstyle="round,pad=0.5", facecolor='#0f0f23', 
                                edgecolor='#64ffda', linewidth=2))
        
        plt.suptitle('PV Soiling Analysis Dashboard', fontsize=16, fontweight='bold', color='#64ffda')
        plt.tight_layout()
        return fig
    
    def save_figure(self, fig: plt.Figure, filename: str, dpi: int = 150):
        """Save figure to file"""
        fig.savefig(filename, dpi=dpi, bbox_inches='tight')
        plt.close(fig)