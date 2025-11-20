import streamlit as st
import pandas as pd
import re
from io import StringIO


# --- FUNCIÓN CENTRAL DE LIMPIEZA ---
@st.cache_data
def limpiar_numeros(uploaded_file):
    """Limpia la primera columna de números de teléfono y devuelve la lista limpia y el DataFrame."""

    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    df = pd.read_csv(stringio, dtype=str)

    columna_telefonos = df.iloc[:, 0]
    lista_numeros_limpios = []

    for item in columna_telefonos:
        texto = str(item)
        solo_digitos = re.sub(r'\D', '', texto)

        if len(solo_digitos) > 8:
            lista_numeros_limpios.append(solo_digitos)

    df_output = pd.DataFrame(lista_numeros_limpios, columns=['Telefono_Limpio'])

    return lista_numeros_limpios, df_output


# --- ESTRUCTURA DE LA APLICACIÓN STREAMLIT ---
st.set_page_config(page_title="Extractor de Números")
st.title("📞 Limpiador de Teléfonos CSV (Web App)")

st.markdown("""
Sube tu archivo CSV. La aplicación extrae, limpia y ofrece el resultado para **descarga** o para **copiar** directamente.
""")

uploaded_file = st.file_uploader("1. Sube tu archivo CSV", type="csv")

if uploaded_file is not None:
    st.success(f"Archivo cargado: {uploaded_file.name}")

    if st.button("2. Procesar y Limpiar"):
        with st.spinner('Procesando datos...'):
            try:
                list_cleaned, df_cleaned = limpiar_numeros(uploaded_file)
                comma_separated_text = ",".join(list_cleaned)  # Unimos con comas

                if not df_cleaned.empty:
                    st.subheader(f"✅ Proceso terminado: {len(df_cleaned)} números limpios encontrados.")
                    st.markdown("---")

                    # 🚀 NUEVA OPCIÓN: CAMPO DE TEXTO PARA COPIAR 🚀
                    st.subheader("3. Copiar en Portapapeles (Separado por Comas)")
                    st.caption("Copia todo el texto a continuación y pégalo donde lo necesites.")

                    # El campo de texto permite al usuario seleccionar todo el contenido y copiarlo
                    st.text_area(
                        label="Resultado Separado por Comas",
                        value=comma_separated_text,
                        height=150,
                        key="copy_area"
                    )

                    st.markdown("---")

                    # --- 💾 OPCIÓN 1: DESCARGA VERTICAL (CSV) ---
                    csv_data = df_cleaned.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="⬇️ Descargar en Columna (CSV)",
                        data=csv_data,
                        file_name="telefonos_limpios_columna.csv",
                        mime="text/csv"
                    )

                    # --- 💾 OPCIÓN 2: DESCARGA SEPARADA POR COMAS (TXT) ---
                    txt_data = comma_separated_text.encode('utf-8')
                    st.download_button(
                        label="⬇️ Descargar en una Línea (TXT)",
                        data=txt_data,
                        file_name="telefonos_limpios_comas.txt",
                        mime="text/plain"
                    )

                    st.markdown("---")
                    st.caption("Previsualización de los primeros 10 números (en formato vertical):")
                    st.dataframe(df_cleaned.head(10))
                else:
                    st.warning("No se encontraron números válidos (más de 8 dígitos) para limpiar.")

            except Exception as e:
                st.error(f"Hubo un error. Detalles: {e}")