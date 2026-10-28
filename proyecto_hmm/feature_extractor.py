
import numpy as np

class FeatureExtractor2D:
    """Cuantiza (Δx, Δy) en K sectores angulares (chain code)."""
    def __init__(self, K=8):
        self.K = K

    def quantize(self, dx, dy):
        """Retorna símbolo entero [0, K-1]."""
        ...

    def extract(self, points):
        """Lista de puntos 2D → secuencia de símbolos."""
        ...

    def extract_partial(self, points, t):
        """Secuencia O_1:t."""
        ...


class FeatureExtractor3D:
    """Convierte (x,y,z) a esféricas (θ,φ) y cuantiza (Δθ, Δφ)."""
    def __init__(self, K=8):
        self.K = K

    @staticmethod
    def cartesian_to_spherical(x, y, z):
        """Retorna (r, θ, φ)."""
        ...

    @staticmethod
    def spherical_to_cartesian(r, theta, phi):
        ...

    def quantize(self, dtheta, dphi):
        ...

    def extract(self, points_3d):
        """Puntos 3D sobre esfera → secuencia de símbolos."""
        ...

    def extract_partial(self, points_3d, t):
        ...