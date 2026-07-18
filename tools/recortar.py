#!/usr/bin/env python3
"""
Convierte una ilustración sobre fondo blanco en un WebP con transparencia real,
que es lo que permite que el hero funcione igual sobre claro y sobre negro.

    python3 tools/recortar.py entrada.jpg assets/hero.webp

Por qué no basta con un umbral de luminancia: el personaje tiene zonas claras
propias (zapatillas, bol, cuello) que un umbral global perforaría.

La clave está en que el fondo y su sombra de contacto son claros y *neutros*,
mientras que lo que hay que conservar es oscuro o tiene color. Medido sobre la
imagen original:

    fondo         lum 251   sat  0
    sombra piso   lum 224   sat  5
    madera banco  lum 129   sat 73

O sea que (claro AND neutro) separa fondo de sujeto sin ambigüedad. Un umbral
solo de luminancia no lo lograría: la sombra es más clara que la madera.

Quedan dos casos y por eso hay dos pasos: el fondo que llega al borde de la
imagen, y los huecos de fondo encerrados por el sujeto, como el espacio entre
las patas del banco, que ninguna búsqueda desde el borde alcanza.
"""
import sys
from PIL import Image, ImageFilter
import numpy as np
from scipy import ndimage

# Fondo y sombra de contacto: claros y neutros. Holgado a propósito, porque la
# sombra baja hasta lum ~209 y la madera nunca sube de ~130.
LUM_FONDO, SAT_FONDO = 190, 25
# Para huecos encerrados el criterio se aprieta: ahí solo hay blanco de fondo,
# y apretarlo evita confundirlo con el cuello o el bol, que son claros pero no
# tan blancos.
LUM_HUECO, SAT_HUECO = 238, 14
# Área mínima para tratar una región clara encerrada como fondo. Medido: los
# huecos del banco dan 1688-12986 px; el detalle más grande del personaje, 266.
MIN_HUECO = 800


def recortar(ruta_entrada, ruta_salida):
    src = Image.open(ruta_entrada).convert('RGB')
    arr = np.array(src).astype(int)
    lum = 0.2126 * arr[:, :, 0] + 0.7152 * arr[:, :, 1] + 0.0722 * arr[:, :, 2]
    sat = arr.max(axis=2) - arr.min(axis=2)

    # --- Paso 1: fondo conectado al borde de la imagen ---
    candidato = (lum > LUM_FONDO) & (sat < SAT_FONDO)
    etiquetas, n = ndimage.label(candidato)
    del_borde = set(etiquetas[0, :]) | set(etiquetas[-1, :]) | \
                set(etiquetas[:, 0]) | set(etiquetas[:, -1])
    del_borde.discard(0)
    fondo = np.isin(etiquetas, list(del_borde))

    # --- Paso 2: huecos de fondo encerrados por el sujeto ---
    hueco = (~fondo) & (lum > LUM_HUECO) & (sat < SAT_HUECO)
    etiquetas, n = ndimage.label(hueco)
    if n:
        areas = ndimage.sum(hueco, etiquetas, range(1, n + 1))
        grandes = np.where(areas >= MIN_HUECO)[0] + 1
        if len(grandes):
            fondo |= np.isin(etiquetas, grandes)
            print(f"  huecos encerrados eliminados: {len(grandes)}")

    # --- Alfa: encoger 1px para descartar el halo claro del borde JPEG ---
    alfa = Image.fromarray(np.where(fondo, 0, 255).astype(np.uint8))
    alfa = alfa.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.7))

    out = src.copy()
    out.putalpha(alfa)
    out = out.crop(out.getbbox())          # recorta al sujeto real
    out.save(ruta_salida, quality=86, method=6)

    print(f"  fondo eliminado: {100 * fondo.mean():.1f}%")
    print(f"  {ruta_entrada} -> {ruta_salida}  {out.size[0]}x{out.size[1]}")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    recortar(sys.argv[1], sys.argv[2])
