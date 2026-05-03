import os
from app import create_app

# Создаём экземпляр нашего приложения из папки app
app = create_app()

if __name__ == '__main__':
    # Render задаёт порт через переменную окружения PORT, по умолчанию 5000
    port = int(os.environ.get('PORT', 5000))
    # Важно: host должен быть '0.0.0.0', чтобы приложение было доступно извне
    app.run(host='0.0.0.0', port=port)
