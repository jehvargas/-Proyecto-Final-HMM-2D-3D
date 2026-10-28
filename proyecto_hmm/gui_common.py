"""Componentes de presentación; no contiene lógica estocástica."""
import math
from PyQt5 import QtCore, QtGui, QtWidgets
from config import Config

STYLE = """
QWidget { font-family: 'Segoe UI'; font-size: 13px; color: #23324a; }
QMainWindow { background: #f3f6fb; }
QFrame#card { background: white; border: 1px solid #dde5ef; border-radius: 14px; }
QPushButton { background: #e7edf7; border: 0; border-radius: 7px; padding: 11px 18px; }
QPushButton:hover { background: #d5e1f5; }
QPushButton#primary { background: #315dd8; color: white; font-weight: 600; }
QLabel#title { font-size: 26px; font-weight: 700; }
QLabel#muted { color: #607089; }
QProgressBar { border: 0; background: #e9eef6; border-radius: 3px; max-height: 6px; }
QProgressBar::chunk { background: #537be4; border-radius: 3px; }
QScrollArea { border: 0; background: white; }
"""

def button(text, callback, primary=False):
    widget = QtWidgets.QPushButton(text)
    if primary:
        widget.setObjectName('primary')
    widget.clicked.connect(callback)
    return widget


class ProbabilityPanel(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName('card')
        self.setMinimumWidth(310)
        layout = QtWidgets.QVBoxLayout(self)
        heading = QtWidgets.QLabel('Clasificación en vivo')
        heading.setStyleSheet('font-size: 18px; font-weight: 600')
        layout.addWidget(heading)
        self.status = QtWidgets.QLabel()
        self.status.setWordWrap(True)
        self.status.setObjectName('muted')
        layout.addWidget(self.status)
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        container = QtWidgets.QWidget()
        self.rows = QtWidgets.QVBoxLayout(container)
        self.rows.setAlignment(QtCore.Qt.AlignTop)
        scroll.setWidget(container)
        layout.addWidget(scroll)
        self.refresh([])

    def refresh(self, results, message=None):
        while self.rows.count():
            self.rows.takeAt(0).widget().deleteLater()
        results = sorted(results or [], key=lambda item: float(item['prob']), reverse=True)
        self.status.setText(message or ('Probabilidades del reconocedor HMM' if results else
            'Dibuja para comenzar. Si el motor no devuelve resultados, no se mostrarán probabilidades.'))
        by_char = {item['char']: item for item in results}
        ordered = [item['char'] for item in results]
        ordered += [char for char in Config.CHARS if char not in by_char]
        for char in ordered:
            row = QtWidgets.QWidget()
            line = QtWidgets.QHBoxLayout(row)
            line.setContentsMargins(3, 4, 3, 4)
            # Referencia estática generada localmente para cada letra.
            icon = QtWidgets.QLabel(char)
            icon.setAlignment(QtCore.Qt.AlignCenter)
            icon.setFixedSize(32, 32)
            icon.setStyleSheet('background: #edf2fd; border-radius: 7px; font: italic 22px Georgia;')
            line.addWidget(icon)
            line.addWidget(QtWidgets.QLabel(char.upper()))
            bar = QtWidgets.QProgressBar()
            bar.setRange(0, 1000)
            bar.setTextVisible(False)
            value = max(0., min(1., float(by_char[char]['prob']))) if char in by_char else None
            bar.setValue(round(value * 1000) if value is not None else 0)
            line.addWidget(bar, 1)
            label = QtWidgets.QLabel(f'{value:.1%}' if value is not None else '—')
            label.setMinimumWidth(52)
            line.addWidget(label)
            self.rows.addWidget(row)


class DrawingCanvas(QtWidgets.QWidget):
    """Esfera unitaria con cámara ortográfica y trazado en coordenadas del objeto."""
    def __init__(self, owner, spherical=False):
        super().__init__()
        self.owner = owner
        self.spherical = spherical
        self.drawing = False
        self.rotating = False
        self.previous = None
        self.breaks = set()
        self.setMinimumSize(480, 400)
        self.setAttribute(QtCore.Qt.WA_AcceptTouchEvents)
        self.setMouseTracking(True)

    def transform(self, point, inverse=False):
        yaw, pitch = self.owner.rotation
        x, y, z = point
        if inverse:
            y, z = math.cos(pitch)*y + math.sin(pitch)*z, -math.sin(pitch)*y + math.cos(pitch)*z
            return (math.cos(yaw)*x - math.sin(yaw)*z, y, math.sin(yaw)*x + math.cos(yaw)*z)
        x, z = math.cos(yaw)*x + math.sin(yaw)*z, -math.sin(yaw)*x + math.cos(yaw)*z
        return (x, math.cos(pitch)*y - math.sin(pitch)*z, math.sin(pitch)*y + math.cos(pitch)*z)

    def radius(self):
        return min(self.width(), self.height()) * .36 * self.owner.zoom

    def sphere_point(self, x, y):
        r = self.radius()
        nx, ny = (x-self.width()/2)/r, -(y-self.height()/2)/r
        norm = nx*nx + ny*ny
        return None if norm > 1 else self.transform((nx, ny, math.sqrt(max(0., 1-norm))), True)

    def screen(self, point):
        if not self.spherical:
            return QtCore.QPointF(*point), True
        x, y, z = self.transform(point)
        return QtCore.QPointF(self.width()/2+x*self.radius(), self.height()/2-y*self.radius()), z >= -0.01

    def paintEvent(self, event):
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing)
        p.fillRect(self.rect(), QtGui.QColor('#ffffff'))
        if self.spherical:
            center = QtCore.QPointF(self.width()/2, self.height()/2)
            r = self.radius()
            gradient = QtGui.QRadialGradient(center-QtCore.QPointF(r*.3, r*.3), r*1.6)
            gradient.setColorAt(0, QtGui.QColor('#f5f9ff'))
            gradient.setColorAt(1, QtGui.QColor('#b9cee9'))
            p.setBrush(gradient)
            p.setPen(QtGui.QPen(QtGui.QColor('#91acd0'), 1))
            p.drawEllipse(center, r, r)
            for lat in range(-60, 90, 30):
                a = math.radians(lat)
                self.polyline(p, [(math.cos(a)*math.cos(t*math.pi/90), math.sin(a), math.cos(a)*math.sin(t*math.pi/90)) for t in range(181)], '#b1c5df', 1)
            for lon in range(0, 180, 30):
                a = math.radians(lon)
                self.polyline(p, [(math.cos(t*math.pi/90)*math.cos(a), math.sin(t*math.pi/90), math.cos(t*math.pi/90)*math.sin(a)) for t in range(181)], '#b1c5df', 1)
        else:
            p.setPen(QtGui.QPen(QtGui.QColor('#edf1f7'), 1))
            for x in range(24, self.width(), 24):
                for y in range(24, self.height(), 24):
                    p.drawPoint(x, y)
        points = self.owner.points_3d if self.spherical else self.owner.points
        self.polyline(p, points, '#000000', 3, breaks=self.breaks)
        self.polyline(p, self.owner.projection, '#000000', 3, dashed=True)
        p.end()

    def polyline(self, painter, points, color, width, dashed=False, breaks=()):
        pen = QtGui.QPen(QtGui.QColor(color), width, QtCore.Qt.DashLine if dashed else QtCore.Qt.SolidLine)
        pen.setCapStyle(QtCore.Qt.RoundCap)
        painter.setPen(pen)
        previous = None
        for index, point in enumerate(points):
            current, visible = self.screen(point)
            if visible and previous is not None and index not in breaks:
                painter.drawLine(previous, current)
            previous = current if visible else None

    def mousePressEvent(self, event):
        self.previous = event.pos()
        if self.spherical and event.button() == QtCore.Qt.RightButton:
            self.rotating = True
        elif event.button() == QtCore.Qt.LeftButton:
            self.drawing = True
            points = self.owner.points_3d if self.spherical else self.owner.points
            self.breaks.add(len(points))
            self.capture(event.pos())

    def event(self, event):
        if event.type() in (QtCore.QEvent.TouchBegin, QtCore.QEvent.TouchUpdate, QtCore.QEvent.TouchEnd):
            touches = event.touchPoints()
            if event.type() == QtCore.QEvent.TouchBegin:
                self.drawing = True
                points = self.owner.points_3d if self.spherical else self.owner.points
                self.breaks.add(len(points))
            if touches:
                self.capture(touches[0].pos())
            if event.type() == QtCore.QEvent.TouchEnd:
                self.drawing = False
                self.owner.update_prediction()
            event.accept()
            return True
        return super().event(event)

    def capture(self, pos):
        point = self.sphere_point(pos.x(), pos.y()) if self.spherical else (pos.x(), pos.y())
        if point is not None:
            self.owner.capture(point)

    def mouseMoveEvent(self, event):
        if self.rotating:
            delta = event.pos()-self.previous
            self.owner.on_rotate(delta.x(), delta.y())
        elif self.drawing:
            self.capture(event.pos())
        self.previous = event.pos()

    def mouseReleaseEvent(self, event):
        if self.drawing:
            self.capture(event.pos())
            self.owner.update_prediction()
        self.drawing = self.rotating = False

    def wheelEvent(self, event):
        if self.spherical:
            self.owner.on_zoom(1.12 if event.angleDelta().y() > 0 else 1/1.12)
            event.accept()


class BaseDrawingWindow:
    spherical = False

    def __init__(self, recognizer, projector, on_back):
        self.recognizer, self.projector, self.on_back = recognizer, projector, on_back
        self.points, self.points_3d, self.projection = [], [], []
        self.rotation, self.zoom = [0., 0.], 1.
        self.window = None

    def build(self):
        self.window = QtWidgets.QMainWindow()
        self.window.setWindowTitle(Config.GUI_TITLE)
        self.window.resize(1180, 780)
        self.window.setStyleSheet(STYLE)
        central = QtWidgets.QWidget()
        self.window.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(26, 22, 26, 22)
        top = QtWidgets.QHBoxLayout()
        top.addWidget(button('← Menú principal', self.on_back))
        top.addStretch()
        top.addWidget(QtWidgets.QLabel('UNILLANOS  /  PROCESOS ESTOCÁSTICOS'))
        layout.addLayout(top)
        title = QtWidgets.QLabel('Reconocedor ' + ('3D · Lienzo esférico' if self.spherical else '2D · Plano cartesiano'))
        title.setObjectName('title')
        layout.addWidget(title)
        hint = QtWidgets.QLabel('Dibuja con clic izquierdo · Gira con clic derecho · Rueda para zoom' if self.spherical else 'Mantén pulsado el ratón o desliza el dedo para dibujar una letra minúscula')
        hint.setObjectName('muted')
        layout.addWidget(hint)
        body = QtWidgets.QSplitter()
        self.canvas = DrawingCanvas(self, self.spherical)
        self.panel = ProbabilityPanel()
        body.addWidget(self.canvas)
        body.addWidget(self.panel)
        body.setStretchFactor(0, 3)
        body.setStretchFactor(1, 1)
        layout.addWidget(body, 1)
        controls = QtWidgets.QHBoxLayout()
        controls.addWidget(button('Limpiar lienzo', self.on_clear))
        controls.addWidget(button('Reiniciar captura', self.on_restart, True))
        if self.spherical:
            controls.addWidget(button('Reorientar esfera', self.reset_view))
        controls.addStretch()
        controls.addWidget(QtWidgets.QLabel('Negro: trazo   ·   Punteado: proyección HMM'))
        layout.addLayout(controls)
        self.status = QtWidgets.QLabel('Captura lista · 0 puntos')
        self.status.setObjectName('muted')
        layout.addWidget(self.status)
        self.timer = QtCore.QTimer(self.window)
        self.timer.setSingleShot(True)
        self.timer.setInterval(60)
        self.timer.timeout.connect(self.update_prediction)

    def capture(self, point):
        points = self.points_3d if self.spherical else self.points
        threshold = .008 if self.spherical else 2.
        if points and math.dist(points[-1], point) < threshold:
            return
        points.append(tuple(point))
        self.status.setText(f'Capturando · {len(points)} puntos')
        if not self.timer.isActive():
            self.timer.start()
        self.canvas.update()

    def update_prediction(self):
        self.timer.stop()
        points = self.points_3d if self.spherical else self.points
        if len(points) < Config.MIN_POINTS:
            return
        try:
            results = self.recognizer.classify_partial(points, len(points))
            self.projection = []
            if results:
                prediction = self.projector.project(points, points[-1], mode='3D' if self.spherical else '2D')
                if prediction is not None:
                    self.projection = [points[-1]] + list(prediction)
            self.panel.refresh(results, None if results else 'Motor HMM sin resultados. Faltan modelos entrenados o la implementación del reconocedor.')
        except Exception as error:
            self.projection = []
            self.panel.refresh([], f'No se pudo evaluar el trazo: {error}')
        self.canvas.update()

    def on_clear(self):
        self.timer.stop()
        self.points.clear()
        self.points_3d.clear()
        self.projection = []
        self.canvas.breaks.clear()
        self.canvas.drawing = self.canvas.rotating = False
        self.panel.refresh([])
        self.status.setText('Captura lista · 0 puntos')
        self.canvas.update()

    def on_restart(self):
        self.on_clear()
        self.status.setText('Nueva captura iniciada · 0 puntos')

    def reset_view(self):
        self.rotation, self.zoom = [0., 0.], 1.
        self.canvas.update()

    def _render_canvas(self):
        self.canvas.update()

    def _refresh_panel(self, results):
        self.panel.refresh(results)

    def show(self):
        self.window.show()

    def close(self):
        if self.window:
            self.timer.stop()
            self.window.close()
