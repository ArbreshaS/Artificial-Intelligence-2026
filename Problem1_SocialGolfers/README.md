# Problemi 1: Social Golfers

## Përgjigjja

Për 32 lojtarë, të ndarë në 8 grupe me nga 4, mund të ketë **maksimumi 10 javë**: çdo lojtar takon 3 lojtarë të tjerë çdo javë, por ka vetëm 31 lojtarë të tjerë. Prandaj `w ≤ floor(31 / 3) = 10`. Ky kufi i sipërm nuk mjafton vetë për të provuar se 10 javë janë të mundshme.

DFS-ja jonë ndërton vetë orarin për numrin e kërkuar të javëve. Për raste të mëdha mund të arrijë kufirin kohor pa e gjetur një orar të plotë. Në atë rast shfaq orarin më të gjatë që ka ndërtuar deri atëherë, por nuk e paraqet atë si përgjigje të plotë.

## Modelimi dhe reprezentimi

- `g`: numri i grupeve; `p`: lojtarët për grup; `n = g × p`; `w`: javët.
- Variabla `X[java][grupi][pozita]` përfaqëson lojtarin në atë pozitë. Domeni i saj është `{0, ..., n-1}`.
- Çdo javë përmban `g` grupe me nga `p` lojtarë dhe secili lojtar shfaqet saktësisht një herë.
- Çdo çift lojtarësh mund të jetë në të njëjtin grup më së shumti një herë në gjithë orarin.
- Në kod, `schedule` është listë javësh; secila javë është listë grupesh dhe secili grup është listë lojtarësh.

## Funksioni objektiv

Për një orar të plotë me grupe dhe lojtarë të vlefshëm, le të jetë `m(i,j)` numri i takimeve të çiftit `i,j`. Minimizojmë:

`f(S) = Σ(i<j) max(0, m(i,j) - 1)`

`f(S) = 0` do të thotë se nuk ka çifte të përsëritura. Zero nuk mjafton për një orar të keqformuar: `is_valid()` kontrollon veçmas numrin e grupeve, madhësinë dhe pjesëmarrjen e lojtarëve.

## Landscape

Numri i ndarjeve të 32 lojtarëve në 8 grupe pa renditje të grupeve ose lojtarëve është `P = 32! / ((4!)^8 × 8!) = 59,287,247,761,257,140,625`. Për 10 javë kemi `P^10 ≈ 10^197.73` orare të mundshme para kontrollit të çifteve. Duke fiksuar javën e parë, mbeten `P^9 ≈ 10^177.96`. Këto nuk janë numra zgjidhjesh të vlefshme.

`landscape.py` merr 500 orare të rastësishme me seed 42: minimumi i `f` është 145, maksimumi 183 dhe mesatarja 163.29; asnjë nuk ka vlerë zero. Një fqinj krijohet duke ndërruar dy lojtarë nga grupe të ndryshme në një javë. Ka `10 × C(8,2) × 4² = 4,480` ndërrime të mundshme për orar. Nga 500 ndërrime të mostruara, 36.6% përmirësuan, 21.0% nuk ndryshuan dhe 42.4% përkeqësuan rezultatin. Këto janë rezultate të mostrës, jo prova për të gjitha oraret.

## DFS dhe backtracking

1. Fiksojmë javën e parë, sepse riemërtimi i lojtarëve jep orare ekuivalente.
2. Për grupin tjetër zgjedhim lojtarin më të vogël të lirë dhe provojmë kombinime me lojtarët e tjerë të lirë. Kjo shmang renditjet e njëjta të grupeve.
3. Nëse ndonjë çift është përdorur më herët, kombinimi refuzohet. Përndryshe ruajmë grupin dhe çiftet e tij dhe vazhdojmë në thellësi.
4. Nëse dega dështon, heqim grupin dhe çiftet e tij dhe provojmë kombinimin tjetër: ky është backtracking.
5. Një orar i plotë është zgjidhje. Shterimi i kërkimit provon pamundësinë; `timeout` vetëm tregon se koha mbaroi.

## Ekzekutimi

Nevojitet Python 3. Nga dosja kryesore e projektit:

```bash
python Problem1_SocialGolfers/social_golfers.py --groups 8 --size 4 --weeks 3 --timeout 30
python Problem1_SocialGolfers/landscape.py
python -m unittest discover -s Problem1_SocialGolfers -v
```

Për ndërfaqen e thjeshtë Streamlit, instalo varësinë dhe hape aplikacionin:

```bash
python -m pip install -r requirements.txt
python -m streamlit run Problem1_SocialGolfers/app.py
```

Ndërfaqja përdor gjithmonë 32 lojtarë në 8 grupe me nga 4; përdoruesi zgjedh numrin e javëve dhe mund të caktojë një kufi kohor. Si parazgjedhje nuk ka kufi kohor: kërkimi mund të zgjasë shumë. Për më shumë se 10 javë shpjegohet menjëherë pse orari është i pamundur. Nëse është aktivizuar kufiri kohor, skadimi i tij do të thotë vetëm që DFS nuk e gjeti orarin e kërkuar në kohë. Programi në terminal mbështet edhe konfigurime të tjera për pyetjen e përgjithshme `n = g × p`.

Provo `--weeks 10` për DFS, por mos e interpreto skadimin e kohës si pamundësi. Testet kontrollojnë DFS-në në raste më të vogla dhe vlefshmërinë e orarit të pjesshëm kur mbaron koha.
