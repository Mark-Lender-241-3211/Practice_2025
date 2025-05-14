import os
import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Загрузка данных
with open("data.json", "r", encoding="utf-8") as f:
    DATA = json.load(f)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот-инструктор по безопасности.\n"
        "— /safety_rules — правила техники безопасности\n"
        "— /siz — список необходимых СИЗ\n"
        "— /first_aid — инструкции по первой помощи"
    )


def build_menu(cmd: str, data_key: str, prompt: str, context, update):
    """
    Универсальный генератор меню:
    - cmd: префикс callback_data (safety_rules, siz или first_aid)
    - data_key: ключ в DATA
    - prompt: текст перед клавиатурой
    """
    options = list(DATA.get(data_key, {}).keys())
    # строим мапу индекс->option
    mapping = {str(i): opt for i, opt in enumerate(options)}
    # сохраняем в user_data
    context.user_data[f"{cmd}_map"] = mapping

    keyboard = [
        [InlineKeyboardButton(opt, callback_data=f"choice:{cmd}:{i}")]
        for i, opt in mapping.items()
    ]
    return update.message.reply_text(
        prompt, reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def safety_rules_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await build_menu(
        cmd="safety_rules",
        data_key="safety_rules",
        prompt="Выберите вид работ для правил безопасности:",
        context=context,
        update=update,
    )


async def siz_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await build_menu(
        cmd="siz",
        data_key="siz",
        prompt="Выберите вид работ для списка СИЗ:",
        context=context,
        update=update,
    )


async def first_aid_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await build_menu(
        cmd="first_aid",
        data_key="first_aid",
        prompt="Выберите тип травмы для инструкции по первой помощи:",
        context=context,
        update=update,
    )


async def on_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    _, cmd, idx = query.data.split(":", 2)
    mapping = context.user_data.get(f"{cmd}_map", {})
    selection = mapping.get(idx)

    entry = DATA.get(cmd, {}).get(selection)
    if not selection or not entry:
        text = "Информация не найдена."
    else:
        if cmd == "first_aid":
            text = (
                f"Инструкция по первой помощи при «{selection}»:\n"
                + "\n".join(f"{i+1}. {s}" for i, s in enumerate(entry))
            )
        elif cmd == "siz":
            text = (
                f"Необходимые СИЗ для «{selection}»:\n"
                + "\n".join(f"- {s}" for s in entry)
            )
        else:  # safety_rules
            text = (
                f"Правила техники безопасности для «{selection}»:\n"
                + "\n".join(f"- {s}" for s in entry)
            )

    await query.edit_message_text(text)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Ошибка при обработке обновления:", exc_info=context.error)


def main():
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        logger.error("Не задан TELEGRAM_TOKEN")
        return

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("safety_rules", safety_rules_menu))
    app.add_handler(CommandHandler("siz", siz_menu))
    app.add_handler(CommandHandler("first_aid", first_aid_menu))
    app.add_handler(CallbackQueryHandler(on_choice, pattern=r"^choice:"))
    app.add_error_handler(error_handler)

    logger.info("Bot started...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
