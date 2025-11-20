import streamlit as st
import pandas as pd
import re
from io import StringIO


# --- FUNCIÓN CENTRAL DE LIMPIEZA ---
# Se modificó para leer el archivo subido por Streamlit y devolver los datos.
@st.cache_data
def limpiar_numeros(uploaded_file):
    """Limpia la primera columna de números de teléfono y devuelve el DataFrame."""

    # 1. Leer el contenido del archivo subido como texto
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

    # 2. Leer CSV, asumiendo que la primera columna es la de teléfonos
    df = pd.read_csv(stringio, dtype=str)

    columna_telefonos = df.iloc[:, 0]
    lista_numeros_limpios = []

    for item in columna_telefonos:
        texto = str(item)

        # Limpieza con Regex: Elimina todo lo que NO sea número
        solo_digitos = re.sub(r'\D', '', texto)

        # Validación de longitud (para evitar nombres/fragmentos)
        if len(solo_digitos) > 8:
            lista_numeros_limpios.append(solo_digitos)

    # 3. Convertir la lista limpia a un DataFrame para el resultado
    df_output = pd.DataFrame(lista_numeros_limpios, columns=['Telefono_Limpio'])

    return df_output


# --- ESTRUCTURA DE LA APLICACIÓN STREAMLIT ---
st.set_page_config(page_title="Extractor de Números")
st.title("📞 Limpiador de Teléfonos CSV (Web App)")

st.markdown("""
Sube tu archivo CSV. La aplicación extraerá y limpiará la **primera columna** de números, eliminando texto, símbolos y caracteres extraños, y los dejará en formato vertical.
""")

uploaded_file = st.file_uploader("1. Sube tu archivo CSV", type="csv")

if uploaded_file is not None:
    st.success(f"Archivo cargado: {uploaded_file.name}")

    # Botón de Procesar
    if st.button("2. Procesar y Limpiar"):
        with st.spinner('Procesando datos...'):
            try:
                # 4. Ejecutar la función de limpieza
                df_cleaned = limpiar_numeros(uploaded_file)

                if not df_cleaned.empty:
                    st.subheader(f"✅ Proceso terminado: {len(df_cleaned)} números limpios encontrados.")

                    # Convertir el DataFrame limpio a formato CSV para la descarga
                    csv_data = df_cleaned.to_csv(index=False)

                    # 5. Botón de Descarga
                    st.download_button(
                        label="3. Descargar Archivo Limpio (.csv)",
                        data=csv_data,
                        file_name="telefonos_limpios.csv",
                        mime="text/csv"
                    )

                    st.markdown("---")
                    st.caption("Previsualización de los primeros 10 números:")
                    st.dataframe(df_cleaned.head(10))
                else:
                    st.warning(
                        "No se encontraron números válidos (más de 8 dígitos) para limpiar en la primera columna.")

            except Exception as e:
                st.error(
                    f"Hubo un error: Asegúrate de que el archivo sea un CSV válido y que la primera columna exista. Error: {e}")