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

**El traje del personaje** se repinta de celeste a negro con un filtro SVG (`#ink-suit`). El arte del hero es un raster remoto, así que el color se cambia al renderizar: se deriva un matte de `(B − R)` para aislar el traje, y se compone encima una copia oscurecida por luminancia que conserva el sombreado de los vóxeles. La piel, la cadena dorada y las llamas quedan fuera del matte y pasan intactas.

**El scrim del hero** existe por contraste, no por estética: el titular es casi negro y el arte de fondo es oscuro, lo que daba ~1.2:1. El scrim levanta el fondo solo donde va el texto y deja libres el sujeto y el lettering grande. Ahora mide ~11.8:1.

## Accesibilidad

`aria-expanded` en el menú, cierre con Escape con retorno de foco, contención de tab dentro del panel, skip link, y `prefers-reduced-motion` respetado en todas las animaciones.

## Nota

Las dos imágenes del hero se cargan desde un host externo (`figma.site`) y podrían dejar de estar disponibles. Las capas tienen un color de fondo de respaldo, pero conviene alojar esos assets en el repo si el sitio va a producción.
