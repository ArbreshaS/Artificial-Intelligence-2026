"""Display the BFS tree and its first goal path."""

import streamlit as st

from search_trees import PROBLEMS, build_tree, format_state, solution_path

st.set_page_config(page_title='Search Trees', page_icon='🌳', layout='wide')
st.markdown("""
<style>
.block-container {max-width: 1100px; padding-top: 2rem;}
.hero {background: linear-gradient(120deg, #14243d, #116f70); color: white;
       border-radius: 16px; padding: 1.6rem 2rem; margin-bottom: 1.5rem;}
.hero h1 {color: white; margin: 0;}
.hero p {color: #d7eeed; margin: .5rem 0 0;}
</style>
<div class="hero"><h1>🌳 Search Trees</h1>
<p>Eksplorimi i gjendjeve me BFS</p></div>
""", unsafe_allow_html=True)

problem = st.selectbox('Problemi', list(PROBLEMS))
depth = st.slider('Thellësia maksimale', 0, 12, 4 if problem == '8-Puzzle' else 12)
nodes = build_tree(problem, depth)
path = solution_path(problem, nodes)
st.caption(f"Nyje: {len(nodes)}. Gjendjet e përsëritura hiqen; nyjet qëllim nuk zgjerohen.")
if path:
    st.success(f"U gjet një zgjidhje me {len(path) - 1} hapa.")
    with st.expander('Shfaq rrugën e zgjidhjes', expanded=True):
        for state, action, step in path:
            st.write(f"{step}. {action}: {format_state(problem, state)}")
else:
    st.info('Nuk u gjet qëllimi brenda kësaj thellësie; kjo nuk provon se nuk ekziston.')

# Large diagrams are difficult to read, so the full tree remains available as text.
if len(nodes) <= 150:
    lines = ['digraph G {', 'rankdir=TB;', 'node [shape=box, style="rounded,filled", fillcolor="#e8f5f4"];']
    for i, (state, parent, action, _) in enumerate(nodes):
        label = format_state(problem, state).replace('"', "'")
        lines.append(f'{i} [label="{i}: {label}"];')
        if parent is not None:
            lines.append(f'{parent} -> {i};')
    lines.append('}')
    st.graphviz_chart('\n'.join(lines))
else:
    st.info('Pema është shumë e madhe për diagramin. Zvogëlo thellësinë ose shiko listën më poshtë.')

with st.expander('Lista e nyjeve dhe veprimeve'):
    for i, (state, parent, action, level) in enumerate(nodes):
        st.write(f"{i}: prindi {parent}, niveli {level}, {action} → {format_state(problem, state)}")
