import streamlit as st
import pyzx as zx
import pyzx.simplify as zxs
from pyzx.circuit import Circuit
from circuit_generators import gen_default_circuit_options


circuit_options = gen_default_circuit_options()


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


st.sidebar.header("Circuit Parameters")
n_qubits = st.sidebar.number_input("Number of Qubits", min_value=1, max_value=10, value=5, step=1)
n_gates = st.sidebar.number_input("Number of Gates", min_value=1, max_value=100, value=20, step=1)
circuit_type = st.selectbox("Select Circuit Type", list(circuit_options.keys()))
simplification_method = st.sidebar.selectbox(
    "Select Simplification Method", list(SIMPLIFICATION_STRATEGIES.keys())
)


if st.button("Generate Circuits"):
    # Unoptimized circuit
    g_gen = circuit_options[circuit_type]
    g_u = g_gen(n_qubits, n_gates)

    st.subheader("Unoptimized Circuit")
    fig_u = zx.draw_matplotlib(g_u)
    st.pyplot(fig_u)

    # Optimizer
    o = SIMPLIFICATION_STRATEGIES[simplification_method]

    # Optimized circuit
    g_o = g_u.copy()
    o(g_o)

    st.subheader("Optimized Circuit")
    fig_o = zx.draw_matplotlib(g_o)
    st.pyplot(fig_o)
