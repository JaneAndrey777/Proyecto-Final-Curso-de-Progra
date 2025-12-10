import pandas as pd
import matplotlib.pyplot as plt

# ======== 1. CARGAR ARCHIVO ========
print("📥 Cargando archivo limpio...")
df = pd.read_csv("clean_data.csv", sep=";")  # Ajusta el nombre si tu archivo se llama distinto
print("✔ Datos cargados correctamente.")
print(f"📊 Registros: {len(df)}")

# ======== 2. CONFIG ESTILO ROSADO ========
pink = "#ff4fa3"

plt.rcParams["text.color"] = pink
plt.rcParams["axes.labelcolor"] = pink
plt.rcParams["xtick.color"] = pink
plt.rcParams["ytick.color"] = pink
plt.rcParams["axes.edgecolor"] = pink
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.titleweight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"

# ======== 3. PROCESAR CAMPOS ========
df["email_domain"] = df["email"].str.split("@").str[1]

password_counts = df["password"].value_counts().head(10)
state_counts = df["state"].value_counts().head(10)
phone_counts = df["phones"].value_counts().head(10)
domain_counts = df["email_domain"].value_counts().head(10)

# ======== 4. DASHBOARD ========
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Dashboard de Patrones Fraudulentos", fontsize=18, fontweight="bold", color=pink)

# 1. Passwords repetidas
axes[0, 0].bar(password_counts.index.astype(str), password_counts.values)
axes[0, 0].set_title("Passwords más repetidas")
axes[0, 0].set_ylabel("Repeticiones")

# 2. Estados
axes[0, 1].bar(state_counts.index.astype(str), state_counts.values)
axes[0, 1].set_title("Estados con más cuentas")

# 3. Teléfonos
axes[1, 0].bar(phone_counts.index.astype(str), phone_counts.values)
axes[1, 0].set_title("Teléfonos más repetidos")

# 4. Dominios email
axes[1, 1].bar(domain_counts.index.astype(str), domain_counts.values)
axes[1, 1].set_title("Dominios de email más comunes")

plt.tight_layout()
plt.show()