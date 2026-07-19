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

**La linterna** se posiciona con dos custom properties. Una implementación anterior codificaba un PNG de viewport completo con `canvas.toDataURL()` en cada frame; ahora el bucle `requestAnimationFrame` solo escribe dos strings y se detiene solo cuando el puntero deja de moverse.

**Las portadas de los proyectos** son arte compuesto en CSS — gradientes en capas más una textura de grano por SVG. Las clases van de `art-1` a `art-6`. No hay imágenes que cargar ni que se puedan romper.

**El hero usa dos fotos distintas del mismo personaje.** En reposo se ve la clara, sobre el fondo de la página. Al entrar el puntero pasan dos cosas a la vez: el hero entero se pinta de negro, y una linterna revela dentro de un círculo la segunda foto. No es un filtro sobre la misma imagen — son dos capturas con otra ropa, otra pose y otra luz.

**El fondo entero tiene que oscurecerse, no solo el círculo.** La foto oscura trae su propio fondo negro y, sobre una página clara, ese fondo se recorta como un rectángulo alrededor del área revelada. Con la página también en negro los dos se funden y solo se ve transformarse al personaje. Por eso `--dark` coincide con la mediana del fondo de la foto, que `tools/alinear.py` mide e informa al generar los assets.

**El recorte claro lleva transparencia real** (`assets/hero-light.webp`), así se apoya sobre el fondo de la página sin caja. La capa oscura, en cambio, conserva su fondo negro a propósito: es lo que hace que dentro del círculo se vea el personaje *y su mundo*, en vez de un recorte flotando.

**El scrim del hero ya no hace falta.** Existía porque el titular casi negro caía sobre arte oscuro (~1.2:1). Ahora el titular vive sobre el fondo claro de la página, fuera del área de la linterna: 14.9:1.

## Accesibilidad

`aria-expanded` en el menú, cierre con Escape con retorno de foco, contención de tab dentro del panel, skip link, y `prefers-reduced-motion` respetado en todas las animaciones.

## Cambiar las imágenes del hero

    python3 tools/recortar.py foto-clara.jpg /tmp/claro.webp
    python3 tools/alinear.py  /tmp/claro.webp foto-oscura.jpg

El primer paso convierte la foto clara (sobre fondo blanco) en un recorte con transparencia. El segundo alinea ambas sobre un lienzo común de 840x935 y escribe los dos assets finales.

### Por qué hace falta alinear

Si los personajes no coinciden en posición y escala, la linterna los hace saltar al mover el mouse y se lee como un error, no como un efecto. El alineado usa **la cabeza** como referencia: es lo que el ojo sigue, y si las cabezas calzan el resto se lee como la misma persona aunque cambien la ropa y la pose.

Se mide el ancho del cráneo a un 12% de la altura del sujeto —a esa altura ya pasó el pelo y todavía no empiezan los hombros— y se escala una imagen hasta igualar la otra. En este par la diferencia era de 279 px contra 224, o sea un factor de 1.246.

**Cuidado con el encuadre.** La foto oscura estaba cortada en los muslos y la clara llegaba hasta el banquito: la zona sin material queda vacía y la linterna no revela nada ahí. Por eso el lienzo se define por la región que ambas cubren, y el hero terminó siendo un plano de busto y no de cuerpo entero.

### El recorte de la foto clara

No es un simple umbral de luminancia, porque el personaje tiene zonas claras propias (zapatillas, bol, cuello) que un umbral global perforaría. La clave está en que el fondo y su sombra de contacto son claros **y neutros**, mientras que lo que hay que conservar es oscuro o tiene color. Medido:

| | luminancia | saturación |
|---|---|---|
| fondo | 251 | 0 |
| sombra del piso | 224 | 5 |
| madera del banco | 129 | 73 |

Un umbral solo de luminancia no serviría: la sombra es **más clara** que la madera.

Hay un segundo paso porque quedan huecos de fondo encerrados por el sujeto —el espacio entre las patas del banco— que ninguna búsqueda desde el borde alcanza. Se detectan por área: los huecos del banco dan 1688–12986 px, mientras que el detalle claro más grande del personaje da 266.

En dispositivos sin cursor no hay linterna posible, así que se muestra solo la versión clara. Lo mismo con `prefers-reduced-motion`.
