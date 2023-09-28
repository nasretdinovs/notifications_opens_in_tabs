import os
import re
import tkinter as tk
import webbrowser
from datetime import datetime, timedelta
from tkinter import Label, W, ttk

import pandas as pd
from dotenv import load_dotenv

load_dotenv()


site_url = os.getenv('SITE_URL')

today = datetime.today().strftime('%Y-%m-%d')
yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')


class NotificationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Обработка нотификаций')
        self.geometry("450x400")

        self.label = Label(
            self,
            text='1. Скопируй текст нотификации',
            font=('Segoe UI', 10)
            )
        self.label.grid(row=1, column=0, padx=30, pady=5, sticky=W)

        # Создание виджетов для ввода текста и кнопок
        self.text_box = tk.Text(
            self, width=130, height=15, font=('Segoe UI', 8)
            )
        self.text_box.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

        self.label_combobox = Label(
            self, text='3. Выбери продукт: ', font=('Segoe UI', 10))
        self.label_combobox.grid(row=3, column=0, sticky=W, padx=30, pady=5)

        self.profiles = []
        self.combobox = ttk.Combobox(values=self.profiles)
        self.combobox.grid(row=3, column=0, sticky=W, padx=180, pady=6)

        self.start_open_button = tk.Button(
            self, text='Открыть в Сансаре', command=self.open_links,
            font=('Segoe UI', 10, 'bold'), width=20, height=2)
        self.start_open_button.grid(
            row=4, column=0, sticky=W, padx=30, pady=5)

        self.label_combobox = Label(
            self, text='или', font=('Segoe UI', 10, 'bold'))
        self.label_combobox.grid(row=4, column=0, sticky=W, padx=210, pady=15)

        self.startsave_button = tk.Button(
            self, text='Сохранить всё в Excel', command=self.save_file,
            font=('Segoe UI', 10, 'bold'), width=20, height=2)
        self.startsave_button.grid(
            row=4, column=0, sticky=W, padx=250, pady=15)

        self.start_button = tk.Button(
            self, text='2. Загрузи нотификацию', command=self.start_parsing,
            font=('Segoe UI', 10, 'bold'),  height=1)
        self.start_button.grid(row=2, column=0, sticky=W, padx=30, pady=5)

        # Создание переменной для хранения результата парсинга
        self.supports = []

    def insert_from_clipboard(self):
        clipboard_text = self.clipboard_get()
        self.text_box.insert('end', clipboard_text)

    def start_parsing(self):
        # Получение текста из поля ввода
        self.insert_from_clipboard()
        raw = self.text_box.get('1.0', 'end-1c')

        login = re.findall(r'Логин: \[([^\]]+)\]', raw)
        profile = re.findall(r'Профиль \W.+', raw)

        supports = []
        for sup in range(len(login)):
            supports.append(
                {
                    'Profile': profile[sup][9:],
                    'Login': login[sup],
                    'Link': (f'{site_url}/search?'
                             f'articleDateFrom={yesterday}&'
                             f'articleDateTo={today}&'
                             f'fromLogin={login[sup]}&ticketsPerPage=15&'
                             f'page=1&sortDirection=DESC'),
                }
            )
        self.supports = supports

        profiles = []
        for notify in supports:
            if notify['Profile'] in profiles:
                continue
            else:
                profiles.append(notify['Profile'])
        self.profiles = profiles
        self.combobox['values'] = self.profiles
        self.combobox.update()

        # Вывод результата в виджете Text
        self.text_box.delete('1.0', 'end')
        self.text_box.insert(
            '1.0', pd.DataFrame(
                supports)[['Profile', 'Login']].to_string(index=False))

    def save_file(self):
        # Сохранение файла
        file_path = './notification_{}.xlsx'.format(
            datetime.now().strftime("%d%m%Y_%H%M%S"))

        pd.set_option('display.max_colwidth', 200)
        df = pd.DataFrame(self.supports)
        writer = pd.ExcelWriter(file_path)
        df.to_excel(
            writer, sheet_name='Нотификации', index=False, na_rep='NaN')

        for column in df:
            column_width = max(
                df[column].astype(str).map(len).max(), len(column))
            col_idx = df.columns.get_loc(column)
            writer.sheets['Нотификации'].set_column(
                col_idx, col_idx, column_width)
        writer._save()

    def open_links(self):
        for support in self.supports:
            if support['Profile'] == self.combobox.get():
                webbrowser.open_new_tab(support['Link'])


if __name__ == '__main__':
    app = NotificationApp()
    app.mainloop()
