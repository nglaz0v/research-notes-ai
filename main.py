import asyncio
import argparse
import sys

from summarizer import summarize_article
from scraper import fetch_article_from_url, load_article_from_file


def cli():
    parser = argparse.ArgumentParser(
        description="ИИ-ассистент для конспектирования научных статей",
    )
    parser.add_argument(
        "input",
        nargs="?",
        help="URL статьи, путь к .txt файлу, или текст статьи (stdin если не указано)",
    )
    parser.add_argument(
        "--type",
        choices=["review", "experimental", "theoretical", "default"],
        default="default",
        help="Тип статьи (по умолчанию: default)",
    )
    parser.add_argument(
        "--discipline",
        default=None,
        help="Дисциплина для использования базы знаний (напр. 'Компьютерные науки')",
    )
    parser.add_argument(
        "--file",
        action="store_true",
        help="Вход — локальный .txt файл",
    )
    parser.add_argument(
        "--vkbot",
        action="store_true",
        help="Запустить VK-бота вместо CLI режима",
    )
    args = parser.parse_args()

    if args.vkbot:
        from vkbot import run_vk_bot
        run_vk_bot()
        return

    if args.input is None and not sys.stdin.isatty():
        article_text = sys.stdin.read().strip()
    elif args.file:
        article_text = load_article_from_file(args.input)
    elif args.input and (args.input.startswith("http://") or args.input.startswith("https://")):
        article_text = fetch_article_from_url(args.input)
    elif args.input:
        article_text = args.input
    else:
        print("Укажите вход: URL, --file <path>, или передайте текст через stdin.")
        parser.print_help()
        return

    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(
        summarize_article(
            article_text=article_text,
            article_type=args.type,
            discipline=args.discipline,
        )
    )
    print(result)


if __name__ == "__main__":
    cli()
