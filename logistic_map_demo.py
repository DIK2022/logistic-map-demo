import sys
import numpy as np
import pyqtgraph as pg
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QSlider, QLabel
)
from PyQt6.QtCore import Qt

class LogisticMapDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Демонстрация теории хаоса: логистическое отображение")
        self.setGeometry(100, 100, 1200, 600)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Левая панель с графиками
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        # График 1: итерационная диаграмма
        self.plot_iter = pg.PlotWidget(title="Итерации (xₙ от n)")
        self.plot_iter.setLabel('left', 'xₙ')
        self.plot_iter.setLabel('bottom', 'Номер итерации')
        self.plot_iter.setXRange(0, 200)
        self.plot_iter.setYRange(0, 1)
        left_layout.addWidget(self.plot_iter)

        # График 2: бифуркационная диаграмма
        self.plot_bifur = pg.PlotWidget(title="Бифуркационная диаграмма")
        self.plot_bifur.setLabel('left', 'x')
        self.plot_bifur.setLabel('bottom', 'r')
        self.plot_bifur.setXRange(2.5, 4.0)
        self.plot_bifur.setYRange(0, 1)
        left_layout.addWidget(self.plot_bifur)

        main_layout.addWidget(left_panel, stretch=3)

        # Правая панель с управлением
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        self.label_r = QLabel("r = 3.200")
        self.label_r.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(self.label_r)

        self.slider = QSlider(Qt.Orientation.Vertical)
        self.slider.setMinimum(250)
        self.slider.setMaximum(400)
        self.slider.setValue(320)  # 3.20
        self.slider.setTickInterval(10)
        self.slider.setTickPosition(QSlider.TickPosition.TicksRight)
        self.slider.valueChanged.connect(self.on_slider_change)
        right_layout.addWidget(self.slider)

        self.label_lyap = QLabel("Показатель Ляпунова: вычисляется...")
        self.label_lyap.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(self.label_lyap)

        right_layout.addStretch()
        main_layout.addWidget(right_panel, stretch=1)

        # Данные для бифуркационной диаграммы
        self.bifur_r = []   # значения r
        self.bifur_x = []   # соответствующие x после переходного процесса
        self.bifur_scatter = pg.ScatterPlotItem(size=2, brush='w')
        self.plot_bifur.addItem(self.bifur_scatter)

        # Начальное построение
        self.update_plots()

    def on_slider_change(self):
        self.update_plots()

    def update_plots(self):
        # Получаем текущее r (слайдер выдаёт значения от 250 до 400 -> делим на 100)
        r = self.slider.value() / 100.0
        self.label_r.setText(f"r = {r:.3f}")

        # --- Итерационная диаграмма ---
        n_iter = 500   # общее число итераций
        x0 = 0.5       # начальное условие
        x = np.zeros(n_iter)
        x[0] = x0
        for i in range(1, n_iter):
            x[i] = r * x[i-1] * (1 - x[i-1])

        # Отображаем последние 200 итераций
        self.plot_iter.clear()
        self.plot_iter.plot(x[-200:], pen='y')

        # --- Обновление бифуркационной диаграммы ---
        # Для текущего r сохраняем значения x после переходного процесса (последние 100 итераций)
        transient = 400
        stable_x = x[transient:]   # значения после переходного процесса

        # Добавляем точки для этого r
        # Чтобы не перегружать график, добавляем не все точки, а каждую 2-ю (опционально)
        for val in stable_x[::2]:   # берём каждую вторую для наглядности
            self.bifur_r.append(r)
            self.bifur_x.append(val)

        # Обновляем scatter-график
        self.bifur_scatter.setData(self.bifur_r, self.bifur_x)

        # --- Вычисление показателя Ляпунова (упрощённо) ---
        lyap = self.compute_lyapunov(r, x0)
        self.label_lyap.setText(f"Показатель Ляпунова: {lyap:.4f}")

    def compute_lyapunov(self, r, x0, n=500):
        """
        Приближённое вычисление показателя Ляпунова для логистического отображения.
        λ = lim (1/n) Σ ln |f'(x_i)|
        f'(x) = r * (1 - 2x)
        """
        x = x0
        sum_ln = 0.0
        for i in range(n):
            x = r * x * (1 - x)
            # Производная
            df = abs(r * (1 - 2 * x))
            if df > 0:
                sum_ln += np.log(df)
        return sum_ln / n

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LogisticMapDemo()
    window.show()
    sys.exit(app.exec())