## Helldivers 2 Data Visualization
This is a basic data visualization of a single players 'Career' stats from the videogame Helldivers 2. The data is taken from the in game stats, and then visualized using Python and Jupyter Notebook.
As of now we are only looking at a single players stats.

The current data visualization covers the following:
- Enemy Distribution Analysis
- Combat Performance Analysis
- Rewardsa and Mission Success Metrics

[Data Visualization Notebook Here](camp_viz.ipynb)

For more information about the game follow the link below:
[Helldivers 2 Wiki](https://helldivers.wiki.gg/wiki/Helldivers_2)

## Statsitical Analysis Results 
```
=== Statistical Analysis Results ===

Efficiency Metrics (per Mission):
Total Kills: 307326
Kills per mission: 112.86
Stratagems per Mission: 20.48
Objectives Per Mission: 4.97
Deaths per Mission: 2.80
Accuracy(%): 51.82
Samples per Mission: 17.37
XP per Mission: 1152.76

Combat Style Distribution:
Regular Kills: 247,755 (80.6%)
Grenade Kills: 4,724 (1.5%)
Melee Kills: 463 (0.2%)
Eagle Kills: 54,384 (17.7%)

Stratagem Efficiency (per Mission):
Orbital Strikes: 3.05
Defensive Tools: 4.90
Eagle Support: 6.07

Mission Performance Metrics:
Success Rate: 96.0%
Extraction Rate: 84.1%
Objectives Completed per Mission: 4.97
Samples Collected per Mission: 17.37
XP Earned per Mission: 1152.76
```

![Enemy Distribution Analysis](./assets/enemy_dist_analysis.png)

## Enemy Distribution
Within the in game stats, "Career Kills" is listed, but there were past issues when adding the values would result in an over/under count. It looks like Arrowhead has fixed the issue, but I removed it from the data and calculated it myself. 

The Illuminates were introduced in mid December 2024, so the data is skewed towards the Automatons and Bugs. I would also say that Illuminates are the easiest faction to play against, and their current roster of enemies incredibly increases a players kill count. Before starting this project Illuminate kills was at 13,000+ and bugs was at 29,000+. Arrowhead has had a lot of major orders, and weapons test against terminids starting from November 2024, which greatly increased the kill count.


## Samples Earned
Samples are used to gain ship upgrades. Which includes a time decrease in weapons, stratagem cooldown and much more. _My_ samples earned may be a bit skewed due to me leaving samples at extract for another player to pick up. It is a tactic used by players to pick up dropped samples, and congregate them to increase the likelihood of extracting with the samples. **ALL** collected samples are shared between players, as in everyone gets the samples collected added to their total sample count. 

## XP (Experience Points)
Experience points increases depending on the level played. Currently there are 10 difficulty levels from 1-10. Players earn more as a group along with total objectives completed.   Where level 10 has a 300x multiplier for XP earned. The XP earned depends on the mission type which is then multiplied.

For more info:
[Helldivers 2 XP Farming Guide](https://game8.co/games/Helldivers-2/archives/446460#hl_2)


