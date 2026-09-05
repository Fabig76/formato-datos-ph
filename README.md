# Formato de Datos PH — Plantilla Reusable para Propiedades Horizontales

Sistema completo para crear un **formulario público** (accedido vía QR) que
permita a residentes y propietarios de cualquier propiedad horizontal
actualizar sus datos en un Google Sheet, conforme a la **Ley 1581 de 2012**
y al **Decreto 768 de 2025** (Colombia).

## ¿Qué problema resuelve?

Las copropiedades en Colombia necesitan mantener una base de datos actualizada
de residentes, propietarios, vehículos, mascotas, contactos de emergencia,
etc. Los métodos tradicionales (formularios impresos, llamadas, WhatsApp)
son lentos, costosos, generan datos incompletos y son difíciles de auditar.

Este sistema convierte el formato PDF oficial (que toda PH maneja) en un
formulario web público responsive, conectado a Google Sheets, con
**deduplicación automática por número de apartamento** y **trazabilidad**
de quién envió y cuándo.

## Implementación de referencia: Urbanización Cerro Azul

El sistema fue desarrollado para la **Urbanización Cerro Azul** (NIT 900770444,
Bello / Niquía) y está en producción.

  · Formulario público: https://fabig76.github.io/cerro-azul-residentes/
  · Repositorio específico: https://github.com/Fabig76/cerro-azul-residentes
  · Google Sheet: https://docs.google.com/spreadsheets/d/16gxeAkcTIWnuwkBFBaHW7Y-nUHaMdtovNzUBaupytPc

El código de Cerro Azul está copiado verbatim en la carpeta
[`implementaciones/cerro-azul/`](implementaciones/cerro-azul/) de este
repositorio, listo para servir como ejemplo punto por punto.

## Arquitectura

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│   Residente escanea QR ──► Abre página pública (GitHub Pages)    │
│                                  │                               │
│                                  ▼                               │
│                          Formulario HTML/CSS/JS                  │
│                                  │                               │
│                                  ▼                               │
│                    Google Apps Script Web App                    │
│                                  │                               │
│                                  ▼                               │
│                            Google Sheets                         │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Componentes

  1. **Página web estática en GitHub Pages** — pública, sin servidor, sin login
     · Tema claro con colores personalizables del logo
     · 11 secciones que corresponden a los bloques del PDF original
     · Validación de obligatorios en cliente
     · Modo crear / modo editar (por N° de apartamento + N° de formulario)
     · Responsive (móvil + desktop, importante para QR)

  2. **Google Apps Script** como backend sin servidor
     · Web App desplegada con permisos "Cualquier persona"
     · Recibe los datos vía POST y los escribe al Sheet
     · Genera N° de formulario correlativo automático (CA-0001, CA-0002, ...)
     · Dedupe: un apartamento = un solo registro
     · Edición con doble verificación (N° Form + N° Apto)
     · Nunca borra filas (los residentes no pueden eliminar)

  3. **Google Sheets** como base de datos
     · Una hoja "Registros" con todas las columnas
     · Encabezados formateados con colores de la PH
     · Validaciones de tipo de dato (listas desplegables, etc.)
     · Hoja auxiliar "Maestros" para catálogos (listado de aptos, etc.)

  4. **QR generado** apuntando a la URL pública de GitHub Pages

### ¿Por qué esta arquitectura?

  · **Cero costos**: GitHub Pages, Apps Script y Google Sheets son gratis
  · **Cero mantenimiento de servidor**: Apps Script escala solo, Google lo hospeda
  · **Cero infraestructura que administrar**: solo archivos en Drive y código en GitHub
  · **Seguro**: el Apps Script valida en servidor antes de escribir al Sheet
  · **Auditable**: cada fila tiene timestamp de creación y última edición
  · **Fácil de replicar**: ~30 minutos para implementar en otra PH

## Estructura del repositorio

```
formato-datos-ph/
├── README.md                          ← Este archivo
├── index.html                         ← Landing page (se sirve en GitHub Pages)
├── LICENSE                            ← MIT
├── docs/
│   ├── guia-proyecto.md               ← 📌 LEER PRIMERO: contexto completo, IDs, problemas, decisiones
│   ├── guia-implementacion.md         ← Paso a paso detallado
│   ├── arquitectura.md                ← Decisiones técnicas
│   ├── seguridad-y-privacidad.md      ← Ley 1581, manejo de datos sensibles
│   ├── personalizacion.md             ← Cómo adaptar a tu PH
│   └── troubleshooting.md            ← Problemas comunes
├── plantillas/
│   ├── configuracion-ph.md            ← Plantilla de configuración por PH
│   ├── campos-formulario.md           ← Lista de campos del formulario oficial
│   └── correo-autorizacion.md         ← Plantilla de correo para residentes
└── implementaciones/
    └── cerro-azul/                    ← Código completo de Cerro Azul (referencia)
        ├── README.md
        ├── apps-script/
        │   ├── Codigo.gs              ← Backend completo
        │   └── README.md              ← Cómo desplegar
        ├── web/
        │   ├── index.html
        │   ├── assets/
        │   │   ├── logo.jpg
        │   │   └── styles.css
        │   └── js/
        │       └── app.js
        ├── qr/
        │   └── qr-formulario-cerro-azul.png
        └── docs/
            └── capturas-pantalla/
```

> 💡 **Para retomar trabajo en este proyecto**, lee primero
> [`docs/guia-proyecto.md`](docs/guia-proyecto.md) — contiene todos los
> IDs, URLs, decisiones de diseño, problemas encontrados y soluciones.
> Es la "memoria del proyecto" para futuras sesiones.

## Cómo implementar en tu propiedad horizontal

Lee [`docs/guia-implementacion.md`](docs/guia-implementacion.md) para el
paso a paso completo (~30-45 minutos).

Resumen ultra-corto:

  1. Crear Google Sheet con 138 columnas (o el número que aplique a tu formato)
  2. Crear el repo GitHub Pages con la página web (copiar de Cerro Azul)
  3. Crear el Apps Script (copiar de Cerro Azul, ajustar SHEET_ID)
  4. Desplegar Apps Script como Web App
  5. Pegar la URL del Web App en `js/app.js`
  6. Generar el QR
  7. Distribuir a los residentes

## Personalización

Cada PH tiene:
  · Nombre propio (ej: "Urbanización Cerro Azul")
  · NIT
  · Dirección
  · Logo propio
  · Paleta de colores del logo
  · Correo de contacto de la administración
  · (Opcional) Campos adicionales específicos

La sección [`docs/personalizacion.md`](docs/personalizacion.md) explica
cómo adaptar el código de Cerro Azul a cualquier otra PH en ~10 minutos.

## Seguridad y privacidad

  · El formulario cumple con la **Ley 1581 de 2012** (protección de datos personales)
  · Aviso legal destacado sobre la obligatoriedad de datos reales
  · El residente firma digitalmente con nombre + cédula
  · El Sheet es privado (solo accesible para la administración)
  · Ver [`docs/seguridad-y-privacidad.md`](docs/seguridad-y-privacidad.md)
    para el análisis completo de riesgos y mitigaciones

## Limitaciones conocidas

  · El QR da acceso público al endpoint de envío. Las validaciones del
    Apps Script evitan datos vacíos pero NO impiden que alguien
    técnicamente sofisticado envíe datos falsos. La administración debe
    validar el Sheet periódicamente.
  · El residente debe recordar su N° de formulario para editar. Si lo pierde,
    debe solicitarlo por correo a la administración.
  · El formulario no soporta adjuntar archivos (fotos de mascotas, etc.)

## Licencia

MIT. Úsalo libremente en cualquier propiedad horizontal.

## Créditos

  · Diseñado e implementado por Hermes Agent para Fabio Lesmes / Urbanización Cerro Azul
  · Basado en el formato oficial colombiano de manejo de datos de residentes
    en propiedad horizontal (Ley 1581 de 2012 + Decreto 768 de 2025)
  · Implementación inicial: Septiembre 2026
