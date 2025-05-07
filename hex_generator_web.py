import numpy as np
import matplotlib.pyplot as plt
from scipy.special import comb
import streamlit as st
from matplotlib.backends.backend_agg import RendererAgg

# Инициализация контрольных точек
if 'control_points' not in st.session_state:
    st.session_state.control_points = np.array([
        [0.1, 0.2], [0.3, 0.8], [0.7, 0.9], [0.9, 0.3]
    ])

# Функции для кривой Безье
def bernstein_poly(i, n, t):
    return comb(n, i) * (t ** i) * ((1 - t) ** (n - i))

def bezier_curve(control_points, num_points=100):
    n = len(control_points) - 1
    t = np.linspace(0, 1, num_points)
    curve = np.zeros((num_points, 2))
    for i in range(n + 1):
        curve += np.outer(bernstein_poly(i, n, t), control_points[i])
    return curve

# Создание графика
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.grid(True)

# Отрисовка кривой и точек
curve = bezier_curve(st.session_state.control_points)
line, = ax.plot(curve[:, 0], curve[:, 1], 'b-', linewidth=2)
points, = ax.plot(
    st.session_state.control_points[:, 0],
    st.session_state.control_points[:, 1],
    'ro-', markersize=8, linewidth=1, picker=5
)

# Обработка событий мыши
def on_click(event):
    if event.inaxes != ax:
        return
    contains, ind = points.contains(event)
    if contains:
        st.session_state.dragging = True
        st.session_state.selected_point = ind["ind"][0]

def on_motion(event):
    if not hasattr(st.session_state, 'dragging') or not st.session_state.dragging:
        return
    if event.inaxes != ax:
        return
    idx = st.session_state.selected_point
    st.session_state.control_points[idx] = [event.xdata, event.ydata]
    # Обновляем кривую
    new_curve = bezier_curve(st.session_state.control_points)
    line.set_data(new_curve[:, 0], new_curve[:, 1])
    points.set_data(
        st.session_state.control_points[:, 0],
        st.session_state.control_points[:, 1]
    )
    fig.canvas.draw()

def on_release(event):
    st.session_state.dragging = False

# Подключаем события
fig.canvas.mpl_connect('button_press_event', on_click)
fig.canvas.mpl_connect('motion_notify_event', on_motion)
fig.canvas.mpl_connect('button_release_event', on_release)

# Интерфейс Streamlit
st.title("🎨 Интерактивная кривая Безье")
st.markdown("**Перетаскивайте красные точки мышкой!**")

# Отображение графика
st.pyplot(fig, use_container_width=True)

# Кнопка сброса
if st.button("Сбросить точки"):
    st.session_state.control_points = np.array([
        [0.1, 0.2], [0.3, 0.8], [0.7, 0.9], [0.9, 0.3]
    ])
    st.experimental_rerun()
