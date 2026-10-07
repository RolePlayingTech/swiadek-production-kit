# Instrukcje dla agentów AI

Budujesz gotowy film dokumentalny w formacie Świadek Dziejów (lub pokrewnym), bez psucia równoległych sesji produkcyjnych.

## Najpierw przeczytaj

1. `README.md`
2. `docs/GEMINI.md` — żelazne zasady audio/kotwic/QC
3. `docs/INSTRUKCJA_PRODUKCJI_FILMOW.md` — książka kucharska
4. `docs/METODOLOGIA_SCENARIUSZA_DOKUMENTALNEGO.md` — dramaturgia
5. `docs/GOOGLE_FLOW_GUIDE.md` — SOP Flow + selektory
6. `docs/HYBRID_MOTION_LIB.md` — kiedy sięgać po narrative-motion-kit

## Nie ruszaj aktywnej produkcji

- Nie zabijaj Chrome na porcie CDP `9222`, jeśli ktoś już generuje klipy.
- Nie nadpisuj cudzych `raw/`, `qc/`, `script.json` w aktywnym projekcie bez prośby użytkownika.
- Nie commituj `.env`, kluczy API, cookies ani portretów postaci.

## Niezmienniki formatu

- A-Roll: natywne audio Flow + kotwica Start Frame. Max ~15–18 słów / 10 s.
- B-Roll: lektor ElevenLabs; multi-shot zamiast pętli wideo.
- Liczby i daty w dialogach — tylko słownie.
- Nazwiska „prominent people” omijaj w promptach Flow; fakty w lektorze B-Roll.
- Whisper QC na czystym dialogu; karaoke ASS z offsetem ok. −90 ms.

## Motion graphics

Dla map historycznych i plansz faktograficznych używaj siblinga [narrative-motion-kit](https://github.com/RolePlayingTech/narrative-motion-kit) ze stylem `chronicle`. Nie rysuj granic „z pamięci modelu”.

## Po zakończeniu pracy

Zwróć ścieżki do masterów, raportów QC i listę znanych ograniczeń. Nie twierdź, że film jest gotowy bez sprawdzenia pliku wynikowego.
