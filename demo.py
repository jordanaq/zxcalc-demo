import streamlit as st
import pyzx as zx
import pyzx.simplify as zxs
from pyzx.graph import Graph
import matplotlib.pyplot as plt
from circuit_generators import gen_default_circuit_options


graph_options = gen_default_circuit_options()

GRAPH_FIGSIZE = (12, 4)

SIMPLIFICATION_STRATEGIES = {
    "No Simplification": zxs.id_simp,
    "Bialg Simplify": zxs.bialg_simp,
    "Clifford Simplify": zxs.clifford_simp,
    "Full Reduce": zxs.full_reduce,
    "Teleport Full Reduce": zxs.teleport_reduce,
    "Gadget Simplify": zxs.gadget_simp,
    "Local Complementations": zxs.lcomp_simp,
    "Phase Free Simplify": zxs.phase_free_simp,
    "Pivot Boundary Simplify": zxs.pivot_simp,
    "Pivot Gadget Simplify": zxs.gadget_simp,
    "Pivot Simplify": zxs.pivot_simp,
    "Scalar Reduce": zxs.reduce_scalar,
    "Spider Simplify": zxs.spider_simp,
    "Supplementarity Simplify": zxs.supplementarity_simp,
    "To Clifford Normal Form": zxs.to_clifford_normal_form_graph,
    "Red to Green": zxs.to_gh,
    "Eliminate H-Edges": zxs.to_rg,
}

st.set_page_config(layout="wide")

st.sidebar.header("Simplification Demo")
st.sidebar.subheader("Graph Parameters")
n_qubits = st.sidebar.number_input(
    "Number of Qubits", min_value=1, max_value=10, value=5, step=1
)
n_gates = st.sidebar.number_input(
    "Number of Gates", min_value=1, max_value=100, value=20, step=1
)
graph_type = st.sidebar.selectbox("Select Graph Type", list(graph_options.keys()))


# Initialize session state
if 'g_u' not in st.session_state:
    st.session_state.g_u = None
if 'g_s' not in st.session_state:
    st.session_state.g_s = None

if st.sidebar.button("Generate Graph"):
    g_gen = graph_options[graph_type]
    g_u = g_gen(n_qubits, n_gates)
    st.session_state.g_u = g_u
    st.session_state.g_s = None

simplification_method = st.sidebar.selectbox(
    "Select Simplification Method", list(SIMPLIFICATION_STRATEGIES.keys())
)

if st.sidebar.button("Simplify"):
    if st.session_state.g_u is None:
        st.warning("Please generate a graph first")

    elif st.session_state.g_s is None:
        g_s = st.session_state.g_u.copy()

        s = SIMPLIFICATION_STRATEGIES[simplification_method]
        s(g_s)

        if st.session_state.get("g_s") is None:
            st.session_state.g_s = [(simplification_method, g_s)]
        else:
            st.session_state.get("g_s").append((simplification_method, g_s))

    else:
        _, g_s = st.session_state.g_s[-1]
        g_s = g_s.copy()

        s = SIMPLIFICATION_STRATEGIES[simplification_method]
        s(g_s)

        if st.session_state.get("g_s") is None:
            st.session_state.g_s = [(simplification_method, g_s)]
        else:
            st.session_state.get("g_s").append((simplification_method, g_s))

if st.sidebar.button("Reset"):
    st.session_state.g_u = None
    st.session_state.g_s = None

if (g_u := st.session_state.get("g_u")) is not None:
    st.subheader("Unoptimized Graph")
    fig_u = zx.draw_matplotlib(g_u, figsize=GRAPH_FIGSIZE)
    st.pyplot(fig_u)

if st.session_state.get("g_s") is not None:
    for s_l, g_s in st.session_state.get("g_s"):
        st.subheader(f"Simplified Graph via {s_l}:")
        fig_s = zx.draw_matplotlib(g_s, figsize=GRAPH_FIGSIZE)
        st.pyplot(fig_s)
