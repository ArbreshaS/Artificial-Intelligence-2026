
"""
Ndërfaqja Streamlit për Social Golfers Problem.
Algoritmi: DFS me Backtracking.

Ekzekutimi:
python -m streamlit run Problem1_SocialGolfers/app.py
"""

import csv
import io
import json
import sys
import time
from pathlib import Path

import streamlit as st

# Importimi i algoritmit ekzistues DFS
sys.path.insert(0, str(Path(__file__).resolve().parent))

from social_golfers import (
    SocialGolfersDFS,
    is_valid,
    objective,
    upper_bound,
)


# Konfigurimi i faqes
st.set_page_config(
    page_title="Problemi i Golfistëve | Inteligjenca Artificiale",
    page_icon="⛳",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Dizajni i aplikacionit
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.7rem;
        padding-bottom: 3rem;
        max-width: 1250px;
    }

    .hero {
        background: linear-gradient(
            114deg,
            #111e35 0%,
            #163d53 52%,
            #116d6e 100%
        );
        border: 1px solid rgba(255,255,255,.1);
        border-radius: 20px;
        padding: 27px 32px;
        margin-bottom: 23px;
        box-shadow: 0 12px 38px rgba(14,45,67,.12);
        color: #fff;
    }

    .hero .kicker {
        letter-spacing: .16em;
        font-size: 12px;
        font-weight: 750;
        color: #95e0db;
        margin-bottom: 12px;
    }

    .hero h1 {
        color: #fff !important;
        margin: 0 0 8px;
        font-size: clamp(27px, 3vw, 40px);
        line-height: 1.2;
    }

    .hero p {
        color: #d2e4e9;
        margin: 0;
        font-size: 15px;
        max-width: 760px;
    }

    .section-eyebrow {
        font-size: 12px;
        letter-spacing: .11em;
        color: #64748b;
        font-weight: 760;
        text-transform: uppercase;
        margin: 6px 0 2px;
    }

    .section-title {
        font-size: 24px;
        margin: 0 0 14px;
        font-weight: 750;
    }

    .group-card {
        background: #ffffff;
        border: 1px solid #dae5eb;
        border-radius: 14px;
        padding: 15px 15px 16px;
        margin: 0 0 13px;
        box-shadow: 0 4px 14px rgba(30,55,78,.06);
        min-height: 119px;
    }

    .group-number {
        font-size: 12px;
        color: #668098;
        font-weight: 800;
        letter-spacing: .08em;
        margin-bottom: 11px;
    }

    .player-chip {
        display: inline-block;
        background: #e8f5f4;
        border: 1px solid #bfdfdc;
        color: #116662;
        padding: 7px 9px;
        border-radius: 9px;
        font-weight: 750;
        font-size: 13px;
        margin: 0 5px 4px 0;
        min-width: 36px;
        text-align: center;
    }

    div[data-testid="stMetric"] {
        background: rgba(120,142,161,.07);
        border: 1px solid rgba(120,142,161,.16);
        border-radius: 13px;
        padding: 14px 16px;
    }

    div[data-testid="stMetricLabel"] {
        font-weight: 650;
    }

    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(120,142,161,.16);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Titulli kryesor
st.markdown(
    """
    <div class="hero">
      <div class="kicker">
        INTELIGJENCA ARTIFICIALE · DETYRA 1
      </div>

      <h1>⛳ Problemi i Golfistëve</h1>

      <p>
        Gjenerimi i grupeve javore duke përdorur algoritmin
        Depth-First Search (DFS) me Backtracking.
        Eksploroni zgjidhjen, kontrolloni kufizimet dhe
        analizoni performancën e algoritmit.
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# Konfigurimet
st.sidebar.header("⚙️ Konfigurimi")

presets = {
    "Standard · 32 lojtarë": (8, 4, 3),
    "Shembull i vogël · 9 lojtarë": (3, 3, 4),
    "Shembull mesatar · 16 lojtarë": (4, 4, 5),
}

scenario = st.sidebar.selectbox(
    "Zgjedh konfigurimin",
    [*presets.keys(), "Konfigurim i personalizuar"],
    help=(
        "Zgjedh një konfigurim të gatshëm ose "
        "përcakto parametrat manualisht."
    ),
)


if scenario == "Konfigurim i personalizuar":

    groups = int(
        st.sidebar.number_input(
            "Numri i grupeve",
            min_value=1,
            max_value=12,
            value=8,
        )
    )

    group_size = int(
        st.sidebar.number_input(
            "Lojtarë për grup",
            min_value=2,
            max_value=8,
            value=4,
        )
    )

    suggested_weeks = 3

else:

    groups, group_size, suggested_weeks = presets[scenario]

    st.sidebar.caption(
        f"**{groups * group_size} lojtarë** · "
        f"{groups} grupe × {group_size} lojtarë"
    )


# Kufiri teorik i javëve
bound = upper_bound(groups, group_size)

weeks = int(
    st.sidebar.number_input(
        "Numri i javëve",
        min_value=1,
        max_value=max(1, bound),
        value=min(suggested_weeks, bound),
        step=1,
        help=(
            "Kufiri teorik maksimal nuk garanton "
            "që algoritmi do të gjejë një zgjidhje."
        ),
    )
)


timeout = int(
    st.sidebar.slider(
        "Koha maksimale e kërkimit (sekonda)",
        min_value=5,
        max_value=120,
        value=30,
        step=5,
    )
)


config = (groups, group_size, weeks, timeout)


st.sidebar.info(
    "Kërkimi përdor **algoritmin ekzistues DFS në Python**. "
    "Ndryshimi i parametrave nuk e ndryshon implementimin."
)


# Përmbledhja e konfigurimit
st.markdown(
    '<div class="section-eyebrow">Përmbledhja e konfigurimit</div>',
    unsafe_allow_html=True,
)

a, b, c, d = st.columns(4)

a.metric("Numri i lojtarëve", groups * group_size)
b.metric("Grupe për javë", groups)
c.metric("Javët e kërkuara", weeks)
d.metric("Kufiri teorik", bound)

st.write("")


# Ekzekutimi i algoritmit
run = st.button(
    "▶ Gjenero orarin",
    type="primary",
    use_container_width=True,
)


if run:

    with st.spinner(
        "Duke kërkuar zgjidhje me DFS dhe Backtracking..."
    ):

        solver = SocialGolfersDFS(
            groups,
            group_size,
            weeks,
            timeout,
        )

        start = time.perf_counter()

        schedule, status = solver.solve()

        elapsed = time.perf_counter() - start

    st.session_state["social_golfers_result"] = {
        "config": config,
        "schedule": schedule,
        "status": status,
        "elapsed": elapsed,
        "nodes": solver.nodes,
        "backtracks": solver.backtracks,
    }


result = st.session_state.get("social_golfers_result")


if not result or result["config"] != config:

    st.info(
        "Zgjedh konfigurimin dhe kliko "
        "**Gjenero orarin** për të parë rezultatet."
    )

    st.stop()


status = result["status"]
schedule = result["schedule"]


st.divider()

st.markdown(
    '<div class="section-eyebrow">Rezultatet e kërkimit</div>',
    unsafe_allow_html=True,
)


# Nëse është gjetur zgjidhja
if status == "found":

    valid = is_valid(
        schedule,
        groups,
        group_size,
    )

    score = objective(schedule)

    if valid:

        st.success(
            f"U gjet një orar i vlefshëm për "
            f"**{weeks} javë**. "
            "Asnjë çift lojtarësh nuk përsëritet."
        )

    else:

        st.error(
            "Algoritmi ktheu një orar, por "
            "validimi i kufizimeve dështoi."
        )


    # Statistikat e algoritmit
    m1, m2, m3, m4 = st.columns(4)

    m1.metric("Funksioni objektiv f(S)", score)

    m2.metric(
        "Nyjet e vizituara",
        f"{result['nodes']:,}",
    )

    m3.metric(
        "Kthimet prapa",
        f"{result['backtracks']:,}",
    )

    m4.metric(
        "Koha e ekzekutimit",
        f"{result['elapsed']:.3f} s",
    )


    # Analiza e çifteve të lojtarëve
    total_possible_pairs = (
        (groups * group_size)
        * (groups * group_size - 1)
        // 2
    )

    unique_pairs_met = (
        weeks
        * groups
        * (group_size * (group_size - 1) // 2)
    )

    coverage = unique_pairs_met / total_possible_pairs

    st.caption(
        f"Çiftet unike të planifikuara: "
        f"{unique_pairs_met} nga {total_possible_pairs} "
        f"({coverage:.1%})."
    )

    st.progress(
        min(coverage, 1.0),
        text="Përqindja e çifteve të planifikuara",
    )

    st.write("")


    # Paraqitja e orarit javor
    st.markdown(
        '<div class="section-title">Orari javor</div>',
        unsafe_allow_html=True,
    )

    tabs = st.tabs(
        [
            f"Java {i}"
            for i in range(1, len(schedule) + 1)
        ]
    )


    for week_index, tab in enumerate(tabs):

        with tab:

            st.caption(
                f"Java {week_index + 1} · "
                f"{groups} grupe · "
                f"{group_size} lojtarë për grup"
            )

            columns = st.columns(min(4, groups))

            for group_index, group in enumerate(
                schedule[week_index]
            ):

                with columns[group_index % len(columns)]:

                    chips = "".join(
                        f'<span class="player-chip">{player}</span>'
                        for player in group
                    )

                    st.markdown(
                        f'<div class="group-card">'
                        f'<div class="group-number">'
                        f'GRUPI {group_index + 1:02d}'
                        f'</div>'
                        f'{chips}'
                        f'</div>',
                        unsafe_allow_html=True,
                    )


    # Përgatitja e rezultateve për eksport
    rows = []

    for wi, week in enumerate(schedule, 1):

        for gi, group in enumerate(week, 1):

            row = {
                "Java": wi,
                "Grupi": gi,
            }

            row.update(
                {
                    f"Lojtari {index}": player
                    for index, player in enumerate(group, 1)
                }
            )

            rows.append(row)


    st.markdown("#### Shkarko rezultatet")

    csv_buffer = io.StringIO()

    csv_writer = csv.DictWriter(
        csv_buffer,
        fieldnames=list(rows[0].keys()),
    )

    csv_writer.writeheader()
    csv_writer.writerows(rows)

    export_a, export_b = st.columns(2)


    with export_a:

        st.download_button(
            "⬇ Shkarko CSV",
            csv_buffer.getvalue().encode("utf-8-sig"),
            file_name="orari_golfisteve.csv",
            mime="text/csv",
            use_container_width=True,
        )


    with export_b:

        st.download_button(
            "⬇ Shkarko JSON",
            json.dumps(
                schedule,
                indent=2,
                ensure_ascii=False,
            ),
            file_name="orari_golfisteve.json",
            mime="application/json",
            use_container_width=True,
        )


# Nëse përfundon koha e kërkimit
elif status == "timeout":

    st.warning(
        f"Kërkimi u ndal pas "
        f"{result['elapsed']:.2f} sekondash. "
        "Kalimi i kohës nuk do të thotë "
        "se zgjidhja nuk ekziston."
    )


# Nëse tejkalohet kufiri teorik
elif status == "impossible_by_bound":

    st.error(
        "Numri i javëve të kërkuara "
        "tejkalon kufirin teorik maksimal."
    )


# Nëse kërkimi përfundon pa zgjidhje
else:

    st.warning(
        "Kërkimi përfundoi pa gjetur "
        "një orar të vlefshëm për këtë konfigurim."
    )


# Statistikat në rast të kërkimit të pasuksesshëm
if status != "found":

    x, y, z = st.columns(3)

    x.metric(
        "Nyjet e vizituara",
        f"{result['nodes']:,}",
    )

    y.metric(
        "Kthimet prapa",
        f"{result['backtracks']:,}",
    )

    z.metric(
        "Koha e ekzekutimit",
        f"{result['elapsed']:.3f} s",
    )


# Shpjegimi i algoritmit
with st.expander("Si funksionon algoritmi?"):

    st.markdown(
        """
        ### DFS me Backtracking

        **Gjendja (State):**
        Një orar javor i plotësuar pjesërisht.

        **DFS (Depth-First Search):**
        Algoritmi zgjedh një grup të vlefshëm dhe
        vazhdon kërkimin në thellësi.

        **Backtracking (Kthimi prapa):**
        Nëse një degë nuk mund të përfundohet,
        algoritmi kthehet te zgjedhja e mëparshme
        dhe provon një kombinim tjetër.

        **Kufizimet (Constraints):**
        - Çdo lojtar paraqitet saktësisht një herë në javë.
        - Çdo grup ka numrin e kërkuar të lojtarëve.
        - Asnjë çift lojtarësh nuk përsëritet.

        **Reduktimi i simetrisë (Symmetry Breaking):**
        Java e parë fiksohet dhe çdo grup i ri
        fillon me lojtarin më të vogël të lirë.
        Kjo zvogëlon kërkimet ekuivalente.

        **Funksioni objektiv (Objective Function):**
        f(S) numëron takimet e përsëritura
        ndërmjet çifteve të lojtarëve.

        Një orar i plotë dhe i vlefshëm ka:

        **f(S) = 0**
        """
    )
