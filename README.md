# 🎉 Group Chat Wrapped

Generuj zabawne statystyki "Wrapped" z eksportu Messengera Facebook!

## ✨ Funkcje

Aplikacja analizuje eksport z Facebook Messenger i generuje interaktywną prezentację HTML z kategoriami:

### 🏆 Kategorie

| Emoji | Nazwa | Opis |
|-------|-------|------|
| 🦉 | **Nocny Marek** | Najwięcej wiadomości w nocy (00:00 - 05:00) |
| 🔥 | **Dzień Apokalipsy** | Najbardziej intensywny dzień w historii grupy |
| 🚪 | **Syn Marnotrawny** | Powrót po najdłuższej przerwie |
| 👑 | **Król Spamu** | Najwięcej wiadomości ogółem (Top 5) |
| ⌨️ | **Maszyna do Pisania** | Najdłuższy ciąg wiadomości pod rząd |
| 📜 | **Poeta** | Najdłuższa pojedyncza wiadomość |
| 📚 | **Słownik Grupy** | Najczęściej używane słowa (Top 10) |
| 👻 | **Duch** | Najmniej aktywny uczestnik |
| 🎬 | **Reżyser** | Najczęściej zaczyna rozmowy |
| 🚪 | **Zamykacz** | Najczęściej kończy rozmowy |
| ❤️ | **Reakcjonista** | Rozdał najwięcej reakcji |
| ⭐ | **Celebryta** | Otrzymał najwięcej reakcji |
| 📸 | **Paparazzo** | Wysłał najwięcej zdjęć |
| 🤡 | **Śmieszek** | Wysłał najwięcej GIFów i naklejek |
| 🔍 | **Detektyw** | Zadał najwięcej pytań |
| 🔗 | **Linkomaniak** | Udostępnił najwięcej linków |
| 😎 | **Emoji Master** | Używa najwięcej emoji |
| 📝 | **Pisarz** | Najdłuższe średnie wiadomości |
| ⏰ | **Godzina Szczytu** | Najbardziej aktywna pora dnia |
| 📊 | **Podsumowanie** | Ogólne statystyki grupy |

## 🚀 Instalacja

```bash
# Sklonuj repozytorium
git clone https://github.com/yourusername/groupchat-wrapped.git
cd groupchat-wrapped

# Zainstaluj zależności
pip install -e .
```

## 📖 Użycie

### 1. Pobierz eksport z Facebooka

1. Idź do **Ustawienia i prywatność** → **Ustawienia** → **Twoje informacje na Facebooku**
2. Kliknij **Pobierz swoje dane**
3. Wybierz **Wiadomości** i format **JSON**
4. Pobierz i rozpakuj archiwum

### 2. Uruchom aplikację

```bash
# Z folderu konwersacji
groupchat-wrapped /path/to/facebook-export/messages/inbox/nazwa_grupy/

# Lub z konkretnego pliku
groupchat-wrapped /path/to/message_1.json

# Zapisz do konkretnego pliku
groupchat-wrapped /path/to/chat/ -o moje_wrapped.html

# Bez automatycznego otwierania w przeglądarce
groupchat-wrapped /path/to/chat/ --no-open
```

### 3. Ciesz się prezentacją!

Wygenerowany plik HTML zawiera:
- 🎵 Muzykę w tle
- 🎨 Animowane slajdy
- ⌨️ Nawigację klawiaturą (strzałki, spacja)
- 📱 Obsługę gestów na urządzeniach mobilnych
- 🎊 Konfetti na końcu!

## 🛠️ Wymagania

- Python 3.10+
- click
- jinja2

## 📁 Struktura projektu

```
groupchat-wrapped/
├── groupchat_wrapped/
│   ├── __init__.py
│   ├── cli.py          # Interfejs CLI
│   ├── parser.py       # Parser eksportu Facebook
│   ├── analyzer.py     # Analizator statystyk
│   └── generator.py    # Generator HTML
├── pyproject.toml
├── requirements.txt
└── README.md
```

## 🤝 Wkład

Pull requesty są mile widziane! Możesz dodawać nowe kategorie, poprawiać styl HTML lub rozszerzać analizę.

## 📄 Licencja

MIT License - używaj jak chcesz!

## 🎊 Powodzenia!

Stwórz swoje Group Chat Wrapped i podziel się z przyjaciółmi! 🎉
