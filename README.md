# Proyecto Final DataOps - John Holden

## Descripción
Este proyecto implementa un pipeline DataOps para integrar, limpiar y analizar datos de producción y ventas utilizando Python, Jenkins, Git y GitHub.

## Problemática
La empresa trabajaba con archivos Excel manuales y separados, sin integración entre producción y ventas, lo que generaba errores, demoras y malas decisiones.

## Solución
Se implementó un flujo automatizado que:
- integra datos de producción y ventas
- limpia la información
- genera KPIs
- exporta resultados
- envía reportes por correo

## Estructura del proyecto
proyecto_final_dataops/
│
├── data/
├── scripts/
├── outputs/
├── Jenkinsfile
├── README.md

## Tecnologías
- Python
- Pandas
- Jenkins
- Git
- GitHub
- Power BI

## KPIs
- Producción total
- Ventas totales
- Ingreso
- Diferencia producción vs ventas
- Nivel de venta
- Estado de stock
- Clasificación de venta

## Ejecución
Ejecutar:

## Automatización
El proyecto se ejecuta automáticamente mediante Jenkins leyendo el Jenkinsfile desde GitHub.

## Autor
Lenin Castilla Llacta
