# Problemi 1 – Social Golfers Problem

## 1. Përshkrimi i problemit

Social Golfers Problem është një problem i planifikimit, ku 32 lojtarë golfi duhet të ndahen në 8 grupe me nga 4 lojtarë çdo javë.

Qëllimi është të krijohet një orar për sa më shumë javë, duke siguruar që asnjë çift lojtarësh të mos jetë në të njëjtin grup më shumë se një herë.

Për zgjidhjen e problemit përdoret algoritmi **Depth-First Search (DFS) me Backtracking**.

## 2. Modelimi i problemit

Problemi modelohet si një *Constraint Satisfaction Problem (CSP)*, ku duhet të gjendet një organizim i lojtarëve që përmbush të gjitha kufizimet.

Parametrat kryesorë janë:

- **n = 32** – numri i lojtarëve
- **g = 8** – numri i grupeve
- **p = 4** – numri i lojtarëve për grup
- **w** – numri i javëve që planifikohen

### Variables (Variablat)

Çdo variabël përfaqëson lojtarin që vendoset në një pozitë të caktuar brenda një grupi dhe një jave.

Reprezentimi i orarit:

`shchedule[week][group][position]`

Në implementim përdoret struktura `schedule[week][group]`, ku çdo grup përmban një listë lojtarësh.

### Domains (Domenet)

Çdo pozitë mund të marrë vlerën e një lojtari nga bashkësia:

**D = {0, 1, 2, ..., 31}**

### Constraints (Kufizimet)

Duhet të respektohen tri kufizime:

1. Çdo lojtar duhet të paraqitet saktësisht një herë gjatë një jave.
2. Çdo grup duhet të përmbajë saktësisht 4 lojtarë.
3. Asnjë çift lojtarësh nuk lejohet të luajë së bashku më shumë se një herë.

Kufizimet kontrollohen përmes funksionit `is_valid()` dhe gjatë procesit të kërkimit.

## 3. Objective Function

Funksioni objektiv llogarit numrin e takimeve të përsëritura ndërmjet çifteve të lojtarëve.

\[
f(S)=\sum_{i<j}\max(0,m_{ij}-1)
\]

Ku:

- **S** – orari i gjeneruar
- **mᵢⱼ** – numri i herëve që lojtarët i dhe j janë në të njëjtin grup
- **f(S)** – numri i takimeve të përsëritura

Qëllimi është të minimizohet funksioni objektiv:

\[
\min f(S)=0
\]

Një orar i plotë që i respekton kufizimet është i vlefshëm kur `f(S) = 0`.

## 4. Landscape Calculation

Landscape analizon madhësinë e hapësirës së kërkimit dhe shpërndarjen e vlerave të funksionit objektiv.

### Madhësia e hapësirës së kërkimit

Numri i mënyrave për të ndarë 32 lojtarë në 8 grupe me nga 4 lojtarë është:

\[
P=\frac{32!}{(4!)^8\cdot8!}
\]

**P = 59,287,247,761,257,140,625**

Për 10 javë, madhësia teorike e hapësirës së ndarjeve është afërsisht:

\[
P^{10}\approx10^{197.73}
\]

Me javën e parë të fiksuar, kjo zvogëlohet në afërsisht:

\[
P^9\approx10^{177.96}
\]

Këto vlera tregojnë hapësirën potenciale të kërkimit, jo numrin e zgjidhjeve të vlefshme.

### Kufiri teorik i javëve

Çdo lojtar takohet me 3 lojtarë të tjerë gjatë një jave dhe ka gjithsej 31 lojtarë të tjerë.

Prandaj:

\[
w\leq\left\lfloor\frac{31}{3}\right\rfloor=10
\]

Pra, kufiri teorik maksimal është **10 javë**.

### Fitness Landscape

Analiza është realizuar duke gjeneruar 500 orare të rastësishme për 10 javë.

Rezultatet:

| Parametri | Rezultati |
|---|---|
| Numri i mostrave | 500 |
| Vlera minimale e f(S) | 145 |
| Vlera maksimale e f(S) | 183 |
| Mesatarja e f(S) | 163.29 |
| Orarë me f(S) = 0 | 0 |

Rezultatet tregojnë se oraret e rastësishme përmbajnë shumë takime të përsëritura, prandaj nevojitet një algoritëm kërkimi që kontrollon kufizimet.

### Neighborhood Analysis

Një zgjidhje fqinje krijohet duke ndërruar dy lojtarë nga grupe të ndryshme brenda së njëjtës javë.

Për konfigurimin me 10 javë ekzistojnë 4,480 fqinj të mundshëm për një orar.

Nga 500 ndërrime të testuara:

- **36.6%** – përmirësojnë funksionin objektiv
- **21.0%** – nuk e ndryshojnë vlerën
- **42.4%** – e përkeqësojnë vlerën

Këto përqindje përfaqësojnë rezultatet e mostrës së analizuar.

## 5. DFS me Backtracking

Algoritmi DFS përdoret për të ndërtuar orarin gradualisht, duke eksploruar kombinimet e mundshme të lojtarëve.

Procesi:

1. Fiksohet java e parë për të zvogëluar kombinimet ekuivalente.
2. Përzgjidhen lojtarët për formimin e grupeve të javës pasuese.
3. Kontrollohet nëse ndonjë çift lojtarësh është takuar më parë.
4. Nëse grupi është i vlefshëm, kërkimi vazhdon në thellësi.
5. Nëse një kombinim nuk mund të çojë në zgjidhje, përdoret Backtracking për t'u kthyer te zgjedhja e mëparshme.
6. Procesi vazhdon derisa të gjendet një orar i vlefshëm, të përfundojë kërkimi ose të arrihet kufiri kohor.

Për zvogëlimin e hapësirës së kërkimit përdoret edhe **Symmetry Breaking**, duke fiksuar javën e parë dhe duke filluar çdo grup me lojtarin më të vogël të lirë.

## 6. Rezultatet e implementimit

Algoritmi është testuar me konfigurimin standard prej 32 lojtarësh, 8 grupesh dhe 3 javësh.

| Parametri | Rezultati |
|---|---|
| Numri i lojtarëve | 32 |
| Numri i grupeve | 8 |
| Lojtarë për grup | 4 |
| Javë të planifikuara | 3 |
| Objective Function | 0 |
| Valid Schedule | True |
| Visited Nodes | 18 |
| Backtracks | 0 |
| Koha e ekzekutimit | 0.008 sekonda |

Algoritmi ka gjeneruar një orar të vlefshëm për 3 javë, pa përsëritje të çifteve të lojtarëve.

Kufiri teorik është 10 javë, por implementimi ynë nuk ka vërtetuar ende që mund ta gjenerojë një orar për të gjitha 10 javët.

## 7. Implementimi dhe ekzekutimi

Projekti është zhvilluar në **Python**, ndërsa për ndërfaqen grafike përdoret **Streamlit**.

### Struktura e projektit

```text
Problem1_SocialGolfers/
├── README.md
├── social_golfers.py
├── landscape.py
├── app.py
└── test_social_golfers.py
```

### Ekzekutimi i algoritmit

Nga folderi kryesor i repository-t:

```bash
python Problem1_SocialGolfers/social_golfers.py
```

### Ekzekutimi i Landscape

```bash
python Problem1_SocialGolfers/landscape.py
```

### Ekzekutimi i ndërfaqes grafike

Pas instalimit të Streamlit:

```bash
python -m streamlit run Problem1_SocialGolfers/app.py
```

Ndërfaqja mundëson konfigurimin e problemit, gjenerimin e orarit, shfaqjen e grupeve sipas javëve dhe analizimin e statistikave të algoritmit.

## 8. Përfundimi

Social Golfers Problem demonstron përdorimin e teknikave të kërkimit të painformuar për zgjidhjen e problemeve me kufizime.

DFS me Backtracking mundëson ndërtimin e orareve të vlefshme, ndërsa kontrollimi i kufizimeve dhe reduktimi i simetrisë ndihmojnë në zvogëlimin e hapësirës së kërkimit.

Analiza e Landscape tregon se problemi ka një numër shumë të madh kombinimesh të mundshme dhe se kërkimi bëhet gjithnjë e më kompleks me rritjen e numrit të javëve.