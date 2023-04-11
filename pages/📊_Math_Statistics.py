import streamlit as st
import pandas as pd
import math


class Selection:
    def __init__(self, data):
        self.data = data
        self.numbers = []
        self.x_max = 0
        self.x_min = 0
        self.x_start = 0
        self.x_end = 0
        self.table = {}
        self.R = 0
        self.k = 0
        self.m = 0
        self.X = 0
        self.S = 0
        self.d = 0
        self.Mo = 0
        self.Me = 0
        self.A = 0
        self.E = 0

    def calculate(self):
        # Числа выборки
        self.numbers = list(map(float, self.data.split()))

        # Количество чисел
        length = len(self.numbers)

        # Макс и мин
        self.x_max = max(self.numbers)
        self.x_min = min(self.numbers)

        # Размах
        self.R = self.x_max - self.x_min

        # Колличество интервалов
        self.k = math.ceil(1 + 3.322 * math.log10(length))

        # Шаг
        self.m = math.ceil(self.R / self.k)

        # Начало и конец
        self.x_start = round(self.x_min - self.m / 2, 1)
        self.x_end = round(self.x_max + self.m / 2, 1)

        # Интервалы
        self.table = {'x_i': []}
        t = self.x_start
        while t < self.x_end:
            self.table['x_i'].append((t, t + self.m))
            t += self.m

        # Частота
        self.table['n_i'] = [0 for _ in range(len(self.table['x_i']))]
        for item in self.numbers:
            for index, value in enumerate(self.table['x_i']):
                if value[0] < item <= value[1]:
                    self.table['n_i'][index] += 1
                    break

        # Относительная частота
        self.table['w_i'] = []
        for value in self.table['n_i']:
            self.table['w_i'].append(value / length)

        # Частота накопленная
        t = self.table['n_i'][0]
        self.table['n*_i'] = [t]
        for value in self.table['n_i'][1:]:
            t += value
            self.table['n*_i'].append(t)

        # Середина отрезка
        self.table['x_middle'] = []
        for value in self.table['x_i']:
            self.table['x_middle'].append((value[0] + value[1]) / 2)

        # Середина в квадрате
        self.table['x^2'] = []
        for value in self.table['x_middle']:
            self.table['x^2'].append(math.pow(value, 2))

        # Христос воскрес
        for x, n in zip(self.table['x_middle'], self.table['n_i']):
            self.X += x * n
        self.X /= length

        # Дисперсия
        for x, n in zip(self.table['x^2'], self.table['n_i']):
            self.S += x * n
        self.S /= length
        self.S -= self.X * self.X

        # Среднеквадратичное отклонение
        self.d = math.sqrt(self.S)

        # Мода
        index = self.table['n_i'].index(max(self.table['n_i']))
        alpha = self.table['x_i'][index][0]
        self.Mo = alpha + self.m * (self.table['n_i'][index] - self.table['n_i'][index - 1]) / \
                  ((self.table['n_i'][index] - self.table['n_i'][index - 1]) + (
                          self.table['n_i'][index] - self.table['n_i'][index + 1]))

        # Медиана
        index = 0
        for i in range(1, len(self.table['n*_i'])):
            if length / 2 <= self.table['n*_i'][i]:
                index = i
                break
        alpha = self.table['x_i'][index][0]
        self.Me = alpha + self.m * (length / 2 - self.table['n*_i'][index - 1]) / self.table['n_i'][index]

        # Куб разности
        self.table['(x-X)^3'] = []
        for value in self.table['x_middle']:
            self.table['(x-X)^3'].append(math.pow(value - self.X, 3))

        # Ассиметрия
        for x, n in zip(self.table['(x-X)^3'], self.table['n_i']):
            self.A += x * n
        self.A /= length * math.pow(self.d, 3)

        # Разность в 4 степени
        self.table['(x-X)^4'] = []
        for value in self.table['x_middle']:
            self.table['(x-X)^4'].append(math.pow(value - self.X, 4))

        # Эксцесс
        for x, n in zip(self.table['(x-X)^4'], self.table['n_i']):
            self.E += x * n
        self.E /= length * math.pow(self.d, 4)
        self.E -= 3


st.header("📊Мат статистика")
st.subheader("Интервальная выборка")
st.caption("Интервалы строятся на основе выборки, а частоты распределяются по интервалам")

data = st.text_input("Selection")

if data:
    selection = Selection(data)
    selection.calculate()

    st.text(f"Количество элементов {len(selection.numbers)}\n"
            f"Мининимальное значение x_min = {selection.x_min}\n"
            f"Максимальное значение x_max = {selection.x_max}\n"
            f"Размах R={selection.R}\n"
            f"Количество интервалов k = {selection.k}\n"
            f"Шаг интервала m = {selection.m}\n"
            f"Начало интервала x_start = {selection.x_start}\n"
            f"Конец интервала интервала x_end = {selection.x_end}\n")

    st.dataframe(selection.table)

    st.text(f"Выборочная средня X_в = {selection.X}\n"
            f"Дисперсия S^2 = {selection.S}\n"
            f"Среднеквадратичное отклонение d = {selection.d}\n"
            f"Мода Мо = {selection.Mo}\n"
            f"Медиана Ме = {selection.Me}\n"
            f"Асимметрия А = {selection.A}\n"
            f"Эксцесс E = {selection.E}")
