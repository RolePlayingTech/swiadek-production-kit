# Świadek Dziejów — Production Kit

Toolkit produkcyjny do tworzenia filmów dokumentalnych AI w formacie **Świadek Dziejów**: Google Flow (A-Roll z lip-sync PL), ElevenLabs (lektor B-Roll), Whisper/FFmpeg (QC i montaż) oraz opcjonalnie [Narrative Motion Kit](https://github.com/RolePlayingTech/narrative-motion-kit) (mapy i plansze `chronicle`).

To **nie** jest dump całego warsztatu z mediami. Tu są instrukcje, szablony i skrypty wielokrotnego użytku. Portret postaci, klucze API i surowe klipy zostają lokalnie.

Pokrewne repo: [documentary-film-skills](https://github.com/RolePlayingTech/documentary-film-skills) (skills dla agentów). Ten zestaw uzupełnia je o aktualny **hybrydowy** workflow Flow + motion-lib.

## Architektura

```text
A-Roll (nieparzyste)     → Google Flow Omni + kotwica Start Frame + natywne audio
B-Roll (parzyste)        → lektor ElevenLabs Piotr v3 + (Flow atmos / motion-lib)
Master                   → FFmpeg + sidechain ducking + napisy ASS/SRT
```

Świadek Dziejów mówi **sam** na swoich scenach. Lektora nie nakłada się na mówiącego aktora.

## Wymagania

- Python 3.11+
- Node 22+ (tylko jeśli używasz motion-lib)
- `ffmpeg` / `ffprobe` w `PATH`
- Google Chrome z profilem zalogowanym do Flow (subskrypcja Ultra zalecana)
- Klucz ElevenLabs (lokalnie w `.env`)

```bash
git clone https://github.com/RolePlayingTech/swiadek-production-kit.git
cd swiadek-production-kit
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
npx playwright install chromium   # jeśli potrzebujesz osobnego Chromium; Flow i tak idzie przez CDP
cp .env.example .env              # uzupełnij klucze i profil Chrome
```

## Szybki start

1. Uruchom Chrome z CDP (nie ruszaj sesji, jeśli inny agent już generuje film):

```bash
python tools/keep_chrome.py
```

2. Przygotuj katalog projektu według `templates/project_layout.md` i skopiuj `templates/script.example.json` → `script.json`.

3. Synteza lektora B-Roll:

```bash
python tools/synthesize_broll.py --project path/to/project
```

4. Produkcja jednej sceny A-Roll (Flow musi być otwarte, kotwice wgrane):

```bash
python tools/generate_aroll_scene.py --project path/to/project --scene s01
```

5. Miks B-Roll:

```bash
python tools/mix_broll.py --video shot.mp4 --voice audio/s02.mp3 --out assembled/s02.mp4
```

## Dokumentacja

| Plik | Treść |
|------|--------|
| [docs/GEMINI.md](docs/GEMINI.md) | Żelazne zasady (audio, kotwice, QC, dramaturgia) |
| [docs/INSTRUKCJA_PRODUKCJI_FILMOW.md](docs/INSTRUKCJA_PRODUKCJI_FILMOW.md) | Pełna książka kucharska + FFmpeg |
| [docs/METODOLOGIA_SCENARIUSZA_DOKUMENTALNEGO.md](docs/METODOLOGIA_SCENARIUSZA_DOKUMENTALNEGO.md) | Scenariusz, limity słów, duety |
| [docs/GOOGLE_FLOW_GUIDE.md](docs/GOOGLE_FLOW_GUIDE.md) | SOP Flow + selektory DOM |
| [docs/HYBRID_MOTION_LIB.md](docs/HYBRID_MOTION_LIB.md) | Integracja z narrative-motion-kit |
| [AGENTS.md](AGENTS.md) | Skrót dla agentów AI |

## Narzędzia (`tools/`)

| Skrypt | Rola |
|--------|------|
| `keep_chrome.py` | Chrome + `--remote-debugging-port` na wybranym profilu |
| `flow_connect.py` | Podłączenie Playwright do CDP |
| `generate_aroll_scene.py` | Generacja + pobranie + QC jednej sceny A-Roll |
| `synthesize_broll.py` | ElevenLabs dla wszystkich `kind: broll` |
| `mix_broll.py` | Miks lektor + cichy ambient |
| `qa_utils.py` | ffprobe / klatki OpenCV / Whisper |

## Bezpieczeństwo

- Nigdy nie commituj `.env`, cookies ani plików z kluczami.
- Portret Świadka Dziejów (`swiadek_dziejow.jpg`) **nie jest** częścią tego repo — trzymaj go lokalnie jako kotwicę.
- Jeśli klucz ElevenLabs kiedykolwiek wpadł do lokalnego skryptu w warsztacie, **zrotuj go** w panelu ElevenLabs.

## Licencja

Kod i dokumentacja toolkitowa: MIT (patrz `LICENSE`). Materiały filmowe, głosy, znaki towarowe i wizerunek postaci podlegają osobnym prawom — nie są tu publikowane.
