# SQL ChatBot z LLM i MySQL

Projekt wykonany w języku python umożliwia generowanie i wykonywanie zapytań SQL do bazy MySQL na podstawie poleceń użytkownika, wykorzystując lokalny model LLM (np. Llama 3 od Ollama).

## Funkcjonalności

- Automatyczne pobieranie i opisywanie schematu bazy danych.
- Generowanie zapytań SQL na podstawie poleceń użytkownika w języku polskim.
- Wykonywanie zapytań SELECT, INSERT, UPDATE, DELETE i prezentacja wyników.
- Bezpieczne połączenie z bazą MySQL (obsługa SSL).
- Integracja z lokalnym serwerem Ollama (np. Llama 3).

## Wymagania

- Python 3.8+
- Po uruchomieniu aplikacja poprosi użytkownika o wpisanie polecenia (promptu) w języku polskim. Następnie:

Jeśli polecenie dotyczy operacji na bazie danych (np. zapytania SELECT, INSERT, UPDATE, DELETE lub innych działań związanych z bazą MySQL):

Aplikacja automatycznie wygeneruje odpowiedni kod SQL przy pomocy lokalnego modelu językowego (LLM).

Wygenerowane zapytanie zostanie wykonane na wskazanej bazie danych.

Wynik działania zostanie wyświetlony użytkownikowi w czytelnej formie.

Jeśli polecenie nie dotyczy bazy danych (np. jest pytaniem ogólnym lub niezwiązanym z SQL):

Aplikacja wyświetli komunikat:
Polecam skorzystać z innego ChatBota.

Dzięki temu użytkownik może w prosty sposób zarządzać bazą danych za pomocą naturalnego języka, bez konieczności ręcznego pisania zapytań SQL.
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

Po uruchomieniu aplikacja poprosi użytkownika o wpisanie polecenia (promptu) w języku polskim. Następnie:
Jeśli polecenie dotyczy operacji na bazie danych (np. zapytania SELECT, INSERT, UPDATE, DELETE lub innych działań związanych z bazą MySQL):
Aplikacja automatycznie wygeneruje odpowiedni kod SQL przy pomocy lokalnego modelu językowego (LLM).
Wygenerowane zapytanie zostanie wykonane na wskazanej bazie danych.
Wynik działania zostanie wyświetlony użytkownikowi w czytelnej formie.
Jeśli polecenie nie dotyczy bazy danych (np. jest pytaniem ogólnym lub niezwiązanym z SQL):
Aplikacja wyświetli komunikat:
Polecam skorzystać z innego ChatBota.
Dzięki temu użytkownik może w prosty sposób zarządzać bazą danych za pomocą naturalnego języka, bez konieczności ręcznego pisania zapytań SQL.

