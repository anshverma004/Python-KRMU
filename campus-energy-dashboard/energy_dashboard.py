# Campus Energy Dashboard - Lab Assignment 5 Capstone
# Ansh Verma - KR Mangalam University

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path
from datetime import datetime, timedelta

print("🔌 Campus Energy Dashboard Starting...")

# Task 1: Generate Sample Data (Multiple Buildings)
def create_sample_data():
    """Task 1: Create multiple CSV files for buildings"""
    Path('data').mkdir(exist_ok=True)
    buildings = ['Library', 'Hostel_A', 'Lecture_Hall', 'Lab_Block']
    
    for building in buildings:
        dates = pd.date_range('2024-01-01', periods=100, freq='H')
        data = {
            'timestamp': dates,
            'kwh': np.random.exponential(40, 100) + np.random.normal(0, 10, 100)
        }
        df = pd.DataFrame(data)
        df.to_csv(f'data/{building}.csv', index=False)
    print("✅ Created 4 building CSV files in data/")

# Task 3: OOP Classes
class MeterReading:
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh
    
    def __str__(self):
        return f"{self.timestamp}: {self.kwh:.1f} kWh"

class Building:
    def __init__(self, name):
        self.name = name
        self.readings = []
    
    def add_reading(self, timestamp, kwh):
        reading = MeterReading(timestamp, kwh)
        self.readings.append(reading)
    
    def total_consumption(self):
        return sum(r.kwh for r in self.readings)
    
    def avg_daily(self):
        df = pd.DataFrame([{'time': r.timestamp, 'kwh': r.kwh} for r in self.readings])
        return df.groupby(df['time'].dt.date)['kwh'].sum().mean()

class BuildingManager:
    def __init__(self):
        self.buildings = []
    
    def add_building(self, building):
        self.buildings.append(building)
    
    def get_summary(self):
        return {b.name: {'total': b.total_consumption(), 'avg_daily': b.avg_daily()} 
                for b in self.buildings}

# Task 1: Data Ingestion (Multiple CSVs)
def load_all_data():
    """Task 1: Load multiple CSV files with error handling"""
    all_data = []
    
    if not os.path.exists('data'):
        create_sample_data()
    
    for file in os.listdir('data'):
        if file.endswith('.csv'):
            try:
                building_name = file.replace('.csv', '')
                df = pd.read_csv(f'data/{file}')
                df['building'] = building_name
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                all_data.append(df)
                print(f"✅ Loaded: {file}")
            except Exception as e:
                print(f"❌ Error loading {file}: {e}")
    
    df_combined = pd.concat(all_data, ignore_index=True).dropna()
    Path('output').mkdir(exist_ok=True)
    df_combined.to_csv('output/cleaned_energy_data.csv', index=False)
    print(f"✅ Combined {len(df_combined)} readings from {len(all_data)} buildings")
    return df_combined

# Task 2: Aggregation Functions
def daily_totals(df):
    """Task 2: Daily aggregation"""
    daily = df.groupby(['building', df['timestamp'].dt.date])['kwh'].sum().reset_index()
    daily.to_csv('output/daily_totals.csv', index=False)
    return daily

def building_summary(df):
    """Task 2: Building-wise summary"""
    summary = df.groupby('building')['kwh'].agg(['mean', 'min', 'max', 'sum']).round(2)
    summary.to_csv('output/building_summary.csv')
    return summary

# Task 4: Dashboard Visualization
def create_dashboard(df):
    """Task 4: 4-chart dashboard"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Campus Energy Consumption Dashboard', fontsize=18, fontweight='bold')
    
    # Chart 1: Daily trend
    daily = daily_totals(df)
    for building in df['building'].unique():
        b_data = daily[daily['building'] == building]
        axes[0,0].plot(b_data['timestamp'], b_data['kwh'], marker='o', label=building)
    axes[0,0].set_title('Daily Consumption Trends')
    axes[0,0].set_ylabel('kWh')
    axes[0,0].legend()
    axes[0,0].grid(True, alpha=0.3)
    
    # Chart 2: Building comparison (bar)
    summary = building_summary(df)
    buildings = summary.index
    totals = summary['sum']
    axes[0,1].bar(buildings, totals, color=['blue', 'green', 'orange', 'red'])
    axes[0,1].set_title('Total Consumption by Building')
    axes[0,1].set_ylabel('Total kWh')
    
    # Chart 3: Peak hours scatter
    peak_data = df[df['kwh'] > df['kwh'].quantile(0.9)]
    for building in peak_data['building'].unique():
        b_peak = peak_data[peak_data['building'] == building]
        axes[1,0].scatter(b_peak['timestamp'], b_peak['kwh'], label=building, s=50)
    axes[1,0].set_title('Peak Hour Consumption')
    axes[1,0].set_xlabel('Time')
    axes[1,0].set_ylabel('kWh')
    axes[1,0].legend()
    
    # Chart 4: Weekly trends
    weekly = df.resample('W', on='timestamp').agg({'kwh': 'sum'}).reset_index()
    axes[1,1].bar(range(len(weekly)), weekly['kwh'], alpha=0.7, color='purple')
    axes[1,1].set_title('Weekly Consumption')
    axes[1,1].set_xlabel('Week #')
    axes[1,1].set_ylabel('Total kWh')
    
    plt.tight_layout()
    plt.savefig('dashboard.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✅ Dashboard saved: dashboard.png")

# Task 5: Executive Summary
def generate_report(df):
    """Task 5: Summary report"""
    total_campus = df['kwh'].sum()
    top_building = df.groupby('building')['kwh'].sum().idxmax()
    peak_reading = df['kwh'].max()
    peak_time = df.loc[df['kwh'].idxmax(), 'timestamp']
    
    report = f"""
CAMPUS ENERGY SUMMARY REPORT
============================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

KEY METRICS:
- Total Campus Consumption: {total_campus:.0f} kWh
- Highest Consumer: {top_building}
- Peak Reading: {peak_reading:.1f} kWh at {peak_time}
- Average Daily: {df['kwh'].mean():.1f} kWh

RECOMMENDATIONS:
• Audit {top_building} for efficiency improvements
• Schedule maintenance during off-peak hours
• Monitor weekly trends for anomalies

Files Generated:
- cleaned_energy_data.csv ({len(df)} records)
- building_summary.csv (4 buildings)
- dashboard.png (4 charts)
"""
    
    with open('summary.txt', 'w') as f:
        f.write(report)
    print(report)
    print("✅ Summary saved: summary.txt")

# MAIN EXECUTION
if __name__ == "__main__":
    print("🏫 Building OOP Manager...")
    manager = BuildingManager()
    
    # All Tasks Pipeline
    df = load_all_data()
    daily = daily_totals(df)
    summary = building_summary(df)
    
    # OOP Processing (Task 3)
    for building_name in df['building'].unique():
        building_df = df[df['building'] == building_name]
        building = Building(building_name)
        for _, row in building_df.iterrows():
            building.add_reading(row['timestamp'], row['kwh'])
        manager.add_building(building)
    
    # Generate outputs
    create_dashboard(df)
    generate_report(df)
    
    print("\n🎉 CAPSTONE COMPLETE! All 5 tasks done:")
    print("✅ Task 1: Data ingestion (4 CSVs)")
    print("✅ Task 2: Aggregations (daily/weekly/building)")
    print("✅ Task 3: OOP (Building/MeterReading classes)")
    print("✅ Task 4: 4-chart dashboard.png")
    print("✅ Task 5: CSVs + summary.txt")
