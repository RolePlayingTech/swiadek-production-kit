# Hybryda: Google Flow + Narrative Motion Kit

Ten toolkit łączy dwie warstwy wizualne. Nie zastępuje repozytorium motion graphics — korzysta z niego jako silnika B-Roll dla map, wykresów i chronologii.

## Repozytoria

| Rola | Repo |
|------|------|
| A-Roll (Świadek, duety, lip-sync PL) | ten toolkit + Google Flow (Chrome CDP) |
| B-Roll dokumentalny / kartografia | [narrative-motion-kit](https://github.com/RolePlayingTech/narrative-motion-kit) (lokalnie często `../motion-lib`) |
| Skills dla agentów (starszy pakiet) | [documentary-film-skills](https://github.com/RolePlayingTech/documentary-film-skills) |

## Kiedy używać której warstwy

- **Flow Omni** — żywa postać mówi do kamery; potrzebujesz lip-sync i emocji.
- **Narrative Motion Kit (`theme: chronicle`)** — fakty, powierzchnie, granice, procesy, dokumenty. Zero „halucynowanych” granic politycznych; autentyczne TopoJSON/GeoJSON.
- **Flow Text-to-Video (B-Roll nastrojowy)** — atmosfera bez mówiącej postaci, gdy nie potrzebujesz naukowej kartografii.

## Przepływ hybrydowy

1. Napisz `script.json` z naprzemiennymi `aroll` / `broll`.
2. Wygeneruj lektora B-Roll: `python tools/synthesize_broll.py --project …`
3. Zmierzone czasy z `audio/measured.json` przekaż do projektu motion-lib (`beats[].at` muszą trafiać w realny waveform).
4. W `motion-lib` utwórz projekt (`npm run new:project`), ustaw `theme: "chronicle"`, zaimplementuj plansze, wyrenderuj draft/final.
5. A-Roll produkuj w Flow z kotwicami Start Frame (`generate_aroll_scene.py`).
6. Złóż master w FFmpeg: A-Roll z natywnym audio Flow + B-Roll z lektorem; muzyka ze sidechain duckingiem.

## Ścieżka lokalna

Ustaw w `.env`:

```bash
MOTION_LIB_PATH=../motion-lib
```

Kluczowe dokumenty motion-lib:

- `AGENTS.md`
- `docs/HISTORY_STYLE.md` (preset `chronicle`)
- `docs/HISTORICAL_MAPS.md`
- `docs/AGENT_PLAYBOOK.md`
- `prompts/CREATE_VIDEO.md`

## Zasada dźwięku (nie zmienia się)

- Na A-Roll **nigdy** nie nakładaj ElevenLabs.
- Na B-Roll mówi lektor (Piotr v3); ambient z wideo ~8%.
