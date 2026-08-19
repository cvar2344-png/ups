#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bot Telegram simple: solo botones "Anterior" / "Siguiente" para navegar entre páginas HTML
Coloca este archivo en la carpeta `bot/` del repo. Lee archivos HTML en la raíz del repo
(index.html, teps2.html, teps3.html, ...)

Uso:
  - Define TELEGRAM_BOT_TOKEN en las variables de entorno
  - Ejecuta: python bot/main.py

Este bot usa polling (fácil para pruebas). Para despliegue con webhooks necesitarás exponer
un endpoint HTTPS (Render lo soporta como servicio web; Vercel funcionaría solo con webhooks).
"""

import os
from bs4 import BeautifulSoup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Config
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # define tu token en la variable de entorno
# La carpeta bot/ se ubicará en la raíz del repo, por eso subimos un nivel para leer las HTML
HTML_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Archivos que queremos mostrar (orden de navegación)
PAGES = [
    "index.html",
    "teps2.html",
    "teps3.html",
    "teps4.html",
    "teps5.html",
]

MAX_SEND_LEN = 4000  # limite para evitar mensajes excesivamente largos


def load_page_text(path):
    """Lee HTML local y devuelve texto plano limpiado."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
    except FileNotFoundError:
        return "Página no encontrada."
    soup = BeautifulSoup(html, "html.parser")
    for s in soup(["script", "style", "noscript"]):
        s.decompose()

    body = soup.body or soup
    text = body.get_text(separator="\n", strip=True)
    if len(text) > MAX_SEND_LEN:
        text = text[:MAX_SEND_LEN] + "\n\n[Texto truncado...]"
    return text


def build_keyboard(index):
    """Construye teclado inline con Anterior y Siguiente según posición."""
    buttons = []
    row = []
    if index > 0:
        row.append(InlineKeyboardButton("⬅️ Anterior", callback_data=f"page:{index-1}"))
    if index < len(PAGES) - 1:
        row.append(InlineKeyboardButton("Siguiente ➡️", callback_data=f"page:{index+1}"))
    if row:
        buttons.append(row)
    return InlineKeyboardMarkup(buttons) if buttons else None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    index = 0
    page = PAGES[index]
    path = os.path.join(HTML_DIR, page)
    text = load_page_text(path)
    keyboard = build_keyboard(index)
    await update.message.reply_text(text, reply_markup=keyboard)


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data or ""
    if data.startswith("page:"):
        try:
            idx = int(data.split(":", 1)[1])
        except Exception:
            await query.edit_message_text("Dato de navegación inválido.")
            return
        if idx < 0 or idx >= len(PAGES):
            await query.edit_message_text("Página fuera de rango.")
            return
        page = PAGES[idx]
        path = os.path.join(HTML_DIR, page)
        text = load_page_text(path)
        keyboard = build_keyboard(idx)
        await query.edit_message_text(text, reply_markup=keyboard)


def main():
    token = TOKEN
    if not token:
        raise RuntimeError("Define la variable de entorno TELEGRAM_BOT_TOKEN con el token del bot.")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_handler))
    print("Bot corriendo (polling). Usa /start en Telegram para probar.")
    app.run_polling()


if __name__ == "__main__":
    main()
