import MySQLdb
import pandas as pd
import warnings
from scipy.stats import ttest_1samp
from scipy.stats import shapiro
from scipy.stats import levene
from scipy.stats import ttest_ind


# Wyłączanie wszystkich UserWarning'ów
warnings.filterwarnings("ignore", category=UserWarning)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'passwd': '',
    'db': 'liga_pilkarska-2'
}


def rownosc_srednich_dla_lat(druzyna_id, kolumna, rok_1, rok_2):
    connection = MySQLdb.connect(**db_config)
    sql_query1 = f"""
                SELECT s.*
                FROM statystyki s
                JOIN mecz m ON s.mecz_id = m.mecz_id
                WHERE s.druzyna_id = {druzyna_id}
                AND YEAR(m.data_meczu) = {rok_1}
            """

    sql_query2 = f"""
                SELECT s.*
                FROM statystyki s
                JOIN mecz m ON s.mecz_id = m.mecz_id
                WHERE s.druzyna_id = {druzyna_id}
                AND YEAR(m.data_meczu) = {rok_2}
            """
    try:
        df1 = pd.read_sql_query(sql_query1, connection)
        df2 = pd.read_sql_query(sql_query2, connection)
        statistic, p_value = levene(df1[kolumna], df2[kolumna])

        print(f"Test równości srednich dla druzyny {druzyna_id} dla {kolumna} pomiędzy latami {rok_1} i {rok_2}:")
        print(f"Statystyka testowa: {statistic}")
        print(f"P-value: {p_value}")

        alpha = 0.05
        if p_value < alpha:
            print("Odrzucamy hipotezę zerową.")
        else:
            print("Nie ma podstaw do odrzucenia hipotezy zerowej.")
    except Exception as e:
        print(f"Błąd: {e}")

    finally:
        connection.close()

def badanie_rownosci_wariancji(druzyna1, druzyna2, kolumna):
    connection = MySQLdb.connect(**db_config)
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT druzyna_id FROM druzyna WHERE nazwa_druzyny IN ('{druzyna1}', '{druzyna2}')")
        results = cursor.fetchall()
        if len(results) != 2:
            print("Błąd: Niewłaściwa ilość drużyn o podanych nazwach.")
            return

        druzyna1_id, druzyna2_id = results[0][0], results[1][0]
        df_druzyna1 = pd.read_sql(f"SELECT {kolumna} FROM statystyki WHERE druzyna_id = {druzyna1_id}", connection)
        df_druzyna2 = pd.read_sql(f"SELECT {kolumna} FROM statystyki WHERE druzyna_id = {druzyna2_id}", connection)
        statistic, p_value = levene(df_druzyna1[kolumna], df_druzyna2[kolumna])

        print(f"Test równości wariancji dla podań pomiędzy drużynami {druzyna1} i {druzyna2}:")
        print(f"Statystyka testowa: {statistic}")
        print(f"P-value: {p_value}")

        alpha = 0.05
        if p_value < alpha:
            print("Odrzucamy hipotezę zerową - wariancje są różne.")
        else:
            print("Nie ma podstaw do odrzucenia hipotezy zerowej - wariancje są równe.")

    except MySQLdb.Error as err:
        print(f"Błąd: {err}")

    finally:
        cursor.close()
        connection.close()


def badanie_normalnosci_dla_zmiennych(nazwa_druzyny, kolumna):
    connection = MySQLdb.connect(**db_config)
    query = f"SELECT druzyna_id FROM druzyna WHERE nazwa_druzyny = '{nazwa_druzyny}'"
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        if result is None:
            print(f"Brak drużyny o nazwie {nazwa_druzyny}.")
            return

        druzyna_id = result[0]
        sql_query = f"SELECT {kolumna} FROM statystyki WHERE druzyna_id = {druzyna_id}"
        df = pd.read_sql(sql_query, connection)
        statistic, p_value = shapiro(df[kolumna])

        print(f"Test normalności dla zmiennej '{kolumna}':")
        print(f"Statystyka testowa: {statistic}")
        print(f"P-value: {p_value}")

        alpha = 0.05
        if p_value < alpha:
            print("Odrzucamy hipotezę zerową - rozkład nie jest normalny.\n")
        else:
            print("Nie ma podstaw do odrzucenia hipotezy zerowej - rozkład jest normalny.\n")

    except MySQLdb.Error as err:
        print(f"Błąd: {err}")

    finally:
        connection.close()


def badanie_hipotez_srednich(nazwa_druzyny, kolumna, expected_mean):
    connection = MySQLdb.connect(**db_config)
    query = f"SELECT druzyna_id FROM druzyna WHERE nazwa_druzyny = '{nazwa_druzyny}'"
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        if result is None:
            print(f"Brak drużyny o nazwie {nazwa_druzyny}.")
            return

        druzyna_id = result[0]
        sql_query = f"SELECT {kolumna} FROM statystyki WHERE druzyna_id = {druzyna_id}"
        df = pd.read_sql(sql_query, connection)

        t_statistic, p_value = ttest_1samp(df[kolumna], expected_mean)
        print(f"Test t-Studenta dla drużyny {nazwa_druzyny} i oczekiwanej średniej {expected_mean}:")
        print(f"T-statistic: {t_statistic}")
        print(f"P-value: {p_value}")

        alpha = 0.05
        if p_value < alpha:
            print("Odrzucamy hipotezę zerową.")
        else:
            print("Nie ma podstaw do odrzucenia hipotezy zerowej.")


    except Exception as e:
        print(f"Błąd: {e}")

    finally:
        connection.close()


badanie_hipotez_srednich('Real Madrid', 'podania', 300)
print('------------------------------------')
badanie_hipotez_srednich('Barcelona', 'strzaly_celne', 10)
print('------------------------------------')
badanie_hipotez_srednich('Barcelona', 'strzaly_celne', 4)
print('------------------------------------')
badanie_normalnosci_dla_zmiennych('Barcelona', 'zolte_kartki')
print('------------------------------------')
badanie_rownosci_wariancji('Barcelona', 'Real Madrid', 'podania')
print('------------------------------------')
rownosc_srednich_dla_lat(16, 'rzuty_karne', 2020, 2021)