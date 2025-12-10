from analisis import analizar_passwords, analizar_emails, analizar_phones, analizar_estados, analizar_fechas
from datos import cargar_y_limpiar

df = cargar_y_limpiar("data_clientes.csv")

result_pass = analizar_passwords(df)
result_email = analizar_emails(df)
result_phone = analizar_phones(df)
result_state = analizar_estados(df)
result_dates = analizar_fechas(df)

top_password = list(result_pass["passwords_repetidas"].keys())[0]
top_domain = list(result_email["top_dominios"].keys())[0]
top_phone = list(result_phone["telefonos_repetidos"].keys())[0]
top_state = max(result_state["actividad_por_estado"], key=result_state["actividad_por_estado"].get)
dias_consecutivos = len(result_dates["actividad_por_dia"])

html = f"""
<h1>Dashboard de Fraude</h1>

<p><b>Contraseña más repetida:</b> {top_password}</p>
<p><b>Dominio más común:</b> {top_domain}</p>
<p><b>Teléfono más repetido:</b> {top_phone}</p>
<p><b>Estado con más actividad:</b> {top_state}</p>
<p><b>Días consecutivos analizados:</b> {dias_consecutivos}</p>

<h2>Patrón Detectado:</h2>
<p>Clientes del mismo estado + misma contraseña + mismo teléfono = dominio OUTLOOK</p>
"""

with open("dashboard.html", "w") as f:
    f.write(html)

print("Dashboard generado: dashboard.html")