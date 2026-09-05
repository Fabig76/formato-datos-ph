# Guía de Implementación Paso a Paso

Esta guía te lleva de cero a un formulario público funcionando para tu
propiedad horizontal. Tiempo estimado: **30-45 minutos** la primera vez,
**15 minutos** si copias de una implementación existente.

## Pre-requisitos

Necesitas:
  · Cuenta de Google (Gmail o Google Workspace) — esta será la **cuenta administradora**
  · Acceso a internet
  · 30-45 minutos ininterrumpidos
  · (Opcional) Conocimientos básicos de copiar/pegar en editor de código

## Decisiones que debes tomar ANTES de empezar

Responde estas preguntas antes de continuar. Te van a hacer falta en pasos
posteriores:

  1. **Nombre oficial de la copropiedad** (ej: "Urbanización Cerro Azul", "Edificio Las Acacias PH")
  2. **NIT** de la copropiedad (lo encuentras en la cámara de comercio o en el RUT)
  3. **Dirección** completa
  4. **Correo de la administración** (ej: administracion@mi-ph.com, ph.mi-conjunto@gmail.com)
  5. **¿Vas a usar el formulario estándar de 11 secciones** o tienes secciones adicionales (inquilinos especiales, locales comerciales, parqueaderos de visitantes)?
  6. **¿Quieres permitir que los residentes editen** o solo enviar (1 sola vez)?

Si tus respuestas son las del "estándar" (como Cerro Azul), puedes saltar
a la siguiente sección. Si tienes campos personalizados, lee primero
[`personalizacion.md`](personalizacion.md).

## Paso 1: Crear el Google Sheet destino (10 min)

### 1.1 Crear el spreadsheet

  1. Abre https://sheets.google.com en la cuenta administradora
  2. Clic en **+ En blanco**
  3. Nómbralo: **"Base datos [Nombre de tu PH]"** (ej: "Base datos Cerro azul formato")
  4. Anota el **ID del Sheet** — aparece en la URL entre `/d/` y `/edit`:
     `https://docs.google.com/spreadsheets/d/`**`ESTE_ES_EL_ID`**`/edit`
     Guárdalo, lo vas a necesitar muchas veces.

### 1.2 Renombrar la hoja principal

  1. En la pestaña inferior dice "Hoja 1"
  2. Doble clic en ella y renómbrala a: **"Registros"**

### 1.3 Escribir los encabezados de las columnas

Los encabezados van en la fila 1, de A1 en adelante. El número exacto
depende de tu formato, pero para el formato estándar colombiano son **138
columnas**.

**Opción A (más fácil):** Copia de la implementación de Cerro Azul.

  1. Abre https://docs.google.com/spreadsheets/d/16gxeAkcTIWnuwkBFBaHW7Y-nUHaMdtovNzUBaupytPc
  2. En una pestaña nueva, ve a "Archivo → Hacer una copia" para tener
     una plantilla editable. NO necesitas copiar el Sheet entero, solo la
     fila 1.
  3. Copia la fila 1 completa de la plantilla al Sheet nuevo.

**Opción B (manual):** Usa el script de Python `scripts/crear-encabezados.py`
de la carpeta [`scripts/`](../scripts/) de este repo.

### 1.4 Formatear la fila de encabezados

  1. Selecciona toda la fila 1
  2. Color de fondo: el azul principal del logo de tu PH (ej: `#0066CC`)
  3. Color de texto: blanco
  4. Negrita
  5. Centrar texto
  6. Altura de fila: 50px
  7. **Congelar fila 1**: Vista → Inmovilizar → 1 fila

### 1.5 Crear hoja auxiliar "Maestros"

  1. Clic en el **+** al lado de "Registros" abajo a la izquierda
  2. Nómbrala: **"Maestros"**
  3. En la fila 1 escribe los encabezados: `N° Apto`, `Estado`, `Notas`
     (opcional — útil para validaciones futuras)

### 1.6 Validaciones

Sugeridas para empezar:
  · Columna "Diligencia como": lista desplegable con
    `Propietario`, `Arrendatario`, `Tenedor / Otro`
  · (Opcional) Columna "Masc - Manejo especial": Sí / No

### 1.7 Compartir el Sheet con quien va a ser administrador

Si más de una persona va a administrar:
  1. Clic en "Compartir" arriba a la derecha
  2. Agregar correos con rol "Editor"
  3. NO compartir con "Cualquier persona con el enlace" — el Sheet es privado

## Paso 2: Crear el repositorio GitHub (10 min)

Necesitas cuenta en GitHub. Si no tienes, créala gratis en https://github.com/signup.

### 2.1 Crear el repo

  1. Ve a https://github.com/new
  2. Nombre: `[tu-ph]-residentes` (ej: `cerro-azul-residentes`,
     `edificio-las-acacias-residentes`)
  3. Descripción: "Formulario público de actualización de datos de
     residentes — [Nombre PH] ([NIT])"
  4. **Público** (obligatorio para GitHub Pages gratis)
  5. NO inicialices con README (lo agregamos nosotros)
  6. Clic en "Create repository"

### 2.2 Subir los archivos

**Opción A (más fácil, sin Git):** Subir archivos vía interfaz web
  1. En la página del repo nuevo, clic en "uploading an existing file"
  2. Arrastra los archivos de la carpeta `implementaciones/cerro-azul/web/`
     (HTML, CSS, JS, logo)
  3. Commit message: "Formulario público inicial"
  4. Clic en "Commit changes"

**Opción B (con Git, mejor para colaboradores futuros):**
  ```bash
  cd /ruta/a/donde/quieras
  git clone https://github.com/Fabig76/[tu-ph]-residentes.git
  cp -r ../formato-datos-ph/implementaciones/cerro-azul/web/* [tu-ph]-residentes/
  cd [tu-ph]-residentes
  git add . && git commit -m "Formulario público inicial"
  git push -u origin main
  ```

### 2.3 Activar GitHub Pages

  1. En el repo, ve a **Settings** (pestaña arriba)
  2. En el menú izquierdo: **Pages**
  3. Source: **Deploy from a branch**
  4. Branch: **main**, folder: **/(root)**
  5. Clic en **Save**
  6. Espera 1-2 minutos. La URL pública aparece:
     `https://[usuario-github].github.io/[nombre-repo]/`

**Verificar**: Abre la URL. Deberías ver el formulario.

### 2.4 Personalizar con datos de tu PH

Edita el archivo `index.html` del repo (clic en el ícono de lápiz):

Busca y reemplaza:
  · `Urbanización Cerro Azul` → tu PH
  · `900770444` → tu NIT
  · `Bello / Niquía` → tu dirección
  · `urb.cerroazul@gmail.com` → correo de tu administración
  · `assets/logo.jpg` → si tienes logo propio, reemplaza el archivo

Para el logo:
  1. Sube tu logo al repo: clic en "Add file" → "Upload files" → arrastra el logo
  2. Si el nombre es distinto a `logo.jpg`, actualiza el `src=` en `index.html`

Para los colores del tema:
  1. Abre `assets/styles.css`
  2. Busca las variables CSS al inicio (`:root { ... }`)
  3. Cambia `--azul` por el color principal de tu PH

Commit y push los cambios. La página se actualiza en 1 minuto.

## Paso 3: Crear el Apps Script backend (10 min)

### 3.1 Crear el proyecto

  1. Abre https://script.google.com en la **cuenta administradora**
  2. Clic en **+ Nuevo proyecto**
  3. Renómbralo: `[Nombre PH] - Formulario Residentes Backend`

### 3.2 Pegar el código

  1. En el panel izquierdo verás "Código.gs"
  2. Borra el contenido por defecto
  3. Abre el archivo `implementaciones/cerro-azul/apps-script/Codigo.gs`
     de este repo, clic en "Raw" → Ctrl+A → Ctrl+C
  4. Vuelve al editor de Apps Script → Ctrl+V
  5. **AJUSTA LAS CONSTANTES** en las primeras líneas del archivo:
     ```js
     const SHEET_ID = 'TU_SHEET_ID_AQUI';  // ← Pega aquí el ID de tu Sheet
     const SHEET_NAME = 'Registros';
     const NUM_COLS = 138;  // ← Si tu formato tiene otras columnas, ajusta
     ```
  6. **PERSONALIZA LA AUTORIZACIÓN**: Busca el texto de la sección 11
     donde dice "Urbanización Cerro Azul (NIT 900770444)" y reemplázalo
     con tu PH + NIT
  7. **PERSONALIZA EL CORREO**: Donde dice "urb.cerroazul@gmail.com",
     pon el correo de tu administración (aparece en 2-3 lugares)
  8. Ctrl+S para guardar

### 3.3 Ejecutar manualmente para autorizar permisos (importante)

  1. En el dropdown de funciones (arriba en el medio), selecciona `getNextFormId`
  2. Clic en **Ejecutar** (▶️)
  3. La primera vez te pide autorizar permisos:
     · "Revisar permisos" → elegir tu cuenta
     · "Advanced" → "Go to [nombre del proyecto] (unsafe)" → "Allow"
  4. Si da error "no se encontró Registros" u otro, es normal — solo era
     para autorizar. Si da un número de formulario (ej: "CA-0001"),
     todo está bien.

### 3.4 Desplegar como Web App

  1. Arriba a la derecha: **Implementar** → **Nueva implementación**
  2. Clic en el ícono del engranaje ⚙️ → selecciona **Aplicación web**
  3. Configuración:
     · **Descripción**: `Backend formulario residentes v1`
     · **Ejecutar como**: **Yo** ([tu correo])
     · **Quién tiene acceso**: **Cualquier persona**
  4. Clic en **Implementar**
  5. Te pedirá autorizar de nuevo (es la primera vez para el deployment)
  6. **MUY IMPORTANTE**: Copia la URL que aparece. Formato:
     `https://script.google.com/macros/s/AKfycb.../exec`

## Paso 4: Conectar la página web al backend (2 min)

  1. Vuelve al repo de GitHub
  2. Abre el archivo `js/app.js`
  3. Busca la línea 5 (más o menos):
     ```js
     const APPS_SCRIPT_URL = '...';
     ```
  4. Reemplaza con la URL del Web App que copiaste en el paso 3.4
  5. Commit changes
  6. Espera 1 minuto a que GitHub Pages publique

## Paso 5: Probar end-to-end (5 min)

  1. Abre la URL pública de tu formulario
  2. Llena los campos obligatorios con datos de prueba
  3. Clic en "Enviar formulario"
  4. Deberías ver un mensaje verde con un N° de formulario tipo CA-0001
  5. Abre el Google Sheet y verifica que aparece una nueva fila
  6. Vuelve a la página, clic en "Editar mi registro", ingresa el N°
     de formulario y el N° de apartamento → debe cargar los datos para editar
  7. Modifica algo y guarda → debe actualizar la misma fila

Si todo funciona: **¡listo!**

## Paso 6: Generar el QR (2 min)

  1. Desde la terminal con Python:
     ```bash
     pip install --break-system-packages qrcode[pil] pillow
     python scripts/generar-qr.py "https://TU_USUARIO.github.io/TU_REPO/"
     ```
  2. El script genera dos archivos:
     · `qr-formulario.png` (con texto decorado, listo para imprimir)
     · `qr-solo.png` (solo el QR, para casos minimalistas)

  3. Sube ambos a la carpeta de Drive de la PH

  4. Imprime el QR con texto y pégalo en:
     · Cartelera del lobby/portería
     · Ascensores
     · Grupos de WhatsApp del conjunto
     · Correo a residentes

## Paso 7: Comunicar a los residentes (10 min)

Usa la plantilla en [`plantillas/correo-autorizacion.md`](../plantillas/correo-autorizacion.md)
y personalízala con los datos de tu PH.

Recomendaciones:
  · Envía el correo a TODOS los residentes, no solo a quienes administran
  · Adjunta el QR como imagen
  · Indica claramente la fecha límite para completar el formulario
  · Ofrece ayuda presencial para quienes no sepan usar QR / internet

## Mantenimiento

  · **Revisar el Sheet periódicamente**: una vez por semana o cada 2 semanas,
    abre el Sheet, verifica que no haya registros sospechosos (datos falsos,
    duplicados), comunícate con quien envió si hay algo raro.
  · **Responder a quienes perdieron su N° de formulario**: cada cierto tiempo
    alguien te va a escribir pidiendo ayuda. Ten a mano una forma de buscar
    por N° de apartamento para ayudarlos.
  · **Actualizar el backend si cambian las leyes**: si sale un nuevo decreto
    que modifique el formato, actualiza el código del Apps Script + la página
    web + el Sheet.
  · **Hacer backup del Sheet**: Google Drive tiene versionado, pero un export
    a Excel/PDF mensual es buena práctica.

## Próximos pasos opcionales

Una vez que el sistema básico esté funcionando, puedes:

  · Agregar **autenticación con token**: que cada residente reciba un token
    único por correo para verificar que es quien dice ser.
  · **Notificaciones automáticas**: que el Apps Script envíe un correo de
    confirmación a la administración cada vez que alguien envía.
  · **Dashboard de administración**: una página privada donde la admin
    vea estadísticas (cuántos apartamentos han enviado, cuántos faltan).
  · **Exportación a PDF**: para imprimir comprobantes por residente.

Si te interesa alguno de estos, pregúntale a Hermes y te lo implementa.

---

**¿Atascado en algún paso?** Revisa [`troubleshooting.md`](troubleshooting.md).
Si no está la solución ahí, pregúntale a Hermes.
