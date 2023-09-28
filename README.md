![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Pandas](https://img.shields.io/badge/Pandas-2.1.1-brightgreen?logo=pandas)
![Tkinter](https://img.shields.io/badge/Tkinter-8.6%2B-orange)

# Обработчик нотификаций

Программа извлекает из текста нужную информацию, подставляет эту информацию в URL и открывает эти ссылки в браузере. 

Также можно сохранить собранную информацию в таблицу Excell.

## Установка

Чтобы начать работу с проектом, выполните следующие шаги:

1. Клонируйте репозиторий:

   ```
   git clone https://git@github.com:nasretdinovs/notifications_opens_in_tabs.git
   ```

2. Перейдите в директорию проекта:

    ```
    cd notifications_opens_in_tabs
    ```

3. Установите зависимости:

    ```
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

4. В файл переменных окружения .env необходимо прописать URL адрес сайта:
    ```
    SITE_URL=https://www.yourwebsite.com
    ```

5. Программа создавалась под определенный сайт, поэтому для корректной работы с другим сайтом необходимо вносить правки в функцию start_parsing().

## Запуск

```
python notification_gui.py
```

## Упаковка в .EXE

1. Для упаковки в EXE достаточно запустить auto-py-to-exe командой:

```
auto-py-to-exe
```
2. Запустится графическая оболочка Auto Py To Exe. В ней можно выбрать все необходимые параметры и нажать CONVERT. 
Рекомендуемые параметры:
```
Script Location: <ваш_путь_до_папки_с_репозиторием>/notifications_opens_in_tabs/notification_gui.py
Onefile: One File
Console Windows: Windows Based
```

## Графическая оболочка
![Notification_GUI](https://raw.githubusercontent.com/nasretdinovs/notifications_opens_in_tabs/main/preview/GUI_screenshot.png)
