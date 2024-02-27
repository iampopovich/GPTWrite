import argparse
import openai


def main():
    parser = argparse.ArgumentParser(description="Procesar argumentos para la aplicación")
    parser.add_argument("--api-key", type=str, required=True, help="OpenAI apikey")
    parser.add_argument("--theme", type=str, required=True, help="Book theme")
    parser.add_argument("--description", type=str, required=True, help="Book description")
    parser.add_argument("--title", type=str, help="Bok title")
    parser.add_argument("--tags", nargs="+", type=str, help="Book tags")
    args = parser.parse_args()


def create_syllabus(theme, description, title=None, tags=None):

    pass


if __name__ == "__main__":
    main()
