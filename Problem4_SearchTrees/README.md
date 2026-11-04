# Problemi 4: Search Trees

Një **search tree** paraqet gjendjen fillestare si rrënjë. Çdo degë përfaqëson një veprim të vlefshëm dhe çdo nyje fëmijë gjendjen pas atij veprimi. Këtu ndërtojmë pemë me **Breadth-First Search (BFS)**: një radhë FIFO zgjeron gjendjet sipas thellësisë. Për secilën nyje ruajmë gjendjen, indeksin e prindit, veprimin dhe thellësinë. Duke ndjekur prindërit mbrapsht gjejmë rrugën deri te qëllimi.

Gjendjet e përsëritura nuk shtohen përsëri dhe nyjet qëllim nuk zgjerohen. Pra, diagrami është një **pemë BFS e gjendjeve të zbuluara**, jo pema e plotë e të gjitha rrugëve: disa degë që çojnë te një gjendje e vizituar mungojnë. Kjo shmang ciklet dhe ruan rrugën më të shkurtër në numër veprimesh. Kufiri i thellësisë kufizon vetëm paraqitjen dhe kërkimin; nëse qëllimi nuk gjendet brenda tij, kjo nuk provon pamundësi.

## 1. 8-Puzzle

- **Gjendja:** nëntë vlera në rend rreshtash; `0` është vendi bosh.
- **Fillimi:** `1 2 3 / 4 5 6 / 0 7 8`.
- **Veprimet:** lëvizja e vendit bosh lart, poshtë, majtas ose djathtas, kur lëvizja mbetet brenda tabelës.
- **Qëllimi:** `1 2 3 / 4 5 6 / 7 8 0`.
- Në këtë shembull, rruga më e shkurtër ka **2 lëvizje**: bosh djathtas, pastaj përsëri djathtas.

Në diagram, `_` është vendi bosh dhe `/` ndan rreshtat. Shembulli është zgjedhur që pema të jetë e lehtë për t'u lexuar; nuk pretendon të paraqesë të gjitha konfigurimet e mundshme të 8-Puzzle.

## 2. Missionaries and Cannibals

- **Gjendja:** `(M, C, B)`, ku `M` dhe `C` janë numrat në bregun e majtë dhe `B` është ana e varkës (`0` majtas, `1` djathtas). Në anën tjetër janë `3-M` dhe `3-C`.
- **Fillimi:** `(3, 3, 0)`; **qëllimi:** `(0, 0, 1)`.
- **Veprimi:** varka transporton 1 ose 2 persona nga ana ku ndodhet në anën tjetër.
- **Kufizimi:** në asnjërin breg kanibalët nuk mund të jenë më shumë se misionarët, përveç kur aty nuk ka misionarë. Numrat e njerëzve duhet të jenë ndërmjet 0 dhe 3.
- BFS gjen një rrugë me **11 kalime**. Mund ta shikosh çdo kalim dhe gjendje në ndërfaqe ose në daljen e programit.

## 3. Rotating Workforce Scheduling

Përshkrimi i detyrës nuk përcakton numrin e punëtorëve, ditëve apo kufizimet, ndaj përdorim këtë shembull të thjeshtë:

- **Punëtorët:** A, B, C dhe D; **ditët:** 3.
- **Gjendja:** lista e çifteve të caktuara deri tani; fillimisht lista është bosh.
- **Veprimi:** caktohen saktësisht dy punëtorë në ditën tjetër.
- **Kufizimi i rotacionit:** askush nuk punon dy ditë radhazi.
- **Qëllimi:** të jenë caktuar punëtorët për të tri ditët. Për shembull: `AB → CD → AB`.

Për këtë model të vogël, çdo çift përcakton çiftin plotësues për ditën pasuese. Ky është një ilustrim i rotacionit, jo model i plotë i një orari real pune.

## Ekzekutimi

Nga dosja kryesore e projektit:

```bash
python Problem4_SearchTrees/search_trees.py puzzle --depth 4
python Problem4_SearchTrees/search_trees.py missionaries --depth 12
python Problem4_SearchTrees/search_trees.py workforce --depth 3
python -m unittest discover -s Problem4_SearchTrees -v
python -m pip install -r requirements.txt
python -m streamlit run Problem4_SearchTrees/app.py
```

Në ndërfaqe zgjedh problemin dhe thellësinë, sheh rrugën e gjetur dhe pemën. Për pemë mbi 150 nyje shfaqet lista e nyjeve në vend të diagramit, që pamja të mbetet e lexueshme.
