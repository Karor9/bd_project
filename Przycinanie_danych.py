import pandas as pd

df1 = pd.read_csv("bzid_data/la-liga_2020-2021_player_data.csv")
df2 = pd.read_csv("bzid_data/la-liga_2020-2021_fixture_data.csv")
merged_df = pd.merge(df1, df2, on='game_id')
print(merged_df)
merged_df['druzyna_id'] = merged_df.apply(lambda row: row['Home'] if row['home'] == 1 else row['Away'], axis=1)

result_df = merged_df[['#', 'Player', 'Age', 'Nation', 'Pos', 'druzyna_id', 'Date', 'Cmp_x']]

result_df = result_df.sort_values(by=['Player', 'Age'], ascending=[True, False])

result_df = result_df.drop_duplicates(subset=['Player'], keep='first')

result_df['DateOfBirth'] = pd.to_datetime(result_df['Date'], format='%Y-%m-%d')

result_df[['Years', 'Days']] = result_df['Age'].str.split('-', expand=True).astype(float)

result_df['Years'] = result_df['Years'] * 365

result_df['DateOfBirth'] = result_df['DateOfBirth'] - pd.to_timedelta(result_df['Years'] + result_df['Days'], unit='D')

result_df = result_df.drop(['Age', 'Date', 'Years', 'Days'], axis=1)

sum_columns = df1.groupby('Player')[['Min', 'Gls', 'Ast', 'CrdY','CrdR', 'Cmp_x']].sum().reset_index()


result_df = pd.merge(result_df, sum_columns, on='Player', how='left')

result_df['Pos'] = result_df['Pos'].str.split(",").str[0]
result_df['Nation'] = result_df['Nation'].str.split(" ").str[1]
print(result_df)
#1.0,Sat,2020-09-12,16:00,Eibar,Celta Vigo,0.4,0.6,0–0,2020-2021,0
#Wk,Day,Date,Time,Home,Away,xG,xG.1,Score,season,game_id
result_df_match = df2[['Date','Time','Home','Away','xG','xG.1','Score']]
result_df_match[['Home Goals', 'Away Goals']] = result_df_match['Score'].str.split('–', expand=True).astype(str)


selected_columns = ['game_id', 'Home', 'Away', 'Sh', 'home', 'SoT', 'CrdY', 'CrdR', 'Gls', 'PK', 'Cmp_x', 'xG_y']

new_df_home = merged_df[selected_columns].rename(columns={'Home': 'Team'})
new_df_home = new_df_home[new_df_home['home'] == 1].groupby(['game_id', 'Team']).agg(
    {'Sh': 'sum', 'SoT': 'sum', 'CrdY': 'sum', 'CrdR': 'sum', 'PK': 'sum', 'Gls': 'sum', 'Cmp_x': 'sum', 'xG_y': 'sum'}).reset_index()

new_df_away = merged_df[selected_columns].rename(columns={'Away': 'Team'})
new_df_away = new_df_away[new_df_away['home'] == 0].groupby(['game_id', 'Team']).agg(
    {'Sh': 'sum', 'SoT': 'sum', 'CrdY': 'sum', 'CrdR': 'sum', 'PK': 'sum', 'Gls': 'sum', 'Cmp_x': 'sum', 'xG_y': 'sum'}).reset_index()

new_df = pd.concat([new_df_home, new_df_away], ignore_index=True)
new_df['Sh'] = new_df['Sh'] - new_df['SoT']
new_df = new_df.sort_values(by=['game_id'])
print(new_df)

new_df_team = pd.DataFrame()
teams = list(new_df["Team"].unique())
new_df_team["Team"] = teams


team_index_mapping = new_df_team['Team'].reset_index().set_index('Team')['index'].to_dict()
result_df['druzyna_id'] = result_df['druzyna_id'].map(team_index_mapping) +1
new_df['Team'] = new_df['Team'].map(team_index_mapping) +1
new_df['game_id'] = new_df['game_id'] + 1
print(new_df)

df_match = pd.DataFrame()
df_match = df2[['Date', 'Home', 'Away', 'Score']]
df_match['Home'] = df_match['Home'].map(team_index_mapping) + 1
df_match['Away'] = df_match['Away'].map(team_index_mapping) + 1
df_match[['Score_Home', 'Score_Away']] = df_match['Score'].str.split('–', expand=True)

# Konwersja kolumn "Score_Home" i "Score_Away" na liczby całkowite
df_match[['Score_Home', 'Score_Away']] = df_match[['Score_Home', 'Score_Away']].astype(int)
df_match = df_match.rename(columns={'Date': 'MatchDate'})
# Usunięcie oryginalnej kolumny "Score"
df_match = df_match.drop('Score', axis=1)





# result_df.to_csv("bzid_data/players.csv")
new_df.to_csv("bzid_data/stats.csv")
# new_df_team.to_csv("bzid_data/teams.csv")
# df_match.to_csv("bzid_data/matches.csv")