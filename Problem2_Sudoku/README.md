# Problemi 2: Sudoku Solver

## Përshkrimi dhe modelimi

Sudoku ka 9 × 9 qeliza. Çdo rresht, kolonë dhe kuti 3 × 3 duhet të përmbajë numrat 1–9 nga një herë. Disa numra janë të dhënë dhe nuk ndryshohen. Programi përfshin shembuj **Easy**, **Medium** dhe **Hard**, si dhe lejon hyrjen e një Sudoku tjetër.

- **Variabla:** një qelizë e zbrazët `X[r][c]`.
- **Domeni:** `{1, ..., 9}`, i kufizuar nga numrat tashmë në rreshtin, kolonën dhe kutinë e saj.
- **Gjendja:** një tabelë prej 81 vlerash; `0` tregon qelizë të zbrazët. Në kod ruhet si tuple, me indeks `r * 9 + c`.
- **Gjendja fillestare:** tabela me numrat e dhënë. Një veprim vendos një kandidat të vlefshëm në një qelizë të zbrazët.
- **Qëllimi:** tabela është e plotë, të gjitha kufizimet respektohen dhe numrat fillestarë ruhen.

## Funksioni objektiv

`f(S) = numri i qelizave të zbrazëta + numri i përsëritjeve në rreshta, kolona dhe kuti`.

Për çdo rresht, kolonë ose kuti, përsëritjet llogariten si numri i vlerave të vendosura minus numri i vlerave të ndryshme. Një konflikt mund të numërohet në më shumë se një njësi. Për një tabelë të formuar me shifra 0–9, `f(S) = 0` do të thotë tabelë e plotë dhe pa konflikte. Numrat fillestarë ruhen veçmas nga mënyra si krijohen gjendjet; vetëm qelizat zero ndryshohen.

## Landscape

Nëse ka `e` qeliza të zbrazëta, modeli i thjeshtë para kufizimeve ka `9^e` tabela të plota të mundshme. Për shembujt e përfshirë:

| Niveli | Qeliza bosh `e` | Hapësira naive |
|---|---:|---:|
| Easy | 51 | `9^51` ≈ 10^48.67 |
| Medium | 45 | `9^45` ≈ 10^42.94 |
| Hard | 53 | `9^53` ≈ 10^50.57 |

Këto nuk janë numra zgjidhjesh të vlefshme: shumica e tabelave shkelin kufizimet. Një fqinj mund të përkufizohet si ndryshimi i një qelize jo fikse; vlera `f` e përshkruan sa larg është tabela nga një zgjidhje sipas funksionit objektiv. DFS nuk përdoret këtu: BFS gjeneron vetëm vendosje të vlefshme dhe zgjeron nivelet sipas numrit të qelizave të plotësuara.

`landscape.py` mbush rastësisht qelizat bosh duke ruajtur numrat fillestarë dhe ndryshon një qelizë jo fikse për të krijuar një fqinj. Për Easy, 500 mostra me seed 42 dhanë minimumin 60, maksimumin 94, mesataren 76.68; nga 500 fqinjë, 189 përmirësuan vlerën, 123 nuk e ndryshuan dhe 188 e përkeqësuan. Histogrami i plotë shfaqet nga skripti. Këto janë mostra, jo analiza e plotë e hapësirës.

## BFS dhe kthimi nga degët e dështuara

1. Vendosim tabelën fillestare në një radhë FIFO (`deque`).
2. Heqim gjendjen e parë; nëse është e plotë, ajo është zgjidhja.
3. Zgjedhim qelizën bosh me më pak kandidatë të vlefshëm (MRV), për të zvogëluar degëzimin. Kjo ndryshon zgjedhjen e qelizës, por radha FIFO vazhdon të japë BFS sipas thellësisë.
4. Për çdo kandidat krijojmë një kopje të tabelës dhe e shtojmë në fund të radhës. Nëse nuk ka kandidat, dega hidhet poshtë; kërkimi vazhdon me gjendjet e tjera në radhë.
5. Nëse radha zbrazet, nuk ka zgjidhje. Kufiri i gjendjeve mbron memorien; arritja e tij **nuk** provon pamundësi.

Kjo heqje e degëve të pamundura është kthim konceptual nga zgjedhjet e dështuara. Ndryshe nga backtracking rekurziv klasik (zakonisht DFS), këtu nuk kthehemi nëpër thirrje rekurzive: BFS ruan alternativa të veçanta në radhë. BFS mund të kërkojë shumë memorie për Sudoku të vështira.

## Ekzekutimi

Nga dosja kryesore e projektit:

```bash
python Problem2_Sudoku/sudoku.py --level Easy
python Problem2_Sudoku/sudoku.py --level Medium
python Problem2_Sudoku/sudoku.py --level Hard
python Problem2_Sudoku/landscape.py --level Easy
python -m unittest discover -s Problem2_Sudoku -v
python -m pip install -r requirements.txt
python -m streamlit run Problem2_Sudoku/app.py
```

Në ndërfaqe, seksioni **Modelimi dhe shpjegimi i detyrës** përmbledh kërkesat dhe algoritmin.
Për një Sudoku tjetër, ndrysho tekstin në fushën e tabelës: shkruaj nëntë rreshta me nga nëntë shifra dhe përdor `0` për qelizat bosh. Hyrjet me numra fillestarë në konflikt refuzohen.

Me shembujt aktualë, BFS viziton përkatësisht 52, 46 dhe 162 gjendje. Këto shifra varen nga përzgjedhja e qelizës dhe kandidatëve; emërtimet e niveleve nuk janë një matje universale e vështirësisë.
