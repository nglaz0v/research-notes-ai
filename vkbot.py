import asyncio
import logging

from vkbottle.bot import Bot, Message
#from vkbottle.dispatch.rules.base import CommandRule
from config import Config
from summarizer import summarize_article
from scraper import fetch_article_from_url

logger = logging.getLogger(__name__)

bot = Bot(token=Config.VK_BOT_TOKEN)


@bot.on.message(text="/start")
async def start_handler(message: Message):
    await message.answer(
        "Привет! Я ИИ-ассистент для конспектирования научных статей.\n\n"
        "Отправьте мне:\n"
        "• Текст статьи — я составлю конспект\n"
        "• Ссылку на статью — я скачаю и проанализирую\n"
        "• /help — справка по командам"
    )


@bot.on.message(text="/help")
async def help_handler(message: Message):
    await message.answer(
        "Доступные команды:\n"
        "/start — Приветствие\n"
        "/help — Справка\n"
        "/type review — Обзорная статья\n"
        "/type experimental — Экспериментальная статья\n"
        "/type theoretical — Теоретическая статья\n"
        "/discipline <name> — Указать дисциплину\n\n"
        "Просто отправьте текст или ссылку на статью!"
    )

# User state tracking
user_settings: dict[int, dict] = {}


@bot.on.message(text="/type review")
async def type_review(message: Message):
    user_settings.setdefault(message.from_id, {})["article_type"] = "review"
    await message.answer("Режим: обзорная статья (review)")


@bot.on.message(text="/type experimental")
async def type_experimental(message: Message):
    user_settings.setdefault(message.from_id, {})["article_type"] = "experimental"
    await message.answer("Режим: экспериментальная статья")


@bot.on.message(text="/type theoretical")
async def type_theoretical(message: Message):
    user_settings.setdefault(message.from_id, {})["article_type"] = "theoretical"
    await message.answer("Режим: теоретическая статья")


@bot.on.message(text="/discipline <discipline>")
async def discipline_handler(message: Message, discipline: str):
    user_settings.setdefault(message.from_id, {})["discipline"] = discipline
    await message.answer(f"Дисциплина установлена: {discipline}")


@bot.on.message()
async def article_handler(message: Message):
    """Handle incoming text: either a URL to fetch or raw article text."""
    settings = user_settings.get(message.from_id, {})
    article_type = settings.get("article_type", "default")
    discipline = settings.get("discipline")

    await message.answer("Анализирую статью, подождите...")

    try:
        text = message.text.strip()

        # Check if message is a URL
        if text.startswith("http://") or text.startswith("https://"):
            article_text = fetch_article_from_url(text)
        else:
            article_text = text

        summary = await summarize_article(
            article_text=article_text,
            article_type=article_type,
            discipline=discipline,
        )

        # VK has message length limits
        if len(summary) > 4096:
            chunks = [summary[i:i+4096] for i in range(0, len(summary), 4096)]
            for chunk in chunks:
                await message.answer(chunk)
        else:
            await message.answer(summary)

    except Exception as e:
        logger.error(f"Error processing article: {e}", exc_info=True)
        await message.answer(f"Произошла ошибка при анализе: {e}")


def run_vk_bot():
    """Start the VK bot."""
    if not Config.VK_BOT_TOKEN:
        logger.warning("VK_BOT_TOKEN not set. VK bot will not start.")
        return
    logger.info("Starting VK bot...")
    bot.run_forever()
