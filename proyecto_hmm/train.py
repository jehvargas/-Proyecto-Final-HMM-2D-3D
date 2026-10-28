from feature_extractor import (FeatureExtractor2D, FeatureExtractor3D)

class ModelTrainer:
    """Script independiente para entrenar los 27 caracteres."""

    def __init__(self, mode="2D", n_states=5, K=8):
        self.mode     = mode
        self.n_states = n_states
        self.K        = K
        if mode == "2D":
            self.extractor = FeatureExtractor2D(K)
            self.n_symbols = K
        else:
            self.extractor = FeatureExtractor3D(K)
            self.n_symbols = K * K

    def train_character(self, char, sequences):
        """Baum-Welch sobre las secuencias del carácter."""
        ...

    def train_all(self, dataset_dir, output_dir):
        """Itera los 27 caracteres y guarda sus .json."""
        ...


if __name__ == "__main__":
    trainer = ModelTrainer(mode="2D")
    trainer.train_all("data/raw_2d/", "models/")