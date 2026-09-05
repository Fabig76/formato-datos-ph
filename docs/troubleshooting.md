# Troubleshooting — Problemas Comunes y Soluciones

## Problemas con la página web (GitHub Pages)

### La página no carga / muestra README

**Síntoma**: Abres `https://[usuario].github.io/[repo]/` y ves el README del
repositorio, no el formulario.

**Causa**: GitHub Pages sirve `README.md` como página principal cuando existe.

**Solución**:
  1. En el repo, renombra `README.md` a `README-project.md` (o bórralo)
  2. Crea un archivo vacío llamado `.nojekyll` en la raíz del repo
  3. Espera 1 minuto y recarga

### Cambios en el código no se ven

**Síntoma**: Hago cambios a `index.html` o `styles.css`, pero la página
muestra la versión anterior.

**Causa**: Caché del navegador + caché de GitHub Pages.

**Solución**:
  1. Espera 2-3 minutos (GitHub Pages tarda en refrescar)
  2. Refresca con Ctrl+Shift+R (forzar recarga sin caché)
  3. Abre en ventana privada/incognito

### El logo no aparece

**Síntoma**: En vez del logo hay un ícono de imagen rota.

**Causa**: El archivo `assets/logo.jpg` no existe o el nombre está mal.

**Solución**:
  1. Verifica que el archivo existe: abre `https://[usuario].github.io/[repo]/assets/logo.jpg`
  2. Si da 404, sube el archivo
  3. Verifica que en `index.html` la línea sea:
     `<img src="assets/logo.jpg" alt="Logo [PH]" class="logo">`

### El QR no se ve bien en el celular

**Síntoma**: El QR no escanea o se ve borroso.

**Causa**: El QR está impreso muy pequeño, o la imagen se pixeleó.

**Solución**:
  1. Imprime el QR a un mínimo de 10x10 cm
  2. Usa el archivo PNG original (no截图/screenshots de baja resolución)
  3. Verifica que el archivo PNG tenga suficiente resolución (mínimo 800x800 px)

## Problemas con el Apps Script

### doGet funciona pero doPost da error 405

**Síntoma**: El endpoint responde a GET (nextId, lookup) pero rechaza POST
con error HTTP 405 "Method Not Allowed".

**Causa**: El deployment de Apps Script no está bien configurado para aceptar
POSTs externos.

**Solución**:
  1. Ve a https://script.google.com → tu proyecto
  2. **Implementar → Administrar implementaciones**
  3. Verifica:
     · Tipo: **Aplicación web** (NO "API Executable")
     · Quién tiene acceso: **Cualquier persona** (NO "Solo yo")
  4. Si está mal, clic en el lápiz → corregir → **Implementar**
  5. Copia la NUEVA URL y actualízala en `js/app.js`

### "Acción no reconocida"

**Síntoma**: Hago un GET o POST y el backend devuelve ese mensaje.

**Causa**: El parámetro `action` no coincide con los esperados.

**Solución**: Solo las acciones `nextId`, `lookup` (GET) y el POST sin
parámetro `action` están soportadas. Cualquier otra cosa devuelve ese error.

### "¿Falta N° de apartamento?" cuando SÍ lo envié

**Síntoma**: Lleno el campo N° Apto pero el backend dice que falta.

**Causa**: El JSON del frontend no se está enviando correctamente, o el
backend no está parseando bien.

**Solución**:
  1. Abre la consola del navegador (F12)
  2. En la pestaña Network, busca el POST al Web App
  3. Verifica el body del request — debe ser JSON con `apto` como string
  4. Si está vacío, hay un problema en el frontend — revisa `js/app.js`
     función `recolectar()`

### Los datos no aparecen en el Sheet

**Síntoma**: Envío el formulario, recibo el N° de Formulario, pero no
veo nada nuevo en el Sheet.

**Causa**: Probablemente el SHEET_ID en `Codigo.gs` está mal, o la hoja
no se llama "Registros".

**Solución**:
  1. Abre `Codigo.gs` línea 9: `const SHEET_ID = '...';`
  2. Verifica que el ID coincide con el de tu Sheet (URL del navegador)
  3. Verifica que la hoja se llama "Registros" (línea 10)
  4. Si renombraste la hoja a otra cosa, actualiza `SHEET_NAME`

### Error de permisos al ejecutar

**Síntoma**: Hago clic en Ejecutar y aparece "Permiso denegado".

**Causa**: Apps Script necesita autorización para acceder al Sheet.

**Solución**:
  1. Ejecuta la función `getNextFormId` manualmente desde el editor
  2. Te pedirá autorizar permisos
  3. "Revisar permisos" → elegir tu cuenta → "Advanced" → "Go to..."
  4. "Allow"
  5. Después de esto, todas las funciones tendrán permiso

## Problemas con el Sheet

### Las celdas aparecen como "###"

**Síntoma**: En el Sheet veo "###" en vez del contenido.

**Causa**: La columna es demasiado angosta.

**Solución**: Doble clic en el borde derecho del encabezado de columna
para autoajustar, o arrastra el borde para hacer la columna más ancha.

### Los headers no aparecen con formato azul

**Síntoma**: Los headers están en negro/normal, no con el formato azul
del Cerro Azul.

**Causa**: El formato no se aplicó, o se perdió al editar.

**Solución**:
  1. Selecciona la fila 1 completa
  2. Color de fondo: `#0066CC` (o tu color)
  3. Color de texto: blanco, negrita
  4. Congelar: Vista → Inmovilizar → 1 fila

### No puedo compartir el Sheet

**Síntoma**: Quiero darle acceso a otra persona al Sheet pero no me deja.

**Causa**: La cuenta actual no es owner del Sheet.

**Solución**:
  · Pide al owner que te agregue como editor
  · O trabaja desde una cuenta que sea owner

## Problemas de los residentes

### "Perdí mi N° de formulario"

**Solución para la administración**:
  1. Pide al residente su N° de apartamento y cédula
  2. Abre el Sheet
  3. Busca la fila con ese N° de apartamento
  4. La columna A tiene el N° de Formulario (ej: CA-0042)
  5. Dile el N° de Formulario al residente

### "Llené el formulario dos veces"

**Síntoma**: Un residente envió el mismo formulario dos veces.

**Causa**: El backend SÍ previene duplicados por N° Apto, pero si el residente
lo llena dos veces seguidas desde dispositivos diferentes, ambas llegan
con el mismo N° Apto.

**Solución**:
  · La segunda vez que intente enviar con el mismo N° Apto, el backend
    le dirá: "Ya existe un registro para el apartamento X. Tu N° de
    formulario es CA-XXXX. Usa la opción EDITAR MI REGISTRO"
  · Si ambas se guardaron (caso raro por race condition), la admin puede
    borrar manualmente la fila duplicada del Sheet

### "No me deja enviar, dice que faltan datos"

**Síntoma**: El residente llenó todo pero la página le pide datos obligatorios.

**Causa**: Algún campo obligatorio está vacío, posiblemente el checkbox de
autorización o la firma.

**Solución**:
  · Verificar que se marcaron TODOS los checkboxes de la sección 11
  · Verificar que se llenaron nombre Y cédula en la firma
  · El frontend resaltará en rojo los campos faltantes y hará scroll
    automáticamente al primero

## Errores comunes en la consola del navegador

### "Mixed Content"

**Causa**: La página se carga por HTTPS pero algún recurso por HTTP.

**Solución**: Verifica que TODOS los recursos (CSS, JS, imágenes) usen
HTTPS o rutas relativas (que se resuelven a HTTPS automáticamente).

### "Refused to connect" / "CORS"

**Causa**: El Apps Script no está bien configurado o la URL es incorrecta.

**Solución**:
  1. Verifica la URL del Web App en `js/app.js` línea 5
  2. Prueba la URL en el navegador:
     `https://script.google.com/macros/s/[TU_ID]/exec?action=nextId`
     Debe devolver JSON, no error
  3. Si devuelve error, el deployment está mal → ver sección Apps Script arriba

### "404 Not Found" en el POST

**Causa**: La URL del Web App cambió o es incorrecta.

**Solución**:
  1. Ve a Apps Script → Implementar → Administrar implementaciones
  2. Verifica que el Web App existe y copia la URL actual
  3. Actualiza `js/app.js` con la URL correcta

## Contacto para soporte técnico

Si nada de esto resuelve tu problema:

  1. Captura de pantalla del error (consola del navegador abierta con F12)
  2. URL del Web App (sin revelarla públicamente)
  3. Pasos para reproducir el error
  4. Mensaje de error exacto

Y compártelo con quien te implementó el sistema o abre un issue en el
repositorio de GitHub.
