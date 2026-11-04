"""Simple interface for the Social Golfers assignment."""

import importlib
import time

import streamlit as st

import social_golfers

# Streamlit reruns this file, but imported modules can remain in memory.
# Reload the solver so updates are applied without restarting the server.
social_golfers = importlib.reload(social_golfers)
SocialGolfersDFS = social_golfers.SocialGolfersDFS
is_valid = social_golfers.is_valid
objective = social_golfers.objective


st.set_page_config(page_title="Social Golfers", page_icon="⛳", layout="centered")
st.markdown("""
<style>
.block-container {max-width: 850px; padding-top: 2rem;}
.hero {background: linear-gradient(120deg, #14243d, #116f70); color: white;
       border-radius: 16px; padding: 1.6rem 2rem; margin-bottom: 1.5rem;}
.hero h1 {color: white; margin: 0;}
.hero p {color: #d7eeed; margin: .5rem 0 0;}
</style>
<div class="hero"><h1>⛳ Social Golfers</h1>
<p>Planifikimi i grupeve me DFS dhe backtracking</p></div>
""", unsafe_allow_html=True)

groups, size = 8, 4
st.write("**32 lojtarë · 8 grupe · 4 lojtarë për grup**")
weeks = st.number_input("Numri i javëve", min_value=1, max_value=52, value=3)
st.caption("Kufiri teorik është 10 javë. Kërkimi për shumë javë mund të marrë kohë.")
limit_time = st.checkbox("Kufizo kohën e kërkimit", value=False)
timeout = None
if limit_time:
    timeout = st.number_input("Koha maksimale (sekonda)", min_value=1, max_value=3600, value=30)
else:
    st.caption("Kërkimi vazhdon derisa të përfundojë; për shumë javë mund të zgjasë shumë.")

with st.expander("Modelimi dhe shpjegimi i detyrës"):
    st.markdown("""
**Problemi dhe kufizimet:** Çdo javë, secili nga 32 lojtarët vendoset
saktësisht një herë në një nga 8 grupet me nga 4. Një çift nuk lejohet
të luajë bashkë më shumë se një herë.

**Variabla:** `X[java][grupi][pozita]` është lojtari në atë pozitë.
**Domeni:** numrat e lojtarëve `{0, 1, ..., 31}`. Në kod, `schedule`
është listë javësh, grupesh dhe lojtarësh.

**Funksioni objektiv:** `f(S) = Σ(i<j) max(0, mᵢⱼ − 1)`, ku `mᵢⱼ`
është numri i takimeve të çiftit. Synojmë `f(S) = 0`, pa çifte të përsëritura.
Kontrollohen veçmas edhe madhësia e grupeve dhe pjesëmarrja e lojtarëve.

**Landscape:** Një javë ka `P = 32! / ((4!)⁸ × 8!)` ≈ `5.93 × 10¹⁹`
ndarje të mundshme. Për 10 javë janë `P¹⁰ ≈ 10¹⁹⁷·⁷³` orare para
kontrollit të çifteve. Nga 500 orare të rastësishme të analizuara,
vlera mesatare e funksionit objektiv ishte 163.29; kjo është mostër,
jo numri i të gjitha zgjidhjeve.

**DFS me backtracking:** Algoritmi ndërton një grup të vlefshëm dhe vazhdon
në thellësi. Kur një zgjedhje nuk çon përpara, e heq atë dhe provon një tjetër.
Java e parë fiksohet për të shmangur orare ekuivalente.
    """)

if st.button("Gjenero orarin me DFS", type="primary"):
    with st.spinner("Duke kërkuar orarin me DFS..."):
        solver = SocialGolfersDFS(groups, size, weeks, timeout=timeout)
        start = time.perf_counter()
        schedule, status = solver.solve()
        elapsed = time.perf_counter() - start

    if status == "found":
        st.success(f"U gjet një orar i vlefshëm për {weeks} javë.")
        st.write(f"Funksioni objektiv: **{objective(schedule)}** · "
                 f"Valid: **{is_valid(schedule, groups, size)}** · "
                 f"Koha: **{elapsed:.2f} s**")
        for number, week in enumerate(schedule, 1):
            with st.expander(f"Java {number}", expanded=number == 1):
                for index, group in enumerate(week, 1):
                    st.write(f"Grupi {index}: {', '.join(map(str, group))}")
    elif status == "impossible_by_bound":
        st.error(f"Nuk ka orar të vlefshëm për {weeks} javë.")
        st.markdown(f"""
Çdo lojtar luan me **3 lojtarë të tjerë** në javë dhe ka gjithsej
**31 lojtarë të tjerë**. Asnjë çift nuk mund të përsëritet, prandaj
**31 ÷ 3 = 10**, me mbetje 1.

Për **{weeks} javë**, secilit lojtar do t'i duheshin **{weeks * 3} partnerë
të ndryshëm**, por janë vetëm 31. Prandaj {weeks} javë janë të pamundura.
        """)
    elif status == "timeout":
        st.warning(f"DFS nuk e gjeti orarin për {weeks} javë brenda {timeout} sekondave. "
                   "Ka shumë kombinime për t'u kontrolluar, prandaj kërkimi mund të "
                   "zgjasë më shumë. Kjo nuk provon se orari është i pamundur.")
        st.write(f"DFS gjeti një orar të pjesshëm të vlefshëm për **{len(solver.best_schedule)} javë**.")
        with st.expander("Shfaq orarin e pjesshëm"):
            for number, week in enumerate(solver.best_schedule, 1):
                st.write(f"Java {number}: " + " | ".join(", ".join(map(str, group)) for group in week))
    else:
        st.warning("Kërkimi përfundoi: nuk ka zgjidhje për këta parametra.")

