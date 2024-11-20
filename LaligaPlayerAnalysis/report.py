import pandas as pd
import datapane as dp
import matplotlib.pyplot as plt
import seaborn as sns
from styled_components import (
    styled_title,
    styled_image,
    styled_table,
    styled_metric
)

# Load the dataset
df = pd.read_csv("resources/laliga_player_stats.csv")

# Preprocess and Summarize
# Top Teams by Goals Scored
top_teams = (
    df.groupby("Team")[["Goals scored", "Assists", "Minutes played"]]
    .sum()
    .sort_values("Goals scored", ascending=False)
    .reset_index()
)

# Top Players by Goals Scored
top_players = (
    df.groupby("Name")[["Goals scored", "Assists", "Minutes played"]]
    .sum()
    .sort_values("Goals scored", ascending=False)
    .reset_index()
)

# Visualization 1: Bar Chart - Top 10 players by goals scored
top_10_players_by_goals = df.groupby("Name")["Goals scored"].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(14, 8))
sns.barplot(
    x=top_10_players_by_goals.values,
    y=top_10_players_by_goals.index,
    palette="viridis"
)
plt.title("Top 10 Players with the Most Goals", fontsize=18)
plt.xlabel("Goals Scored", fontsize=14)
plt.ylabel("Player Name", fontsize=14)
plt.tight_layout()
bar_chart_path = "top_10_players_goals_large.png"
plt.savefig(bar_chart_path, dpi=300)
plt.close()

# Visualization 2: Bar Chart - Total goals scored by each team
team_goals = df.groupby("Team")["Goals scored"].sum().sort_values(ascending=False)
plt.figure(figsize=(16, 10))
sns.barplot(
    x=team_goals.index,
    y=team_goals.values,
    palette="magma"
)
plt.title("Total Goals Scored by Each Team", fontsize=18)
plt.xlabel("Team", fontsize=14)
plt.ylabel("Total Goals", fontsize=14)
plt.xticks(rotation=45, fontsize=12)
plt.tight_layout()
team_goals_path = "team_goals_large.png"
plt.savefig(team_goals_path, dpi=300)
plt.close()

# Visualization 3: Pie Chart - Position distribution (if available)
if "Position" in df.columns:
    position_distribution = df["Position"].value_counts()
    plt.figure(figsize=(12, 12))
    plt.pie(
        position_distribution.values,
        labels=position_distribution.index,
        autopct='%1.1f%%',
        startangle=140,
        colors=sns.color_palette("pastel")
    )
    plt.title("Distribution of Positions Among Players", fontsize=18)
    position_distribution_path = "position_distribution_large.png"
    plt.savefig(position_distribution_path, dpi=300)
    plt.close()

# Visualization 4: Improved Scatter Plot - Minutes Played vs Goals Scored
player_stats = df.groupby("Name")[["Minutes played", "Goals scored"]].sum().reset_index()

# Filter players with 0 minutes played for meaningful data
filtered_player_stats = player_stats[player_stats["Minutes played"] > 0]

plt.figure(figsize=(14, 8))
sns.scatterplot(
    data=filtered_player_stats,
    x="Minutes played",
    y="Goals scored",
    hue="Goals scored",
    size="Goals scored",
    sizes=(50, 300),
    palette="coolwarm",
    alpha=0.7
)

# Highlight top players with the highest goals scored
top_scorers = filtered_player_stats.sort_values(by="Goals scored", ascending=False).head(5)
for _, row in top_scorers.iterrows():
    plt.text(
        x=row["Minutes played"],
        y=row["Goals scored"],
        s=row["Name"],
        fontsize=10,
        weight="bold",
        color="black"
    )

plt.title("Minutes Played vs Goals Scored (Filtered)", fontsize=18)
plt.xlabel("Minutes Played", fontsize=14)
plt.ylabel("Goals Scored", fontsize=14)
plt.tight_layout()
scatter_plot_path = "filtered_minutes_vs_goals_large.png"
plt.savefig(scatter_plot_path, dpi=300)
plt.close()

# Metrics
highest_goals_team = top_teams.iloc[0]
highest_goals_player = top_players.iloc[0]

highest_goals_metric = styled_metric(
    heading="Top Scoring Team",
    value=highest_goals_team["Team"],
    change=f"{highest_goals_team['Goals scored']} Goals",
    is_upward_change=True,
)

highest_goals_player_metric = styled_metric(
    heading="Top Scoring Player",
    value=highest_goals_player["Name"],
    change=f"{highest_goals_player['Goals scored']} Goals",
    is_upward_change=True,
)

# Create the Report
report = dp.Report(
    styled_title("La Liga Player Stats Report", "Season 2021/2022"),
    dp.Text("## Key Metrics"),
    highest_goals_metric,
    highest_goals_player_metric,
    dp.Text("## Visualizations"),
    dp.Text("### Top 10 Players by Goals Scored"),
    styled_image(bar_chart_path, width="800px"),
    dp.Text("### Total Goals Scored by Each Team"),
    styled_image(team_goals_path, width="1000px"),
    dp.Text("### Distribution of Positions"),
    styled_image(position_distribution_path, width="800px") if "Position" in df.columns else dp.Text("No position data available."),
    dp.Text("### Improved Minutes Played vs Goals Scored"),
    styled_image(scatter_plot_path, width="800px"),
    dp.Text("## Data Tables"),
    styled_table(top_teams),
    styled_table(top_players)
)

grouped_data = df.groupby("Name")[["Goals scored", "Minutes played"]].sum()
print(grouped_data.loc["Messi"])


# Save the Report
report.save("laliga_visualization_report.html", open=True)
