import pandas as pd
import matplotlib.pyplot as plt
from datos import cargar_y_limpiar

#Configuración visual
COLOR = "#FF0080"
plt.rcParams["font.size"] = 11
plt.rcParams["font.weight"] = "bold"

df = cargar_y_limpiar("data_clientes.csv")

# VALIDACIONES BÁSICAS
columnas_necesarias = ["password", "phones", "state", "email"]

for col in columnas_necesarias:
    if col not in df.columns:
        raise ValueError(f"Falta la columna requerida: {col}")

# PREPARACIÓN DE DATOS
df["email_domain"] = df["email"].astype(str).str.split("@").str[-1]

passwords_rep = df["password"].value_counts().head(5)
phones_rep = df["phones"].value_counts().head(5)
states_rep = df["state"].value_counts().head(5)
domains_rep = df["email_domain"].value_counts().head(5)

# DASHBOARD
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle(
    "Fraud Pattern Dashboard\nShared Credentials & Locations",
    fontsize=18,
    fontweight="bold",
    color=COLOR
)

# -------- Passwords --------
axs[0, 0].bar(passwords_rep.index, passwords_rep.values, color=COLOR)
axs[0, 0].set_title("Most Shared Passwords", fontsize=14, color=COLOR)
axs[0, 0].tick_params(axis="x", rotation=30)

# -------- Phones --------
axs[0, 1].bar(phones_rep.index, phones_rep.values, color=COLOR)
axs[0, 1].set_title("Shared Phone Numbers", fontsize=14, color=COLOR)
axs[0, 1].tick_params(axis="x", rotation=30)

# -------- States --------
axs[1, 0].bar(states_rep.index.str.upper(), states_rep.values, color=COLOR)
axs[1, 0].set_title("Accounts by State", fontsize=14, color=COLOR)

# -------- Email Domains --------
axs[1, 1].bar(domains_rep.index, domains_rep.values, color=COLOR)
axs[1, 1].set_title("Email Domains Used", fontsize=14, color=COLOR)

# ======================
# AJUSTES FINALES
# ======================
for ax in axs.flat:
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.set_ylabel("Number of Accounts", fontweight="bold")

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
