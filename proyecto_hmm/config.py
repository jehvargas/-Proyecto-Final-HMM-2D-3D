
class Config:

    """Configuración global del proyecto."""

    MODELS_DIR   = "models/"
    CHARS        = "abcdefghijklmnñopqrstuvwxyz"   # 27 letras
    N_STATES     = 5          # estados ocultos por carácter
    K_2D         = 8          # sectores angulares (chain code)
    K_3D         = 8          # sectores esféricos
    MIN_POINTS   = 3          # mínimo de puntos para clasificar
    PROJECTION_ALPHA = 0.5    # transparencia de proyección
    GUI_TITLE    = "Reconocedor HMM 2D/3D"
    