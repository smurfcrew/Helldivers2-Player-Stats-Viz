from flask import Flask, render_template, request, jsonify
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import io
import os
from typing import Dict, List, Tuple
from dataclasses import dataclass

app = Flask(__name__)

@dataclass
class EnemyKillStats:
    terminid_kills: int
    automaton_kills: int
    illuminate_kills: int
    friendly_kills: int

    @property
    def total_kills(self):
        return self.terminid_kills + self.automaton_kills + self.illuminate_kills

    def to_dict(self) -> Dict[str, int]:
        return {
            "Terminid Kills": self.terminid_kills,
            "Automaton Kills": self.automaton_kills,
            "Illuminate Kills": self.illuminate_kills,
            "Friendly Kills": self.friendly_kills
        }

class CombatStatsAnalysis:
    def __init__(self, stats_dict: dict):
        self.stats = stats_dict
        self.total_kills = (stats_dict['terminid_kills'] + 
                           stats_dict['automaton_kills'] + 
                           stats_dict['illuminate_kills'])
        
        self.efficiency_metrics = self.calculate_efficiency_metrics()
        self.combat_style = self.calculate_combat_stats()
        self.stratagem_efficiency = self.calculate_stratagem_efficiency()
        
        missions = stats_dict['missions_played']
        self.mission_success_rate = stats_dict['missions_won'] / missions * 100 if missions > 0 else 0
        self.extraction_rate = stats_dict['successful_extractions'] / missions * 100 if missions > 0 else 0
        self.objective_completion_rate = stats_dict['objectives_completed'] / missions if missions > 0 else 0
        self.samples_per_mission = stats_dict['samples_collected'] / missions if missions > 0 else 0
        self.xp_per_mission = stats_dict['total_xp'] / missions if missions > 0 else 0

    def calculate_efficiency_metrics(self) -> Dict[str, float]:
        missions = self.stats['missions_played']
        if missions == 0:
            return {key: 0 for key in ["Kills per mission", "Stratagems per Mission", "Objectives Per Mission", "Deaths per Mission", "Accuracy(%)", "Samples per Mission", "XP per Mission"]}
        
        accuracy = (self.stats['shots_hit'] / self.stats['shots_fired'] * 100) if self.stats['shots_fired'] > 0 else 0
        
        return {
            "Kills per mission": self.total_kills / missions,
            "Stratagems per Mission": self.stats['total_stratagems'] / missions,
            "Objectives Per Mission": self.stats['objectives_completed'] / missions,
            "Deaths per Mission": self.stats['deaths'] / missions,
            "Accuracy(%)": accuracy,
            "Samples per Mission": self.stats['samples_collected'] / missions,
            "XP per Mission": self.stats['total_xp'] / missions
        }

    def calculate_combat_stats(self) -> Dict[str, float]:
        return {
            "Regular Kills": self.total_kills - self.stats['grenade_kills'] - self.stats['melee_kills'] - self.stats['eagle_kills'],
            "Grenade Kills": self.stats['grenade_kills'],
            "Melee Kills": self.stats['melee_kills'],
            "Eagle Kills": self.stats['eagle_kills']
        }

    def calculate_stratagem_efficiency(self) -> Dict[str, float]:
        missions = self.stats['missions_played']
        if missions == 0:
            return {"Orbital Strikes": 0, "Defensive Tools": 0, "Eagle Support": 0}
        
        return {
            "Orbital Strikes": self.stats['orbitals_used'] / missions,
            "Defensive Tools": self.stats['defensive_stratagems'] / missions,
            "Eagle Support": self.stats['eagles_used'] / missions
        }

def add_value_labels(ax: plt.Axes, format_str: str = '{:.2f}') -> None:
    """Add labels to the end of each bar in a bar chart."""
    for rect in ax.patches:
        height = rect.get_height()
        if height > 0:  # only add label if there's a value
            ax.text(rect.get_x() + rect.get_width() / 2, height,
                    format_str.format(height),
                    ha='center', va='bottom')

def create_visualizations(stats_dict: dict) -> List[str]:
    """Create all visualizations and return them as base64 encoded strings"""
    plt.style.use('default')
    images = []
    
    analysis = CombatStatsAnalysis(stats_dict)
    
    # 1. kill distribution Chart
    fig1 = plt.figure(figsize=(12, 8))
    fig1.suptitle("Enemy Kill Distribution Analysis", fontsize=16)

    # bar plot
    ax1 = plt.subplot(2, 1, 1)
    enemy_stats = EnemyKillStats(
        terminid_kills=stats_dict['terminid_kills'],
        automaton_kills=stats_dict['automaton_kills'],
        illuminate_kills=stats_dict['illuminate_kills'],
        friendly_kills=stats_dict['friendly_kills']
    )
    
    kills_data = enemy_stats.to_dict()
    kills_df = pd.DataFrame(list(kills_data.items()), columns=['Enemy Type', 'Kills'])
    
    if kills_df['Kills'].sum() > 0:  # only create chart if there are kills
        sns.barplot(x='Enemy Type', y='Kills', data=kills_df, ax=ax1)
        ax1.set_title("Kills by Enemy Type")
        plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')
        add_value_labels(ax1, format_str='{:.0f}')

        # Pie chart
        ax2 = plt.subplot(2, 1, 2)
        kill_values = [v for v in kills_data.values() if v > 0]
        kill_labels = [k for k, v in kills_data.items() if v > 0]
        
        if kill_values:
            ax2.pie(kill_values, labels=kill_labels, autopct='%1.1f%%')
            ax2.set_title("Enemy Kills Distribution")
    
    plt.tight_layout()
    images.append(fig_to_base64(fig1))
    plt.close(fig1)
    
    #2. main Analysis Chart
    fig2, axs = plt.subplots(3, 1, figsize=(14, 12))
    fig2.suptitle("Combat Performance Analysis", fontsize=16)

    # efficiency metrics
    metrics_df = pd.DataFrame(list(analysis.efficiency_metrics.items()),
                              columns=['Metric', 'Value'])
    sns.barplot(data=metrics_df, x='Metric', y='Value', ax=axs[0])
    axs[0].set_title('Performance Metrics per Mission')
    axs[0].tick_params(axis='x', rotation=45)
    add_value_labels(axs[0])

    #combat style
    combat_df = pd.DataFrame(list(analysis.combat_style.items()),
                             columns=['Style', 'Kills'])
    sns.barplot(data=combat_df, x='Style', y='Kills', ax=axs[1])
    axs[1].set_title('Combat Style Distribution')
    axs[1].tick_params(axis='x', rotation=45)
    add_value_labels(axs[1], '{:,.0f}')

    #stratagem efficiency
    stratagem_df = pd.DataFrame(list(analysis.stratagem_efficiency.items()),
                                columns=['Stratagem', 'Usage per Mission'])
    sns.barplot(data=stratagem_df, x='Stratagem', y='Usage per Mission', ax=axs[2])
    axs[2].set_title('Stratagem Usage per Mission')
    axs[2].tick_params(axis='x', rotation=45)
    add_value_labels(axs[2])

    fig2.tight_layout(rect=[0, 0, 1, 0.97])
    images.append(fig_to_base64(fig2))
    plt.close(fig2)
    
    #3. rewards and success metrics
    fig3, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig3.suptitle("Rewards and Mission Success Metrics", fontsize=16)
    
    # rewards bar chart
    metrics = {
        'Samples per Mission': analysis.samples_per_mission,
        'XP per Mission (÷100)': analysis.xp_per_mission / 100
    }
    metrics_df = pd.DataFrame(list(metrics.items()), columns=['Metric', 'Value'])
    
    sns.barplot(x='Metric', y='Value', data=metrics_df, ax=ax1)
    ax1.set_title('Reward Metrics per Mission')
    
    for i, v in enumerate(metrics_df['Value']):
        if metrics_df['Metric'].iloc[i] == 'XP per Mission (÷100)':
            ax1.text(i, v + max(metrics_df['Value']) * 0.01, f"{v*100:.1f}", ha='center')
        else:
            ax1.text(i, v + max(metrics_df['Value']) * 0.01, f"{v:.1f}", ha='center')
    
    # Mission success pie chart
    missions_won = stats_dict['missions_won']
    missions_failed = stats_dict['missions_played'] - missions_won
    
    if stats_dict['missions_played'] > 0:
        labels = ['Successful Missions', 'Failed Missions']
        sizes = [missions_won, missions_failed]
        colors = ['#4CAF50', '#F44336']
        ax2.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors)
        ax2.set_title('Mission Success Rate')
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    images.append(fig_to_base64(fig3))
    plt.close(fig3)
    
    return images

def fig_to_base64(fig):
    """convert matplotlib figure to base64 string"""
    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight', dpi=100)
    img.seek(0)
    img_b64 = base64.b64encode(img.getvalue()).decode()
    return img_b64

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # get form data
        stats_dict = {
            'missions_played': int(request.form.get('missions_played', 0)),
            'missions_won': int(request.form.get('missions_won', 0)),
            'successful_extractions': int(request.form.get('successful_extractions', 0)),
            'objectives_completed': int(request.form.get('objectives_completed', 0)),
            'terminid_kills': int(request.form.get('terminid_kills', 0)),
            'automaton_kills': int(request.form.get('automaton_kills', 0)),
            'illuminate_kills': int(request.form.get('illuminate_kills', 0)),
            'friendly_kills': int(request.form.get('friendly_kills', 0)),
            'grenade_kills': int(request.form.get('grenade_kills', 0)),
            'melee_kills': int(request.form.get('melee_kills', 0)),
            'eagle_kills': int(request.form.get('eagle_kills', 0)),
            'shots_fired': int(request.form.get('shots_fired', 0)),
            'shots_hit': int(request.form.get('shots_hit', 0)),
            'deaths': int(request.form.get('deaths', 0)),
            'samples_collected': int(request.form.get('samples_collected', 0)),
            'total_xp': int(request.form.get('total_xp', 0)),
            'total_stratagems': int(request.form.get('total_stratagems', 0)),
            'orbitals_used': int(request.form.get('orbitals_used', 0)),
            'defensive_stratagems': int(request.form.get('defensive_stratagems', 0)),
            'eagles_used': int(request.form.get('eagles_used', 0))
        }
        
        # create visualizations
        images = create_visualizations(stats_dict)
        
        # calculate summary stats
        analysis = CombatStatsAnalysis(stats_dict)
        
        summary_stats = {
            'total_kills': analysis.total_kills,
            'mission_success_rate': analysis.mission_success_rate,
            'extraction_rate': analysis.extraction_rate,
            'samples_per_mission': analysis.samples_per_mission,
            'xp_per_mission': analysis.xp_per_mission,
            'efficiency_metrics': analysis.efficiency_metrics
        }
        
        return render_template('results.html', images=images, stats=summary_stats)
        
    except Exception as e:
        return render_template('error.html', error=str(e))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
