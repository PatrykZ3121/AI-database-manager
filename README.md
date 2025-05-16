# SQL ChatBot z LLM i MySQL

Projekt umożliwia generowanie i wykonywanie zapytań SQL do bazy MySQL na podstawie poleceń użytkownika, wykorzystując lokalny model LLM (np. Llama 3 przez Ollama).

## Funkcjonalności

- Automatyczne pobieranie i opisywanie schematu bazy danych.
- Generowanie zapytań SQL na podstawie poleceń użytkownika w języku polskim.
- Wykonywanie zapytań SELECT, INSERT, UPDATE, DELETE i prezentacja wyników.
- Bezpieczne połączenie z bazą MySQL (obsługa SSL).
- Integracja z lokalnym serwerem Ollama (np. Llama 3).

## Wymagania

- Python 3.8+
- MySQL (lub MariaDB)
- [Ollama](https://ollama.com/) (np. model llama3)
- Plik `config_secret.json` z danymi dostępowymi do bazy
- Zainstalowane biblioteki Python:
  - `sqlalchemy`
  - `pymysql`
  - `requests`

## Instalacja

1. **Klonuj repozytorium**


2. **Zainstaluj wymagane biblioteki:**
pip install sqlalchemy pymysql requests


3. **Przygotuj plik konfiguracyjny:**

Utwórz plik `config_secret.json` w katalogu głównym projektu:
{
"DB_HOST": "adres_bazy",
"DB_PORT": 3306,
"DB_USER": "nazwa_uzytkownika",
"DB_PASSWORD": "haslo",
"DB_NAME": "nazwa_bazy",
"SSL_CA_PATH": "/sciezka/do/cacert.pem"
}



4. **Pobierz Ollama, a następnie w terminalu zainstaluj i uruchom llama3:**
ollama pull llama3
ollama run llama3


## Uruchom aplikację

