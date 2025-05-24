import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from prettytable import PrettyTable

import IO
import calculation
import examples
import math
import os


class InterpolationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Интерполяция функций")
        self.root.geometry("1200x800")

        self.input_type = tk.IntVar(value=1)
        self.func_choice = tk.StringVar()
        self.x = tk.StringVar()
        self.a = tk.StringVar()
        self.b = tk.StringVar()
        self.n = tk.IntVar(value=5)
        self.filename = tk.StringVar()
        self.xi = []
        self.yi = []

        self.create_widgets()

    def create_widgets(self):
        input_frame = ttk.LabelFrame(self.root, text="Тип ввода данных")
        input_frame.pack(pady=10, padx=10, fill="x")

        ttk.Radiobutton(input_frame, text="Ручной ввод", variable=self.input_type, value=1,
                        command=self.update_interface).grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(input_frame, text="Из файла", variable=self.input_type, value=2,
                        command=self.update_interface).grid(row=0, column=1, sticky="w")
        ttk.Radiobutton(input_frame, text="Функция", variable=self.input_type, value=3,
                        command=self.update_interface).grid(row=0, column=2, sticky="w")

        self.dynamic_frame = ttk.Frame(self.root)
        self.dynamic_frame.pack(pady=10, padx=10, fill="x")

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Рассчитать", command=self.calculate).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Очистить", command=self.clear_all).pack(side="left", padx=5)

        self.result_text = tk.Text(self.root, height=10, state="disabled")
        self.result_text.pack(pady=10, padx=10, fill="both", expand=True)

        self.graph_frame = ttk.Frame(self.root)
        self.graph_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.update_interface()

    def update_interface(self):
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

        input_type = self.input_type.get()

        if input_type == 1:
            self.create_manual_input()
        elif input_type == 2:
            self.create_file_input()
        elif input_type == 3:
            self.create_function_input()

    def create_manual_input(self):
        # Точка интерполяции (строка 0)
        ttk.Label(self.dynamic_frame, text="Точка интерполяции (x):").grid(row=0, column=0)
        ttk.Entry(self.dynamic_frame, textvariable=self.x).grid(row=0, column=1)

        # Заголовок таблицы (строка 1)
        ttk.Label(self.dynamic_frame, text="Узлы интерполяции (xi yi):").grid(row=1, column=0, sticky="w", pady=(10, 0))

        # Кнопки добавить/удалить узел (строка 2)
        button_frame = ttk.Frame(self.dynamic_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=5)
        ttk.Button(button_frame, text="Добавить узел", command=self.add_row).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Удалить узел", command=self.remove_row).pack(side="left", padx=5)

        # Таблица узлов (строка 3)
        self.table_frame = ttk.Frame(self.dynamic_frame)
        self.table_frame.grid(row=3, column=0, columnspan=3, pady=5)

        # Заголовки столбцов таблицы
        ttk.Label(self.table_frame, text="xi").grid(row=0, column=0)
        ttk.Label(self.table_frame, text="yi").grid(row=0, column=1)

        self.rows = []
        self.add_row()

    def create_file_input(self):
        ttk.Label(self.dynamic_frame, text="Имя файла с узлами:").grid(row=0, column=0)
        ttk.Entry(self.dynamic_frame, textvariable=self.filename, width=30).grid(row=0, column=1)
        ttk.Button(self.dynamic_frame, text="Обзор", command=self.browse_file).grid(row=0, column=2)

        ttk.Label(self.dynamic_frame, text="Точка интерполяции (x):").grid(row=1, column=0)
        ttk.Entry(self.dynamic_frame, textvariable=self.x).grid(row=1, column=1)

    def create_function_input(self):
        ttk.Label(self.dynamic_frame, text="Функция:").grid(row=0, column=0)
        func_combo = ttk.Combobox(self.dynamic_frame, textvariable=self.func_choice,
                                  values=[f"{k}: {v[0]}" for k, v in examples.available_functions.items()])
        func_combo.grid(row=0, column=1)

        ttk.Label(self.dynamic_frame, text="Интервал [a, b]:").grid(row=1, column=0)
        ttk.Entry(self.dynamic_frame, textvariable=self.a, width=10).grid(row=1, column=1)
        ttk.Entry(self.dynamic_frame, textvariable=self.b, width=10).grid(row=1, column=2)

        ttk.Label(self.dynamic_frame, text="Количество точек (n >= 2):").grid(row=2, column=0)
        ttk.Entry(self.dynamic_frame, textvariable=self.n).grid(row=2, column=1)

        ttk.Label(self.dynamic_frame, text="Точка интерполяции (x):").grid(row=3, column=0)
        ttk.Entry(self.dynamic_frame, textvariable=self.x).grid(row=3, column=1)

    def add_row(self):
        row_num = len(self.rows) + 1
        xi_entry = ttk.Entry(self.table_frame, width=10)
        yi_entry = ttk.Entry(self.table_frame, width=10)
        xi_entry.grid(row=row_num, column=0)
        yi_entry.grid(row=row_num, column=1)
        self.rows.append((xi_entry, yi_entry))

    def remove_row(self):
        if self.rows:
            row = self.rows.pop()
            for entry in row:
                entry.destroy()

    def browse_file(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.filename.set(filename)

    def clear_all(self):
        self.xi = []
        self.yi = []
        self.x.set("0.0")
        self.a.set("0.0")
        self.b.set("0.0")
        self.n.set(5)
        self.filename.set("")
        self.func_choice.set("")
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state="disabled")
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        self.update_interface()

    def validate_input(self):
        try:
            x_val = self.parse_float(self.x.get())
            if len(self.xi) < 2:
                raise ValueError("Нужно ввести хотя бы 2 узла!")

            if not (min(self.xi) <= x_val <= max(self.xi)):
                raise ValueError("Точка интерполяции должна быть внутри диапазона узлов")

            if len(set(self.xi)) != len(self.xi):
                raise ValueError("Все значения X должны быть уникальными")

            return True
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
            return False

    def calculate(self):
        try:
            input_type = self.input_type.get()
            self.xi = []
            self.yi = []

            if input_type == 1:
                self.process_manual_input()
            elif input_type == 2:
                self.process_file_input()
            elif input_type == 3:
                self.process_function_input()

            if not self.validate_input():
                return

            # Вычисление результатов
            func_values = [
                calculation.lagrange_interpolation(self.xi, self.yi, self.parse_float(self.x.get())),
                calculation.newton_divided_differences(self.xi, self.yi, self.parse_float(self.x.get())),
                calculation.newton_forward_difference(self.xi, self.yi, self.parse_float(self.x.get())),
                calculation.newton_backward_difference(self.xi, self.yi, self.parse_float(self.x.get()))
            ]

            self.show_results(func_values)
            self.plot_graphs()

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def parse_float(self, value):
        try:
            return float(str(value).replace(',', '.'))
        except ValueError:
            raise ValueError(f"Некорректное числовое значение: {value}")

    def process_manual_input(self):
        for xi_entry, yi_entry in self.rows:
            try:
                xi = self.parse_float(xi_entry.get())
                yi = self.parse_float(yi_entry.get())
                self.xi.append(xi)
                self.yi.append(yi)
            except Exception as e:
                raise ValueError(f"Ошибка в строке {xi_entry.get()}, {yi_entry.get()}: {str(e)}")

    def process_file_input(self):
        if not os.path.exists(self.filename.get()):
            raise FileNotFoundError("Файл не найден")

        self.xi, self.yi = IO.read_data_from_file(self.filename.get())

        if len(self.xi) < 2:
            raise ValueError("Файл должен содержать минимум 2 узла")

        # Проверка уникальности xi
        if len(set(self.xi)) != len(self.xi):
            raise ValueError("X-узлы должны быть уникальными")

    def process_function_input(self):
        try:
            func_key = int(self.func_choice.get().split(":")[0])
            func_name, func = examples.available_functions[func_key]
        except:
            raise ValueError("Выберите функцию из списка")

        a = self.parse_float(self.a.get())
        b = self.parse_float(self.b.get())
        x = self.parse_float(self.x.get())
        n = self.n.get()

        if a >= b:
            raise ValueError("Левая граница должна быть меньше правой")

        if n < 2:
            raise ValueError("Количество точек должно быть не меньше 2")

        if func_key == 5 and a <= 0:
            raise ValueError("Для ln(x) левая граница должна быть больше 0")

        if not (a <= x <= b):
            raise ValueError("Точка интерполяции должна быть внутри интервала")

        self.xi = [a + i * (b - a) / (n - 1) for i in range(n)]
        self.yi = [func(x_val) for x_val in self.xi]

    def show_results(self, func_values):
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)

        self.result_text.configure(font=('Courier New', 10))

        diff_table = calculation.compute_differences(self.xi, self.yi)

        pt = PrettyTable()
        pt.field_names = ["x", "y"] + [f"Δ^{i}y" for i in range(1, len(diff_table[0]) - 1)]
        pt.align = "r"
        pt.float_format = ".3"

        for row in diff_table:
            cleaned_row = [row[0]] + [f"{val:.3f}" if isinstance(val, float) else "" for val in row[1:]]
            pt.add_row(cleaned_row)

        self.result_text.insert(tk.END, "Таблица конечных разностей:\n")
        self.result_text.insert(tk.END, pt.get_string() + "\n\n")

        self.result_text.insert(tk.END, "Результаты интерполяции:\n")
        for name, value in zip(examples.func_names, func_values):
            self.result_text.insert(tk.END, f"{name}: {value:.6f}\n")

        self.result_text.config(state="disabled")

    def plot_graphs(self):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111)

        # Узлы интерполяции
        ax.scatter(self.xi, self.yi, color='red', zorder=5, label='Узлы интерполяции')

        # Цвета и метки для методов
        methods = [
            (calculation.lagrange_interpolation, 'Лагранж', 'blue'),
            (calculation.newton_divided_differences, 'Ньютон (раздел. разности)', 'green'),
            (calculation.newton_forward_difference, 'Ньютон (вперед)', 'purple'),
            (calculation.newton_backward_difference, 'Ньютон (назад)', 'orange')
        ]

        # Построение графиков для каждого метода
        x_plot = np.linspace(min(self.xi), max(self.xi), 500)
        for method, label, color in methods:
            y_plot = [method(self.xi, self.yi, xp) for xp in x_plot]
            ax.plot(x_plot, y_plot, linestyle='--', linewidth=1.5, alpha=0.8, color=color, label=label)

        # Вертикальная линия для точки интерполяции
        x_val = self.parse_float(self.x.get())
        ax.axvline(x=x_val, color='gray', linestyle=':', label=f'x = {x_val:.2f}')

        # Настройки графика
        ax.set_title("Графики интерполяции")
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1))  # Легенда справа
        ax.grid(True, alpha=0.3)

        # Размещение графика с учетом легенды
        fig.tight_layout(rect=[0, 0, 0.85, 1])  # Оставляем место для легенды

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = InterpolationApp(root)
    root.mainloop()