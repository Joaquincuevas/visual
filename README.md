# Visual

Sitio personal de Joaquín Cuevas — desarrollo web.

HTML, CSS y JS planos en un solo archivo. Sin build, sin dependencias: se abre `index.html` y funciona.

## Estado

El diseño y el comportamiento están terminados. **El contenido es placeholder.**

Los textos, proyectos y datos de contacto están marcados con comentarios `TODO` en `index.html`. Buscá `TODO` para encontrarlos todos:

- Correo de contacto (aparece en tres lugares: menú y sección de contacto)
- URL de LinkedIn (menú y footer)
- Los tres proyectos: título, stack, año y enlace
- Los dos párrafos de «Sobre mí» y la frase de apertura
- La lista de tecnologías — dejá solo las que uses de verdad
- Los servicios del marquee

La sección de Notas está en estado vacío a propósito. Cuando publiques la primera, reemplazá el `<p class="posts-empty">` por enlaces `<a class="post reveal">`.

## Estructura

Hero → marquee de servicios → Proyectos → Sobre mí → Notas → Contacto → Footer.

El menú navega a las secciones reales de la página.

## Decisiones técnicas

**El resplandor que sigue al cursor** se posiciona con dos custom properties. Una implementación anterior codificaba un PNG de viewport completo con `canvas.toDataURL()` en cada frame; ahora el bucle `requestAnimationFrame` solo escribe dos strings y se detiene solo cuando el puntero deja de moverse.

**Las portadas de los proyectos** son arte compuesto en CSS — gradientes en capas más una textura de grano por SVG. Las clases van de `art-1` a `art-6`. No hay imágenes que cargar ni que se puedan romper.

**El hero tiene dos estados.** En reposo es claro y el personaje va en gris; al entrar el puntero se invierte a negro, el personaje pasa a color saturado, el titular a crema y el lettering al celeste de marca. Todo el cambio son cuatro propiedades animadas más un resplandor que sigue al cursor para que el negro no quede plano. Sin elementos extra.

**El recorte lleva transparencia real** (`assets/hero.webp`), y eso es lo que hace posible el estado oscuro. La versión anterior usaba `mix-blend-mode: multiply` para borrar el fondo blanco, pero multiply sobre negro habría hecho desaparecer al personaje: cualquier color por negro da negro.

**El scrim del hero ya no hace falta.** Existía porque el titular casi negro caía sobre arte oscuro (~1.2:1). Ahora el titular cambia de color junto con el fondo: 14.9:1 en claro, 17.4:1 en oscuro.

## Accesibilidad

`aria-expanded` en el menú, cierre con Escape con retorno de foco, contención de tab dentro del panel, skip link, y `prefers-reduced-motion` respetado en todas las animaciones.

## Cambiar la imagen del hero

    python3 tools/recortar.py tu-foto.jpg assets/hero.webp

El script convierte una ilustración sobre fondo blanco en un WebP con transparencia. Conviene que el sujeto quede vertical: la composición lo ubica a la derecha, con el titular a la izquierda.

El recorte no es un simple umbral de luminancia, porque el personaje tiene zonas claras propias (zapatillas, bol, cuello) que un umbral global perforaría. La clave está en que el fondo y su sombra de contacto son claros **y neutros**, mientras que lo que hay que conservar es oscuro o tiene color. Medido sobre esta imagen:

| | luminancia | saturación |
|---|---|---|
| fondo | 251 | 0 |
| sombra del piso | 224 | 5 |
| madera del banco | 129 | 73 |

Un umbral solo de luminancia no serviría: la sombra es **más clara** que la madera.

Hay un segundo paso porque quedan huecos de fondo encerrados por el sujeto —el espacio entre las patas del banco— que ninguna búsqueda desde el borde alcanza. Se detectan por área: los huecos del banco dan 1688–12986 px, mientras que el detalle claro más grande del personaje da 266.

En dispositivos sin cursor no hay estado oscuro posible, así que se muestra el personaje en color sobre el fondo claro. Con `prefers-reduced-motion` se conserva el cambio de color, que no es movimiento, y se quitan la transición y el resplandor.
