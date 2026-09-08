import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# --------------------------------------------------

st.set_page_config(
    page_title="Equilibrio de Fuerzas 2D",
    layout="wide"
)

st.title("Distribución Rectangular de Fuerzas")

st.markdown("""
Esta aplicación calcula una distribución rectangular de fuerzas:

- ΣF = 0
- ΣM = Momento solicitado
- Todas las fuerzas del lado izquierdo son iguales.
- Todas las fuerzas del lado derecho son iguales.
""")

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "forces_list" not in st.session_state:
    st.session_state.forces_list = [
        {"name": "F1", "position": -1.0},
        {"name": "F2", "position": 1.0}
    ]

# --------------------------------------------------
# BOTONES
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    if st.button("➕ Agregar fuerza"):
        n = len(st.session_state.forces_list) + 1

        st.session_state.forces_list.append(
            {
                "name": f"F{n}",
                "position": 0.0
            }
        )

with col2:
    if (
        st.button("➖ Quitar última fuerza")
        and len(st.session_state.forces_list) > 2
    ):
        st.session_state.forces_list.pop()

# --------------------------------------------------
# MOMENTO
# --------------------------------------------------

moment_expected = st.number_input(
    "Momento solicitado (Nm)",
    value=1000.0,
    step=100.0
)

# --------------------------------------------------
# DEFINICIÓN DE POSICIONES
# --------------------------------------------------

st.subheader("Posiciones")

positions = []
names = []

for i, item in enumerate(st.session_state.forces_list):

    c1, c2 = st.columns([1, 2])

    with c1:
        item["name"] = st.text_input(
            f"Nombre fuerza {i + 1}",
            value=item["name"],
            key=f"name_{i}"
        )

    with c2:
        item["position"] = st.number_input(
            f"Posición de {item['name']} (m)",
            value=float(item["position"]),
            key=f"pos_{i}"
        )

    names.append(item["name"])
    positions.append(item["position"])

positions = np.array(positions, dtype=float)

# --------------------------------------------------
# CÁLCULO
# --------------------------------------------------

if st.button("Calcular distribución"):

    left_idx = [i for i, x in enumerate(positions) if x < 0]
    right_idx = [i for i, x in enumerate(positions) if x > 0]

    if len(left_idx) == 0:
        st.error(
            "Debe existir al menos una posición negativa."
 
