import numpy as np

class HMM:
    """Modelo λ = (A, B, π) para un carácter."""
    def __init__(self, n_states, n_symbols, name=""):
        self.n_states  = n_states
        self.n_symbols = n_symbols
        self.name = name
        self.A  = np.full((n_states, n_states), 1.0 / n_states)
        self.B  = np.full((n_states, n_symbols), 1.0 / n_symbols)
        self.pi = np.full(n_states, 1.0 / n_states)

    def to_dict(self): ...
    @classmethod
    def from_dict(cls, d): ...
    def save(self, path): ...
    @classmethod
    def load(cls, path): ...


class HMMEngine:
    """Algoritmos estocásticos implementados desde cero (sin librerías)."""

    @staticmethod
    def forward(hmm, obs):
        """α_t(i) y P(O|λ). Retorna (alpha, log_likelihood)."""
        ...

    @staticmethod
    def backward(hmm, obs):
        """β_t(i)."""
        ...

    @staticmethod
    def viterbi(hmm, obs):
        """Retorna (mejor_camino, log_prob)."""
        ...

    @staticmethod
    def posterior(hmm, obs):
        """γ_t(i) vía Forward-Backward."""
        ...

    @staticmethod
    def baum_welch(hmm, sequences, max_iter=100, tol=1e-4):
        """Entrena A, B, π (offline). Retorna log-likelihood final."""
        ...