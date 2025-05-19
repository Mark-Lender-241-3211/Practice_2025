# Структра [/src](https://github.com/Mark-Lender-241-3211/Practice_2025/tree/main/src)
```markdawn
/ src
├── Dockerfile          # Cборка Docker-контейнера
├── bot.py              # Исполнительный файл
├── data.json           # Хранилище данных
└── requirements.txt    # Список зависимостей
```

# Описание
- Телеграм-бот SafetyBot ([@SafetyTheBestBot](https://web.telegram.org/k/#@SafetyTheBestBot)) - это бот-инструктор по безопасности, предоставляющий информацию о правилах техники безопасности для различных видов работ, 
опасностях, способах их предотвращения, использовании средств индивидуальной защиты (СИЗ).
- Как работает
  - Пользователь выбирает вид работ (например, "работа на высоте", "работа с электроинструментом", "сварочные работы"), а бот предоставляет 
релевантные инструкции и правила.
- Преимущества
  - Легкий доступ к информации
  - Dозможность быстро получить нужную инструкцию прямо на рабочем месте

# Функционал
- Команды:
    - /safety_rules [вид работ] - Получить инструкции по ТБ для конкретного вида работ.
    - /sizo [вид работ] - Получить информацию о необходимых СИЗ для конкретного вида работ.
    - /first_aid [травма] - Получить инструкции по оказанию первой помощи при травме (например, при ожоге, порезе).
- Локальная база в формате JSON

# Планируемый функционал
- Парсинг актуальных документов
- Автоматическое обновление инструкций с сайтов
  - Росстандарт – ГОСТы.
  - Минтруд – приказы по ОТ.

# Изучение технологии
- Ресурсы:
  - [Официальная документация Telegram Bot API](https://core.telegram.org/)
  - [Интернет-ресурс FredCodeCamp](https://www.freecodecamp.org/news/how-to-create-a-telegram-bot-using-python/)
  - [Гайд видео-курс "Телеграм бот на Python"](https://www.youtube.com/watch?v=ObwoMskHDoA)
  - [Гайд "Телеграм Бот на Python с нуля!"](https://www.youtube.com/watch?v=7mdyOUjECP0)
## Этап 1: Реализация минимального функционала
1) Создание бота с помощью официального тг-бота BotFather
![image](https://github.com/user-attachments/assets/b95f8183-a518-441b-80ac-2b209016f7f8)
2) Реализация
  - Написание минимального бота с помощью официальной документации
```python
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

async def start(update: Update, context):
    await update.message.reply_text("Привет! Я бот-инструктор по безопасности.")

app = ApplicationBuilder().token("YOUR_TOKEN").build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
```
## Этап 2: Разработка функционала
Основные компоненты:
1) Меню с инлайн-кнопками:
```python
keyboard = [
    [InlineKeyboardButton("Правила безопасности", callback_data="safety_rules")],
    [InlineKeyboardButton("СИЗ", callback_data="siz")]
]
reply_markup = InlineKeyboardMarkup(keyboard)
await update.message.reply_text("Выберите раздел:", reply_markup=reply_markup)
```
2) Универсальная система генерации меню:
```python
def build_menu(cmd: str, data_key: str, prompt: str, context, update):
    options = list(DATA.get(data_key, {}).keys())
    mapping = {str(i): opt for i, opt in enumerate(options)}
    context.user_data[f"{cmd}_map"] = mapping

    keyboard = [
        [InlineKeyboardButton(opt, callback_data=f"choice:{cmd}:{i}")]
        for i, opt in mapping.items()
    ]
    return update.message.reply_text(prompt, reply_markup=InlineKeyboardMarkup(keyboard))
```
## Этап 3: Работа с данными
- Структура данных (data.json):
```json
{
  "safety_rules": {
    "Работа на высоте": ["Использовать страховочный пояс", "Проверить леса"],
    "Электроработы": ["Отключить напряжение", "Использовать диэлектрические перчатки"]
  },
  "siz": {
    "Сварка": ["Маска сварщика", "Краги"],
    "Покраска": ["Респиратор", "Защитные очки"]
  }
}
```
## Этап 4: Логирование
```python
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
```
## Этап 5: Развертывание
- Docker-контейнеризация
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY data.json bot.py ./
CMD ["python", "bot.py"]
```
- Сборка и запуск:
```bash
docker build -t safety-bot .
docker run -d -e TELEGRAM_TOKEN --name safety-bot safety-bot
```
