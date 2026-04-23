import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import os

FILE = "trainings.json"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.data = []

        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Label(frame, text="Дата (YYYY-MM-DD)").grid(row=0, column=0)
        tk.Label(frame, text="Тип тренировки").grid(row=1, column=0)
        tk.Label(frame, text="Длительность (мин)").grid(row=2, column=0)

        self.date = tk.Entry(frame)
        self.type = tk.Entry(frame)
        self.duration = tk.Entry(frame)

        self.date.grid(row=0, column=1)
        self.type.grid(row=1, column=1)
        self.duration.grid(row=2, column=1)

        tk.Button(frame, text="Добавить тренировку", command=self.add).grid(row=3, columnspan=2)

        # Таблица
        self.tree = ttk.Treeview(root, columns=("Date","Type","Duration"), show="headings")
        self.tree.heading("Date", text="Дата")
        self.tree.heading("Type", text="Тип")
        self.tree.heading("Duration", text="Длительность")
        self.tree.pack(pady=10)

        # Фильтр
        filter_frame = tk.Frame(root)
        filter_frame.pack()

        tk.Label(filter_frame, text="Тип").grid(row=0, column=0)
        tk.Label(filter_frame, text="Дата").grid(row=0, column=2)

        self.f_type = tk.Entry(filter_frame)
        self.f_date = tk.Entry(filter_frame)

        self.f_type.grid(row=0, column=1)
        self.f_date.grid(row=0, column=3)

        tk.Button(filter_frame, text="Фильтр", command=self.filter).grid(row=0, column=4)

        # Кнопки
        tk.Button(root, text="Сохранить", command=self.save).pack()
        tk.Button(root, text="Загрузить", command=self.load).pack()

        self.load()

    def add(self):
        try:
            datetime.strptime(self.date.get(), "%Y-%m-%d")
        except:
            messagebox.showerror("Ошибка", "Дата в формате YYYY-MM-DD")
            return

        try:
            duration = float(self.duration.get())
            if duration <= 0:
                raise ValueError
        except:
            messagebox.showerror("Ошибка", "Длительность должна быть положительной")
            return

        item = {
            "date": self.date.get(),
            "type": self.type.get(),
            "duration": duration
        }

        self.data.append(item)
        self.update(self.data)

    def update(self, data):
        self.tree.delete(*self.tree.get_children())
        for i in data:
            self.tree.insert("", tk.END, values=(i["date"], i["type"], i["duration"]))

    def filter(self):
        result = self.data

        if self.f_type.get():
            result = [i for i in result if self.f_type.get().lower() in i["type"].lower()]

        if self.f_date.get():
            result = [i for i in result if i["date"] == self.f_date.get()]

        self.update(result)

    def save(self):
        with open(FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def load(self):
        if os.path.exists(FILE):
            with open(FILE, "r", encoding="utf-8") as f:
                self.data = json.load(f)
                self.update(self.data)


root = tk.Tk()
app = App(root)
root.mainloop()