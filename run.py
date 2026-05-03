import os
import sys
from app import create_app

# Добавим диагностику: выведем путь к проекту и список файлов в нём
print(f"Current working directory: {os.getcwd()}")
print(f"Files and dirs in current dir: {os.listdir('.')}")

# Эта проверка покажет, есть ли папка 'app' и что внутри неё
if os.path.exists('app'):
    print(f"Contents of 'app' dir: {os.listdir('app')}")
else:
    print("ERROR: The 'app' directory is missing!")

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)