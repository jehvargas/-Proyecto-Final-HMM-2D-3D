
from gui_common import BaseDrawingWindow


class Canvas2DWindow(BaseDrawingWindow):
    """Captura 2D y presentación de resultados del reconocedor inyectado."""
    def on_draw_start(self, event):
        self.canvas.mousePressEvent(event)

    def on_draw_move(self, event):
        self.canvas.mouseMoveEvent(event)

    def on_draw_end(self, event):
        self.canvas.mouseReleaseEvent(event)
