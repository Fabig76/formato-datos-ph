# Personalización para tu Propiedad Horizontal

Esta guía explica cómo adaptar el código de Cerro Azul a cualquier otra
propiedad horizontal. Tiempo estimado: **10-15 minutos**.

## Lista de cambios necesarios

Para personalizar el formulario a tu PH, necesitas modificar **6 archivos**:

  1. `index.html` — cambiar textos del encabezado, pie de página y sección 11
  2. `assets/logo.jpg` — reemplazar con tu logo
  3. `assets/styles.css` — cambiar colores del tema
  4. `js/app.js` — ya está configurado para Cerro Azul (no requiere cambios
     si sigues el estándar)
  5. `apps-script/Codigo.gs` — cambiar SHEET_ID y textos de la sección 11
  6. Generar nuevo QR con la URL de tu GitHub Pages

Vamos uno por uno.

## 1. Cambiar textos del encabezado (index.html)

Busca y reemplaza estas cadenas:

```
"Urbanización Cerro Azul" → "[Tu PH]"
"900770444"               → "[Tu NIT]"
"Bello / Niquía"          → "[Tu dirección completa]"
"urb.cerroazul@gmail.com" → "[tu-correo@administracion.com]"
```

Hay ~5 lugares donde aparece "urb.cerroazul@gmail.com":
  · Sección 11 (texto de derechos ARCO)
  · Sección "Editar mi registro" (texto "¿Perdiste tu N° de formulario?")
  · Footer

Usa Ctrl+H (Buscar y reemplazar) en el editor de GitHub para hacer todos
los reemplazos a la vez.

También puedes editar el aviso legal. El aviso actual dice:
"Los datos aquí solicitados corresponden al **dueño real del inmueble**"

Si tu PH tiene su propio aviso legal (recomendable que lo tenga un abogado),
reemplaza el texto del `<div class="legal-banner">` en `index.html`.

## 2. Cambiar el logo

  1. Sube tu logo al repo: clic en "Add file" → "Upload files"
  2. Nombre: `logo.jpg` (o `.png` si tu logo es transparente)
  3. Si usas otro formato, edita `index.html` línea 7:
     `<link rel="icon" href="assets/logo.jpg" type="image/jpeg">`
     Cambia la extensión y el type.

**Tamaño recomendado del logo**: 200x200 px, fondo transparente (si es PNG)
o blanco (si es JPG). Mantén proporción cuadrada.

## 3. Cambiar los colores del tema (styles.css)

Abre `assets/styles.css`. Las primeras líneas tienen:

```css
:root {
  --azul:        #0066CC;   /* Color principal (botones, bordes) */
  --azul-osc:    #004C99;   /* Hover, fondo header */
  --azul-claro:  #E6F0FA;   /* Fondos suaves */
  --verde-azul:  #00A89C;   /* Acentos secundarios */
  --naranja:     #F39200;   /* Avisos legales */
  --naranja-osc: #C97500;
  --gris-tx:     #333333;   /* Texto principal */
  ...
}
```

### Cómo elegir los colores

  1. Toma el logo de tu PH
  2. Identifica los 2-3 colores principales (uno dominante + 1-2 acentos)
  3. Con una herramienta online (ej: https://imagecolorpicker.com/) extrae
     los hex codes
  4. Reemplaza en el CSS

### Ejemplo: PH con logo verde y dorado

```css
:root {
  --azul:        #2E8B57;   /* Verde principal */
  --azul-osc:    #1B5E3A;
  --azul-claro:  #E8F5E9;
  --verde-azul:  #D4AF37;   /* Dorado acento */
  --naranja:     #D4AF37;   /* Para avisos */
  --naranja-osc: #8B7500;
  --gris-tx:     #333333;
  ...
}
```

Después de cambiar, también edita la regla del gradiente del header
en `assets/styles.css`:

```css
header.site-header {
  background: linear-gradient(180deg, #FFFFFF 0%, var(--azul-claro) 100%);
}
```

Puedes dejarlo así (usa las variables) o cambiarlo para que combine
mejor con tus colores.

## 4. Cambiar SHEET_ID en el Apps Script (Codigo.gs)

Este es el cambio más importante. Abre `Codigo.gs` y en la línea 9:

```js
const SHEET_ID = '16gxeAkcTIWnuwkBFBaHW7Y-nUHaMdtovNzUBaupytPc';
```

Reemplaza con el ID de TU Sheet (lo anotaste en el paso 1.1 de la guía
de implementación).

También personaliza la sección 11 del texto legal. Busca la función
`buildRowFromPayload` o `rowToObject` y ajusta los textos que aparecen
en el código HTML (estos no están en el Codigo.gs sino en el index.html).

## 5. Generar el QR

Desde la terminal, en el directorio de tu repo:

```bash
python scripts/generar-qr.py "https://TU_USUARIO.github.io/TU_REPO/"
```

(O usa el script que está en [`../scripts/`](../scripts/) de este repo)

Si tu logo es en PNG con transparencia, puedes opcionalmente superponerlo
en el centro del QR (requiere edición manual del script).

## Cambios opcionales

### Agregar/quitar secciones

Si tu PH tiene necesidades especiales:

  · **Agregar campos al Sheet**: agregar columnas + actualizar `Codigo.gs`
  · **Agregar campos al formulario**: agregar HTML en `index.html` + agregar
    los IDs al recolector en `js/app.js`
  · **Cambiar número de residentes/menores/vehículos**: cambiar el bucle
    `for (let i = 1; i <= N; i++)` en `index.html` y ajustar `NUM_COLS`
    en `Codigo.gs`

### Cambiar la cantidad de mascotas (default 2)

Busca en `index.html` el patrón `for (let i = 1; i <= 2; i++)` y reemplaza
el `2` por el número deseado. Ajusta las columnas correspondientes en
`Codigo.gs`.

### Cambiar el idioma de las plantillas de correo

Si vas a implementar el envío automático de correo (feature opcional),
edita las plantillas en [`../plantillas/`](../plantillas/).

### Soporte para múltiples torres

Si tu PH tiene varias torres o manzanas:

  · Agrega una columna "Torre/Manzana" en el Sheet (al lado de N° Apto)
  · En el formulario, agrega un campo "Torre" antes del N° de Apto
  · Cambia la llave de dedupe a (Torre, N° Apto) en vez de solo N° Apto

## Validación final

Después de personalizar:

  1. Recarga la página pública
  2. Verifica:
     · Logo se ve correctamente
     · Colores son del PH
     · Textos mencionan tu PH correctamente
     · El formulario funciona (envía y edita)
     · El QR apunta a la URL correcta
  3. Imprime el QR y verifica que escanea bien desde tu celular

## Soporte

Si te atascas en algún paso, pregúntale a Hermes Agent o abre un issue en
el repositorio de GitHub.
