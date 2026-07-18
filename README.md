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

**El spotlight del hero** usa una máscara CSS (`radial-gradient`) manejada por custom properties. Una implementación anterior codificaba un PNG de viewport completo con `canvas.toDataURL()` en cada frame; ahora el bucle `requestAnimationFrame` solo escribe dos strings y se detiene solo cuando el puntero deja de moverse.

**Las portadas de los proyectos** son arte compuesto en CSS — gradientes en capas más una textura de grano por SVG. Las clases van de `art-1` a `art-6`. No hay imágenes que cargar ni que se puedan romper.

**El hero es un recorte sobre blanco** (`assets/hero.jpg`, alojado en el repo). En vez de recortar el fondo se usa `mix-blend-mode: multiply`: blanco × cualquier color da ese color, así que el fondo de la imagen desaparece contra el gris de la página sin dejar borde de caja. De paso el personaje se oscurece un ~10%, lo que ayuda a que se asiente sobre la página en vez de flotar.

**Los casi-blancos se corrigen con `brightness(1.04)`.** El fondo del JPEG no es blanco puro: mide 249–252. Multiplicado contra el gris da ~224 contra 228, lo que dibuja un rectángulo visible alrededor de la imagen. El `brightness` lleva esos valores a 255 para que el multiply los borre del todo. Va en las dos capas, porque la de color es la que se muestra sola en dispositivos táctiles.

**El scrim del hero ya no hace falta.** Existía porque el titular casi negro caía sobre arte oscuro (~1.2:1). Con un hero claro el titular queda sobre el fondo de la página y el contraste es alto por defecto.

## Accesibilidad

`aria-expanded` en el menú, cierre con Escape con retorno de foco, contención de tab dentro del panel, skip link, y `prefers-reduced-motion` respetado en todas las animaciones.

## El spotlight con una sola imagen

Las dos capas del hero usan **el mismo archivo**. La de base lleva `grayscale(1)` y la de arriba va en color, recortada por la máscara del cursor — o sea que el efecto de revelado no necesita una segunda imagen, solo un filtro CSS.

Para cambiar la foto alcanza con reemplazar `assets/hero.jpg`. Conviene que sea un recorte sobre fondo blanco y en vertical: la composición espera al sujeto a la derecha, con el titular a la izquierda.

En dispositivos sin cursor no hay spotlight posible, así que se oculta la capa gris y se muestra la de color directamente. Lo mismo con `prefers-reduced-motion`.
