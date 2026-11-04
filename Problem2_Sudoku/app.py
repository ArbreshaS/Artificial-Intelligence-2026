"""Simple Streamlit interface for the Sudoku BFS solver."""

import streamlit as st

from sudoku import PUZZLES, objective, parse, solve

st.set_page_config(page_title="Sudoku Solver", page_icon="🧩", layout="centered")
st.markdown("""
<style>
.block-container {max-width: 850px; padding-top: 2rem;}
.hero {background: linear-gradient(120deg, #14243d, #116f70); color: white;
       border-radius: 16px; padding: 1.6rem 2rem; margin-bottom: 1.5rem;}
.hero h1 {color: white; margin: 0;}
.hero p {color: #d7eeed; margin: .5rem 0 0;}
</style>
<div class="hero"><h1>🧩 Sudoku Solver</h1>
<p>Zgjidhja e Sudoku me BFS</p></div>
""", unsafe_allow_html=True)

level = st.selectbox("Niveli", list(PUZZLES))
st.caption("0 përfaqëson një qelizë të zbrazët. Mund ta ndryshosh Sudoku-n më poshtë.")
default = '\n'.join(PUZZLES[level][i:i+9] for i in range(0, 81, 9))
text = st.text_area("Sudoku: 9 rreshta me nga 9 shifra", value=default, height=240)

with st.expander("Modelimi dhe shpjegimi i detyrës"):
    st.markdown("""
**Problemi dhe kufizimet:** Sudoku ka 9 × 9 qeliza. Çdo rresht, kolonë
dhe kuti 3 × 3 duhet t'i përmbajë numrat 1–9 nga një herë. Numrat e
dhënë në fillim nuk ndryshohen.

**Variabla:** `X[r][c]` është vlera e një qelize të zbrazët.
**Domeni:** numrat `{1, ..., 9}` që nuk janë përdorur në rreshtin,
kolonën ose kutinë e asaj qelize. Gjendja në kod është një tabelë me
81 vlera; `0` tregon një qelizë të zbrazët.

**Funksioni objektiv:** `f(S) = qelizat e zbrazëta + përsëritjet`
në rreshta, kolona dhe kuti. Për një tabelë të plotë dhe pa konflikte,
`f(S) = 0`. Numrat fillestarë ruhen sepse ndryshohen vetëm qelizat bosh.

**Landscape:** Nëse një Sudoku ka `e` qeliza bosh, para kontrollit të
kufizimeve ka `9^e` mënyra për t'i mbushur. Shembulli Easy ka 51 qeliza
bosh: `9^51 ≈ 10^48.67` tabela të mundshme. Këto nuk janë domosdoshmërisht
zgjidhje të vlefshme. Një fqinj mund të krijohet duke ndryshuar një qelizë
që nuk ishte e dhënë në fillim.

**BFS dhe degët e dështuara:** BFS ruan tabelat në një radhë FIFO dhe i
shqyrton sipas numrit të qelizave të plotësuara. Zgjedh një qelizë me më
pak kandidatë dhe shton në radhë një tabelë të re për secilin kandidat të
vlefshëm. Nëse një degë nuk ka kandidatë, ajo hidhet poshtë dhe kërkimi
vazhdon me alternativat në radhë. Ky është kthimi nga dega e dështuar;
nuk është backtracking rekurziv klasik, i cili zakonisht përdor DFS.
    """)

if st.button("Zgjidh Sudoku", type="primary"):
    try:
        board = parse(text)
        with st.spinner("Duke kërkuar me BFS..."):
            solution, status, visited = solve(board)
        if status == "solved":
            st.success("Sudoku u zgjidh.")
            st.code('\n'.join(' '.join(map(str, solution[i:i+9])) for i in range(0, 81, 9)))
            st.write(f"Gjendje të vizituara: **{visited}** · Funksioni objektiv: **{objective(solution)}**")
        elif status == "limit":
            st.warning("U arrit kufiri i gjendjeve. Kjo nuk provon se Sudoku nuk ka zgjidhje.")
        else:
            st.warning("Kërkimi përfundoi: kjo Sudoku nuk ka zgjidhje.")
    except ValueError as error:
        st.error(str(error))
