import MySQLdb
import pandas as pd
import warnings
import matplotlib.pyplot as plt
# Wyłączanie wszystkich UserWarning'ów
warnings.filterwarnings("ignore", category=UserWarning)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'liga_pilkarska2',
}

def wizualizuj_podsumowanie():
    connection = MySQLdb.connect(**db_config)
    query = "SELECT * FROM podsumowanie"
    
    try:
        data = pd.read_sql_query(query, connection)
        
        if data.empty:
            print("No data to plot.")
            return

        dates = data['data_m']
        goals = data['ilosc_bramek']

        plt.figure(figsize=(10, 6))
        plt.plot(dates, goals, marker='o', linestyle='-')

        for i, (date, goal) in enumerate(zip(dates, goals)):
            plt.text(date, goal - 0.2, f'{(date)}', ha='center', va='top', rotation=90, fontsize=8,
                    color='red')

        plt.xlabel('Data')
        plt.ylabel('Suma bramek')
        plt.title('Podsumowanie bramek dzień po dniu')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Błąd: {e}")
    finally:
        connection.close()

def liczba_bramek_rok_miesiac(rok, miesiac):
    connection = MySQLdb.connect(**db_config)
    query = f"SELECT wynik_gospodarz, wynik_gosc, data_meczu FROM mecz WHERE YEAR(data_meczu) = {rok} AND MONTH(data_meczu) = {miesiac}"
    try:
        df = pd.read_sql_query(query, connection)
        wszystkie_bramki = df['wynik_gospodarz'].sum() + df['wynik_gosc'].sum()
        print(f"Ilosc bramek w {miesiac} miesiacu roku {rok}: {wszystkie_bramki}")
    except Exception as e:
        print(f"Błąd: {e}")

    finally:
        connection.close()


def liczba_bramek_rok(rok):
    connection = MySQLdb.connect(**db_config)
    query = f"SELECT wynik_gospodarz, wynik_gosc, data_meczu FROM mecz WHERE YEAR(data_meczu) = {rok}"
    try:
        df = pd.read_sql_query(query, connection)
        wszystkie_bramki = df['wynik_gospodarz'].sum() + df['wynik_gosc'].sum()
        print(f"Ilosc bramek w roku {rok}: {wszystkie_bramki}")
    except Exception as e:
        print(f"Błąd: {e}")

    finally:
        connection.close()

def statystyka_opisowa_dla_meczu(druzyna_id, czy_gospodarz):
    connection = MySQLdb.connect(**db_config)
    if czy_gospodarz:
        query = f"SELECT wynik_gospodarz FROM mecz WHERE druzyna_gospodarz_id = {druzyna_id}"
    else:
        query = f"SELECT wynik_gosc FROM mecz WHERE druzyna_gosc_id = {druzyna_id}"

    try:
        df = pd.read_sql_query(query, connection)
        print(df.describe())
        variance = df.var()
        print(f"var     {variance}")
        median = df.median()
        print(f"median     {median}")
    except Exception as e:
        print(f"Błąd: {e}")

    finally:
        connection.close()


def statystyka_opisowa_dla_statystyk(druzyna_id, column_name):
    connection = MySQLdb.connect(**db_config)

    try:
        df = pd.read_sql_query(f"CALL PokazStatystykiZDruzynaId({druzyna_id})", connection)
        print(df[column_name].describe())
        variance = df[column_name].var()
        print(f"var     {variance}")
        median = df[column_name].median()
        print(f"median     {median}")
    except Exception as e:
        print(f"Błąd: {e}")

    finally:
        connection.close()


# statystyka_opisowa_dla_statystyk(1, 'podania')
# statystyka_opisowa_dla_meczu(1, True)
# statystyka_opisowa_dla_meczu(1, False)
# liczba_bramek_rok(2020)
wizualizuj_podsumowanie()

