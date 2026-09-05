# Arquitectura Técnica

Este documento explica las decisiones técnicas detrás del sistema, para
futuros mantenedores o para quien quiera adaptar el código.

## Stack tecnológico

  · **Frontend**: HTML5 + CSS3 + JavaScript (ES6+) vanilla. Cero
    dependencias externas, cero frameworks. Funciona en cualquier
    navegador moderno, incluyendo móviles viejos.
  · **Hosting**: GitHub Pages (estático, HTTPS gratis, CDN global).
  · **Backend**: Google Apps Script como Web App. Ejecuta JavaScript del
    lado del servidor con acceso a las APIs de Google Workspace.
  · **Base de datos**: Google Sheets (estructura tabular, acceso por API,
    colaboración nativa).
  · **Generación de QR**: Python con `qrcode` + `Pillow` (ejecutado una vez).

## ¿Por qué no usar frameworks JS?

React, Vue, Angular son poderosas pero overkill para esto:
  · El formulario es estático, no necesita reactividad compleja
  · Cero dependencias = cero actualizaciones de seguridad, cero `node_modules`
  · El navegador del residente (muchas veces un celular viejo) carga instant
  · El código es legible por cualquier desarrollador sin curva de aprendizaje
  · El repo pesa menos de 50 KB

## ¿Por qué Google Apps Script y no Firebase, AWS Lambda, etc.?

  · **Costo cero**: las alternativas cuestan dinero a partir de cierto uso
  · **Acceso nativo a Google Sheets**: con Firebase/AWS necesitas API keys,
    conexión a Google, facturación de egress...
  · **Cero DevOps**: Google hospeda, escala, y mantiene el código
  · **Tiempo de respuesta**: <500ms para una petición típica
  · **El residente no necesita cuenta de Google**: la URL del Web App es
    pública, cualquiera puede hacer POST/GET sin auth

Limitaciones:
  · No es ideal para >10K requests/día (límite de Apps Script)
  · Cold start puede ser lento (primer request del día)
  · Más difícil de testear que un backend tradicional

## Flujo de datos detallado

### Envío de un nuevo registro

```
[Residente]
   │ Escanea QR
   ▼
[GitHub Pages - index.html]
   │ Llena formulario, validación cliente
   ▼
[fetch() POST al Web App URL]
   │ Body: JSON con todos los campos
   │ Headers: Content-Type: text/plain (workaround CORS Apps Script)
   ▼
[Apps Script - doPost()]
   │ 1. Parsea JSON
   │ 2. Valida campos obligatorios
   │ 3. Si falta algo → JSON error
   │ 4. Si OK → submitRecord()
   ▼
[submitRecord()]
   │ 1. Busca si ya existe registro con ese N° Apto
   │ 2. Si existe → error con mensaje amigable
   │ 3. Si no → genera nuevo N° Form (getNextFormId)
   │ 4. Construye array de 138 valores (buildRowFromPayload)
   │ 5. Escribe fila en el Sheet
   ▼
[Sheet]
   │ Nueva fila con timestamp + hash dedupe
   ▼
[Respuesta JSON al frontend]
   │ { ok: true, numForm: "CA-0042", message: "..." }
   ▼
[Frontend muestra tarjeta de éxito]
```

### Edición de un registro existente

```
[Residente]
   │ Va a pestaña "Editar mi registro"
   ▼
[Ingresa N° Form + N° Apto]
   │
   ▼
[fetch() GET al Web App URL?action=lookup&numForm=X&apto=Y]
   │
   ▼
[Apps Script - doGet() con action=lookup]
   │ 1. findRowByNumFormAndApto()
   │ 2. Si no encuentra → error
   │ 3. Si encuentra → rowToObject() convierte fila a JSON
   ▼
[Frontend recibe objeto JS, poblarFormulario()]
   │ Llena todos los campos del formulario
   │ Modo = 'edit'
   ▼
[Residente modifica y guarda]
   │
   ▼
[fetch() POST con editMode=true]
   │
   ▼
[submitRecord() con editMode]
   │ 1. Verifica que numForm+apto coincidan con fila existente
   │ 2. Si no → error de seguridad
   │ 3. Si sí → actualiza fila (mismo rowNumber)
   │ 4. NO incrementa N° Form (conserva el original)
   ▼
[Sheet actualizado + respuesta JSON]
```

## Estructura del Sheet

### Hoja "Registros" (138 columnas, A1:EH1)

Los nombres de las columnas siguen una convención:

  · `N° Formulario` (A) — ID único del registro
  · `Fecha Registro` (B) — ISO datetime de creación
  · `Fecha Última Edición` (C) — ISO datetime de la última modificación
  · `N° Apto` (D) — **Llave de dedupe** (un apartamento = un registro)
  · `Diligencia como` (E) — Propietario / Arrendatario / Tenedor
  · `Nombre/CC/Correo/Celular Propietario` (F-J) — titular
  · `Parqueaderos / Matrículas` (K-L)
  · Datos del arrendatario (M-P)
  · Parqueadero autorizado a tercero (Q-S)
  · Inmobiliaria/representante (T-X)
  · Residentes (Y-AN, 4 personas × 5 campos)
  · Menores (AO-AT, 4 personas × 3 campos)
  · Vehículos (AU-BF, 2 vehículos × 6 campos)
  · Motas (BG-BR, 2 motos × 6 campos)
  · Bicicletas (BS-CB, 2 bicis × 4 campos)
  · Llaveros/tags autorizados (CC-CD)
  · Dispositivos (CE-DO, 3 dispositivos × 5 campos)
  · Mascotas (DP-FI, 2 mascotas × 10 campos)
  · Emergencias (FJ-FO, 2 contactos × 3 campos)
  · Autorizaciones (FP-FR)
  · Firma (FS-FU)
  · Hash Dedupe (FV) — sha256[:16] de apto+cc+firma

### Hoja "Maestros"

Tabla auxiliar con:
  · `N° Apto` — listado de todos los apartamentos de la PH
  · `Estado` — Activo / Inactivo / En venta
  · `Notas` — observaciones (cambio de propietario, etc.)

**Uso futuro**: cuando el formulario se envíe, validar contra esta hoja
que el N° Apto existe en la PH. Si quieres implementar esto, es un cambio
de ~20 líneas en `Codigo.gs`.

## Decisiones de diseño controversiales

### ¿Por qué `Content-Type: text/plain` en vez de `application/json`?

Apps Script Web App NO soporta CORS preflight para `application/json`.
Si el frontend manda `application/json`, el navegador hace un OPTIONS
preflight, Apps Script no responde correctamente, y el POST falla.

**Workaround**: enviar el body como `text/plain`. Apps Script igual parsea
el contenido como string y nosotros lo parseamos a JSON en `doPost()`.
Esto evita el preflight completamente.

Tradeoff: perdemos validación de tipo de body en el navegador. Pero
como el frontend SIEMPRE envía JSON.stringify(), no es problema real.

### ¿Por qué no usar `Mode: no-cors`?

`no-cors` permite hacer POST pero la respuesta es opaca (no se puede leer).
Necesitamos leer la respuesta para saber si fue exitoso y mostrar el N° de
formulario al residente. Por eso usamos `text/plain` + CORS simple.

### ¿Por qué no guardar el Sheet en GitHub en vez de Google Sheets?

GitHub NO es buena base de datos:
  · Difícil de consultar/filtrar como Sheets
  · No permite edición colaborativa nativa
  · No genera gráficos ni tablas dinámicas
  · Git no escala bien con muchos registros (commits lentos)

### ¿Por qué SHA-256 en columna Hash Dedupe?

Para auditoría: detecta si alguien intenta enviar el mismo apto+cc+firma
otra vez. Como el N° Apto ya es la llave única, este hash es redundante,
pero es útil para:
  · Detectar envíos automatizados (mismo hash repetido N veces)
  · Auditoría de la administración
  · Verificación rápida de integridad

## Performance

  · **Cold start del Web App**: hasta 5 segundos la primera vez al día.
    Después es instantáneo.
  · **Tiempo de respuesta típico**: 1-2 segundos (validación + escritura)
  · **Carga de la página**: <500ms (HTML+CSS+JS pesan ~50KB sin comprimir)
  · **Capacidad**: hasta ~10K requests/día según documentación de Apps Script
  · **Para >100 apartamentos** (caso típico PH colombiano): rendimiento excelente

## Seguridad (resumen)

  · El Apps Script valida en servidor antes de escribir al Sheet
  · El Sheet es privado (solo accesible para la cuenta administradora)
  · La página pública NO expone el Sheet ni los datos
  · El QR apunta a la página pública, no al Sheet
  · HTTPS en todo el flujo (GitHub Pages + Apps Script)

**Lo que NO está protegido**:
  · Cualquier persona con la URL del Web App puede enviar datos al Sheet
  · Las validaciones del Apps Script son básicas (solo obligatorios)
  · No hay rate limiting: alguien podría hacer spam con un script
  · No hay CAPTCHA: bots pueden enviar formularios

**Mitigaciones recomendadas para producción seria**:
  · Implementar un token compartido: cada residente recibe un token único
    por correo, debe ingresarlo para enviar (más seguro, menos conveniente)
  · Rate limiting: Apps Script puede usar CacheService para limitar a
    N envíos por IP por hora
  · Revisión periódica del Sheet por la administración

Ver [`seguridad-y-privacidad.md`](seguridad-y-privacidad.md) para el
análisis completo.
