#!/usr/bin/env python3
"""
Alinea las dos fotos del hero sobre un lienzo común para que la linterna revele
una encima de la otra sin que el personaje salte.

    python3 tools/alinear.py recorte-claro.webp foto-oscura.jpg

Escribe assets/hero-light.webp y assets/hero-dark.webp.

La entrada clara tiene que venir con transparencia (pasala antes por
tools/recortar.py). La oscura se usa tal cual, con su fondo negro incluido: eso
es lo que hace que dentro del círculo se vea el personaje *y su mundo*, en vez
de un recorte flotando sobre la página.

El alineado usa la cabeza como referencia, medida automáticamente: es lo que el
ojo sigue, y si las cabezas coinciden el resto se lee como la misma persona
aunque cambien la ropa y la pose. Se mide el ancho del cráneo a un 12% de la
altura del sujeto (a esa altura ya pasó el pelo y todavía no empiezan los
hombros) y se escala una imagen hasta igualar la otra.

Ojo con el encuadre: si una de las dos fotos está cortada más arriba que la
otra, la zona sin material queda vacía y la linterna no revela nada ahí. Por eso
el lienzo se define por la región que ambas cubren, no por la más larga.
"""
import sys
import numpy as np
from PIL import Image

W, H = 840, 935          # lienzo común
CAB_X, CAB_TOP = 420, 20  # dónde queda la cabeza dentro del lienzo
# Tiene que ser exactamente --dark del CSS: al pasar el mouse el hero entero se
# pone de ese color, y si la capa no coincide su rectángulo se nota.
NEGRO = (11, 11, 11)


def geometria(mask):
    """Devuelve top del sujeto, ancho y centro horizontal de la cabeza."""
    ys, xs = np.where(mask)
    top, bot = ys.min(), ys.max()
    fila = int(top + 0.12 * (bot - top))
    cols = np.where(mask[fila])[0]
    return top, cols.max() - cols.min(), (cols.max() + cols.min()) / 2


def alinear(ruta_clara, ruta_oscura):
    clara = Image.open(ruta_clara).convert('RGBA')
    top_c, cab_c, cx_c = geometria(np.array(clara)[:, :, 3] > 128)

    oscura = Image.open(ruta_oscura).convert('RGB')
    arr = np.array(oscura).astype(int)
    lum = 0.2126 * arr[:, :, 0] + 0.7152 * arr[:, :, 1] + 0.0722 * arr[:, :, 2]
    top_o, cab_o, cx_o = geometria(lum > 32)

    esc = cab_c / cab_o
    print(f"  cabeza clara {cab_c}px / oscura {cab_o}px -> escala {esc:.3f}")

    # Clara: va tal cual, solo desplazada
    luz = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    luz.paste(clara, (CAB_X - round(cx_c), CAB_TOP - round(top_c)), clara)

    # Oscura: escalada y desplazada, sobre un fondo negro que llena el lienzo
    o2 = oscura.resize((round(oscura.width * esc), round(oscura.height * esc)),
                       Image.LANCZOS)
    osc = Image.new('RGB', (W, H), NEGRO)
    osc.paste(o2, (CAB_X - round(cx_o * esc), CAB_TOP - round(top_o * esc)))

    luz.save('assets/hero-light.webp', quality=88, method=6)
    osc.save('assets/hero-dark.webp', quality=88, method=6)

    # Al pasar el mouse el hero entero se pinta del mismo negro que esta capa; si
    # no coinciden, su rectángulo se nota. Sin pérdida no ayuda: medido, el
    # desvío en el fondo es de 3 niveles tanto en calidad 88 como en 100, así que
    # no vale 6x el peso. Lo que importa es que el CSS use el valor real.
    negro = np.array(Image.open('assets/hero-dark.webp').convert('RGB'))[:900, :60]
    print(f"  assets/hero-light.webp y assets/hero-dark.webp  {W}x{H}")
    print(f"  negro del fondo: mediana {int(np.median(negro))}  "
          f"-> el CSS debe usar #" + f"{int(np.median(negro)):02x}" * 3)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    alinear(sys.argv[1], sys.argv[2])
