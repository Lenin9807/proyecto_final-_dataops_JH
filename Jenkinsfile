pipeline {
    agent any

    environment {
        PYTHON_PATH = 'C:\\Users\\USER\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
        DESTINATARIO = 'lenincastillacta@gmail.com'
    }

    stages {
        stage('Preparar entorno') {
            steps {
                bat '"%PYTHON_PATH%" -m pip install pandas openpyxl >nul 2>&1'
                echo 'Entorno preparado correctamente'
            }
        }

        stage('Validar fuentes') {
            steps {
                bat 'if exist "%WORKSPACE%\\data\\plan_produccion.csv" (echo Archivo plan_produccion.csv encontrado) else (echo Falta plan_produccion.csv & exit /b 1)'
                bat 'if exist "%WORKSPACE%\\data\\sistema_venta.csv" (echo Archivo sistema_venta.csv encontrado) else (echo Falta sistema_venta.csv & exit /b 1)'
                bat 'if exist "%WORKSPACE%\\scripts\\tratamiento.py" (echo Archivo tratamiento.py encontrado) else (echo Falta tratamiento.py & exit /b 1)'
            }
        }

        stage('Procesar datos') {
            steps {
                bat 'cd /d "%WORKSPACE%" && "%PYTHON_PATH%" "scripts\\tratamiento.py"'
                echo 'Proceso de datos completado'
            }
        }

        stage('Validar resultados') {
            steps {
                bat 'if exist "%WORKSPACE%\\outputs\\consolidado_limpio.xlsx" (echo Archivo consolidado_limpio.xlsx generado) else (echo No se genero consolidado_limpio.xlsx & exit /b 1)'
                bat 'if exist "%WORKSPACE%\\outputs\\resumen_producto.xlsx" (echo Archivo resumen_producto.xlsx generado) else (echo No se genero resumen_producto.xlsx & exit /b 1)'
            }
        }

        stage('Enviar correo') {
            steps {
                emailext(
                    to: "${DESTINATARIO}",
                    subject: "Resultado del pipeline DataOps - Ejecucion ${env.BUILD_NUMBER}",
                    body: """
Hola,

El pipeline DataOps de integración de Producción y Ventas finalizó correctamente.

Detalle:
- Proyecto: Integración de Producción y Ventas
- Ejecución: ${env.BUILD_NUMBER}
- Estado: SUCCESS

Se adjuntan los archivos generados:
- consolidado_limpio.xlsx
- resumen_producto.xlsx

Saludos,
Jenkins
""",
                    attachmentsPattern: 'outputs/consolidado_limpio.xlsx,outputs/resumen_producto.xlsx'
                )
                echo 'Correo enviado correctamente'
            }
        }
    }

    post {
        failure {
            emailext(
                to: "${DESTINATARIO}",
                subject: "Error en pipeline DataOps - Ejecucion ${env.BUILD_NUMBER}",
                body: """
Hola,

El pipeline DataOps de integración de Producción y Ventas presentó un error.

Detalle:
- Proyecto: Integración de Producción y Ventas
- Ejecución: ${env.BUILD_NUMBER}
- Estado: FAILURE

Revisa la consola de Jenkins para identificar el problema.

Saludos,
Jenkins
"""
            )
            echo 'Correo de error enviado'
        }
    }
}