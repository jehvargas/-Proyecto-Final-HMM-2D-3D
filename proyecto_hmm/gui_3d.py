import math
from gui_common import BaseDrawingWindow


class Canvas3DWindow(BaseDrawingWindow):
    """Captura sobre esfera unitaria; cámara independiente del trazo."""
    spherical = True

    def raycast_to_sphere(self, screen_x, screen_y):
        return self.canvas.sphere_point(screen_x, screen_y)

    @staticmethod
    def cartesian_to_spherical(point):
        x, y, z = point
        radius = math.sqrt(x*x + y*y + z*z)
        return radius, math.atan2(y, x), math.acos(max(-1., min(1., z/radius))) if radius else 0.

    @property
    def angular_points(self):
        return [self.cartesian_to_spherical(point)[1:] for point in self.points_3d]

    def on_draw_3d(self, event):
        self.canvas.capture(event.pos())

    def on_rotate(self, dx, dy):
        self.rotation[0] += dx*.008
        self.rotation[1] += dy*.008
        self.canvas.update()

    def on_zoom(self, factor):
        self.zoom = max(.45, min(1.3, self.zoom*factor))
        self.canvas.update()
