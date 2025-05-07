import random
import pyzx as zx
import pyzx.generate as zxg


def gen_cnot_had_phase(n_qubits, n_gates):
    c = zxg.CNOT_HAD_PHASE_circuit(n_qubits, n_gates)
    return c.to_graph()


def gen_clifford_t(n_qubits, n_gates):
    graph = zxg.cliffordT(n_qubits, n_gates)
    return graph


def gen_clifford_t_meas(n_qubits, n_gates):
    graph = zxg.cliffordTmeas(n_qubits, n_gates)
    return graph


def gen_cliffords(n_qubits, n_gates):
    graph = zxg.cliffords(n_qubits, n_gates)
    return graph


def gen_cnots(n_qubits, n_gates):
    graph = zxg.cnots(n_qubits, n_gates)
    return graph


def gen_identity(n_qubits, n_gates):
    graph = zxg.identity(n_qubits, n_gates)
    return graph


def gen_phase_poly(n_qubits, n_gates):
    n_layers = random.randint(1, min(n_gates, 10))
    c = zxg.phase_poly(n_qubits, n_layers, n_gates // n_layers)
    return c.to_graph()


def gen_phase_approx(n_qubits, n_gates):
    n_layers = random.randint(1, min(n_gates, 10))
    c = zxg.phase_poly_approximate(n_qubits, n_gates, n_layers)
    return c.to_graph()


def gen_phase_from_gadgets(n_qubits, n_gates):
    n_gadgets = random.randint(1, min(n_gates, 10))
    c = zxg.phase_poly_from_gadgets(n_qubits, n_gadgets)
    return c.to_graph()


def gen_qft(n_qubits, n_gates):
    c = zxg.qft(n_qubits)
    return c.to_graph()


def gen_default_circuit_options():
    return {
        "CNOT-HAD-PHASE": gen_cnot_had_phase,
        "Clifford + T": gen_clifford_t,
        "Clifford + T + Measurements": gen_clifford_t_meas,
        "Clifford": gen_cliffords,
        "CNOTs Only": gen_cnots,
        "Identity": gen_identity,
        "Phase Polynomial": gen_phase_poly,
        "Phase Polynomial Approximate": gen_phase_approx,
        # "Phase Polynomial from Gadgets": gen_phase_from_gadgets,
        "Quantum Fourier Transform (QFT)": gen_qft,
    }
