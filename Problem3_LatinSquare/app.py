"""Simple Streamlit interface for the Latin Square solver."""

import streamlit as st

from latin_square import objective, solve, valid

st.set_page_config(page_title="Latin Square", page_icon="🔢", layout="centered")
st.markdown("""
<style>
.block-container {max-width: 850px; padding-top: 2rem;}
.hero {background: linear-gradient(120deg, #14243d, #116f70); color: white;
       border-radius: 16px; padding: 1.6rem 2rem; margin-bottom: 1.5rem;}
.hero h1 {color: white; margin: 0;}
.hero p {color: #d7eeed; margin: .5rem 0 0;}
</style>
<div class="hero"><h1>🔢 Latin Square</h1>
<p>Ndërtimi i katrorit latin me IDDFS dhe backtracking</p></div>
""", unsafe_allow_html=True)

st.write("Zgjedh madhësinë n. Çdo rresht dhe kolonë përmban numrat 1 deri në n nga një herë.")
n = st.number_input("Madhësia n", min_value=1, max_value=5, value=5, step=1,
                    help="Ndërfaqja kufizohet në 5 sepse kërkimi bëhet shumë i kushtueshëm.")

with st.expander("Modelimi dhe shpjegimi i detyrës"):
    st.markdown("""
**Problemi dhe kufizimet:** Ndërtojmë një tabelë `n × n` ku çdo rresht
dhe çdo kolonë përmban numrat nga 1 deri në `n` saktësisht një herë.

**Variabla:** `X[r][c]` është vlera në një qelizë të tabelës.
**Domeni:** `{1, 2, ..., n}`. Gjendja fillestare është tabela bosh;
në kod, `0` përfaqëson një qelizë të zbrazët. Gjendja qëllim është
tabela e plotë që i respekton kufizimet.

**Funksioni objektiv:** `f(S) = qelizat bosh + përsëritjet në rreshta
+ përsëritjet në kolona`. Synojmë `f(S) = 0`, që tregon një tabelë të
plotë pa përsëritje. Validimi kontrollon gjithashtu madhësinë dhe vlerat.

**Landscape:** Para kontrollit të kufizimeve, `n²` qelizat mund të
mbushen në `n^(n²)` mënyra. Për `n = 5`, ka `5^25 ≈ 2.98 × 10¹⁷`
tabela kandidate. Këto nuk janë të gjitha katrorë latinë. Si fqinj
konsiderojmë një tabelë që ndryshon në një qelizë jo të fiksuar.

**IDDFS dhe backtracking:** IDDFS përsërit DFS-në me kufijtë e thellësisë
nga 0 deri në `n²`; çdo hap mbush një qelizë. Algoritmi provon vetëm
numra që nuk janë tashmë në rreshtin ose kolonën përkatëse. Kur një degë
nuk çon në zgjidhje, e heq zgjedhjen dhe provon një tjetër: ky është
backtracking. Rreshti dhe kolona e parë fiksohen në rendin `1, ..., n`
për të shmangur kërkimin e katrorëve ekuivalentë.
    """)

if st.button("Gjenero katrorin", type="primary"):
    with st.spinner("Duke kërkuar me IDDFS..."):
        square, visited = solve(n)
    if square is None:
        st.warning("Nuk u gjet zgjidhje.")
    else:
        st.success("U gjenerua katrori latin.")
        st.code('\n'.join('  '.join(map(str, row)) for row in square))
        st.write(f"Valid: **{valid(square)}** · Funksioni objektiv: **{objective(square)}** · "
                 f"Nyje të vizituara: **{visited}**")
