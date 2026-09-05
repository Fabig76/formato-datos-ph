# Implementación de Referencia: Urbanización Cerro Azul

Esta carpeta contiene **verbatim** el código que está en producción para la
**Urbanización Cerro Azul** (NIT 900770444, Bello / Niquía).

Sirve como **ejemplo punto por punto** de cómo queda una implementación
completa del sistema.

## URLs en producción

  · Formulario público: https://fabig76.github.io/cerro-azul-residentes/
  · Repositorio: https://github.com/Fabig76/cerro-azul-residentes
  · Google Sheet: https://docs.google.com/spreadsheets/d/16gxeAkcTIWnuwkBFBaHW7Y-nUHaMdtovNzUBaupytPc
  · QR en Drive: https://drive.google.com/file/d/12OuEtvwb72m9YZkxpqWteeRIExbIf3cv/view

## Estructura

```
cerro-azul/
├── apps-script/
│   ├── Codigo.gs              ← Backend completo
│   └── README.md              ← Cómo desplegar el Web App
├── web/
│   ├── index.html             ← Página principal
│   ├── assets/
│   │   ├── logo.jpg           ← Logo del conjunto
│   │   └── styles.css         ← Estilos (azul Cerro Azul)
│   └── js/
│       └── app.js             ← Lógica del formulario
├── qr/
│   └── qr-formulario-cerro-azul.png    ← QR generado, listo para imprimir
└── docs/
    └── capturas-pantalla/     ← (Vacío — agregar capturas reales)
```

## ¿Cómo usar este código como base para otra PH?

Sigue los pasos en [`../../docs/personalizacion.md`](../../docs/personalizacion.md).
En resumen:

  1. Copia la carpeta `web/` a un nuevo repo de GitHub
  2. Reemplaza el logo (`web/assets/logo.jpg`)
  3. Cambia textos en `web/index.html` (buscar/reemplazar "Cerro Azul",
     "900770444", "urb.cerroazul@gmail.com", etc.)
  4. Cambia colores en `web/assets/styles.css` (variables CSS al inicio)
  5. Copia `apps-script/Codigo.gs` a un nuevo proyecto Apps Script
  6. Cambia `SHEET_ID` en `Codigo.gs`
  7. Despliega como Web App
  8. Pega la URL del Web App en `web/js/app.js`
  9. Genera nuevo QR con `../../scripts/generar-qr.py`

## Diferencias con el código "plantilla" genérico

El código de Cerro Azul es el código "vivo", con todas las pequeñas
modificaciones que se hicieron durante la implementación:

  · Textos específicos del Cerro Azul (NIT, dirección, correos)
  · Optimizaciones específicas (ej: lógica de búsqueda por apto)
  · Datos de prueba que quedaron en el Sheet (CA-0001, CA-0002 si no se
    limpiaron)

Si quieres usar esto como base para una PH nueva, RECOMENDAMOS:
  · Hacer una copia del repo `formato-datos-ph` (este repo) en lugar de
    `cerro-azul-residentes`, ya que es el código "neutro"
  · O copiar la carpeta `web/` y `apps-script/` de Cerro Azul y limpiar
    los textos específicos

## Historial de implementación

  · **Septiembre 2026**: Implementación inicial para Cerro Azul
    · Setup del Sheet destino (138 columnas)
    · Creación del repo público cerro-azul-residentes
    · Activación de GitHub Pages
    · Implementación del Apps Script Web App
    · Pruebas end-to-end
    · Generación del QR
    · Distribución a residentes (pendiente)

## Métricas de la implementación

  · **Tiempo total de implementación**: ~3 horas (incluyendo iteraciones
    por problemas con OAuth de Hermes y configuración de Apps Script)
  · **Tiempo si se replica desde esta plantilla**: ~30-45 minutos
  · **Tamaño del código**: ~50 KB (HTML + CSS + JS sin comprimir)
  · **Costo mensual**: $0 (todo en plan gratuito)
  · **Mantenimiento**: ~1 hora/mes para revisar el Sheet

## Lecciones aprendidas

  1. Apps Script Web App con doPost funciona correctamente desde navegador
     pero da errores confusos cuando se prueba con curl. **Usar SIEMPRE
     navegador para pruebas.**
  2. Google requiere que el Apps Script se cree desde la cuenta que es
     OWNER del Sheet, no desde una cuenta con rol de writer. Si no, los
     permisos pueden no funcionar bien.
  3. GitHub Pages sirve `README.md` como página principal si Jekyll está
     activado. Agregar `.nojekyll` en la raíz para evitarlo.
  4. El Dedupe por N° Apto + N° de Formulario es suficiente para que
     un residente pueda editar sus datos. La clave es comunicar bien
     que DEBE guardar el N° de Formulario.
  5. El aviso legal destacado en la cabecera es fundamental para cumplir
     con la Ley 1581/2012. No sacrifiques su visibilidad por estética.
