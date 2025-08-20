
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Análisis de Fuerzas en 2D", layout="wide")

st.title("Aplicación de Estática Estructural en 2D")

st.markdown("""
Esta aplicación permite ingresar fuerzas con nombre, distancia y dirección, y calcula los valores necesarios para que el sistema esté en equilibrio (∑F = 0 y ∑M = Momento esperado).
""")

# Entrada del número de fuerzas
num_forces = st.number_input("Número de fuerzas", min_value=1, max_value=10, value=3)

# Entrada de datos de fuerzas
forces_data = []
st.subheader("Datos de las fuerzas")
for i in range(num_forces):
    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input(f"Nombre de la fuerza {i+1}", value=f"F{i+1}")
    with col2:
        distance = st.number_input(f"Distancia de {name} (m)", value=1.0, key=f"dist_{i}")
    with col3:
        direction = st.selectbox(f"Dirección de {name}", options=["Positiva", "Negativa"], key=f"dir_{i}")
    forces_data.append({"name": name, "distance": distance, "direction": 1 if direction == "Positiva" else -1})

# Entrada del momento esperado
moment_expected = st.number_input("Momento esperado (Nm)", value=0.0)

# Botón para calcular
if st.button("Calcular fuerzas para equilibrio"):
    distances = np.array([f["distance"] for f in forces_data])
    directions = np.array([f["direction"] for f in forces_data])

    # Matriz de coeficientes
    A = np.vstack([directions, distances * directions])
    b = np.array([0, moment_expected])

    # Resolver sistema de ecuaciones
    try:
        forces = np.linalg.lstsq(A.T, b, rcond=None)[0]
        st.success("Sistema resuelto correctamente.")
        for i, f in enumerate(forces):
            st.write(f"{forces_data[i]['name']}: {f:.2f} N")
    except Exception as e:
        st.error(f"Error al resolver el sistema: {e}")
        forces = [0] * num_forces

    # Gráfico de fuerzas
    fig, ax = plt.subplots(figsize=(10, 4))
    for i, f in enumerate(forces):
        x = distances[i]
        ax.arrow(x, 0, 0, f / 10, head_width=0.2, head_length=0.5, fc='blue', ec='blue')
        ax.text(x, f / 10 + 0.5, f"{forces_data[i]['name']} ({f:.2f} N)", ha='center')
    ax.axhline(0, color='black', linewidth=0.5)
    ax.set_xlim(0, max(distances) + 1)
    ax.set_ylim(-max(abs(np.array(forces))) / 5 - 2, max(abs(np.array(forces))) / 5 + 2)
    ax.set_title("Distribución de Fuerzas Calculadas")
    ax.set_xlabel("Distancia (m)")
    ax.set_ylabel("Fuerza (N)")
    st.pyplot(fig)
