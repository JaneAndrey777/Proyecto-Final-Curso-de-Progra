import pandas as pd

def cargar_y_limpiar(ruta_archivo):
    """
    Lee el archivo CSV, limpia la data y devuelve un DataFrame listo para análisis.
    """
    try:
        print("📥 Cargando archivo...")

        # Detecta automáticamente CSV o Excel
        if ruta_archivo.endswith(".csv"):
            df = pd.read_csv(ruta_archivo, sep=";")   # 👈 CORRECCIÓN IMPORTANTE
        else:
            df = pd.read_excel(ruta_archivo)

        print("✔ Archivo cargado correctamente.")

        # 1. LIMPIEZA GENERAL

        # Normalizar nombres de columnas
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
            .str.replace("-", "_")
        )

        # Quitar duplicados
        df = df.drop_duplicates()

        # Manejo de valores nulos
        df = df.fillna({
            "email": "unknown",
            "phones": "unknown",
            "password": "unknown",
            "state": "unknown"
        })

        # Convertir columna de fecha a datetime
        if "joined" in df.columns:
            df["joined"] = pd.to_datetime(df["joined"], errors="coerce")

        # Filtrar solo noviembre–diciembre (fraude reportado)
        if "joined" in df.columns:
            df = df[
                (df["joined"].dt.month == 11) |
                (df["joined"].dt.month == 12)
            ]

        print(f"📊 Registros filtrados (nov–dic): {len(df)}")


        # 2. LIMPIEZA DE NOMBRES

        columnas_nombres = [col for col in df.columns if "name" in col or col == "customer"]

        for col in columnas_nombres:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(r"[^a-zA-ZáéíóúüñÁÉÍÓÚÜÑ' ]", "", regex=True)  # quitar ? ! % * etc
                .str.replace(r"\s+", " ", regex=True)
                .str.strip()
                .str.title()
            )


        # 3. LIMPIEZA ESPECÍFICA PARA DETECCIÓN DE FRAUDE

        if "phones" in df.columns:
            df["phones"] = df["phones"].astype(str).str.replace(r"\D", "", regex=True)

        if "password" in df.columns:
            df["password"] = df["password"].astype(str).str.lower().str.strip()

        if "email" in df.columns:
            df["email"] = df["email"].astype(str).str.lower().str.strip()

        if "state" in df.columns:
            df["state"] = df["state"].astype(str).str.lower().str.strip()

        print("✨ Limpieza completada.")

        return df

    except Exception as e:
        print(f"❌ Error al limpiar los datos: {e}")
        return pd.DataFrame()


if __name__ == "__main__":
    ruta = "data_clientes.csv"
    df_limpio = cargar_y_limpiar(ruta)

    print("\n--- Vista previa de datos limpios ---")
    print(df_limpio.head())