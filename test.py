import requests
import json
import sqlalchemy
from sqlalchemy import MetaData, text

with open('config_secret.json') as f:
    config = json.load(f)

MYSQL_CONFIG = {
    "host": config["DB_HOST"],
    "port": config["DB_PORT"],
    "username": config["DB_USER"],
    "password": config["DB_PASSWORD"],
    "database": config["DB_NAME"],
    "ssl_ca": config["SSL_CA_PATH"]
}

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"
def generate_db_schema(engine):
    """Automatycznie generuje opis schematu bazy danych w formacie SQL"""
    metadata = MetaData()
    metadata.reflect(bind=engine)
    schema_description = []
    for table in metadata.sorted_tables:
        schema_description.append(f"-- Tabela {table.name}")
        columns = []
        for column in table.columns:
            col_info = f"{column.name} {column.type}"
            if column.primary_key:
                col_info += " PRIMARY KEY"
            if getattr(column, "autoincrement", False):
                col_info += " AUTO_INCREMENT"
            if not column.nullable:
                col_info += " NOT NULL"
            if column.unique:
                col_info += " UNIQUE"
            for fk in column.foreign_keys:
                col_info += f" REFERENCES {fk.column.table.name}({fk.column.name})"
            columns.append(col_info)
        schema_description.append(
            f"CREATE TABLE {table.name} (\n  " + ",\n  ".join(columns) + "\n);\n"
        )
    return "\n".join(schema_description)

def init_db_connection():
    """Inicjalizuje połączenie z bazą MySQL i pobiera schemat"""
    try:
        ssl_args = {'ssl_ca': MYSQL_CONFIG['ssl_ca']} if MYSQL_CONFIG.get('ssl_ca') else {}
        
        engine = sqlalchemy.create_engine(
            sqlalchemy.engine.url.URL.create(
                drivername="mysql+pymysql",
                username=MYSQL_CONFIG['username'],
                password=MYSQL_CONFIG['password'],
                host=MYSQL_CONFIG['host'],
                port=MYSQL_CONFIG['port'],
                database=MYSQL_CONFIG['database']
            ),
            connect_args=ssl_args
        )
        conn = engine.connect()
        db_schema = generate_db_schema(engine)
        return conn, db_schema
    except Exception as e:
        print(f"Błąd połączenia z bazą: {str(e)}")
        return None, None

def get_sql_query(user_prompt: str, db_schema: str) -> str:
    """Generuje zapytanie SQL przy użyciu modelu LLM"""
    prompt = f"""
Na podstawie poniższego schematu bazy danych wygeneruj tylko jedno, poprawne zapytanie mySQL odpowiadające poleceniu użytkownika.
Zwróć wyłącznie zapytanie mySQL, bez żadnych wyjaśnień.
Jeśli polecenie nie dotyczy mySQL, odpowiedz: "Polecam skorzystać z innego ChatBota".

Schemat bazy:
{db_schema}

Polecenie użytkownika:
{user_prompt}
"""
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": True
    }

    full_response = []
    try:
        with requests.post(OLLAMA_URL, json=payload, stream=True) as response:
            response.raise_for_status()

            print("Generuję odpowiedź...\n")
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line.decode('utf-8'))
                    print(chunk['response'], end='', flush=True)
                    full_response.append(chunk['response'])

    except requests.exceptions.RequestException as e:
        return f"Błąd połączenia: {str(e)}"

    return ''.join(full_response).strip()

def execute_sql_query(conn, sql_query: str):
    """Wykonuje zapytanie SQL i zwraca wyniki"""
    try:
        result = conn.execute(text(sql_query))

        if sql_query.strip().upper().startswith('SELECT'):
            return [dict(row) for row in result.mappings()]
        else:
            conn.commit()
            return f"Operacja wykonana pomyślnie. Liczba zmienionych wierszy: {result.rowcount}"

    except Exception as e:
        return f"Błąd wykonania zapytania: {str(e)}"

if __name__ == "__main__":
    # Inicjalizacja połączenia z bazą i pobranie schematu
    db_connection, DB_SCHEMA = init_db_connection()
    if not db_connection or not DB_SCHEMA:
        exit()

    # WYSWIETLANIE SCHEMATU BAZY DANYCH
    #print("\nWygenerowany schemat bazy:\n")
    #print(DB_SCHEMA)

    try:
        # Pobranie polecenia od użytkownika
        user_input = input("\nPodaj polecenie: ")

        # Generowanie zapytania SQL
        generated_sql = get_sql_query(user_input, DB_SCHEMA)

        if not generated_sql or "Polecam skorzystać" in generated_sql:
            exit()
        else:
            # Wykonanie zapytania
            print("\n\nWygenerowane SQL:")
            print(generated_sql)

            result = execute_sql_query(db_connection, generated_sql)

            # Prezentacja wyników
            print("\nWynik wykonania:")
            if isinstance(result, list):
                if len(result) > 0:
                    for row in result:
                        print(row)
                else:
                    print("Brak wyników")
            else:
                print(result)

    finally:
        db_connection.close()
        print("\n\nPołączenie z bazą zostało zamknięte.")
