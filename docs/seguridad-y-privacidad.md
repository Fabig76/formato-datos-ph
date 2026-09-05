# Seguridad y Privacidad

Este documento analiza los riesgos de seguridad y privacidad del sistema
de formulario público para propiedad horizontal, y las mitigaciones aplicadas
y recomendadas.

## Marco legal colombiano

### Ley 1581 de 2012 (Protección de Datos Personales)

Establece:
  · Principio de **consentimiento libre, previo, expreso e informado**
  · El responsable del tratamiento debe informar al titular las finalidades
  · El titular tiene derecho a conocer, actualizar, rectificar y suprimir
    sus datos
  · El responsable debe implementar medidas de seguridad
  · Sanciones: hasta 2.000 SMLMV ($2.6 millardos COP en 2026) por incumplimiento

**Cómo cumplimos**:
  · El formulario incluye texto legal claro en la sección 11 sobre las
    finalidades del tratamiento
  · El residente debe marcar 3 checkboxes de consentimiento explícito
  · El residente firma electrónicamente (nombre + cédula + fecha)
  · El aviso legal destacado en la cabecera recuerda la obligatoriedad
    de datos reales

### Decreto 768 de 2025 (Censo de animales de compañía)

Establece:
  · Obligación de las PH de censar todas las mascotas
  · Caninos de manejo especial requieren registro + póliza de responsabilidad
    civil extracontractual

**Cómo cumplimos**:
  · El formulario tiene una sección completa (9) para datos de mascotas
  · Para manejo especial, pide N° de registro canino y N° de póliza

### Ley 1801 de 2016 (Código de Policía)

Artículos 128 y 134:
  · Reglas sobre caninos de manejo especial (razas peligrosas)
  · Tenedor debe ser mayor de edad
  · Póliza de responsabilidad civil extracontractual vigente

## Análisis de riesgos

### Riesgo 1: Envío de datos falsos o de terceros

**Descripción**: Un residente con malas intenciones, o alguien externo
que descubra la URL, puede enviar datos falsos o datos de otros residentes
sin su consentimiento.

**Probabilidad**: Media-Alta
**Impacto**: Medio (datos incorrectos en Sheet, problemas administrativos)

**Mitigaciones aplicadas**:
  · Aviso legal destacado en la página sobre Ley 1581/2012
  · Checkbox obligatorio de "Autorizo el tratamiento de datos"
  · Firma electrónica con cédula (vincula al responsable legal)
  · Hash de dedupe (sha256) detecta envíos duplicados exactos
  · La administración debe revisar el Sheet periódicamente

**Mitigaciones recomendadas (no implementadas)**:
  · Implementar un token único por apartamento: cada residente recibe un
    token (por correo físico o WhatsApp) y debe ingresarlo para enviar
  · Verificación de cédula: enviar código OTP al celular registrado
  · CAPTCHA para evitar bots

### Riesgo 2: Acceso no autorizado al Sheet

**Descripción**: Si alguien accede a la cuenta administradora, podría
robar o modificar los datos de todos los residentes.

**Probabilidad**: Baja (depende de la seguridad de la cuenta Google)
**Impacto**: Alto (robo de datos personales de todos los residentes)

**Mitigaciones aplicadas**:
  · El Sheet es privado (no compartido con "Cualquier persona con el enlace")
  · Solo los editores designados pueden acceder
  · Google Drive tiene autenticación 2FA configurable

**Mitigaciones recomendadas**:
  · Habilitar verificación en 2 pasos para la cuenta administradora
  · Usar cuenta de Google Workspace (mejor control de acceso)
  · Revisar periódicamente la lista de editores del Sheet
  · Logs de actividad: Google Drive registra quién accedió a qué y cuándo

### Riesgo 3: Manipulación del código del frontend

**Descripción**: Como GitHub Pages es público, cualquiera puede ver el
código HTML/CSS/JS. Un atacante podría entender el flujo y atacar el backend.

**Probabilidad**: Baja (es código estático, no hay secretos)
**Impacto**: Bajo (no hay secretos en el frontend)

**Mitigación**:
  · El frontend NO contiene secretos (ni tokens, ni passwords)
  · La URL del Apps Script es pública por diseño (debe serlo)
  · Toda validación sensible se hace en el backend (Apps Script)

### Riesgo 4: Manipulación del código del Apps Script

**Descripción**: Si alguien accede a la cuenta donde está el Apps Script,
podría modificar el código para hacer algo malicioso (enviar spam,
borrar datos, etc.).

**Probabilidad**: Muy Baja (igual que riesgo 2)
**Impacto**: Alto

**Mitigaciones aplicadas**:
  · El Apps Script está en una cuenta Google protegida
  · Solo el dueño puede modificar el código
  · Google tiene versionado automático del código del Apps Script

**Mitigaciones recomendadas**:
  · Activar 2FA en la cuenta
  · Hacer backup regular del código (copiar a un archivo .gs en Drive)
  · No compartir acceso al Apps Script innecesariamente

### Riesgo 5: Pérdida del N° de Formulario por el residente

**Descripción**: El residente pierde su N° de Formulario y no puede editar
su información cuando algo cambia (mudanza, nuevo vehículo, etc.).

**Probabilidad**: Alta (es un número alfanumérico fácil de olvidar)
**Impacto**: Bajo-Medio (datos desactualizados, fricción administrativa)

**Mitigaciones aplicadas**:
  · El N° se muestra prominentemente después del envío exitoso
  · Se sugiere "imprimir comprobante" y "guardar"
  · En el modo edición, hay un link visible: "¿Perdiste tu N° de formulario?
    Escríbenos a [correo administración]"
  · La administración puede buscar por N° Apto en el Sheet para
    ayudar a recuperar el N° de Formulario

**Mitigaciones recomendadas**:
  · Enviar el N° de Formulario por correo electrónico al residente cuando
    envía (requiere guardar el correo en el Apps Script y enviar via MailApp)
  · Implementar un sistema de "lookup por cédula": residente ingresa
    su cédula, recibe su N° de Formulario por correo

### Riesgo 6: Spam o ataques de denegación de servicio

**Descripción**: Un atacante podría hacer miles de requests al Web App
para llenarlo de basura o para que Google lo deshabilite.

**Probabilidad**: Baja (no hay incentivo obvio)
**Impacto**: Medio (filas basura, posible suspensión del Apps Script)

**Mitigaciones aplicadas**:
  · Las validaciones del Apps Script evitan datos vacíos
  · Google Apps Script tiene rate limiting interno

**Mitigaciones recomendadas**:
  · Implementar rate limiting con CacheService en el Apps Script:
    ```js
    const cache = CacheService.getScriptCache();
    const clientIP = ...; // difícil de obtener
    const key = 'rate_' + clientIP;
    const calls = parseInt(cache.get(key) || '0');
    if (calls > 10) return { ok: false, error: 'Demasiadas solicitudes.' };
    cache.put(key, String(calls + 1), 600); // 10 min
    ```
  · Implementar CAPTCHA (reCAPTCHA v3) en el frontend
  · Monitorear el Sheet para detectar patrones anómalos

### Riesgo 7: Datos de menores de edad

**Descripción**: Los datos de menores requieren tratamiento especial bajo
la ley colombiana.

**Probabilidad**: Alta (casi todas las familias tienen menores)
**Impacto**: Medio (responsabilidad legal)

**Mitigaciones aplicadas**:
  · Sección 5.1 dedicada a menores
  · Texto legal sobre Ley 1581/2012 y representación legal
  · Checkbox explícito "Autorizo el tratamiento de datos de los menores
    que represento"
  · Solo se piden datos básicos (nombre, edad, parentesco) — NO cédula,
    NO información sensible

## Privacidad por diseño (Privacy by Design)

El sistema implementa los 7 principios de privacy by design:

  1. **Proactivo, no reactivo**: medidas preventivas (validaciones, avisos)
  2. **Privacidad como configuración por defecto**: el residente decide
     qué compartir
  3. **Privacidad embebida en el diseño**: la arquitectura misma protege
     los datos
  4. **Funcionalidad completa**: todas las funciones se mantienen
     (no sacrificamos funcionalidad por privacidad)
  5. **Seguridad end-to-end**: HTTPS, validación servidor, hash de integridad
  6. **Visibilidad y transparencia**: código abierto, documentación pública
  7. **Respeto por la privacidad del usuario**: solo se piden los datos
     necesarios, con explicación clara de para qué se usan

## Checklist de cumplimiento legal

Antes de implementar en una nueva PH, verificar:

  - [ ] La PH tiene **RUT actualizado** y está registrada ante la SIC si maneja
        datos personales (obligatorio si son >10.000 registros)
  - [ ] La PH tiene **Política de Tratamiento de Datos Personales** publicada
        (puede ser un documento simple pero debe existir)
  - [ ] El aviso legal del formulario menciona correctamente la PH (nombre + NIT)
  - [ ] El aviso legal menciona el correo de la administración como canal para
        ejercer derechos ARCO (Acceso, Rectificación, Cancelación, Oposición)
  - [ ] La PH tiene un **responsable del tratamiento** identificado (puede ser
        el administrador o la junta)
  - [ ] El Sheet tiene los **datos mínimos necesarios** (no se piden datos
        excesivos)
  - [ ] El aviso de **retención de datos** está claro (cuánto tiempo se
        conservan, cuándo se eliminan)

## Checklist de seguridad operativa

  - [ ] Cuenta administradora con **verificación en 2 pasos** activada
  - [ ] **Copia de seguridad** mensual del Sheet (exportar a Excel/PDF)
  - [ ] **Revisión periódica** del Sheet (al menos mensual) para detectar
        registros sospechosos
  - [ ] **Bitácora** de quién accede al Sheet (Google Drive lo registra
        automáticamente)
  - [ ] **Procedimiento documentado** para responder a solicitudes ARCO de
        titulares
  - [ ] **Plan de contingencia** si la cuenta administradora se ve comprometida

## ¿Qué pasa si hay una filtración de datos?

Pasos recomendados:

  1. **Contener**: cambiar contraseña de la cuenta Google, revocar acceso
     a Apps Script, mover el Sheet a otra cuenta
  2. **Notificar a la SIC** (Superintendencia de Industria y Comercio)
     dentro de los **15 días hábiles** siguientes al descubrimiento
  3. **Notificar a los titulares** afectados (todos los residentes)
  4. **Documentar el incidente**: qué pasó, qué datos se filtraron,
     qué medidas se tomaron
  5. **Aprender y mejorar**: implementar las medidas que faltaron

Referencia: Ley 1581 de 2012, Artículo 17 (Deberes de los responsables del tratamiento).

## Contacto para temas de privacidad

Para cualquier pregunta sobre privacidad o para ejercer derechos ARCO:

  · Correo de la administración (configurado en el formulario)
  · Superintendencia de Industria y Comercio (SIC): www.sic.gov.co
