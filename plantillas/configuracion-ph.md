# Configuración de Propiedad Horizontal

Copia este archivo, llénalo con los datos de tu PH, y guárdalo como
referencia cuando implementes el sistema.

## Datos básicos

```
Nombre oficial:        ____________________________________________
Sigla o nombre corto:  ____________________________________________
Tipo:                  [ ] Urbanización  [ ] Edificio  [ ] Conjunto Residencial
                        [ ] Otro: _______________________________
NIT:                   ____________________________________________
Dirección completa:    ____________________________________________
                        ____________________________________________
Ciudad/Municipio:      ____________________________________________
Departamento:          ____________________________________________
```

## Datos de contacto

```
Correo de la administración:      ____________________________________________
Teléfono principal:               ____________________________________________
Portería (24/7):                  ____________________________________________
Administrador(a) nombre:          ____________________________________________
Administrador(a) correo:          ____________________________________________
Presiente Junta nombre:           ____________________________________________
Presiente Junta correo:           ____________________________________________
```

## Identidad visual

```
Logo archivo:        ____________________________________________ (subir a assets/logo.jpg)
Color principal:     ____________________________________________ (hex)
Color acento 1:      ____________________________________________ (hex)
Color acento 2:      ____________________________________________ (hex)
Tipografía preferida: ____________________________________________ (opcional)
```

## Configuración del Sheet

```
Nombre del Sheet:           ____________________________________________
ID del Sheet:               ____________________________________________
Hoja principal nombre:      ____________________________________________
Hoja auxiliar nombre:       ____________________________________________
Número de columnas:         ____________________________________________
Validación obligatoria:     [ ] Sí  [ ] No
                            Si sí, cuáles: _____________________________
```

## Configuración GitHub

```
Usuario de GitHub:          ____________________________________________
Nombre del repo:            ____________________________________________
URL pública GitHub Pages:   ____________________________________________
```

## Configuración Apps Script

```
Nombre del proyecto:        ____________________________________________
ID del proyecto:            ____________________________________________
URL del Web App:            ____________________________________________
Cuenta Google usada:        ____________________________________________
"Ejecutar como":            ____________________________________________
"Quién tiene acceso":       ____________________________________________
```

## URLs importantes

```
URL pública del formulario: ____________________________________________
URL del Google Sheet:        ____________________________________________
URL del QR archivo en Drive: ____________________________________________
URL del Apps Script editor:  ____________________________________________
URL del repo GitHub:        ____________________________________________
```

## Configuración de correos a residentes

```
Plantilla correo:           [ ] Sí, personalizada  [ ] Usar plantilla genérica
Fecha límite para enviar:   ____________________________________________
Recordatorio 1:             ____________________________________________
Recordatorio 2:             ____________________________________________
```

## Checklist de lanzamiento

  - [ ] Logo subido al repo (`assets/logo.jpg`)
  - [ ] Colores del tema actualizados en `styles.css`
  - [ ] NIT, dirección y correo actualizados en `index.html`
  - [ ] Texto legal de la sección 11 personalizado en `Codigo.gs`
  - [ ] SHEET_ID actualizado en `Codigo.gs`
  - [ ] GitHub Pages activado y verificado
  - [ ] Apps Script desplegado y probado
  - [ ] APPS_SCRIPT_URL actualizado en `js/app.js`
  - [ ] Prueba end-to-end: enviar + editar un registro
  - [ ] QR generado y descargado
  - [ ] QR subido a Drive de la PH
  - [ ] QR impreso en formato A5/A4
  - [ ] QR pegado en carteleras
  -[ ] Correo enviado a todos los residentes con QR adjunto
  - [ ] Política de Tratamiento de Datos Personales publicada
  - [ ] Aviso de privacidad visible en la web
  - [ ] Backup inicial del Sheet (export a Excel/PDF)
