import pandas as pd
import MySQLdb
import numpy as np
import time

db_host = 'localhost'
db_user = 'root'
db_password = ''
db_name = 'liga_pilkarska2'

csv_file_path_team = 'bzid_data/teams.csv'
csv_file_path_player = 'bzid_data/players.csv' 
csv_file_path_stats = 'bzid_data/stats.csv'
csv_file_path_matches = 'bzid_data/matches.csv'

def connect_to_database():
    try:
        connection = MySQLdb.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def load_team_names_to_table(connection, csv_file_path, table_name):
    try:
        data_frame = pd.read_csv(csv_file_path, usecols=['Team'])
        data_frame.rename(columns={'Team': 'nazwa_druzyny'}, inplace=True)

        cursor = connection.cursor()

        for index, row in data_frame.iterrows():
            team_name = row['nazwa_druzyny']
            query = f"INSERT INTO {table_name} (nazwa_druzyny) VALUES (%s)"
            cursor.execute(query, (team_name,))

        connection.commit()
        print("Team names loaded successfully to the database.")

    except Exception as e:
        print(f"Error loading team names to the database: {e}")
    finally:
        if cursor:
            cursor.close()

def load_players_to_table(connection, csv_file_path, table_name):
    try:
        data_frame = pd.read_csv(csv_file_path)
        data_frame.replace({np.nan: None}, inplace=True)
        data_frame = data_frame.dropna()
        # data_frame.rename(columns={'Team': 'nazwa_druzyny'}, inplace=True)

        cursor = connection.cursor()

        for index, row in data_frame.iterrows():
            query = f"INSERT INTO {table_name} (imie_nazwisko, data_urodzenia, reprezentacja, pozycja, druzyna_id) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (row['Player'], row['DateOfBirth'], row['Nation'], row['Pos'], row['druzyna_id']))

        connection.commit()
        print("Team names loaded successfully to the database.")

    except Exception as e:
        print(f"Error loading players to the database: {e}\nQuery: {query}")
    finally:
        if cursor:
            cursor.close()

def load_matches_to_table(connection, csv_file_path, table_name):
    try:
        data_frame = pd.read_csv(csv_file_path)
        data_frame.replace({np.nan: None}, inplace=True)
        data_frame = data_frame.dropna()
        # data_frame.rename(columns={'Team': 'nazwa_druzyny'}, inplace=True)

        cursor = connection.cursor()

        for index, row in data_frame.iterrows():
            query = f"INSERT INTO {table_name} (data_meczu, druzyna_gospodarz_id, druzyna_gosc_id, wynik_gospodarz, wynik_gosc) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (row['MatchDate'], row['Home'], row['Away'], row['Score_Home'], row['Score_Away']))

        connection.commit()
        print("Matches names loaded successfully to the database.")

    except Exception as e:
        print(f"Error loading players to the database: {e}\nQuery: {query}")
    finally:
        if cursor:
            cursor.close()

def load_stats_to_table(connection, csv_file_path, table_name):
    try:
        data_frame = pd.read_csv(csv_file_path)
        data_frame.replace({np.nan: None}, inplace=True)
        data_frame = data_frame.dropna()

        cursor = connection.cursor()

        for index, row in data_frame.iterrows():
            query = f"INSERT INTO {table_name} (mecz_id, druzyna_id, xg, podania, strzaly_celne, strzaly_niecelne, rzuty_karne, zolte_kartki, czerwone_kartki) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (row['game_id'], row['Team'], np.round(row['xG_y'], 2), row['Cmp_x'], row['SoT'], row['Sh'], row['PK'], row['CrdY'], row['CrdR']))

        connection.commit()
        print("Statistics loaded successfully to the database.")

    except Exception as e:
        print(f"Error loading statistics to the database: {e}\nQuery: {query}")
    finally:
        if cursor:
            cursor.close()

if __name__ == "__main__":
    db_connection = connect_to_database()

    if db_connection:
        #load_team_names_to_table(db_connection, csv_file_path_team, 'druzyna')
        #load_players_to_table(db_connection, csv_file_path_player, 'zawodnik')
        #load_matches_to_table(db_connection, csv_file_path_matches, 'mecz')
        load_stats_to_table(db_connection, 'bzid_data/stats.csv', 'statystyki')
        if db_connection:
            db_connection.close()