# Telegram Bot — Navegación entre páginas HTML

Este repositorio contiene un bot de Telegram muy sencillo que muestra el texto de páginas HTML locales y permite navegar entre ellas con los botones "Anterior" y "Siguiente".

Archivos importantes
- bot/main.py — Código del bot (usa polling). Ya incluido en el repo.
- requirements.txt — Dependencias Python.
- Procfile — (opcional) facilita el despliegue en plataformas que usan Procfile.

Ejecución local
1. Instala dependencias:
   python -m pip install -r requirements.txt

2. Define la variable de entorno con el token del bot (obtenido de @BotFather):
   - Linux/macOS:
       export TELEGRAM_BOT_TOKEN="TU_TOKEN"
   - Windows (PowerShell):
       $Env:TELEGRAM_BOT_TOKEN="TU_TOKEN"

3. Desde la raíz del repo ejecuta:
   python bot/main.py

4. En Telegram, envía /start al bot y usa los botones "Anterior" / "Siguiente".

Despliegue recomendado — Render (para polling)
- Por qué Render: permite ejecutar procesos de larga duración (ideal para polling). Vercel no es recomendable para polling porque sólo sirve funciones serverless y no mantiene procesos en ejecución.

Pasos resumidos para Render:
1. Crea una cuenta en https://render.com y conecta el repositorio `cvar2344-png/ups`.
2. Crea un nuevo servicio:
   - Tipo: Background Worker
   - Build Command: pip install -r requirements.txt
   - Start Command: python bot/main.py
3. Añade la variable de entorno TELEGRAM_BOT_TOKEN en la configuración del servicio con el token de tu bot.
4. Despliega: Render instalará dependencias y mantendrá el proceso corriendo.

Notas y consideraciones
- Telegram no renderiza CSS/JS dentro de mensajes: el bot envía el texto extraído del HTML (no la apariencia). Si quieres mantener el estilo visual, es necesario hospedar las páginas y enviar enlaces o imágenes (capturas).
- Si prefieres usar webhooks (ej.: para Vercel), se necesitará adaptar el bot para exponer un endpoint HTTPS y configurar setWebhook en la API de Telegram.

Si quieres, puedo:
- Convertir el bot a webhook para desplegar en Vercel y añadir el endpoint /api/webhook.
- Añadir una opción para abrir la página en el navegador (botón con URL).
