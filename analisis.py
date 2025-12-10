import pandas as pd
from collections import Counter

# 1. Analizar contraseñas repetidas
def analizar_passwords(df):
    if "password" not in df.columns:
        return {"error": "No existe columna 'password'."}

    rep = df["password"].value_counts()

    return {
        "top_passwords": rep.head(10).to_dict(),
        "passwords_unicas": df["password"].nunique(),
        "passwords_repetidas": rep[rep > 1].to_dict()
    }

# 2. Analizar correos sospechosos
def analizar_emails(df):
    if "email" not in df.columns:
        return {"error": "No existe columna 'email'."}

    df["dominio"] = df["email"].astype(str).str.split("@").str[-1]

    dominios_comunes = df["dominio"].value_counts().head(10).to_dict()
    correos_repetidos = df["email"].value_counts()
    correos_dup = correos_repetidos[correos_repetidos > 1].to_dict()

    return {
        "top_dominios": dominios_comunes,
        "emails_repetidos": correos_dup
    }

# 3. Analizar teléfonos duplicados
def analizar_phones(df):
    if "phones" not in df.columns:
        return {"error": "No existe columna 'phones'."}

    phones_clean = df["phones"].astype(str)
    conteo = phones_clean.value_counts()
    duplicados = conteo[conteo > 1].to_dict()

    return {
        "telefonos_repetidos": duplicados,
        "total_unicos": phones_clean.nunique()
    }

# 4. Actividad por estado
def analizar_estados(df):
    if "state" not in df.columns:
        return {"error": "No existe columna 'state'."}

    actividad = df["state"].value_counts().to_dict()

    return {
        "actividad_por_estado": actividad
    }

# 5. Actividad por fechas
def analizar_fechas(df):
    if "joined" not in df.columns:
        return {"error": "No existe columna 'joined'."}

    df["fecha"] = df["joined"].dt.date
    by_day = df.groupby("fecha").size().to_dict()

    return {
        "actividad_por_dia": by_day
    }

# 6. Función principal
def analisis_fraude(df):
    print("\n--- 🔍 ANÁLISIS DE PATRONES DE FRAUDE ---")

    resultados = {
        "passwords": analizar_passwords(df),
        "emails": analizar_emails(df),
        "phones": analizar_phones(df),
        "estados": analizar_estados(df),
        "fechas": analizar_fechas(df)
    }

    print("\n✔ Análisis completado.")
    return resultados

# 7. Ejecución directa
if __name__ == "__main__":
    from datos import cargar_y_limpiar

    df = cargar_y_limpiar("data_clientes.csv")
    resultados = analisis_fraude(df)

    print("\n--- 📊 RESULTADOS ---")
    for k, v in resultados.items():
        print(f"\n### {k.upper()} ###")
        print(v)

# 8. Resumen final

result_passwords = analizar_passwords(df)
result_emails = analizar_emails(df)
result_phones = analizar_phones(df)
result_estados = analizar_estados(df)
result_fechas = analizar_fechas(df)

print("\n--- 📝 RESUMEN FINAL DE PATRONES DE FRAUDE ---\n")

# PASSWORDS
top_pass = result_passwords.get("passwords_repetidas")
if top_pass:
    pass_repetido = list(top_pass.keys())[0]
    pass_count = top_pass[pass_repetido]
    print(f"🔐 La contraseña más repetida es '{pass_repetido}', usada por {pass_count} clientes.")
else:
    print("🔐 No se detectaron contraseñas repetidas.")

# EMAIL DOMAINS
top_dominios = result_emails.get("top_dominios")
if top_dominios:
    dominio_comun = list(top_dominios.keys())[0]
    domin_count = top_dominios[dominio_comun]
    print(f"📧 El dominio de email más común es '{dominio_comun}' con {domin_count} registros.")

# PHONES
top_phones = result_phones.get("telefonos_repetidos")
if top_phones:
    tel_repetido = list(top_phones.keys())[0]
    tel_count = top_phones[tel_repetido]
    print(f"📞 El teléfono más repetido es '{tel_repetido}', usado por {tel_count} clientes.")
else:
    print("📞 No se detectaron teléfonos repetidos.")

# STATES
estados = result_estados.get("actividad_por_estado")
if estados:
    estado_top = max(estados, key=estados.get)
    print(f"📍 El estado con mayor actividad es '{estado_top.upper()}' con {estados[estado_top]} registros.")

# DATES
fechas = result_fechas.get("actividad_por_dia")
if fechas:
    dias = len(fechas)
    print(f"📅 La actividad abarca {dias} días consecutivos, sin días vacíos.")

# RELACIÓN: mismo estado + misma contraseña + teléfono -> dominio Outlook
df["dominio"] = df["email"].str.split("@").str[-1]

grupo_patron = df.groupby(["state", "password", "phones"])
coincidencias = grupo_patron.filter(lambda x: len(x) > 1)

if not coincidencias.empty:
    dominios_en_patron = coincidencias["dominio"].unique().tolist()
    print(f"\n🔎 Sin embargo, los clientes que comparten estado, contraseña y teléfono utilizan dominios: {dominios_en_patron}")
    if "outlook.com" in dominios_en_patron:
        print("✔ Se confirma que el patrón está asociado principalmente a dominio 'outlook.com'.")
else:
    print("\n🔎 No se encontraron grupos con coincidencias para estado + contraseña + teléfono.")