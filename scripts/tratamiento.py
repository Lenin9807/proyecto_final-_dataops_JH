import pandas as pd
import os

BASE_DIR = os.environ.get("WORKSPACE", r"C:\Usuarios\USER\workspace\proyecto_final_dataops")

archivo_produccion = os.path.join(BASE_DIR, "data", "plan_produccion.csv")
archivo_ventas = os.path.join(BASE_DIR, "data", "sistema_venta.csv")

salida_detalle = os.path.join(BASE_DIR, "outputs", "consolidado_limpio.xlsx")
salida_resumen = os.path.join(BASE_DIR, "outputs", "resumen_producto.xlsx")

print("Iniciando proceso")

# Leer archivos fuente
df_prod = pd.read_csv(archivo_produccion)
df_ventas = pd.read_csv(archivo_ventas)

print("Archivos leidos correctamente")

# Renombrar columnas de produccion
df_prod = df_prod.rename(columns={
    "produccion_real": "produccion",
    "ventas_asociadas": "ventas",
    "ciudad_destino": "ciudad",
    "fecha_produccion": "fecha"
})

# Renombrar columnas de ventas
df_ventas = df_ventas.rename(columns={
    "unidades_vendidas": "ventas",
    "stock_recibido": "produccion",
    "importe_total": "ingreso",
    "fecha_venta": "fecha"
})

# Seleccionar columnas necesarias de produccion
columnas_prod = ["producto", "produccion", "ventas", "precio_unitario", "ciudad", "fecha"]
df_prod = df_prod[columnas_prod]

# Seleccionar columnas necesarias de ventas
columnas_ventas = ["producto", "produccion", "ventas", "precio_unitario", "ciudad", "fecha"]
df_ventas = df_ventas[columnas_ventas]

# Unir ambos datasets
df = pd.concat([df_prod, df_ventas], ignore_index=True)

print("Archivos unidos correctamente")

# Eliminar duplicados
df = df.drop_duplicates()

# Convertir columnas numericas
for col in ["produccion", "ventas", "precio_unitario"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Rellenar nulos numericos
df[["produccion", "ventas", "precio_unitario"]] = df[["produccion", "ventas", "precio_unitario"]].fillna(0)

# Quitar precios negativos
df = df[df["precio_unitario"] >= 0]

# Rellenar nulos de texto
df["producto"] = df["producto"].fillna("SIN_DATO")
df["ciudad"] = df["ciudad"].fillna("SIN_DATO")
df["fecha"] = df["fecha"].fillna("SIN_FECHA")

# Crear ingreso calculado
df["ingreso"] = df["ventas"] * df["precio_unitario"]

# Crear diferencia entre produccion y ventas
df["diferencia"] = df["produccion"] - df["ventas"]

# Crear nivel de venta
df["nivel_venta"] = df.apply(
    lambda row: row["ventas"] / row["produccion"] if row["produccion"] != 0 else 0,
    axis=1
)

# Crear estado de stock
def estado_stock(x):
    if x > 50:
        return "SobreStock"
    elif x > 0:
        return "Stock_OK"
    else:
        return "SinStock"

df["estado_stock"] = df["diferencia"].apply(estado_stock)

# Crear clasificacion de venta
def clasificacion_venta(x):
    if x > 0.8:
        return "Alta"
    elif x > 0.5:
        return "Media"
    else:
        return "Baja"

df["clasificacion_venta"] = df["nivel_venta"].apply(clasificacion_venta)

# Crear porcentaje de venta
df["porcentaje_venta"] = (df["nivel_venta"] * 100).round(2)

# Ordenar dataset detalle
df = df.sort_values(by=["producto", "fecha"]).reset_index(drop=True)

print("Limpieza completada")

# Crear resumen por producto
df_resumen = df.groupby("producto").agg(
    produccion=("produccion", "sum"),
    ventas=("ventas", "sum"),
    ingreso=("ingreso", "sum")
).reset_index()

# Crear KPIs del resumen
df_resumen["diferencia"] = df_resumen["produccion"] - df_resumen["ventas"]

df_resumen["nivel_venta"] = df_resumen.apply(
    lambda row: row["ventas"] / row["produccion"] if row["produccion"] != 0 else 0,
    axis=1
)

df_resumen["estado_stock"] = df_resumen["diferencia"].apply(estado_stock)
df_resumen["clasificacion_venta"] = df_resumen["nivel_venta"].apply(clasificacion_venta)
df_resumen["porcentaje_venta"] = (df_resumen["nivel_venta"] * 100).round(2)

# Ordenar resumen
df_resumen = df_resumen.sort_values(by="ventas", ascending=False).reset_index(drop=True)

print("Resumen analitico generado")

# Exportar archivo detalle
df.to_excel(salida_detalle, index=False)

# Exportar archivo resumen
df_resumen.to_excel(salida_resumen, index=False)

print("Proceso finalizado correctamente")
print(f"Archivo detalle generado: {salida_detalle}")
print(f"Archivo resumen generado: {salida_resumen}")