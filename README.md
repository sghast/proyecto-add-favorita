# Proyecto Final - Análisis de Datos

## 1. Descripción del proyecto

Este proyecto implementa un pipeline ETL para el análisis del dataset *Corporación Favorita Store Sales*, utilizando Apache Airflow como orquestador, Polars para el procesamiento de datos, PostgreSQL como base de datos intermedia y Power BI para la visualización.

El pipeline permite cargar los archivos CSV del dataset, ejecutar un análisis exploratorio inicial, limpiar los datos, consolidar las diferentes fuentes de información, realizar un análisis exploratorio profundo, almacenar los resultados en PostgreSQL y visualizarlos mediante un dashboard en Power BI.

---

# 2. Descripción de los archivos del dataset y su rol en el pipeline

| Archivo | Descripción | Rol |
|---------|-------------|-----|
| train.csv | Ventas diarias por tienda y familia de productos | Fuente principal del análisis |
| stores.csv | Información de las tiendas | Complementa ubicación y clasificación |
| transactions.csv | Número de transacciones diarias | Permite analizar comportamiento comercial |
| oil.csv | Precio diario del petróleo | Análisis económico |
| holidays_events.csv | Información de feriados nacionales, regionales y locales | Análisis de estacionalidad |

---

# 3. Diagrama de arquitectura de la solución

![Diagrama](images/diagrama_arq.jpeg)

Infraestructura utilizada:

- Ubuntu VM
- Apache Airflow
- Python 3
- Polars
- PostgreSQL
- Power BI Desktop
- GitHub

---

# 4. Descripción del DAG

Nombre del DAG:


favorita_pipeline


## Tareas

1. Inicio
2. Carga de datos
3. EDA inicial
4. Limpieza
5. Consolidación
6. EDA profundo
7. Exportación a PostgreSQL
8. Fin

## Dependencias

![Flujo del DAG](images/flujo_dag.jpeg)

## Configuración

- schedule = None
- retries = 1
- retry_delay = 5 minutos
- catchup = False

---

# 5. Proceso del pipeline

## Carga

Se leen los cinco archivos CSV mediante Polars.



---

## EDA Inicial

Se genera automáticamente un reporte JSON con:

- número de filas
- columnas
- tipos de datos
- nulos
- duplicados
- rango de fechas



---

## Limpieza

Se realizan las siguientes tareas:

- eliminación de duplicados
- conversión de fechas
- interpolación del precio del petróleo
- estandarización de tipos de datos



---

## Consolidación

Se unen las cinco fuentes mediante joins utilizando:

- date
- store_nbr

Se genera un DataFrame consolidado.



---

## EDA Profundo

Se generan los siguientes reportes:

- sales_by_family
- stores_ranking
- sales_by_city
- sales_by_state
- monthly_sales
- yearly_sales
- holiday_sales
- holiday_sales_before_after
- promotion_by_family
- oil_sales
- oil_lag
- oil_city_sensitivity
- sales_transactions_ticket

Todos los reportes son exportados en formato CSV.


---

## Exportación

Se exportan:

- favorita_consolidated
- reportes del EDA profundo

a PostgreSQL.


---

# 6. Métricas del pipeline

## Registros procesados

| Etapa | Registros |
|--------|-----------|
| train | 3 000 000+ |
| consolidado | 3 054 348 |

## Registros eliminados

Completar después de ejecutar el pipeline.

## Tiempo por tarea

Completar con los tiempos obtenidos desde Airflow.

---

# 7. Dashboard de Power BI

El dashboard contiene:

- Ventas por familia
- Evolución mensual
- Ranking de tiendas
- Ventas por ciudad
- Impacto de promociones
- Impacto de feriados
- Precio del petróleo vs ventas
- Ticket promedio

*Capturas*

- Ventas por familia


![Flujo del DAG](images/total_sales_por_family.png)


- Evolución mensual


![Flujo del DAG](images/evolucion_mensual.png)


- Ranking de tiendas


![Flujo del DAG](images/ranking_tiendas.png)


- Ventas por ciudad


![Flujo del DAG](images/ventas_por_ciudad.png)


- Impacto de promociones


![Flujo del DAG](images/impacto_promociones.png)


- Impacto de feriados


![Flujo del DAG](images/impacto_de_feriados.png)


- Precio del petróleo vs ventas


![Flujo del DAG](images/precio_petroleo_ventas.png)


- Ticket promedio


![Flujo del DAG](images/ticket_promedio.png)



# 8. Despliegue

## Requisitos

- Ubuntu (VM)
- Python 3
- PostgreSQL
- Apache Airflow
- Power BI Desktop (Windows)

## Instalación

### 1. Clonar el repositorio

bash
git clone https://github.com/sghast/proyecto-add-favorita


Ingresar al directorio del proyecto:

bash
cd proyecto-add-favorita


### 2. Instalar las dependencias

Instalar todas las librerías necesarias mediante el archivo requirements.txt:

bash
pip install -r requirements.txt


### 3. Crear la base de datos

Crear la base de datos en PostgreSQL:

sql
CREATE DATABASE favorita_db;


### 4. Configurar la conexión

Editar el archivo:


scripts/database/export_postgres.py


con los parámetros de conexión correspondientes:

- Host
- Puerto
- Usuario
- Contraseña
- Nombre de la base de datos

### 5. Copiar el dataset

Crear la carpeta:


data/


Copiar dentro de ella los siguientes archivos:

- train.csv
- stores.csv
- transactions.csv
- oil.csv
- holidays_events.csv

### 6. Ejecutar Apache Airflow

Iniciar Apache Airflow y ejecutar el DAG:


favorita_pipeline


El pipeline realizará automáticamente:

- Carga de datos.
- EDA inicial.
- Limpieza.
- Consolidación.
- EDA profundo.
- Exportación a PostgreSQL.

### 7. Visualización en Power BI

Abrir Power BI Desktop.

Conectarse a PostgreSQL utilizando:

- Servidor: *IP de la máquina virtual*.
- Base de datos: favorita_db.

Importar las tablas generadas por el pipeline y construir el dashboard con las visualizaciones requeridas.

# 9. Conclusiones y recomendaciones

## Conclusiones

- Se implementó un pipeline ETL funcional utilizando Airflow como orquestador.
- Polars permitió procesar eficientemente más de tres millones de registros.
- PostgreSQL centralizó la información consolidada para su consumo por Power BI.
- El análisis exploratorio permitió identificar patrones relacionados con promociones, feriados, transacciones y precio del petróleo.

## Recomendaciones

- Automatizar la ejecución mediante GitHub Actions.
- Incorporar validaciones de calidad adicionales durante la limpieza.
- Agregar monitoreo del pipeline mediante alertas en Airflow.
- Optimizar la exportación a PostgreSQL utilizando cargas incrementales.
