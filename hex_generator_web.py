import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import RendererAgg
import streamlit as st
from scipy.special import comb

# Кэшируем вычисления для производительности
@st.cache_data
def bernstein_poly(i, n, t):
    return comb(n, i) * (t ** i) * ((1 - t) ** (n - i))

@st.cache_data
def bezier_curve(control_points, num_points=100):
    n = len(control_points) - 1
    t = np.linspace(0, 1, num_points)
    curve = np.zeros((num_points, 2))
    for i in range(n + 1):
        curve += np.outer(bernstein_poly(i, n, t), control_points[i])
    return curve

class DraggablePoints:
    def __init__(self, ax, control_points):
        self.ax = ax
        self.control_points = control_points
        self.points, = ax.plot(
            control_points[:, 0], control_points[:, 1], 
            'ro-', markersize=8, linewidth=1, picker=5
        )
        self.current_point = None
        self.cid_press = ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cid_motion = ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.cid_release = ax.figure.canvas.mpl_connect('button_release_event', self.on_release)

    def on_press(self, event):
        if event.inaxes != self.ax:
            return
        contains, ind = self.points.contains(event)
        if contains:
            self.current_point = ind["ind"][0]

    def on_motion(self, event):
        if self.current_point is None or event.inaxes != self.ax:
            return
        self.control_points[self.current_point] = [event.xdata, event.ydata]
        self.update_plot()

    def on_release(self, event):
        self.current_point = None
        self.update_plot()

    def update_plot(self):
        self.points.set_data(self.control_points[:, 0], self.control_points[:, 1])
        self.ax.figure.canvas.draw()

# Интерфейс Streamlit
st.title("🎨 Редактор кривой Безье")
st.markdown("Перемещайте красные точки мышкой!")

# Инициализация контрольных точек
if 'control_points' not in st.session_state:
    st.session_state.control_points = np.array([
        [0.1, 0.2], [0.3, 0.8], [0.7, 0.9], [0.9, 0.3]
    ])

# Создание графика
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.grid(True)

# Кривая Безье
curve = bezier_curve(st.session_state.control_points)
ax.plot(curve[:, 0], curve[:, 1], 'b-', linewidth=2)

# Интерактивные точки
draggable = DraggablePoints(ax, st.session_state.control_points)

# Обновление кривой при перемещении точек
def update_curve():
    curve = bezier_curve(st.session_state.control_points)
    ax.lines[0].set_data(curve[:, 0], curve[:, 1])
    fig.canvas.draw()

# Отображение в Streamlit
with st.container():
    st.pyplot(fig)

# Кнопка для сброса точек
if st.button("Сбросить точки"):
    st.session_state.control_points = np.array([
        [0.1, 0.2], [0.3, 0.8], [0.7, 0.9], [0.9, 0.3]
    ])
    update_curve()
