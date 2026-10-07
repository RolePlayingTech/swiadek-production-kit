# Żelazny Schemat Produkcyjny Filmów: Świadek Dziejów (Google Flow)

> **Oficjalny, obowiązujący schemat produkcji dla każdej sceny z postacią Świadka Dziejów.**
> Aktualizowany na bieżąco, aby zapewnić powtarzalność, spójność postaci i bezbłędną jakość.

---

## 1. Architektura Środowiska

- **Profil Chrome:** ustawiany przez `CHROME_PROFILE` w `.env` (domyślnie `Profile 60`).
- **Subskrypcja:** konto Google Flow z aktywnym planem (np. Ultra).
- **Połączenie:** CDP `http://127.0.0.1:9222` utrzymywane w tle przez `tools/keep_chrome.py`.
- **Narzędzia analityczne (QA):** `ffmpeg`, `ffprobe`, `cv2` (OpenCV) zainstalowane i aktywne lokalnie.

---

## 2. Standardowa Procedura Produkcyjna (SOP) – Krok po Kroku

### KROK 1: Generowanie zdjęcia bazowego (Nano Banana Pro)
1. **Pigułka ustawień w dolnym pasku:**
   - Przełączenie na zakładkę **`Image`** (`button.flow_tab_slider_trigger:has-text('Image')`).
   - Format: **`16:9`** (lub `9:16` dla Shorts).
   - Model: **`Nano Banana Pro`** (najlepszy model graficzny).
   - Warianty: `x1`.
2. **Dołączenie referencji:**
   - Przycisk `+` w polu promptu -> wybór lokalnego pliku referencyjnego `swiadek_dziejow.jpg` (portret kotwiczący; nie jest częścią tego repo).
3. **Prompt sceny:**
   - Opis otoczenia historycznego, oświetlenia, stroju (np. lniana koszula, kaszkiet, rekwizyty).
4. **Zatwierdzenie:**
   - Kliknięcie `arrow_forward` i wygenerowanie klatki (ok. 10–15s).

---

### KROK 2: Weryfikacja jakości wygenerowanego zdjęcia
1. Otwarcie wygenerowanego zdjęcia na płótnie i pobranie pliku do katalogu projektu (`scena_X_baza.png`).
2. **Checklist jakości:**
   - [ ] Twarz: czy zachowano rysy i tożsamość Świadka Dziejów?
   - [ ] Strój i rekwizyty: czy są zgodne z epoką i promptem?
   - [ ] Tło: brak zniekształceń, właściwa perspektywa.
3. Jeśli kadr jest poprawny – przechodzimy do KROKU 3. Jeśli nie – drobna korekta promptu i regeneracja.

---

### Krok 2: Animacja kadru wideo (Video via Frames)
1. Pigułka ustawień -> Zakładka `Video` -> Tryb **`Frames`** (`button:has-text('Frames')`).
2. Format: `16:9`, warianty: `x1`, Model: **`Omni 1.1 Flash`**, Czas: **`10s`**.
3. Kliknięcie przycisku **`Start`** (Start Frame) w polu promptu.
4. **BARDZO WAŻNE (Wybór klatki w oknie dialogowym):**
   - Okno wyboru mediów domyślnie podświetla pierwszą miniaturę (stary plik `swiadek_dziejow.jpg` przy biurku).
   - **Należy bezwzględnie kliknąć na liście nowo wygenerowane zdjęcie bazowe** (np. `Man standing in Castle Square`), aby podgląd po prawej stronie zmienił się na nowe zdjęcie.
   - Dopiero po kliknięciu właściwego zdjęcia naciskamy **`Add to Prompt`**.
5. Wpisanie promptu animacji i mimiki (np. spojrzenie w kamerę, uśmiech, gest powitania ręką, wypowiedzenie kwestii).
6. Uruchomienie generowania (czas: ok. 60–75s).
7. Pobranie gotowego pliku `.mp4` przez `expect_download`.
8. **Automatyczna weryfikacja klatki 0 (t=0s):** natychmiastowe sprawdzenie `frame_0`, czy wideo na 100% zaczyna się od nowego kadru, a nie od zdjęcia referencyjnego przy biurku.

---

### KROK 4: Pobranie i automatyczna kontrola jakości (QA Audiowizualna)
1. **Pobranie:** Zapisanie pliku `.mp4` w katalogu projektu (`scena_X.mp4`) przez Playwright `expect_download`.
2. **Analiza obrazu (Ekstrakcja klatek):**
   - Za pomocą skryptu Python (`cv2` / `ffmpeg`) wyciągamy klatki z początku (np. 1.0s), środka (5.0s) i końca (9.0s) filmu.
   - Weryfikacja: czy postać nie deformuje się w trakcie ruchu, czy mimika jest naturalna.
3. **Analiza dźwięku (Audio Track):**
   - Sprawdzenie metadanych przez `ffprobe`: czy wideo posiada ścieżkę dźwiękową, jaka jest liczba kanałów, głośność i czy nie ma zakłóceń.
4. **Zatwierdzenie ujęcia:** Klip jest gotowy do montażu całościowego.

---

## 3. Precyzyjne selektory DOM do szybkiej nawigacji

```python
# Pigułka trybu
mode_pill = page.locator("button:has-text('Video'), button:has-text('Image'), div:has-text('720p')").last

# Zakładki nadrzędne
img_tab = page.locator("button.flow_tab_slider_trigger:has-text('Image')").first
video_tab = page.locator("button.flow_tab_slider_trigger:has-text('Video')").first

# Podtryby wideo
frames_mode = page.locator("button:has-text('Frames')").first

# Formaty i czasy
btn_169 = page.locator("button:has-text('16:9')").first
btn_10s = page.locator("button:has-text('10s')").first
btn_x1 = page.locator("button:has-text('x1'), text='x1'").first

# Modele
model_dropdown = page.locator("button:has-text('Omni'), button:has-text('Veo'), button:has-text('Banana')").first

# Pasek promptu i akcje
prompt_input = page.locator("div[contenteditable='true']").first
submit_btn = page.locator("button:has-text('arrow_forward')").first
download_btn = page.locator("button:has-text('download'), [aria-label*='Download']").first
```
