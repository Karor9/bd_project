import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import MySQLdb
from sklearn.preprocessing import PolynomialFeatures

db_config = {
    'host': 'localhost',
    'user': 'root',
    'passwd': '',
    'db': 'liga_pilkarska2'
}

sql_query = "CALL PokazStatystyki()"

def execute_query_and_load_to_dataframe(sql_query):
    connection = MySQLdb.connect(**db_config)

    try:
        df = pd.read_sql_query(sql_query, connection)
        
        regression(df)
        # draw_scatter_sot_all(df)

    except Exception as e:
        print(f"Błąd: {e}")

    finally:
        connection.close()

def regression_shot(druzyna_id):
    connection = MySQLdb.connect(**db_config)

    try:
        df = pd.read_sql_query(f"CALL PokazStatystykiZDruzynaId({druzyna_id})", connection)
        print(df)
        regression(df)

    except Exception as e:
        print(f"Błąd: {e}")

    finally:
        connection.close()

def regression_league():
    connection = MySQLdb.connect(**db_config)

    try:
        df = pd.read_sql_query(f"CALL PokazStatystyki()", connection)
        print(df)
        # regression(df)
        # polynomial_regression(df)

    except Exception as e:
        print(f"Błąd: {e}")

    finally:
        connection.close()

def xg_goal_by_team(druzyna_id):
    connection = MySQLdb.connect(**db_config)

    try:
        df = pd.read_sql_query(f"CALL PokazStatystykiZDruzynaId({druzyna_id})", connection)
        draw_scatter_sot_all(df)

    except Exception as e:
        print(f"Błąd: {e}")

    finally:
        connection.close()


def passes_df(druzyna_id):
    connection = MySQLdb.connect(**db_config)

    try:
        df = pd.read_sql_query(f"CALL PokazLiczbePodanDlaDruzyny({druzyna_id})", connection)
        draw_plot(df)

    except Exception as e:
        print(f"Błąd: {e}")

    finally:
        connection.close()

def polynomial_regression(df, degree=2):
    X = df['strzaly_celne'].values.reshape(-1, 1)
    y = df['strzaly_niecelne'].values.reshape(-1, 1)

    poly_features = PolynomialFeatures(degree=degree)
    X_poly = poly_features.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_poly, y, test_size=0.2, random_state=42)

    model = LinearRegression()

    model.fit(X_train, y_train)

    X_range = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
    X_range_poly = poly_features.transform(X_range)
    y_pred = model.predict(X_range_poly)

    plt.scatter(X, y, color='black', label='Actual data')
    plt.plot(X_range, y_pred, color='blue', linewidth=3, label=f'Regresja wielomianowa (Stopień={degree})')
    plt.xlabel('Strzały Celne')
    plt.ylabel('Strzały Niecelne')
    plt.title('Regresja wielomianowa - Strzały Celne vs. Strzały Niecelne')
    plt.legend()
    plt.show()

    y_pred_test = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred_test)
    print(f"Średni błąd kwadratowy (MSE): {mse}")

    print("Współczynniki regresji:")
    for i, coef in enumerate(model.coef_[0]):
        print(f"  Coefficient {i}: {coef}")
    print(f"Intercept: {model.intercept_[0]}")


def regression(df):
    X = df['strzaly_celne'].values.reshape(-1, 1)
    y = df['strzaly_niecelne'].values.reshape(-1, 1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    plt.scatter(X_test, y_test, color='black', label='Actual data')
    plt.plot(X_test, y_pred, color='blue', linewidth=3, label='Linear Regression')
    plt.xlabel('Strzały Celne')
    plt.ylabel('Strzały Niecelne')
    plt.title('Regresja liniowa - Strzały Celne vs. Strzały Niecelne')
    plt.legend()
    plt.show()

    mse = mean_squared_error(y_test, y_pred)
    print(f"Średni błąd kwadratowy (MSE): {mse}")

    print(f"Współczynniki regresji: Intercept={model.intercept_[0]}, Coefficient={model.coef_[0][0]}")

def show_table():
    connection = MySQLdb.connect(**db_config)

    try:
        df = pd.read_sql_query(f"CALL WygenerujTabele()", connection)
        print(df)

    except Exception as e:
        print(f"Błąd: {e}")

    finally:
        connection.close()

def draw_plot(df):
    plt.bar(df.index+1, df['podania'], label='Podania')
    plt.axhline(y=df['podania'].mean(), color='r', linestyle='--', label='Średnia')

    plt.xticks(df.index+1)

    plt.xlabel('Drużyna')
    plt.ylabel('Liczba podań')
    plt.title('Liczba podań dla drużyny Barcelona')

    plt.legend()

    plt.show()


def logistic_regression(df):
    X = df['strzaly_celne'].values.reshape(-1, 1)
    y = df['strzaly_niecelne'].values.ravel()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression()

    model.fit(X_train, y_train)

    y_pred_proba = model.predict_proba(X_test)[:, 1]
    y_pred = np.round(y_pred_proba)

    plt.scatter(X_test, y_test, color='black', label='Actual data')
    plt.plot(X_test, y_pred_proba, color='blue', linewidth=3, label='Logistic Regression')
    plt.xlabel('Strzały Celne')
    plt.ylabel('Prawdopodobieństwo Strzałów Niecelnych')
    plt.title('Regresja logistyczna - Strzały Celne vs. Strzały Niecelne')
    plt.legend()
    plt.show()

def draw_scatter_sot_all(df):
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'brown', 'pink', 'gray', 'cyan', 'magenta', 'yellow', 'lime', 'teal', 'indigo', 'violet', 'salmon', 'olive', 'maroon', 'navy', 'turquoise']
    markers = ['o', 's', '^', 'D', '*', 'p', 'X', 'H', '+', '>', '<', 'v', '|', '_', '.', ',']


    unique_teams = df['nazwa_druzyny'].unique()

    team_color_map = {team: (colors[i % len(colors)], markers[i % len(markers)]) for i, team in enumerate(unique_teams)}

    df['color'] = df['nazwa_druzyny'].map(lambda x: team_color_map[x][0])
    df['marker'] = df['nazwa_druzyny'].map(lambda x: team_color_map[x][1])

    plt.figure(figsize=(10, 6))
    for team, color_marker in team_color_map.items():
        team_data = df[df['nazwa_druzyny'] == team]
        plt.scatter(team_data['strzaly_celne'], team_data['strzaly_niecelne'], label=f'{team}', color=color_marker[0], marker=color_marker[1])

    plt.legend()
    plt.xlabel('Strzały celne')
    plt.ylabel('Strzały niecelne')
    plt.title('Strzały celne, a niecelne')
    plt.grid(True)
    plt.show()

def draw_scatter_plot(df):
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'brown', 'pink', 'gray', 'cyan', 'magenta', 'yellow', 'lime', 'teal', 'indigo', 'violet', 'salmon', 'olive', 'maroon', 'navy', 'turquoise']
    markers = ['o', 's', '^', 'D', '*', 'p', 'X', 'H', '+', '>', '<', 'v', '|', '_', '.', ',']


    unique_teams = df['nazwa_druzyny'].unique()

    team_color_map = {team: (colors[i % len(colors)], markers[i % len(markers)]) for i, team in enumerate(unique_teams)}

    df['color'] = df['nazwa_druzyny'].map(lambda x: team_color_map[x][0])
    df['marker'] = df['nazwa_druzyny'].map(lambda x: team_color_map[x][1])

    plt.figure(figsize=(10, 6))
    for team, color_marker in team_color_map.items():
        team_data = df[df['nazwa_druzyny'] == team]
        plt.scatter(team_data['xg'], team_data['liczba_bramek'], label=f'{team}', color=color_marker[0], marker=color_marker[1])

    plt.legend()
    plt.xlabel('xg')
    plt.ylabel('Bramki')
    plt.title('xG Zawodników a bramki')
    plt.grid(True)
    plt.show()

# execute_query_and_load_to_dataframe(sql_query)
# regression_shot(5)
# passes_df(20)
# show_table()
regression_league()