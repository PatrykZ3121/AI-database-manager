import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

DB_SCHEMA = """
-- Tabela użytkownicy
CREATE TABLE uzytkownicy (
    id INT PRIMARY KEY AUTO_INCREMENT,
    imie VARCHAR(50) NOT NULL,
    nazwisko VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    data_rejestracji TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Tabela mieszkania
CREATE TABLE mieszkania (
    id INT PRIMARY KEY AUTO_INCREMENT,
    adres VARCHAR(255) NOT NULL,
    powierzchnia DECIMAL(6,2),
    liczba_pokoi INT,
    uzytkownik_id INT NOT NULL,
    FOREIGN KEY (uzytkownik_id) REFERENCES uzytkownicy(id)
        ON DELETE CASCADE
) ENGINE=InnoDB;
"""
SQL_TYPE = "mySQL"

def get_sql_query(user_prompt: str) -> str:
    prompt = f"""
Na podstawie poniższego schematu bazy danych wygeneruj tylko jedno, poprawne zapytanie {SQL_TYPE} odpowiadające poleceniu użytkownika. 
Zwróć wyłącznie zapytanie {SQL_TYPE}, bez żadnych wyjaśnień. 
Jeśli polecenie nie dotyczy {SQL_TYPE}, odpowiedz: "Polecam skorzystać z innego ChatBota".

Schemat bazy:
{DB_SCHEMA}

Polecenie użytkownika:
{user_prompt}
"""
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": True  # Włączamy strumieniowanie
    }
    
    full_response = []
    try:
        with requests.post(OLLAMA_URL, json=payload, stream=True) as response:
            response.raise_for_status()
            
            print("Generuję odpowiedź...\n")
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line.decode('utf-8'))
                    print(chunk['response'], end='', flush=True)  # Wyświetl na bieżąco
                    full_response.append(chunk['response'])
                    
    except requests.exceptions.RequestException as e:
        return f"Błąd połączenia: {str(e)}"
    
    return '\n'.join(full_response)

if __name__ == "__main__":
    user_input = input("Podaj polecenie: ")
    print()
    final_sql = get_sql_query(user_input)
