import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

archivo_produccion = os.path.join(BASE_DIR, "data", "plan_produccion.csv")
archivo_ventas = os.path.join(BASE_DIR, "data", "sistema_venta.csv")

salida_detalle = os.path.join(BASE_DIR, "outputs", "consolidado_limpio.xlsx")
salida_resumen = os.path.join(BASE_DIR, "outputs", "resumen_producto.xlsx")

print("Iniciando proceso")
print(f"Ruta base del proyecto: {BASE_DIR}")

df_prod = pd.read_csv(archivo_produccion)
df_ventas = pd.read_csv(archivo_ventas)

print("Archivos leidos correctamente")

df_prod = df_prod.rename(columns={
    "produccion_real": "produccion",
    "ventas_asociadas": "ventas",
    "ciudad_destino": "ciudad",
    "fecha_produccion": "fecha"
})

df_ventas = df_ventas.rename(columns={
    "unidades_vendidas": "ventas",
    "stock_recibido": "produccion",
    "importe_total": "ingreso",
    "fecha_venta": "fecha"
})

columnas_prod = ["producto", "produccion", "ventas", "precio_unitario", "ciudad", "fecha"]
columnas_ventas = ["producto", "produccion", "ventas", "precio_unitario", "ciudad", "fecha"]

df_prod = df_prod[columnas_prod]
df_ventas = df_ventas[columnas_ventas]

df = pd.concat([df_prod, df_ventas], ignore_index=True)

print("Archivos unidos correctamente")

df = df.drop_duplicates()

for col in ["produccion", "ventas", "precio_unitario"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df[["produccion", "ventas", "precio_unitario"]] = df[["produccion", "ventas", "precio_unitario"]].fillna(0)

df = df[df["precio_unitario"] >= 0]

df["producto"] = df["producto"].fillna("SIN_DATO")
df["ciudad"] = df["ciudad"].fillna("SIN_DATO")
df["fecha"] = df["fecha"].fillna("SIN_FECHA")

df["ingreso"] = df["ventas"] * df["precio_unitario"]
df["diferencia"] = df["produccion"] - df["ventas"]

df["nivel_venta"] = df.apply(
    lambda row: row["ventas"] / row["produccion"] if row["produccion"] != 0 else 0,
    axis=1
)

def estado_stock(x):
    if x > 50:
        return "SobreStock"
    elif x > 0:
        return "Stock_OK"
    else:
        return "SinStock"

df["estado_stock"] = df["diferencia"].apply(estado_stock)

def clasificacion_venta(x):
    if x > 0.8:
        return "Alta"
    elif x > 0.5:
        return "Media"
    else:
        return "Baja"

df["clasificacion_venta"] = df["nivel_venta"].apply(clasificacion_venta)
df["porcentaje_venta"] = (df["nivel_venta"] * 100).round(2)

df = df.sort_values(by=["producto", "fecha"]).reset_index(drop=True)

print("Limpieza completada")

df_resumen = df.groupby("producto").agg(
    produccion=("produccion", "sum"),
    ventas=("ventas", "sum"),
    ingreso=("ingreso", "sum")
).reset_index()

df_resumen["diferencia"] = df_resumen["produccion"] - df_resumen["ventas"]

df_resumen["nivel_venta"] = df_resumen.apply(
    lambda row: row["ventas"] / row["produccion"] if row["produccion"] != 0 else 0,
    axis=1
)

df_resumen["estado_stock"] = df_resumen["diferencia"].apply(estado_stock)
df_resumen["clasificacion_venta"] = df_resumen["nivel_venta"].apply(clasificacion_venta)
df_resumen["porcentaje_venta"] = (df_resumen["nivel_venta"] * 100).round(2)

df_resumen = df_resumen.sort_values(by="ventas", ascending=False).reset_index(drop=True)

print("Resumen analitico generado")

os.makedirs(os.path.join(BASE_DIR, "outputs"), exist_ok=True)

df.to_excel(salida_detalle, index=False)
df_resumen.to_excel(salida_resumen, index=False)

print("Proceso finalizado correctamente")
print(f"Archivo detalle generado: {salida_detalle}")
print(f"Archivo resumen generado: {salida_resumen}")