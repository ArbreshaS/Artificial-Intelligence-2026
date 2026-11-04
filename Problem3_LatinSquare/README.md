# Problemi 3: Latin Square

## Modelimi dhe reprezentimi

Për një hyrje `n`, kërkojmë një tabelë `n × n` ku çdo rresht dhe çdo kolonë përmban secilin numër nga 1 deri në `n` saktësisht një herë.

- **Variablat:** qelizat `X[r][c]` të tabelës.
- **Domeni:** `{1, 2, ..., n}` për secilën qelizë.
- **Gjendja fillestare:** tabelë bosh, e paraqitur me zero.
- **Gjendja:** një tabelë pjesërisht e mbushur; në kod është listë rreshtash. Zero do të thotë qelizë e zbrazët.
- **Veprimi:** vendos një numër në qelizën tjetër në rend rreshtash, vetëm nëse nuk është në rreshtin ose kolonën e saj.
- **Gjendja qëllim:** tabela është plot dhe secili rresht e kolonë përmban të gjithë numrat 1–n.

## Funksioni objektiv

Për një tabelë me vlera në `{0, ..., n}`, përcaktojmë:

`f(S) = numri i qelizave bosh + përsëritjet në rreshta + përsëritjet në kolona`.

Për çdo rresht dhe kolonë, përsëritjet llogariten si numri i vlerave të vendosura minus numri i vlerave të ndryshme. `f(S) = 0` do të thotë tabelë e plotë pa përsëritje. Funksioni `valid()` kontrollon gjithashtu madhësinë dhe domenin e vlerave. Kërkimi nuk e përdor `f` si heuristikë; kontrollon drejtpërdrejt kufizimet.

## Landscape

Para zbatimit të kufizimeve, secila nga `n²` qelizat ka `n` vlera të mundshme: ka `n^(n²)` tabela të plota kandidate. Për `n = 5`, kjo është `5^25 = 298,023,223,876,953,125` tabela. Nëse çdo rresht detyrohet të jetë permutim i numrave 1–n, mbeten `(n!)^n` kandidatë: për `n = 5`, `120^5 = 24,883,200,000`. Këto ende mund të shkelin kufizimet e kolonave; asnjëri numër nuk është numri i katrorëve latinë.

Si fqinjësi mund të marrim tabelat që ndryshojnë vetëm në një qelizë jo të fiksuar. Funksioni objektiv u jep këtyre tabelave lartësinë e landscape: zero është zgjidhje; vlerat më të larta tregojnë qeliza bosh ose përsëritje. Kërkimi ynë ndërton vetëm gjendje pa përsëritje, prandaj në gjendjet e tij të pjesshme `f` është numri i qelizave bosh.

`landscape.py` gjeneron tabela të plota rastësisht dhe ndryshon një qelizë për të krijuar një fqinj. Për `n = 5`, 500 mostra me seed 42 dhanë minimumin 9, maksimumin 22 dhe mesataren 16.27. Nga 500 fqinjë, 170 përmirësuan vlerën, 150 nuk e ndryshuan dhe 180 e përkeqësuan. Skripti shfaq histogramin; shifrat përshkruajnë vetëm mostrën.

## IDDFS dhe backtracking

IDDFS ekzekuton kërkim në thellësi me kufij `0, 1, ..., n²`. Thellësia është numri i qelizave të mbushura; një lëvizje mbush një qelizë. Në çdo kufi kërkimi fillon përsëri nga tabela bosh. Një zgjidhje e plotë mund të gjendet vetëm në kufirin `n²`.

Në çdo qelizë, algoritmi provon numrat sipas rendit. Nëse numri gjendet tashmë në rresht ose kolonë, ai refuzohet. Përndryshe vendoset në tabelë, kërkimi vazhdon në thellësi, dhe më pas vendosja hiqet kur kthehemi nga thirrja. Kjo heqje është **backtracking**. Zgjidhja kopjohet para se tabela të rikthehet.

Për të shmangur katrorë ekuivalentë, rreshti dhe kolona e parë fiksohen si `1, ..., n`. Kjo është e sigurt për kërkimin e një zgjidhjeje: duke riemërtuar simbolet mund të rendisim rreshtin e parë, pastaj duke rirenditur rreshtat e tjerë mund të rendisim kolonën e parë, pa prishur vetinë latine. Programi gjen një katror, jo të gjithë katrorët.

IDDFS përsërit punë në çdo kufi dhe hapësira rritet shpejt. Ndërfaqja kufizohet në `n ≤ 5`; kjo përfshin shembullin e detyrës. Implementimi është për mësim, jo për madhësi të mëdha.

## Ekzekutimi

Nga dosja kryesore:

```bash
python Problem3_LatinSquare/latin_square.py 5
python Problem3_LatinSquare/landscape.py --size 5
python -m unittest discover -s Problem3_LatinSquare -v
python -m pip install -r requirements.txt
python -m streamlit run Problem3_LatinSquare/app.py
```

Ndërfaqja përmban një përmbledhje të këtyre kërkesave te seksioni **Modelimi dhe shpjegimi i detyrës**.
