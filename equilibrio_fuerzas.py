
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Configuración de la página
st.set_page_config(page_title="Equilibrio de Fuerzas 2D", layout="wide")
st.title("Análisis de Equilibrio de Fuerzas en 2D")

st.markdown("""
Esta aplicación permite agregar o quitar fuerzas dinámicamente, definir sus posiciones y calcular automáticamente los valores que cumplen:
- ∑F = 0 (equilibrio de fuerzas)
- ∑M = Momento esperado (equilibrio de momentos)
""")

# Estado persistente para fuerzas
if "forces" not in st.session_state:
    st.session_state.forces = [{"name": "F1", "position": 0.0}]

# Botones para agregar o quitar fuerzas
col_add, col_remove = st.columns(2)
with col_add:
    if st.button("➕ Agregar fuerza"):
        idx = len(st.session_state.forces) + 1
        st.session_state.forces.append({"name": f"F{idx}", "position": 0.0})
with col_remove:
    if st.button("➖ Quitar última fuerza") and len(st.session_state.forces) > 1:
        st.session_state.forces.pop()

# Entrada del momento esperado
moment_expected = st.number_input("Momento esperado (Nm)", value=0.0)

# Entrada de posiciones
st.subheader("Posiciones de las fuerzas (en metros)")
positions = []
names = []
for i, force in enumerate(st.session_state.forces):
    col1, col2 = st.columns([1, 2])
    with col1:
        force["name"] = st.text_input(f"Nombre de fuerza {i+1}", value=force["name"], key=f"name_{i}")
    with col2:
        force["position"] = st.number_input(f"Posición de {force['name']}", value=force["position"], key=f"pos_{i}")
    positions.append(force["position"])
    names.append(force["name"])

# Función objetivo
def objective(F):
    return 0  # Solo se usan restricciones

# Restricciones estrictas
constraints = [
    {'type': 'eq', 'fun': lambda F: np.sum(F)},
    {'type': 'eq', 'fun': lambda F: np.dot(F, positions) - moment_expected}
]

# Optimización
initial_guess = [0.0] * len(positions)
result = minimize(objective, initial_guess, constraints=constraints)

if result.success:
    forces = result.x
    st.success("Fuerzas encontradas que cumplen con las condiciones de equilibrio:")
    for i in range(len(forces)):
        st.write(f"{names[i]} = {forces[i]:.4f} N")

    # Verificación
    sumF = np.sum(forces)
    sumM = np.dot(forces, positions)
    st.info(f"∑F = {sumF:.4f} N")
    st.info(f"∑M = {sumM:.4f} Nm")
    st.info(f"Diferencia absoluta = {abs(sumM - moment_expected):.10f} Nm")

    # Mostrar gráfico
    fig, ax = plt.subplots(figsize=(10, 4))
    for i in range(len(forces)):
        x = positions[i]
        f = forces[i]
        ax.arrow(x, 0, 0, f / 10, head_width=0.2, head_length=0.5, fc='blue', ec='blue')
        ax.text(x, f / 10 + 0.5, f"{names[i]} = {f:.4f} N", ha='center')
    ax.axhline(0, color='black', linewidth=0.5)
    ax.set_xlim(min(positions) - 1, max(positions) + 1)
    ax.set_ylim(-max(abs(np.array(forces))) / 5 - 2, max(abs(np.array(forces))) / 5 + 2)
    ax.set_title("Distribución de Fuerzas en Equilibrio")
    ax.set_xlabel("Distancia (m)")
    ax.set_ylabel("Fuerza (N)")
    st.pyplot(fig)
else:
    st.error("No se pudo encontrar una solución que cumpla con las condiciones de equilibrio.")
