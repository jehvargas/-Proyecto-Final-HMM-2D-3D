# Interfaz gráfica HMM 2D/3D

Desde esta carpeta, ejecutar en PowerShell:

```powershell
.\.venv\Scripts\python.exe main.py
```

Si se prepara otro entorno: `python -m pip install -r requirements.txt`.

- Menú institucional con acceso a los dos modos.
- 2D: dibujar manteniendo pulsado el botón izquierdo; también admite eventos táctiles.
- 3D: botón izquierdo para dibujar sobre la superficie visible, botón derecho para girar y rueda para acercar/alejar. Reorientar esfera restablece la cámara sin borrar el trazo.
- Limpiar lienzo borra los puntos y resultados. Reiniciar captura comienza una nueva secuencia.
- La columna derecha contiene las 27 letras, referencias tipográficas, porcentajes y barras; ordena los resultados recibidos de mayor a menor probabilidad.
- Los trazos azules son la entrada; las trayectorias futuras recibidas del proyector se dibujan punteadas. Girar la cámara conserva las coordenadas del trazo sobre la esfera unitaria.

## Integración pendiente del motor existente

La GUI no inventa probabilidades ni utiliza modelos de demostración. El proyecto original contiene métodos vacíos en el reconocedor, proyector, extracción de características y motor HMM; models/a.json está vacío. Por ello, actualmente se puede dibujar y navegar, pero la clasificación real y el autocompletado requieren completar esos módulos y cargar modelos entrenados.

La vista llama a `classify_partial(points, len(points))`, que debe devolver una lista de diccionarios `{'char': 'a', 'prob': 0.8}` con probabilidades normalizadas. Luego llama a `project(points, points[-1], mode='2D' o '3D')`, que debe devolver puntos futuros. En 3D los puntos son cartesianos sobre la esfera unitaria; la propiedad `angular_points` expone sus coordenadas angulares (theta, phi). El extractor del motor recibe los puntos cartesianos conforme a su contrato original.

La esfera se renderiza con QPainter y proyección ortográfica, sin añadir dependencias OpenGL. Se ocultan los segmentos de la cara posterior. La lógica de presentación compartida está en gui_common.py y las vistas conservan las clases utilizadas por main.py.
