
class ModelLoader:
    """Carga/guarda los 27 modelos HMM en .json."""

    def __init__(self, models_dir, chars, n_states, n_symbols):
        self.models_dir = models_dir
        self.chars      = chars
        self.n_states   = n_states
        self.n_symbols  = n_symbols
        self._cache     = {}

    def load(self, char):
        ...

    def load_all(self):
        """Retorna dict {'a': HMM, 'b': HMM, ...}."""
        ...

    def save(self, hmm):
        ...