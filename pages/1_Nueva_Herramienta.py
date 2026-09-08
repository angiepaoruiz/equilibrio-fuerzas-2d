import streamlit as st

st.title("Nueva Herramienta")

valor = st.number_input("Ingrese un valor")

if st.button("Procesar"):
    st.write(f"Resultado: {valor}")
