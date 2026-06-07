# Инструкция по адаптации ассистента под новую дисциплину

## 1. Добавить шаблон конспекта

Откройте `knowledge_base/templates.csv` и добавьте строку:

```csv
Название дисциплины,"Введение: ... Методы: ... Результаты: ... Выводы: ...","Примечание"
```

## 2. Добавить формулировки

Откройте `knowledge_base/formulations.csv` и добавьте готовые формулировки:

```csv
domain,formulation,use_case
Название,"Готовая формулировка...","Раздел конспекта"
```

## 3. Добавить вопросы для самопроверки

Откройте `knowledge_base/questions.csv`:

```csv
discipline,question_template,type
Название,"Вопрос по материалу?",Анализ
```

## 4. Настроить LLM-бэкенд

Создайте `.env` файл (или измените существующий):

```bash
# Выбор бэкенда: openai, gigachat, yandexgpt, ollama
LLM_BACKEND=openai

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_BASE_URL=https://api.smartbuddy.ru/v1
OPENAI_MODEL=gpt-4o-mini

# GigaChat
GIGACHAT_AUTH_KEY=...
GIGACHAT_SCOPE=GIGACHAT_API_PERS
GIGACHAT_MODEL=GigaChat-2

# YandexGPT
YANDEX_IAM_TOKEN=...
YANDEX_FOLDER_ID=...
YANDEX_MODEL=yandexgpt-lite

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen3.5:4b

# VK Bot (опционально)
VK_BOT_TOKEN=...

# Параметры генерации
TEMPERATURE=0.3
MAX_TOKENS=4096
```

## 5. Запуск

```bash
pip install -r requirements.txt

# Из файла
python main.py --file article.txt

# Из URL
python main.py https://example.com/article

# Из stdin
echo "Текст статьи" | python main.py

# С указанием типа и дисциплины
python main.py --file article.txt --type experimental --discipline "Компьютерные науки"

# VK-бот
python main.py --vkbot
```
