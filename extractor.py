import streamlit as st
import pandas as pd
import re
from io import StringIO


# --- FUNCIÓN CENTRAL DE LIMPIEZA ---
# Se utiliza la caché para que la limpieza no se repita si solo se cambia la opción de descarga.
@st.cache_data
def limpiar_numeros(uploaded_file):
    """Limpia la primera columna de números de teléfono y devuelve el DataFrame."""

    # Leer el contenido del archivo subido como texto
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

    # Leer CSV, asumiendo que la primera columna es la de teléfonos
    df = pd.read_csv(stringio, dtype=str)

    columna_telefonos = df.iloc[:, 0]
    lista_numeros_limpios = []

    for item in columna_telefonos:
        texto = str(item)

        # Limpieza con Regex: Elimina todo lo que NO sea un dígito
        solo_digitos = re.sub(r'\D', '', texto)

        # Validación de longitud (para evitar nombres/fragmentos)
        if len(solo_digitos) > 8:
            # Opción: Filtrar duplicados, si es necesario, se haría aquí.
            lista_numeros_limpios.append(solo_digitos)

    # 3. Crear el DataFrame final
    df_output = pd.DataFrame(lista_numeros_limpios, columns=['Telefono_Limpio'])

    return lista_numeros_limpios, df_output


# --- ESTRUCTURA DE LA APLICACIÓN STREAMLIT ---
st.set_page_config(page_title="Extractor de Números")
st.title("📞 Limpiador de Teléfonos CSV (Web App)")

st.markdown("""
Sube tu archivo CSV. La aplicación extraerá y limpiará la **primera columna** de números, eliminando texto y símbolos, y te ofrecerá dos formatos de descarga.
""")

uploaded_file = st.file_uploader("1. Sube tu archivo CSV", type="csv")

if uploaded_file is not None:
    st.success(f"Archivo cargado: {uploaded_file.name}")

    # Botón de Procesar
    if st.button("2. Procesar y Limpiar"):
        with st.spinner('Procesando datos...'):
            try:
                # 4. Ejecutar la función de limpieza, obteniendo la lista y el DataFrame
                list_cleaned, df_cleaned = limpiar_numeros(uploaded_file)

                if not df_cleaned.empty:
                    st.subheader(f"✅ Proceso terminado: {len(df_cleaned)} números limpios encontrados.")
                    st.markdown("---")

                    # --- 💾 OPCIÓN 1: DESCARGA VERTICAL (CSV) ---
                    # El formato CSV es el que deja los números en una columna (vertical).
                    csv_data = df_cleaned.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="⬇️ Descargar en Columna (CSV)",
                        data=csv_data,
                        file_name="telefonos_limpios_columna.csv",
                        mime="text/csv"
                    )

                    # --- 💾 OPCIÓN 2: DESCARGA SEPARADA POR COMAS (TXT) ---
                    # Unimos la lista con una coma (",") para el formato TXT horizontal.
                    comma_separated_text = ",".join(list_cleaned).encode('utf-8')
                    st.download_button(
                        label="⬇️ Descargar Separado por Comas (TXT)",
                        data=comma_separated_text,
                        file_name="telefonos_limpios_comas.txt",
                        mime="text/plain"
                    )

                    st.markdown("---")
                    st.caption("Previsualización de los primeros 10 números (en formato vertical):")
                    st.dataframe(df_cleaned.head(10))
                else:
                    st.warning(
                        "No se encontraron números válidos (más de 8 dígitos) para limpiar en la primera columna.")

            except Exception as e:
                st.error(
                    f"Hubo un error: Asegúrate de que el archivo sea un CSV válido y que la primera columna exista. Detalles: {e}")