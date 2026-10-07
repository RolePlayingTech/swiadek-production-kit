# Układ katalogu projektu filmowego

```text
my-film/
  script.json          # kanoniczny scenariusz (aroll / broll)
  anchors/             # Start Frame 16:9 (kotwice postaci)
  raw/                 # surowe MP4 z Google Flow
  audio/               # lektor ElevenLabs + measured.json
  assembled/           # zmontowane sceny przed masterem
  qc/                  # raporty Whisper / klatki / screenshoty
  prompts/             # opcjonalne pliki promptów
  SCENARIUSZ.md        # wersja czytelna dla człowieka
  STAN_PRODUKCJI.md    # status bramek QC
```

Media nie trafiają do tego repozytorium toolkitowego — trzymaj je lokalnie w katalogu projektu.
