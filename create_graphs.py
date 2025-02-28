from typing import Dict, List, Tuple
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dataclasses import dataclass

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
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.total_kills = (df['Terminid Kills'].iloc[0] +
                            df['Automaton Kills'].iloc[0] +
                            df['Illuminate Kills'].iloc[0])

        self.efficiency_metrics = self.calculate_efficiency_metrics()
        self.combat_style = self.calculate_combat_stats()
        self.stratagem_efficiency = self.calculate_stratagem_efficiency()
        self.mission_success_rate = df['Mission Won'].iloc[0] / df['Missions Played'].iloc[0] * 100
        self.extraction_rate = df['Successful Extractions'].iloc[0] / df['Missions Played'].iloc[0] * 100
        self.objective_completion_rate = df['Obj Completed'].iloc[0] / df['Missions Played'].iloc[0]
        
        # added new metrics for samples and xp per mission
        self.samples_per_mission = df['Samples Collected'].iloc[0] / df['Missions Played'].iloc[0]
        self.xp_per_mission = df['Total XP Earned'].iloc[0] / df['Missions Played'].iloc[0]

    def calculate_efficiency_metrics(self) -> Dict[str, float]:
        return {
            "Kills per mission": self.total_kills / self.df['Missions Played'].iloc[0],
            "Stratagems per Mission": self.df['Total Strats Used'].iloc[0] / self.df['Missions Played'].iloc[0],
            "Objectives Per Mission": self.df['Obj Completed'].iloc[0] / self.df['Missions Played'].iloc[0],
            "Deaths per Mission": self.df['Deaths'].iloc[0] / self.df['Missions Played'].iloc[0],
            "Accuracy(%)": self.df['Shots Hit'].iloc[0] / self.df['Shots Fired'].iloc[0] * 100,
            "Samples per Mission": self.df['Samples Collected'].iloc[0] / self.df['Missions Played'].iloc[0],
            "XP per Mission": self.df['Total XP Earned'].iloc[0] / self.df['Missions Played'].iloc[0]
        }

    def calculate_combat_stats(self) -> Dict[str, float]:
        return {
            "Regular Kills": self.total_kills - self.df['Grenade Kills'].iloc[0]
                             - self.df['Melee Kills'].iloc[0]
                             - self.df['Eagle Kills'].iloc[0],
            "Grenade Kills": self.df['Grenade Kills'].iloc[0],
            "Melee Kills": self.df['Melee Kills'].iloc[0],
            "Eagle Kills": self.df['Eagle Kills'].iloc[0]
        }

    def calculate_stratagem_efficiency(self) -> Dict[str, float]:
        return {
            "Orbital Strikes": self.df['Orbitals Used'].iloc[0] / self.df['Missions Played'].iloc[0],
            "Defensive Tools": self.df['Defensive Stratagems Used'].iloc[0] / self.df['Missions Played'].iloc[0],
            "Eagle Support": self.df['Eagles Used'].iloc[0] / self.df['Missions Played'].iloc[0]
        }


def add_value_labels(ax: plt.Axes, format_str: str = '{:.2f}') -> None:
    """
    Add labels to the end of each bar in a bar chart.
    Args:
        ax: the axis of the plot that we want to add the labels to
        format_str: the format of the string to be displayed
    """
    for rect in ax.patches:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height,
                format_str.format(height),
                ha='center', va='bottom')


def create_kill_distribution_pie_chart(
        stats: EnemyKillStats,
        figsize: tuple = (15, 10)
) -> plt.Figure:
    fig = plt.figure(figsize=figsize)
    fig.suptitle("Enemy Kill Distribution Analysis", fontsize=16)

    # 1. create bar plot
    ax1 = plt.subplot(2, 1, 1)
    kills_df = pd.DataFrame(
        list(stats.to_dict().items()),
        columns=['Enemy Type', 'Kills']
    )
    sns.barplot(x='Enemy Type', y='Kills', data=kills_df, ax=ax1)
    ax1.set_title("Kills by Enemy Type")
    plt.xticks(rotation=45, ha='right')
    add_value_labels(ax1, format_str='{:.0f}')

    # 2. create pie chart
    ax2 = plt.subplot(2, 1, 2)
    kill_values = list(stats.to_dict().values())
    kill_labels = list(stats.to_dict().keys())
    ax2.pie(kill_values, labels=kill_labels, autopct='%1.1f%%')
    ax2.set_title("Enemy Kills Distribution")

    plt.tight_layout()
    return fig


def analyze_combat_stats(df: pd.DataFrame) -> plt.Figure:
    stats = EnemyKillStats(
        terminid_kills=df['Terminid Kills'].iloc[0],
        automaton_kills=df['Automaton Kills'].iloc[0],
        illuminate_kills=df['Illuminate Kills'].iloc[0],
        friendly_kills=df['Friendly Kills'].iloc[0]
    )

    return create_kill_distribution_pie_chart(stats)


def perform_analysis(df: pd.DataFrame) -> Tuple[plt.Figure, plt.Figure]:
    """
    Perform analysis on combat stats data and return multiple figures
    
    Returns:
        Tuple containing (main_analysis_figure, reward_metrics_figure)
    """
    analysis = CombatStatsAnalysis(df)

    # create figure with subplots for main analysis
    main_fig, axs = plt.subplots(3, 1, figsize=(14, 12))
    main_fig.suptitle("Combat Performance Analysis", fontsize=16)

    # 1. efficiency metrics viz
    metrics_df = pd.DataFrame(list(analysis.efficiency_metrics.items()),
                              columns=['Metric', 'Value'])
    sns.barplot(data=metrics_df, x='Metric', y='Value', ax=axs[0])
    axs[0].set_title('Performance Metrics per Mission')
    axs[0].tick_params(axis='x', rotation=45)
    add_value_labels(axs[0])

    # 2. combat style viz
    combat_df = pd.DataFrame(list(analysis.combat_style.items()),
                             columns=['Style', 'Kills'])
    sns.barplot(data=combat_df, x='Style', y='Kills', ax=axs[1])
    axs[1].set_title('Combat Style Distribution')
    axs[1].tick_params(axis='x', rotation=45)
    add_value_labels(axs[1], '{:,.0f}')

    # 3. stratagem efficiency viz
    stratagem_df = pd.DataFrame(list(analysis.stratagem_efficiency.items()),
                                columns=['Stratagem', 'Usage per Mission'])
    sns.barplot(data=stratagem_df, x='Stratagem', y='Usage per Mission', ax=axs[2])
    axs[2].set_title('Stratagem Usage per Mission')
    axs[2].tick_params(axis='x', rotation=45)
    add_value_labels(axs[2])

    main_fig.tight_layout(rect=[0, 0, 1, 0.97])  # adjust

    # create a separate figure for rewards metrics
    reward_fig = create_reward_metrics_chart(df)

    # print analysis summary
    print("\n=== Statistical Analysis Results ===")
    print("\nEfficiency Metrics (per Mission):")
    # print total kills
    print(f"Total Kills: {analysis.total_kills}")
    for metric, value in analysis.efficiency_metrics.items():
        print(f"{metric}: {value:.2f}")

    print("\nCombat Style Distribution:")
    for style, kills in analysis.combat_style.items():
        percentage = (kills / analysis.total_kills) * 100
        print(f"{style}: {kills:,} ({percentage:.1f}%)")

    print("\nStratagem Efficiency (per Mission):")
    for strat, usage in analysis.stratagem_efficiency.items():
        print(f"{strat}: {usage:.2f}")

    print("\nMission Performance Metrics:")
    print(f"Success Rate: {analysis.mission_success_rate:.1f}%")
    print(f"Extraction Rate: {analysis.extraction_rate:.1f}%")
    print(f"Objectives Completed per Mission: {analysis.objective_completion_rate:.2f}")
    print(f"Samples Collected per Mission: {analysis.samples_per_mission:.2f}")
    print(f"XP Earned per Mission: {analysis.xp_per_mission:.2f}")

    return main_fig, reward_fig

def create_reward_metrics_chart(df: pd.DataFrame) -> plt.Figure:
    """Creates a visualization specifically for reward-based metrics"""
    # calculate metrics
    missions_played = df['Missions Played'].iloc[0]
    samples_per_mission = df['Samples Collected'].iloc[0] / missions_played
    xp_per_mission = df['Total XP Earned'].iloc[0] / missions_played
    
    # create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Rewards and Mission Success Metrics", fontsize=16)
    
    # bar chart for per-mission metrics
    metrics = {
        'Samples per Mission': samples_per_mission,
        'XP per Mission (÷100)': xp_per_mission / 100
    }
    metrics_df = pd.DataFrame(list(metrics.items()), columns=['Metric', 'Value'])
    
    # create bar chart
    sns.barplot(x='Metric', y='Value', data=metrics_df, ax=ax1)
    ax1.set_title('Reward Metrics per Mission')
    
    # add value labels
    for i, v in enumerate(metrics_df['Value']):
        if metrics_df['Metric'][i] == 'XP per Mission (÷100)':
            # show the actual XP value (not divided by 100)
            ax1.text(i, v + 0.1, f"{v*100:.1f}", ha='center')
        else:
            ax1.text(i, v + 0.1, f"{v:.1f}", ha='center')
    
    # pie chart for samples by mission result
    labels = ['Successful Missions', 'Failed Missions']
    sizes = [df['Mission Won'].iloc[0], df['Missions Played'].iloc[0] - df['Mission Won'].iloc[0]]
    ax2.pie(sizes, labels=labels, autopct='%1.1f%%', 
            colors=['#4CAF50', '#F44336'])
    ax2.set_title('Mission Success Rate')
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # adjust
    return fig


def show_all_visualizations(df: pd.DataFrame):
    """
    generate and display all visualizations in a single function call
    """
    plt.close('all')  # close any existing plots

    stats = EnemyKillStats(
        terminid_kills=df['Terminid Kills'].iloc[0],
        automaton_kills=df['Automaton Kills'].iloc[0],
        illuminate_kills=df['Illuminate Kills'].iloc[0],
        friendly_kills=df['Friendly Kills'].iloc[0]
    )
    kill_dist_fig = create_kill_distribution_pie_chart(stats)
    main_fig, reward_fig = perform_analysis(df)
    plt.show()