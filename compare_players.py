from typing import Dict, List,Tuple
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# import function from the create_graphs.py
from create_graphs import (
    EnemyKillStats,
    CombatStatsAnalysis,
    add_value_labels,
    create_kill_distribution_pie_chart,
    analyze_combat_stats,
)

def compare_players_metrics(df: pd.DataFrame, player_names: List[str] = ["Player 1", "Player 2"]) -> plt.Figure:
    """
    Create a comparison of key metrics between two players

    Args:
        df (pd.DataFrame): DataFrame containing player data.
        player_names (List[str]): List of two player names to compare.
    Returns:
        Figure with the comp viz.
    """

    player1_data = CombatStatsAnalysis(df) # @ index 0
    player2_data = CombatStatsAnalysis(df.iloc[[1]].reset_index(drop=True)) #

    # create fig for comp
    fig, axs = plt.subplots(3, 1, figsize=(16, 15))
    fig.suptitle(f"Comparison of {player_names[0]} and {player_names[1]}", fontsize=20)

    #1. Efficiency metrics comp
    metrics_to_compare = [
        "Kills per mission",
        "Accuracy(%)",
        "Deaths per mission",
        "Objectives Per Mission",
        "Samples per mission",
    ]

    # empty df for comp
    comparison_data = []

    for metric in metrics_to_compare:
        comparison_data.append({
            'Metric': metric,
            'Player': player_names[0],
            'Value': player1_data.efficiency_metrics[metric],
        })
        comparison_data.append({
            'Metric': metric,
            'Player': player_names[1],
            'Value': player2_data.efficiency_metrics[metric],
        })

    comparison_df = pd.DataFrame(comparison_data)

    # plot eff comp
    sns.barplot(data=comparison_df, x='Metric', y='Value', hue='Player', ax=axs[0])
    axs[0].set_title("Efficiency Metrics Comparison")
    axs[0].tick_params(axis='x', rotation=30)

    # 2. combat style comp
    combat_data = []

    for style, kills in player1_data.combat_style.items():
        combat_data.append({
            'Style': style,
            'Player': player_names[0],
            'Kills': kills,
        })
    for style, kills in player2_data.combat_style.items():
        combat_data.append({
            'Style': style,
            'Player': player_names[1],
            'Kills': kills,
        })

    combat_df = pd.DataFrame(combat_data) 
    
    # plot combat style comp
    sns.barplot(data=combat_df, x='Style', y='Kills', hue='Player', ax=axs[1])
    axs[1].set_title("Combat Style Comparison")
    axs[1].tick_params(axis='x', rotation=30)
    axs[1].legend(title='')

    # 3. succ met comp
    success_data = [
        {
            'Metric': 'Mission Success Rate(%)',
            'Player': player_names[0],
            'Value': player1_data.mission_success_rate,
        },
        {
            'Metric': 'Mission Success Rate(%)',
            'Player': player_names[1],
            'Value': player2_data.mission_success_rate,
        },
        {
            'Metric': 'Extraction Rate(%)',
            'Player': player_names[0],
            'Value': player1_data.extraction_rate,
        },
        {
            'Metric': 'Extraction Rate(%)',
            'Player': player_names[1],
            'Value': player2_data.xp_per_mission / 100, # we divide by 100 to get the percentage
        },
        {
            'Metric': 'XP per Mission',
            'Player': player_names[0],
            'Value': player1_data.xp_per_mission / 100,
        }
    ]

    success_df = pd.DataFrame(success_data)

    # plot succ met comp
    bars = sns.barplot(data=success_df, x='Metric', y='Value', hue='Player', ax=axs[2])
    axs[2].set_title("Success Metrics Comparison")
    axs[2].tick_params(axis='x', rotation=30)
    axs[2].legend(title='')

    for i, container in enumerate(axs[2].containers):
        plaer_idx = 1 % 2 # to identify the player
        for j, patch in enumerate(container):
            value = success_df['Value'].iloc[j + (i * len(container) // 2)] # we use // to get the index
            # if the value is a percentage, we divide by 100
            # else we just use the value
            if success_df['Value'].iloc[j + (i * len(container) // 2)]  == 'XP per Mission':
                # show actual XP
                label = f"{value * 100:.0f}"
            else:
                label = f"{value:.1f}"
            axs[2].annotate(
                label,
                # position the label above the bar
                (patch.get_x() + patch.get_width() / 2, patch.get_height()),
                ha='center',
                va='bottom',
                size=10, xytext=(0, 5), # 5 points vertical offset
                textcoords='offset points',
            )
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    return fig

def compare_enemy_kills(df: pd.DataFrame, player_names: List[str] = ["Player 1", "Player 2"]) -> plt.Figure:
    '''Compare enemy kills between two players '''

    player1_stats = EnemyKillStats(
        terminid_kills=df['Terminid Kills'].iloc[0],
        automaton_kills=df['Automaton Kills'].iloc[0],
        illuminate_kills=df['Illuminate Kills'].iloc[0],
        friendly_kills=df['Friendly Kills'].iloc[0],
    )
    player2_stats = EnemyKillStats(
        terminid_kills=df['Terminid Kills'].iloc[1],
        automaton_kills=df['Automaton Kills'].iloc[1],
        illuminate_kills=df['Illuminate Kills'].iloc[1],
        friendly_kills=df['Friendly Kills'].iloc[1],
    )

    # create comparison fig
    fig, axs = plt.subplots(2, 1, figsize=(16, 12))
    fig.suptitle(f"Enemy Kill Distribution Comparison:, {player_names[0]} vs {player_names[1]}", fontsize=20)

    # prep data for bar plots
    comparison_data = []
    for enemy_kills in player1_stats.to_dict().items():
        comparison_data.append({
            'Enemy': enemy_kills[0],
            'Player': player_names[0],
            'Kills': enemy_kills[1],
        })
    for enemy_kills in player2_stats.to_dict().items():
        comparison_data.append({
            'Enemy': enemy_kills[0],
            'Player': player_names[1],
            'Kills': enemy_kills[1],
        })
    comparison_df = pd.DataFrame(comparison_data)

    # 1. bar chart comp
    sns.barplot(data=comparison_df, x='Enemy Type', y='Kills', hue='Player', ax=axs[0, 0])
    axs[0,0].set_title("Kills by Enemy Type")
    axs[0,0].tick_params(axis='x', rotation=45)
    axs[0,0].legend(title='')

    # 2. pie char for P1
    labels1 = list(player1_stats.to_dict().keys())
    sizes1 = list(player1_stats.to_dict().values())
    axs[0,1].pie(sizes1, labels=labels1, autopct='%1.1f%%')
    axs[0,1].set_title(f"{player_names[0]} Enemy Kill Distribution")

    # 3. pie char for P2
    labels2 = list(player2_stats.to_dict().keys())
    sizes2 = list(player2_stats.to_dict().values())
    axs[1,1].pie(sizes2, labels=labels2, autopct='%1.1f%%')
    axs[1,1].set_title(f"{player_names[1]} Enemy Kill Distribution")

    # 4. kill eff. comp
    efficiency_data = []

    for enemy, kills in player1_stats.to_dict().items():
        efficiency_data.append({
            'Enemy': enemy,
            'Player': player_names[0],
            'Efficiency': kills / player1_stats.total_kills,
        })
    for enemy, kills in player2_stats.to_dict().items():
        efficiency_data.append({
            'Enemy': enemy,
            'Player': player_names[1],
            'Efficiency': kills / player2_stats.total_kills,
        })
    efficiency_df = pd.DataFrame(efficiency_data)

    sns.barplot(data=efficiency_df, x='Enemy', y='Efficiency', hue='Player', ax=axs[1,0])
    axs[1,0].set_title("Kill Efficiency by Enemy Type per Mission")
    axs[1,0].tick_params(axis='x', rotation=45)
    axs[1,0].legend(title='')

    plt.tight_layout(rect=[0, 0, 1, 0.97])
    return fig

if __name__ == "__main__":