#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Graph Generator - Flera graf-varianter för Konto 1
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from datetime import datetime
import random


def create_price_trend_graph(df, region):
    """Graf 1: Prisutveckling med trendlinje"""
    
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 7), dpi=120)
    
    # Huvudlinje
    ax.plot(df['date'], df['price'], 
            marker='o', linewidth=3, markersize=10, 
            color='#2E86AB', label='Genomsnittspris')
    
    # Trendlinje
    z = np.polyfit(range(len(df)), df['price'], 2)
    p = np.poly1d(z)
    ax.plot(df['date'], p(range(len(df))), 
            "--", color='#A23B72', linewidth=2, 
            alpha=0.7, label='Trend')
    
    # Statistik
    latest_price = df['price'].iloc[-1]
    change_pct = ((df['price'].iloc[-1] - df['price'].iloc[0]) / df['price'].iloc[0]) * 100
    
    title = f'Småhuspriser - {region}\n'
    title += f'Senaste: {latest_price:,.0f} SEK  |  Årsförändring: {change_pct:+.1f}%'
    
    ax.set_title(title, fontsize=18, fontweight='bold', pad=20)
    ax.set_xlabel('Månad', fontsize=14, fontweight='bold')
    ax.set_ylabel('Pris (SEK)', fontsize=14, fontweight='bold')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x/1000000):.1f}M'))
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper left', fontsize=12, framealpha=0.9)
    
    fig.text(0.99, 0.01, 'Källa: SCB | @HousingStats', 
             ha='right', va='bottom', fontsize=10, style='italic', color='gray')
    
    plt.tight_layout()
    return fig


def create_monthly_change_graph(df, region):
    """Graf 2: Månadsförändringar (bar chart)"""
    
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 7), dpi=120)
    
    # Beräkna månadsförändringar
    changes = df['price'].pct_change() * 100
    changes = changes.fillna(0)
    
    # Färger baserat på upp/ner
    colors = ['#27AE60' if x >= 0 else '#E74C3C' for x in changes]
    
    ax.bar(df['date'], changes, color=colors, alpha=0.8, edgecolor='black', linewidth=0.5)
    
    # Noll-linje
    ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
    
    avg_change = changes.mean()
    latest_change = changes.iloc[-1]
    
    title = f'Månadsförändringar - {region}\n'
    title += f'Senaste: {latest_change:+.1f}%  |  Genomsnitt: {avg_change:+.1f}%'
    
    ax.set_title(title, fontsize=18, fontweight='bold', pad=20)
    ax.set_xlabel('Månad', fontsize=14, fontweight='bold')
    ax.set_ylabel('Förändring (%)', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    fig.text(0.99, 0.01, 'Källa: SCB | @HousingStats', 
             ha='right', va='bottom', fontsize=10, style='italic', color='gray')
    
    plt.tight_layout()
    return fig


def create_price_range_graph(df, region):
    """Graf 3: Prisfördelning senaste året"""
    
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=120)
    
    # Histogram
    ax1.hist(df['price'], bins=8, color='#3498DB', alpha=0.7, edgecolor='black')
    ax1.axvline(df['price'].mean(), color='red', linestyle='--', linewidth=2, label='Genomsnitt')
    ax1.set_xlabel('Pris (SEK)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Antal månader', fontsize=12, fontweight='bold')
    ax1.set_title('Prisfördelning', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x/1000000):.1f}M'))
    
    # Box plot
    ax2.boxplot(df['price'], vert=True, patch_artist=True,
                boxprops=dict(facecolor='#3498DB', alpha=0.7),
                medianprops=dict(color='red', linewidth=2))
    ax2.set_ylabel('Pris (SEK)', fontsize=12, fontweight='bold')
    ax2.set_title('Prisstatistik', fontsize=14, fontweight='bold')
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x/1000000):.1f}M'))
    ax2.set_xticklabels([region])
    
    fig.suptitle(f'Prisanalys - {region} (senaste 12 månader)', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    fig.text(0.99, 0.01, 'Källa: SCB | @HousingStats', 
             ha='right', va='bottom', fontsize=10, style='italic', color='gray')
    
    plt.tight_layout()
    return fig


def create_year_comparison_graph(df, region):
    """Graf 4: År-över-år jämförelse"""
    
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 7), dpi=120)
    
    # Simulera föregående år (i produktion: riktiga data)
    prev_year = df.copy()
    prev_year['price'] = prev_year['price'] * 0.95  # -5% föregående år
    prev_year['date'] = prev_year['date'] - pd.DateOffset(years=1)
    
    ax.plot(df['date'].dt.month, df['price'], 
            marker='o', linewidth=3, markersize=8, 
            color='#2E86AB', label='2024/2025')
    
    ax.plot(prev_year['date'].dt.month, prev_year['price'], 
            marker='s', linewidth=3, markersize=8, 
            color='#95A5A6', linestyle='--', label='2023/2024', alpha=0.7)
    
    yearly_change = ((df['price'].mean() - prev_year['price'].mean()) / prev_year['price'].mean()) * 100
    
    title = f'År-över-år Jämförelse - {region}\n'
    title += f'Genomsnittlig förändring: {yearly_change:+.1f}%'
    
    ax.set_title(title, fontsize=18, fontweight='bold', pad=20)
    ax.set_xlabel('Månad', fontsize=14, fontweight='bold')
    ax.set_ylabel('Pris (SEK)', fontsize=14, fontweight='bold')
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'Maj', 'Jun', 
                        'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dec'])
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x/1000000):.1f}M'))
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper left', fontsize=12, framealpha=0.9)
    
    fig.text(0.99, 0.01, 'Källa: SCB | @HousingStats', 
             ha='right', va='bottom', fontsize=10, style='italic', color='gray')
    
    plt.tight_layout()
    return fig


def generate_random_graph(df, output_dir):
    """Välj random graf-typ och generera"""
    
    region = df['region'].iloc[0]
    
    graph_types = [
        ('trend', create_price_trend_graph),
        ('monthly', create_monthly_change_graph),
        ('range', create_price_range_graph),
        ('comparison', create_year_comparison_graph)
    ]
    
    graph_type, graph_func = random.choice(graph_types)
    
    print(f"📊 Genererar graf-typ: {graph_type}")
    
    fig = graph_func(df, region)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/housing_{graph_type}_{timestamp}.png"
    fig.savefig(filename, bbox_inches='tight', dpi=150, facecolor='white')
    plt.close(fig)
    
    print(f"✅ Graf sparad: {filename}")
    return filename, graph_type