import argparse
import ast
from mdutils.mdutils import MdUtils
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()


def main():
    parser = argparse.ArgumentParser(description="Procesar argumentos para la aplicación")
    parser.add_argument("--theme", type=str, required=True, help="Book theme")
    parser.add_argument("--description", type=str, required=True, help="Book description")
    parser.add_argument("--title", type=str, help="Bok title")
    parser.add_argument("--tags", nargs="+", type=str, help="Book tags")
    parser.add_argument("--pages", type=int, help="Pages count")
    parser.add_argument("--details", type=str, help="Book details")
    parser.add_argument("--language", type=str, help="Book language")
    parser.add_argument("--output", required=True, type=str, help="Book output name")

    args = parser.parse_args()
    md_file = MdUtils(file_name=f'{args.output}.md')
    syllabus = ast.literal_eval(create_syllabus(args.theme, args.description, args.title, args.tags, args.details))
    pages_number = args.pages // len(syllabus)
    for chapter in syllabus:
        chapter_content = generate_chapter_content(chapter, pages_number, args.details, args.language)
        md_file.new_line(chapter_content)
    md_file.create_md_file()


def create_syllabus(theme, description, title=None, tags=None, details=None, language="English"):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "Предоставь план контента для книги на основе указанной темы, описания и тегов."},
            {"role": "system",
             "content": "Ожидается предоставление ответа в виде списка python-списка, например: [\"1. Chapter 1. Title 1. subtitle 1.1\", \"2. Chapter 2. Title 2. subtitle 2.1\", \"3. Chapter 3. Title 3]"},
            {"role": "system",
             "content": "Убедись, что план контента включает детальное описание, соответствующее предоставленным деталям."},
            {"role": "system",
             "content": "Просим составить план контента на указанном языке."},
            {"role": "system",
             "content": "Use chapter format **<Chapter number>. <Title>.**\n\n"},
            {"role": "user",
             "content": f"Theme: {theme}\nDescription: {description}\nTitle: {title}\nTags: {tags}\nDetails: {details}\nLanguage: {language}"}
        ]
    )
    return completion.choices[0].message.content


def generate_chapter_content(chapter, pages_number, details, language="English"):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "Напиши главу книги на основе предоставленного краткого описания <chapter overview>."},
            {"role": "system",
             "content": "Размер главы должен соответсвовать указанному количеству страниц <pages number in chapter>."},
            {"role": "system",
             "content": "Включи в текст главы тематические примеры"},
            {"role": "system",
             "content": "Одна страница текста формата А5 может содержать около 200 слов."},
            {"role": "system",
             "content": "Одна страница текста формата А4 может содержать около 350 слов."},
            {"role": "system",
             "content": "Ожидается, что глава книги будет представлена в формате Markdown."},
            {"role": "system",
             "content": "глава содержит содержательный материал и соответствует теме книги."},
            {"role": "system",
             "content": "используй для написания текста язык <language>."},
            {"role": "user",
             "content": f"Напиши главу книги длиной {pages_number} страниц формата А4 на тему '{chapter}' с уровнем детализации '{details}' на языке {language}"}
        ]
    )
    return completion.choices[0].message.content


if __name__ == "__main__":
    main()

# python3 app.py --title "android development" --description "книга по разработке андроид приожений. предназначена для новичков. последовательно освещает освноные концепции разработки, паттерны проектирования, приемы проектирования UI и UX приложений" --tags java nadroid development tutorial --details подробно --theme "руководство по разработке приложений для ОС андроид" --pages 50 --output android
# python3 app.py --title "android development" --description "книга по разработке андроид приожений. предназначена для новичков. последовательно освещает освноные концепции разработки, паттерны проектирования, приемы проектирования UI и UX приложений" --tags java nadroid development tutorial --details подробно --theme "руководство по разработке приложений для ОС андроид" --pages 200 --output android --language Russian
# python3 app.py --title "quality assurance" --description "книга является справочником для опытного QA инженера. в нее включены основные понятия QA, основные метрики качества, подходы к тестированию" --tags qa quality assurance cookbook  --details подробно --theme "справочник для QA инженера" --pages 200 --output qaguide --language Russian
