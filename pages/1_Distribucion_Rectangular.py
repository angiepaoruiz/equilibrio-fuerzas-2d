import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Distribución Rectangular de Fuerzas",
    layout="wide"
)

st.title("Análisis de Equilibrio de Fuerzas en 2D")

st.markdown("""
Esta aplicación genera una distribución rectangular de fuerzas:

- ∑F = 0
- ∑M = Momento solicitado
- Todas las fuerzas del lado izquierdo tienen la misma magnitud.
- Todas las fuerzas del lado derecho tienen la misma magnitud.
""")

# Estado persistente
if "forces_rect" not in st.session_state:
    st.session_state.forces_rect = [
        {"name": "F1", "position": -1.0},
        {"name": "F2", "position": 1.0}
    ]

# Botones
col1, col2 = st.columns(2)

with col1:
    if st.button("➕ Agregar fuerza"):
        idx = len(st.session_state.forces_rect) + 1
        st.session_state.forces_rect.append(
            {
                "name": f"F{idx}",
                "position": 0.0
            }
        )

with col2:
    if st.button("➖ Quitar última fuerza"):
        if len(st.session_state.forces_rect) > 2:
            st.session_state.forces_rect.pop()

# Momento solicitado
moment_expected = st.number_input(
    "Momento solicitado (Nm)",
    value=1000.0,
    step=100.0
)

st.subheader("Posiciones de las fuerzas")

positions = []
names = []

for i, force in enumerate(st.session_state.forces_rect):

    c1, c2 = st.columns([1, 2])

    with c1:
        force["name"] = st.text_input(
            f"Nombre {i + 1}",
            value=force["name"],
            key=f"name_rect_{i}"
        )

    with c2:
        force["position"] = st.number_input(
            f"Posición de {force['name']} (m)",
            value=float(force["position"]),
            key=f"pos_rect_{i}"
        )

    names.append(force["name"])
    positions.append(force["position"])

positions = np.array(positions)

st.divider()

left_idx = [i for i, x in enumerate(positions) if x < 0]
right_idx = [i for i, x in enumerate(positions) if x > 0]

if st.button("Calcular distribución rectangular"):

    if len(left_idx) == 0:
        st.error("Debe existir al menos una fuerza con posición negativa.")
        st.stop()

    if len(right_idx) == 0:
        st.error("Debe existir al menos una fuerza con posición positiva.")
        st.stop()

    brazo_total = (
        np.sum(positions[right_idx])
        - np.sum(positions[left_idx])
    )

    if abs(brazo_total) < 1e-12:
        st.error("No es posible generar momento con esta geometría.")
        st.stop()

    F = moment_expected / brazo_total

    forces = np.zeros(len(positions))

    for i in left_idx:
        forces[i] = -F

    for i in right_idx:
        forces[i] = F

    sumF = np.sum(forces)
    sumM = np.dot(forces, positions)

    st.success("Distribución rectangular calculada correctamente")

    st.subheader("Resultados")

    for i in range(len(forces)):
        st.write(
            f"**{names[i]} = {forces:.4f} N**"
        )

    st.subheader("Verificación")

    st.info(f"∑F = {sumF:.10f} N")
    st.info(f"∑M = {sumM:.10f} Nm")
    st.info(
        f"Error momento = {abs(sumM - moment_expected):.10e} Nm"
    )

    fig, ax = plt.subplots(figsize=(12, 5))

    max_force = (
        np.max(np.abs(forces))
        if np.max(np.abs(forces)) > 0
        else 1
    )

    for i in range(len(forces)):

        x = positions[i]
        f = forces[i]

        ax.arrow(
            x,
            0,
            0,
            f / max_force * 2,
            head_width=0.15,
            head_length=0.2,
            fc="blue",
            ec="blue",
            length_includes_head=True
        )

        ax.text(
            x,
            f / max_force * 2.2,
            f"{names[i]}\n{f:.2f} N",
            ha="center"
        )

    ax.axhline(0, color="black")

    ax.set_title("Distribución Rectangular de Fuerzas")
    ax.set_xlabel("Posición (m)")
    ax.set_ylabel("Fuerza")

    xmin = np.min(positions) - 1
    xmax = np.max(positions) + 1

    ax.set_xlim(xmin, xmax)
    ax.grid(True)

    st.pyplot(fig)
