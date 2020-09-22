import sys

from utils import Config
from web import Jira

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Введены не все аргументы!")
    elif len(sys.argv) > 2:
        print("Введено слишком много аргументов!")
    else:
        config = Config.Config
        data = config.translate_arv(sys.argv[1])
        jira = Jira.Jira()
        result = jira.exec(data)
        if result == "ERROR_LEN":
            print("Битый файл!")
        else:
            print("Выполнено!")
