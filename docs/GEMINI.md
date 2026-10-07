# ŻELAZNE ZASADY PRODUKCJI FILMÓW DOKUMENTALNYCH

## 1. BEZWZGLĘDNY PODZIAŁ AUDIO: A-ROLL (ŚWIADEK) vs B-ROLL (LEKTOR)

### Sceny A-Roll (Sceny nieparzyste: Świadek Dziejów, bohaterowie rozmawiający):
1. **Źródło dźwięku**: 100% natywne audio wygenerowane przez model wideo Google Flow (Omni 1.1 Flash) z pliku raw.mp4.
2. **Kategoryczny zakaz**: **NIGDY NIE NAKŁADAJ LEKTORA Z ELEVENLABS NA SCENY ZE ŚWIADKIEM!**
   - Świadek Dziejów mówi SAM swoim własnym głosem i z idealnym lip-syncem.
   - W scenach dialogowych słychać wyłącznie żywe postacie ze sceny.
3. **Miksowanie audio A-Roll**:
   - Pobieramy ścieżkę dźwiękową z wideo ([0:a]).
   - Normalizujemy do standardu emisyjnego: loudnorm=I=-16:TP=-1.5:LRA=7.
   - Żadnych nakładek dubbingowych z ElevenLabs na scenach A-Roll!

### Sceny B-Roll (Sceny parzyste: przebitki, krajobrazy, architektura, detale bez postaci mówiącej):
1. **Źródło dźwięku**: Lektor wygenerowany w ElevenLabs z **oficjalnym, stałym profilem głosu Piotr** (Voice ID: `gFl0NeqphJUaoBLtWrqM`, plik konfiguracyjny `elevenlabs_config.py`).
2. **Model i ekspresja**: Bezwzględny obowiązek stosowania modelu **Eleven v3 (`eleven_v3`)** z naturalnymi tagami ekspresji emocjonalnej (np. `[chuckles]`, `[sighs]`, `[thoughtful]`, `[ironic]`, `[intrigued]`, `[pause]`), aby lektor brzmiał dynamicznie, zróżnicowanie i żywo opowiadał fakty historyczne.
3. **Miks**: Lektor (znormalizowany do -16 LUFS) + cichy ambient z wideo (volume=0.08).

---

## 2. WYRAŹNA DYNAMIKA DLA WIDZA
- **Gdy w kadrze jest Świadek Dziejów**: Mówi nasz bohater / postacie na scenie.
- **Gdy w kadrze jest ujęcie B-Roll**: Mówi lektor wyjaśniający szczegóły.
- Pomiędzy scenami płynie jednolity, nieprzerwany podkład muzyczny z sidechain duckingiem (sidechaincompress).

---

## 3. ZASADA MULTI-SHOT DLA B-ROLL (ZAKAZ PĘTLI WIDEO)
1. **Całkowity zakaz zapętlania wideo (`-stream_loop`)**: Nigdy nie wolno zapętlać pojedynczego 10-sekundowego ujęcia B-roll pod dłuższy głos lektora. Zapętlony ruch kamery i powtarzające się motywy wyglądają sztucznie.
2. **Sekwencja wieloujęciowa dopasowana do długości narracji**:
   - **Gdy lektor trwa 10–18 s (Sekwencja dwuujęciowa)**: Montujemy scenę B-roll z **dwóch unikalnych ujęć**:
     - **Shot A** (np. plan ogólny / panorama / wprowadzenie): trwa 6–9 sekund.
     - **Shot B** (np. detal, praca maszyny, plan bliski): trwa 6–9 sekund.
   - **Gdy lektor trwa > 18 s (Sekwencja trójujęciowa: Shot A + Shot B + Shot C)**:
     - W przypadku dłuższej narracji (19–27 s) generujemy **dodatkowe trzecie ujęcie (Shot C)**, dzieląc scenę na 3 dynamiczne cięcia (np. po 7–9 sekund na ujęcie).
     - Kategoryczny zakaz ucinania obrazu przed końcem głosu lektora ani sztucznego zamrażania klatek.
   - Wszystkie części montujemy bez cięcia audio lektora, przycinając łączne wideo dokładnie do `t = lektor_dur + 0.8s`.

---

## 4. BUDŻET SŁÓW DLA SCEN A-ROLL (MAX 15–18 SŁÓW / 10s)
1. **Rygor czasowy modelu**: Model wideo generuje klipy o długości 10.0 sekund. Jeśli kwestia mówiona ma > 20 słów, mowa zostaje bezwzględnie ucięta w połowie zdania na granicy 10.00s.
2. **Maksymalny limit**: Każda kwestia mówiona (Świadka lub Bohatera) w 10-sekundowym ujęciu musi liczyć **maksymalnie 15–18 słów** w języku polskim.
3. **Naturalny oddech**: Wypowiedź musi zakończyć się najpóźniej w 7,5–8,5 sekundy klipu, aby zostawić minimum 1,5 sekundy naturalnej pauzy / oddechu aktora przed montażowym cięciem sceny.

---

## 5. SPÓJNOŚĆ WIZUALNA POSTACI (KOTWICA „POCZĄTEK”)
1. **Żelazna tożsamość Świadka Dziejów**:
   - Świadek Dziejów jest osią narracyjną całego filmu. Widz musi natychmiast rozpoznawać tę samą charyzmatyczną postać: te same rysy twarzy, szpakowaty zarost, fryzurę, skupione spojrzenie oraz charakterystyczną, prostą lnianą koszulę.
2. **Kategoryczny zakaz generowania A-Roll z samego tekstu**:
   - Sam prompt tekstowy powoduje losowy dryf twarzy, wieku, ubioru i stylu.
3. **Bezwzględny obowiązek kotwicy referencyjnej (`Początek` / Start Frame)**:
   - **Świadek Dziejów**: Każde ujęcie ze Świadkiem musi mieć bezwzględnie przypiętą klatkę referencyjną (`Początek`) z zatwierdzonego pliku kotwicy (`swiadek_dziejow.jpg` lub dedykowanej kotwicy scenicznej np. `cw_s01_swiadek_metronome.jpg`).
   - **Sceny w duecie (Dialogi)**: Kadr startowy musi przedstawiać obu rozmówców (Świadek + postać drugoplanowa) w tej samej fizycznej przestrzeni. Zakaz łączenia postaci z oddzielnych, niespójnych kadrów!
   - Każde wygenerowane ujęcie, w którym twarz Świadka odbiega od referencji, zostaje natychmiast bezwzględnie odrzucone i skierowane do ponownego renderu.

---

## 6. PRECYZYJNA SYNCHRONIZACJA NAPISÓW KARAOKE
1. **Transkrypcja na czystym dialogu**: Znaczniki czasu słów (`word_timestamps=True`) w Whisperze wyznaczamy WYŁĄCZNIE na czystej ścieżce dialogowej (przed zmiksowaniem podkładu muzycznego), co eliminuje zakłócenia detekcji głosu (VAD).
2. **Kalibracja wyprzedzenia (Offset)**: Zdarzenia podświetlania słów w formacie ASS karaoke muszą posiadać skalibrowany offset wyprzedzający (-80ms do -100ms), aby oko widza rejestrowało podświetlenie idealnie w momencie wybrzmienia głoski.

---

## 7. MIKSUJĄCY PRIORYTET AUDIO W B-ROLL (ZAKAZ UCIĘĆ LEKTORA)
1. **Lektor jako strumień nadrzędny**: W scenach B-Roll głos lektora z ElevenLabs jest wiodącą ścieżką narracyjną. W filtrze `amix` strumień lektora z dopełnieniem `apad=whole_dur=t_total` MUSI być wejściem pierwszym (`[lektor][ambient]amix=inputs=2:duration=first`).
2. **Kategoryczny zakaz podawania ambientu na wejście pierwsze**: Podanie ambientu jako pierwszego wejścia (`[ambient][lektor]`) przy `duration=first` powoduje przedwczesne obcięcie głosu lektora na granicy długości pojedynczego klipu wideo (zwykle w 10.0s) i grobową ciszę przez pozostałe sekundy sceny.
3. **Ambient w sekwencji Multi-Shot**: Ścieżki ambientowe z ujęć (`shot_a` i `shot_b`) łączymy (`concat`) i dopasowujemy do pełnego czasu `t_total`.

---

## 8. METODOLOGIA SCENARIUSZA DLA AGENTÓW I SCENARZYSTÓW
- Szczegółowy podręcznik reguł dramaturgicznych, limitów słów, wspólnej przestrzeni bohaterów i szablonów JSON/Markdown znajduje się w pliku: [`METODOLOGIA_SCENARIUSZA_DOKUMENTALNEGO.md`](./METODOLOGIA_SCENARIUSZA_DOKUMENTALNEGO.md).
- Każdy scenariusz musi przejść checklistę weryfikacyjną przed przekazaniem do renderowania wideo i syntezy audio.

---

## 9. REŻYSERIA SOUND DESIGNU I FOLEY (WARSTWA KINOWA)
1. **Akcenty przejść (Transitions & Sub-basses)**:
   - Każde kluczowe przejście z A-Roll do B-Roll (lub zmiana aktu) musi posiadać subtelny świst powietrza (*whoosh*) lub głębokie uderzenie niskotonowe (*sub-bass boom*), podkreślające powagę ujawnianego faktu.
2. **Dedykowany foley synchroniczny**:
   - Dźwięki fizyczne widoczne na ekranie (tykanie metronomu, trzask rygla sejfu, stukot klawiszy terminala, praca robota w fabryce) muszą być osadzone w ścieżce audio w punkcie cięcia lub akcji.
3. **Dynamiczny Sidechain Ducking**:
   - Podkład muzyczny nie może być płaski. Gdy mówi Świadek lub Lektor, muzyka obniża się o 5–7 dB (`sidechaincompress`), a w pauzach oddechu (1–2s) delikatnie i organicznie narasta, podbijając emocje.

---

## 10. MOTION DESIGN, PRACA KAMERY I POSTPRODUKCJA
1. **Cyfrowy najazd kamery (Slow Push-In)**:
   - Na kluczowych 10-sekundowych ujęciach A-Roll oraz monumentalnych ujęciach B-Roll stosujemy subtelny, powolny najazd cyfrowy (skalowanie od 1.00 do 1.05–1.07 w czasie trwania ujęcia). Eliminuje to wrażenie martwego, statycznego kadru AI i magnetyzuje wzrok widza.
2. **Belki informacyjne (Lower Thirds) i Karty Aktów**:
   - **Chyrony / Lower Thirds**: Każda nowa postać w duecie otrzymuje minimalistyczną, elegancką belkę (imię, nazwisko, funkcja). Każda zmiana lokacji historycznej otrzymuje znacznik czasu i miejsca (np. *„Genewa, 1963”*, *„Tajpej, 2026”*).
   - **Karty Aktów (Title Cards)**: Przejścia między 5 głównymi aktami są akcentowane 1,5-sekundową minimalistyczną planszą tytułową z mocnym uderzeniem dźwiękowym.
3. **Film Look & 35mm Grain**:
   - Nałożenie subtelnego ziarna taśmy filmowej 35mm i zbalansowanie kontrastu unifikuje wizualnie ujęcia pochodzące z różnych nasion generatywnych, nadając im spójny, organiczny charakter kinowy.

---

## 11. ZŁOTA REGUŁA SCENARIUSZA: ZERO AI-BEŁKOTU (LUDZKI, WCIĄGAJĄCY GŁOS)
1. **Zakaz sztucznych szablonów AI**:
   - Bezwzględny zakaz zwrotów-klisz typu: *„Warto zauważyć, że...”*, *„Stanowi to kluczowy element...”*, *„W obliczu rosnących wyzwań...”*, *„Zarówno X, jak i Y...”*, *„W dobie cyfrowej transformacji...”*, *„Nie tylko... ale również...”*.
2. **Zasada soczystego konkretu (Tactile Storytelling)**:
   - Zamiast ogólników i liczb z encyklopedii – namacalne, plastyczne porównania (np. zamiast *„Superkomputer zużywa gigawaty mocy”* -> *„To pojedyncze pomieszczenie pije tyle prądu, co stotysięczne miasto”*; zamiast *„Wagi modelu są poufne”* -> *„Dwieście gigabajtów liczb na pendrivie w kieszeni marynarki – i masz w ręku technologię wartą miliardy”*).
3. **Żywy, ludzki styl wypowiedzi**:
   - **Świadek Dziejów**: Mówi jak dociekliwy, charyzmatyczny człowiek, nie robot. Rzuca prowokacyjne pytania, używa ironii, zawiesza głos, sprowadza skomplikowaną teorię do prostej, bezkompromisowej prawdy.
   - **Lektor (Piotr v3)**: Opowiada fascynującą historię, buduje tajemnicę, używa tagów ekspresji (`[whispers]`, `[ironic]`, `[chuckles]`, `[pause]`, `[thoughtful]`), intryguje i wciąga widza jak w rasowym thrillerze dokumentalnym.

---

## 12. PROTOKÓŁ WIELOETAPOWEJ WERYFIKACJI (ZERO TOLERANCJI DLA BŁĘDÓW)

Każda produkcja podlega 4-etapowej, bezwzględnej procedurze kontroli jakości (Quality Control Gates):

### Bramka 1: Audyt merytoryczny i dramaturgiczny scenariusza
1. **Fact-Checking (100% prawdy)**: Żadnych halucynacji AI. Każda data, nazwisko, traktat, organizacja i parametr techniczny (np. HBM, EUV, TSMC, SALT, COCOM) muszą być zweryfikowane w wiarygodnych źródłach.
2. **Dramaturgia i humanizacja**: Tekst musi wciągać od pierwszej sekundy, operować paradoksem i zagadką, być wolny od klisz AI i posiadać wyłącznie liczby zapisane słownie.
3. **Rygor czasowy**: Żadna kwestia A-Roll nie może przekraczać 14–16 słów (gwarancja min. 1,5s pauzy przed cięciem).

### Bramka 2: Weryfikacja pobierania z Google Flow
1. **Weryfikacja słów kluczowych (Keyword Guard)**: Przed kliknięciem pobierania skrypt MUSI otworzyć kartę i sprawdzić, czy tekst w oknie szczegółów zawiera minimum **3 unikalne słowa kluczowe** zadanego promptu. Kategoryczny zakaz pobierania kart „w ciemno”!
2. **Kontrola parametrów wideo**: Weryfikacja programowa (cv2/ffprobe): rozdzielczość 1280x720, 24fps, dokładnie 10.00 sekund trwania.

### Bramka 3: Audyt mowy i eliminacji błędów językowych (Whisper STT)
1. **Automatyczny audyt Whisper (PL)**: Każdy wygenerowany klip A-Roll jest natychmiast transkrybowany modelem Whisper.
2. **Kryteria dyskwalifikacji (Re-render)**:
   - Jeśli mowa zostanie ucięta przed końcem zdania -> **RE-RENDER**.
   - Jeśli aktor przekręcił kluczowe słowo lub zaczął bełkotać -> **RE-RENDER**.
   - Jeśli w tle pojawił się niepożądany głos obcy -> **RE-RENDER**.

### Bramka 4: Wizualna inspekcja glitchy (Visual Artifact Hunt)
1. **Ekstrakcja klatek inspekcyjnych**: Automatyczna ekstrakcja klatek w punktach $t = 2.0s$, $t = 5.0s$ i $t = 8.0s$.
2. **Sprawdzane anomalie**:
   - **Twarz i tożsamość**: Czy rysy Świadka odpowiadają kotwicy referencyjnej?
   - **Dłonie i rekwizyty**: Czy dłonie nie mają anomalii (zrośnięte palce, 6 palców), czy rekwizyty (wafer krzemowy, sejf, metronom) nie „pływają” i zachowują stabilną geometrię?
   - W przypadku wykrycia rażącego glitcha ujęcie jest powtarzane z innym seedem.

### Bramka 5: Ostateczny audyt zmontowanego Mastera
1. **Weryfikacja osi czasu**: Kontrola czy nie ma powtórzonych ujęć ani zduplikowanych kwestii na całej długości filmu.
2. **Precyzja napisów Karaoke**: Weryfikacja czy podświetlenie słów wyprzedza foniczny początek głoski o dokładnie **-90ms** i czy tekst wyświetlany na ekranie pochodzi w 100% z kanonicznego scenariusza.


