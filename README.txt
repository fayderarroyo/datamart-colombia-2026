================================================================================
 DATAMART COLOMBIA · PLANEACIÓN ESTRATÉGICA 2026
 Dashboard de Inteligencia Geográfica para Redistribución de Pauta Digital
 Proyecto Integrador — Clase de Visualización de Datos
================================================================================

ESTUDIANTES: Juan Alvarez – Fayder Arroyo – Rafael Sevilla
DOCENTE    : Laura Mancera
ASIGNATURA : Visualización de Datos · Especialización en Analítica de Datos e Información
INSTITUCIÓN: Fundación Universitaria Tecnológico Comfenalco · Cartagena de Indias, mayo de 2026
TECNOLOGÍA : Python · Streamlit · Supabase (PostgreSQL) · Plotly

________________________________________________________________________________
TABLA DE CONTENIDOS
________________________________________________________________________________

  1. Descripción del Proyecto
  2. Hipótesis de Negocio
  3. Fuentes de Datos y Bases de Datos
  4. Modelo de Datos (Arquitectura)
  5. Métricas e Indicadores (DAX → Python)
  6. Estructura del Dashboard
  7. Visualizaciones
  8. Tecnologías y Stack
  9. Estructura de Archivos del Proyecto
 10. Cómo Ejecutar el Proyecto

________________________________________________________________________________
1. DESCRIPCIÓN DEL PROYECTO
________________________________________________________________________________

DataMart Colombia es una empresa de marketing digital y datos que gestiona
presupuestos de publicidad digital para clientes en Colombia. Históricamente,
la inversión publicitaria se ha concentrado en las tres ciudades principales
(Bogotá, Medellín, Cali), dejando sin explorar mercados digitales emergentes
en ciudades intermedias y grandes del país.

Este proyecto construye un dashboard analítico e interactivo que permite
visualizar, cuantificar y justificar con datos la redistribución estratégica
del presupuesto de pauta digital, respondiendo a la pregunta clave de 2026:

  "La pregunta para 2026 no es ¿dónde vive más gente?,
   sino ¿dónde está creciendo más rápido el consumidor digital?"

El dashboard integra tres fuentes de datos (MinTIC, DANE, tabla puente propia)
para calcular indicadores compuestos que identifican las ciudades con mayor
Potencial Digital, permitiendo argumentar la reubicación de hasta el 30% del
presupuesto de pauta hacia mercados digitales subexplotados.

________________________________________________________________________________
2. HIPÓTESIS DE NEGOCIO
________________________________________________________________________________

Las ciudades intermedias de Colombia (100.000–500.000 habitantes) ofrecen
una oportunidad de inversión publicitaria digital subexplotada, con:

  ✔ Mayor eficiencia de costo (menor CPC/CPM por menor competencia)
  ✔ Menor saturación publicitaria digital
  ✔ Audiencia creciente habilitada por la expansión de cobertura 4G LTE
  ✔ Clase media emergente con poder adquisitivo y acceso móvil creciente

Argumentos que la sustentan:
  - Saturación en las 3 grandes ciudades → CPMs más altos, menor diferenciación
  - Datos MinTIC muestran crecimiento sostenido de 4G LTE en ciudades secundarias
  - Ciudades como Rionegro (TD: 4.87%), Yopal (TD: 9.0%) tienen baja desocupación
    y alto dinamismo económico, generando consumidores digitales activos
  - El 30% es un umbral conservador para diversificar el riesgo y testear
    mercados con menor inversión pero alto potencial de retorno

________________________________________________________________________________
3. FUENTES DE DATOS Y BASES DE DATOS
________________________________________________________________________________

Se utilizan TRES fuentes de datos almacenadas en Supabase (PostgreSQL):

────────────────────────────────────────────────────────────────────────────────
TABLA 1: cobertura_movil
────────────────────────────────────────────────────────────────────────────────
Fuente  : MinTIC — Cobertura Móvil por Tecnología, Departamento y Municipio
          por Proveedor (dataset público actualizado al 16/05/2026)
Archivo : Cobertura_móvil_por_tecnología,_departamento_y_municipio_por_
          proveedor_20260516.csv
Filas   : 407.281 registros
Período : 2015 Q4 — 2023
Granularidad: Por operador, municipio y trimestre

Columnas principales:
  ano              — Año del reporte (2015–2023)
  trimestre        — Trimestre del año (1–4)
  proveedor        — Operador de telefonía (Claro, Movistar, Tigo, etc.)
  cod_departamento — Código DIVIPOLA del departamento (clave de unión)
  departamento     — Nombre del departamento (MAYÚSCULAS)
  cod_municipio    — Código DIVIPOLA del municipio
  municipio        — Nombre del municipio
  cabecera_municipal — ¿Tiene cobertura en cabecera? (S/N)
  cobertura_2g     — Cobertura tecnología 2G (S/N)
  cobertura_3g     — Cobertura tecnología 3G (S/N)
  cobertura_hspa_hspa_dc — Cobertura HSPA+/DC (3.5G) (S/N)
  cobertuta_4g     — Cobertura tecnología 4G (S/N) [nota: typo original]
  cobertura_lte    — Cobertura tecnología LTE (S/N)
  cobertura_5g     — Cobertura tecnología 5G (S/N)

NOTA: Esta tabla contiene datos a nivel nacional (todos los municipios de
Colombia). La unión con la tabla ciudades_puente filtra solo las 36 ciudades
de análisis usando el código de departamento (cod_departamento = codigo_dp).

────────────────────────────────────────────────────────────────────────────────
TABLA 2: datos_ciudad
────────────────────────────────────────────────────────────────────────────────
Fuente  : DANE — Gran Encuesta Integrada de Hogares (GEIH)
          Tasas de Ocupación y Desempleo por Ciudad 2025–2026
Archivo : DANE — Tasa de ocupación y desempleo por ciudad 2025-2026 (GEIH).xlsx
Filas   : 36 ciudades (un registro por ciudad, año móvil más reciente)
Período : Año Móvil: Abril 2025 — Marzo 2026

Columnas:
  ciudad                              — Nombre de la ciudad (clave de unión)
  periodo_dato                        — Período GEIH (ej: "Abr 25 - Mar 26")
  hoja_fuente_dane                    — Encuesta DANE de origen
  pct_poblacion_en_edad_de_trabajar   — % PET sobre población total
  tasa_global_de_participacion_tgp    — TGP: % PET que participa en el mercado
  tasa_de_ocupacion_to                — TO: % PET empleado ← KPI ESTRATÉGICO
  tasa_de_desocupacion_td             — TD: % fuerza laboral desocupada ← KPI
  tasa_de_subocupacion_ts             — TS: % subempleados sobre ocupados
  poblacion_total                     — Población total (en miles)
  poblacion_total_mill                — Población total (en unidades)
  poblacion_en_edad_de_trabajar_pet   — PET (en miles)
  fuerza_de_trabajo                   — Fuerza laboral total (en miles)
  poblacion_ocupada                   — Empleados (en miles) ← KPI ESTRATÉGICO
  poblacion_desocupada                — Desempleados (en miles)
  poblacion_fuera_de_la_fuerza_de_trabajo — Inactivos (en miles)
  poblacion_subocupada                — Subocupados (en miles)
  fuerza_de_trabajo_potencial         — Fuerza laboral potencial (en miles)

NOTA: Las últimas 5 ciudades (Buenaventura, Barrancabermeja, Soacha, Tumaco,
Rionegro) provienen de la encuesta especial "Año_móvil_5_ciudades_interm" del
DANE, diferente a la encuesta principal de 32 ciudades.

────────────────────────────────────────────────────────────────────────────────
TABLA 3: ciudades_puente
────────────────────────────────────────────────────────────────────────────────
Fuente  : Tabla propia construida por el equipo DataMart Colombia
          para cruzar los datos MinTIC (por departamento) con los datos
          DANE (por nombre de ciudad)
Archivo : Tabla_Puente_Ciudades.xlsx
Filas   : 36 ciudades

Columnas:
  id_ciudad             — ID único (1–36)
  nombre_geih           — Nombre en la nomenclatura DANE GEIH (clave de unión)
  nombre_poblacion_dane — Nombre oficial DANE
  depto_mintic          — Nombre del departamento según MinTIC (MAYÚSCULAS)
  municipio_mintic      — Nombre del municipio según MinTIC
  codigo_dp             — Código DIVIPOLA del departamento ← CLAVE DE UNIÓN
  poblacion_2024        — Población estimada 2024
  clasificacion         — Categoría de ciudad:
                            · Principal (Bogotá, Medellín, Cali, Barranquilla)
                            · Área Metro (Bucaramanga, Pereira, Manizales…)
                            · Intermedia (ciudades 100k–500k hab)
                            · Grande (>500k, no capitales)
                            · Pequeña (<100k)
  cumple_100k_500k      — "SÍ"/"NO": ¿tiene entre 100k y 500k habitantes?
  es_intermedia_estricta — "SÍ"/"NO": ¿ciudad intermedia del análisis?

────────────────────────────────────────────────────────────────────────────────
VISTA SQL: vw_cobertura_intermedia  (optimización de rendimiento)
────────────────────────────────────────────────────────────────────────────────
Creada en Supabase para evitar descargar los 407.281 registros brutos.
Pre-agrega los datos de cobertura por ciudad y año antes de enviarlos
a Streamlit (~300 filas en lugar de 407.281).

Código SQL:
  CREATE OR REPLACE VIEW vw_cobertura_intermedia AS
  SELECT
      c.ano,
      p.id_ciudad,
      p.nombre_geih as ciudad,
      p.es_intermedia_estricta,
      COUNT(*) as total_filas,
      SUM(CASE WHEN c.cobertuta_4g = 'S' OR c.cobertura_lte = 'S'
          THEN 1 ELSE 0 END) as filas_4g
  FROM cobertura_movil c
  JOIN ciudades_puente p ON c.cod_departamento = p.codigo_dp
  GROUP BY c.ano, p.id_ciudad, p.nombre_geih, p.es_intermedia_estricta;

RAZÓN DEL JOIN: El código de departamento (codigo_dp) es el nivel de
granularidad que comparten MinTIC (datos por municipio agrupados en depto)
y la tabla puente (que identifica ciudades por su código de departamento).

________________________________________________________________________________
4. MODELO DE DATOS (ARQUITECTURA)
________________________________________________________________________________

                    ┌──────────────────────────┐
                    │    ciudades_puente        │
                    │  (tabla dimensional)      │
                    │  36 ciudades · PK:id_ciudad│
                    │  codigo_dp ─────────────┐ │
                    └──────────────────────────┘ │
                            │ 1                  │
                            │                    │
                    ┌───────┴──────────────────┐ │
               ┌───│   vw_cobertura_intermedia │◄┘
               │   │   (vista agregada SQL)    │
               │   │   ano · ciudad · total ·  │
               │   │   filas_4g                │
               │   └───────────────────────────┘
               │              ↑ GROUP BY
               │   ┌──────────────────────────┐
               │   │     cobertura_movil       │
               │   │  (tabla de hechos)        │
               │   │  407.281 filas            │
               │   │  2015–2023 · por proveedor│
               │   └──────────────────────────┘
               │
               │   ┌──────────────────────────┐
               └──▶│     datos_ciudad          │
                   │  (tabla de medidas DANE)  │
                   │  36 ciudades · GEIH 2026  │
                   │  Tasas laborales          │
                   └──────────────────────────┘

Las uniones se realizan en Python (Pandas .merge()):
  cobertura_movil  ──[cod_departamento = codigo_dp]──▶ ciudades_puente
  ciudades_puente  ──[nombre_geih = ciudad]──────────▶ datos_ciudad

________________________________________________________________________________
5. MÉTRICAS E INDICADORES (DAX → PYTHON)
________________________________________________________________________________

Todas las métricas originalmente calculadas en Power BI con DAX fueron
traducidas a Python con Pandas. Se añadieron 3 nuevas métricas propias.

────────────────────────────────────────────────────────────────────────────────
MÉTRICAS ORIGINALES (equivalentes a las medidas DAX del Power BI)
────────────────────────────────────────────────────────────────────────────────

  KPI 1: % Cobertura 4G LTE
  ──────────────────────────
  DAX original:
    % Cobertura 4G LTE =
    DIVIDE(
      CALCULATE(
        COUNTROWS(tabla),
        tabla[COBERTUTA 4G] = "S" || tabla[COBERTURA LTE] = "S"
      ),
      COUNTROWS(tabla),
      0
    )

  Python equivalente:
    pct_4g = filas_4g / total_filas

  Donde filas_4g = SUM(CASE WHEN cobertuta_4g='S' OR cobertura_lte='S'
                         THEN 1 ELSE 0 END)
  y total_filas = COUNT(*) — calculados en la vista SQL.

  Interpretación: Porcentaje de registros de cobertura (por proveedor,
  municipio, trimestre) donde existe cobertura 4G o LTE. Mide la penetración
  de conectividad de alta velocidad en cada ciudad o período.


  KPI 2: Tasa de Desempleo (TD)
  ─────────────────────────────
  Fuente: Directo del dataset DANE GEIH.
  Columna: tasa_de_desocupacion_td
  Interpretación: % de la fuerza laboral activa que no tiene empleo.
  Usado como proxy de la salud económica del consumidor en cada ciudad.


  KPI 3: Índice Potencial Digital (IPD)
  ─────────────────────────────────────
  DAX original:
    Indice Potencial Digital =
    VAR MaxDesempleo = CALCULATE(MAX(Datos_Por_Ciudad[TD]),
                                 ALL(Ciudades_Puente))
    VAR DesempleoInverso = MaxDesempleo - [Tasa Desempleo]
    RETURN [% Cobertura 4G LTE] * DesempleoInverso

  Python equivalente:
    max_des = df_dc['tasa_de_desocupacion_td'].max()   # 24.82 (Quibdó)
    IPD = pct_4g * (max_des - tasa_de_desocupacion_td) * 10

  Lógica: Ciudades con ALTA cobertura 4G Y BAJO desempleo relativo
  obtienen IPD alto. El desempleo actúa de forma inversa: más desempleo
  = menos consumo potencial. Se multiplica × 10 para escala visual.

  Interpretación: Mide el potencial real de conversión publicitaria digital.
  Una ciudad con 90% de cobertura 4G pero 25% de desempleo tiene bajo IPD
  porque la conectividad no se traduce en poder adquisitivo para compras.


  KPI 4: Score Eficiencia Costo
  ─────────────────────────────
  DAX original:
    Score Eficiencia Costo =
    VAR DesempleoCiudad = [Tasa Desempleo]
    RETURN DIVIDE(1, DesempleoCiudad, 0)

  Python equivalente:
    score_eficiencia = (1 / tasa_de_desocupacion_td) * 100

  Interpretación: Ciudades con menor desempleo tienen Score alto, indicando
  que el presupuesto publicitario "rinde más" porque hay más consumidores
  activos con poder adquisitivo. A menor desempleo, mayor eficiencia.

────────────────────────────────────────────────────────────────────────────────
NUEVAS MÉTRICAS PROPIAS (propuestas en este dashboard)
────────────────────────────────────────────────────────────────────────────────

  NUEVA 1: Índice de Dinamismo Digital
  ────────────────────────────────────
  Fórmula Python:
    indice_dinamismo_digital = tasa_de_ocupacion_to * pct_4g

  Interpretación: Combina la Tasa de Ocupación (qué tan empleada está la
  población activa — TO) con la penetración de 4G. Una ciudad puede tener
  cobertura digital pero si sus habitantes no están empleados, el impacto
  comercial es bajo. Esta métrica captura el dinamismo real del consumidor:
  "Conectado + con trabajo = consumidor digital activo".

  Diferencia con IPD: El IPD usa desempleo como penalizador (negativo).
  El Dinamismo Digital usa ocupación directamente (positivo). Son complementarios.


  NUEVA 2: Mercado Digital Potencial (MDP)
  ─────────────────────────────────────────
  Fórmula Python:
    mercado_digital_potencial = poblacion_ocupada * pct_4g   [en miles]

  Interpretación: Estima el tamaño real del mercado de consumidores digitales
  activos en cada ciudad: personas que están empleadas (tienen ingresos) Y
  tienen acceso a internet 4G (pueden comprar online). Es una métrica de
  tamaño de mercado, no de eficiencia.

  Uso: Para comparar el tamaño absoluto del mercado digital accesible entre
  ciudades de diferente tamaño poblacional.


  NUEVA 3: Crecimiento Cobertura 4G (pp)
  ────────────────────────────────────────
  Fórmula Python:
    crecimiento_4g = pct_4g_2023 - pct_4g_2015   [en puntos porcentuales]

  Interpretación: Cuántos puntos porcentuales creció la cobertura 4G entre
  el primer y último año disponible. Identifica las ciudades donde el
  ecosistema digital creció más aceleradamente (mercados emergentes).

  Ejemplo:
    Manizales A.M.: de 3.7% (2015) a 89.9% (2023) = +86.1 pp ← LÍDER
    Armenia:        de 8.1% (2015) a 88.4% (2023) = +80.2 pp
    Pereira A.M.:   de 6.0% (2015) a 83.4% (2023) = +77.3 pp
    Bogotá D.C.:    de 53.8% (2015) a 75.0% (2023) = +21.2 pp ← MÁS BAJA

  Insight: Las ciudades intermedias (Manizales, Armenia, Pereira) tuvieron
  el crecimiento más acelerado, mientras Bogotá ya estaba saturada en 2015.

________________________________________________________________________________
6. ESTRUCTURA DEL DASHBOARD
________________________________________________________________________________

El dashboard tiene 4 secciones principales:

  SECCIÓN 0: SIDEBAR (Filtros interactivos)
  ─────────────────────────────────────────
  • Slider de Rango de Años: filtra el período de análisis (2015–2023)
  • Multiselect Clasificación de Ciudad: Solo Ciudades Intermedias por defecto.
  • Toggle "Solo ciudades intermedias": activa el foco estratégico (sugerido siempre activo)
  • Selector de Métrica del Mapa: cambia la variable que controla el tamaño
    y color de las burbujas en el mapa (IPD / % Cobertura 4G / Tasa Ocupación /
    Mercado Digital Potencial)
  • Recursos Académicos (Evaluación): Botones de descarga para PBIX original
    y PDF de la presentación, además de stack tecnológico detallado.

  SECCIÓN 1: 5 KPIs (fila superior)
  ───────────────────────────────────
  Tarjetas con glassmorphism, gradientes y tooltips (ⓘ) con definiciones:
  1. % Cobertura 4G LTE (global filtrado)
  2. Índice Potencial Digital promedio + ciudad líder
  3. Score Eficiencia Costo promedio
  4. Índice Dinamismo Digital promedio
  5. Crecimiento 4G total período (puntos porcentuales)

  SECCIÓN 2: PESTAÑAS (TABS) - Pantalla Completa (100% Width)
  ───────────────────────────────────────────────────────────
  El dashboard se divide en dos pestañas principales sin scroll vertical excesivo.

  TAB 1: INTELIGENCIA GEOGRÁFICA
  Fila Superior:
  • Columna 1 (50%): Mapa de Colombia con Plotly Scattermapbox (estilo claro carto-positron).
    Burbujas dinámicas (tamaño y color según métrica). Tooltip enriquecido.
  • Columna 2 (50%): Cuadrante Estratégico (Cobertura 4G vs Desempleo), tamaño = población.
  Fila Inferior:
  • Columna 1 (50%): Barras Top 10 Índice Potencial Digital.
  • Columna 2 (50%): Barras Top 10 Score Eficiencia Costo.

  TAB 2: RANKINGS ESTRATÉGICOS (Aceleración Digital)
  • Columna 1 (50%): Barras horizontales — Crecimiento 4G por ciudad (2015→2023).
  • Columna 2 (50%): Barras horizontales — Índice Dinamismo Digital por ciudad.

  CONCLUSIÓN ESTRATÉGICA (caja de insight)
  ─────────────────────────────────────────
  Texto automático que nombra las top 3 ciudades del período seleccionado
  y argumenta la redistribución del 30% del presupuesto.

________________________________________________________________________________
7. VISUALIZACIONES
________________________________________________________________________________

Librería: Plotly (plotly.graph_objects y plotly.express)

  Gráfico 1: Mapa de Burbujas Geográfico (px.scatter_mapbox)
  ────────────────────────────────────────────────────────
  Tipo: Mapa interactivo de burbujas sobre Colombia
  Eje X: Longitud geográfica
  Eje Y: Latitud geográfica
  Color y Tamaño: Métrica seleccionada por el usuario (IPD / Cobertura / etc.)
  Estilo: carto-positron (fondo claro neutral), zoom y centro calculados para Colombia
  Interactividad: Hover con datos completos y formato limpio

  Gráfico 2: Líneas Temporales por Clasificación (go.Scatter)
  ────────────────────────────────────────────────────────────
  Tipo: Líneas con marcadores (spline suavizado)
  Eje X: Año (2015–2023)
  Eje Y: % Cobertura 4G LTE
  Color: Clasificación de ciudad (5 líneas simultáneas)
  Insight: Muestra convergencia — las intermedias crecieron más rápido

  Gráfico 3: Mercado Digital Potencial por Clasificación (go.Bar)
  ────────────────────────────────────────────────────────────────
  Tipo: Barras horizontales simples
  Eje Y: Clasificación de ciudad
  Eje X: Suma del Mercado Digital Potencial (miles de consumidores)
  Color: Verde para Intermedias, azul para el resto

  Gráfico 4: Top 10 IPD vs Score Eficiencia — Barras Duales (px.bar)
  ────────────────────────────────────────────────────────────────────
  Tipo: Barras horizontales agrupadas (grouped bar chart)
  Eje Y: Ciudad (ordenado por IPD descendente)
  Eje X: Valor de la métrica
  Colores: Azul (#3b82f6) = IPD, Púrpura (#8b5cf6) = Score Eficiencia
  Equivalente al "Top 5 para Redistribución de Pauta" del Power BI original,
  ampliado a Top 10 con ambas métricas visibles simultáneamente

  Gráfico 5: Dispersión — Cobertura 4G vs Desempleo (go.Scatter)
  ────────────────────────────────────────────────────────────────
  Tipo: Gráfico de burbujas (scatter con size variable)
  Eje X: Tasa de Desempleo (%)
  Eje Y: % Cobertura 4G LTE
  Tamaño de burbuja: Población 2024
  Color: Clasificación de ciudad
  Líneas de referencia: Medianas de X e Y (cuadrantes)
  Anotación: "★ ZONA IDEAL" (alto 4G + bajo desempleo)
  Equivalente al scatter del Power BI original, enriquecido con cuadrantes

  Gráfico 6: Crecimiento 4G 2015→2023 (go.Bar)
  ─────────────────────────────────────────────
  Tipo: Barras horizontales con gradiente de color (Viridis colorscale)
  Eje Y: Ciudad
  Eje X: Puntos porcentuales de crecimiento
  Color: Proporcional al crecimiento (más verde = mayor crecimiento)
  Novedad: Muestra cuáles ciudades se digitalizaron más rápido

  Gráfico 7: Índice Dinamismo Digital (go.Bar)
  ────────────────────────────────────────────
  Tipo: Barras horizontales coloreadas por clasificación
  Eje Y: Ciudad (Top 12)
  Eje X: Índice Dinamismo Digital (TO × pct_4g)
  Novedad: Identifica dónde el consumidor digital es más activo

________________________________________________________________________________
8. TECNOLOGÍAS Y STACK
________________________________________________________________________________

  FRONTEND / VISUALIZACIÓN
  ─────────────────────────
  Streamlit 1.58.0    — Framework principal de la app web
  Plotly 6.7.0        — Gráficos interactivos (Go + Express)
  CSS Personalizado   — Glassmorphism, gradientes, tipografía Inter
  Google Fonts Inter  — Tipografía profesional

  BACKEND / DATOS
  ────────────────
  Python 3.13         — Lenguaje de programación
  Pandas 3.0.3        — Procesamiento y transformación de datos
  NumPy 2.4.6         — Cálculos numéricos
  python-dotenv 1.2.2 — Manejo seguro de credenciales

  BASE DE DATOS
  ─────────────
  Supabase            — PostgreSQL en la nube (plan gratuito 500MB)
  supabase-py 2.30.0  — SDK oficial Python de Supabase
  postgrest 2.30.0    — Cliente REST para las consultas

  LECTURA DE ARCHIVOS
  ───────────────────
  openpyxl 3.1.5      — Lectura de archivos Excel (.xlsx)

  MAPAS
  ──────
  Plotly Scattergeo   — Mapas interactivos nativos (sin dependencias extra)
  Coordenadas lat/lon hardcodeadas para las 36 ciudades de análisis

  ENTORNO
  ────────
  Entorno virtual Python (venv/) — aislado del sistema
  .env                — Variables de entorno (URL y API Key de Supabase)

________________________________________________________________________________
9. ESTRUCTURA DE ARCHIVOS DEL PROYECTO
________________________________________________________________________________

  Visualizacion/
  │
  ├── app.py                            ← Aplicación principal Streamlit
  ├── requirements.txt                  ← Dependencias Python
  ├── .env                              ← Credenciales Supabase (NO compartir)
  │
  ├── upload_to_supabase.py             ← Script de carga inicial a Supabase
  │
  ├── [DATOS ORIGINALES]
  │   ├── Cobertura_móvil_por_tecnología,...csv   ← MinTIC (42 MB)
  │   ├── DANE — Tasa de ocupación y desempleo... ← DANE GEIH (.xlsx)
  │   └── Tabla_Puente_Ciudades.xlsx              ← Tabla dimensional propia
  │
  ├── [DATOS PROCESADOS — generados automáticamente]
  │   ├── cobertura_movil_clean.csv     ← CSV limpio listo para Supabase
  │   ├── datos_ciudad_clean.csv        ← CSV limpio listo para Supabase
  │   └── ciudades_puente_clean.csv     ← CSV limpio listo para Supabase
  │
  ├── [DOCUMENTACIÓN]
  │   ├── Fase 1 — Planeación Estratégica · DataMart Colombia.docx
  │   ├── Proyecto_Integrador_Visualizacion.docx
  │   ├── Ciudades-intermedias-la-nueva-frontera-del-marketing-digital...pdf
  │   └── README.txt                    ← Este archivo
  │
  ├── [POWER BI — versión original]
  │   ├── visualizacion 1/              ← Carpeta del proyecto Power BI
  │   └── visualizacion 1.7z            ← Backup comprimido
  │
  └── venv/                             ← Entorno virtual Python (local)

  SUPABASE (en la nube — proyecto: bqouxvxmfvlnaenmbnmn)
  ├── TABLA: cobertura_movil            (407.281 filas)
  ├── TABLA: datos_ciudad               (36 filas)
  ├── TABLA: ciudades_puente            (36 filas)
  └── VISTA: vw_cobertura_intermedia    (~300 filas — pre-agregada)

________________________________________________________________________________
10. CÓMO EJECUTAR EL PROYECTO
________________________________________________________________________________

  REQUISITOS PREVIOS
  ───────────────────
  • Python 3.13 instalado
  • Cuenta en Supabase con las 3 tablas y la vista creadas
  • Archivo .env con:
      SUPABASE_URL="https://bqouxvxmfvlnaenmbnmn.supabase.co"
      SUPABASE_KEY="<tu_api_key_publica_anon>"

  PASOS PARA EJECUTAR
  ────────────────────

  Paso 1: Abrir una terminal (PowerShell) en la carpeta del proyecto
    cd "c:\Users\Fayder Arroyo Herazo\Desktop\Estadistica Especializacion\Visualizacion"

  Paso 2: Activar el entorno virtual
    .\venv\Scripts\Activate.ps1

  Paso 3: Lanzar la aplicación
    streamlit run app.py

  Paso 4: Abrir en el navegador
    http://localhost:8501

  PRIMERA CONFIGURACIÓN (si es una instalación nueva)
  ──────────────────────────────────────────────────────
  1. Crear entorno virtual:
     python -m venv venv

  2. Instalar dependencias:
     .\venv\Scripts\pip install -r requirements.txt

  3. Crear las tablas en Supabase (SQL Editor):
     — Ejecutar el código SQL del archivo schema.sql

  4. Crear la vista en Supabase (SQL Editor):
     CREATE OR REPLACE VIEW vw_cobertura_intermedia AS
     SELECT c.ano, p.id_ciudad, p.nombre_geih as ciudad,
            p.es_intermedia_estricta,
            COUNT(*) as total_filas,
            SUM(CASE WHEN c.cobertuta_4g='S' OR c.cobertura_lte='S'
                THEN 1 ELSE 0 END) as filas_4g
     FROM cobertura_movil c
     JOIN ciudades_puente p ON c.cod_departamento = p.codigo_dp
     GROUP BY c.ano, p.id_ciudad, p.nombre_geih, p.es_intermedia_estricta;

  5. Deshabilitar RLS para lectura pública:
     ALTER TABLE cobertura_movil DISABLE ROW LEVEL SECURITY;
     ALTER TABLE datos_ciudad DISABLE ROW LEVEL SECURITY;
     ALTER TABLE ciudades_puente DISABLE ROW LEVEL SECURITY;

  6. Subir los datos (desde Python):
     .\venv\Scripts\python upload_to_supabase.py

________________________________________________________________________________
 NOTAS FINALES
________________________________________________________________________________

• La aplicación usa @st.cache_data(ttl=300) para cachear los datos 5 minutos,
  evitando consultas repetidas a Supabase en cada interacción del usuario.

• El mapa usa coordenadas lat/lon hardcodeadas para las 36 ciudades.
  No requiere ninguna API de mapas adicional (Google Maps, Mapbox, etc.),
  funciona 100% con Plotly nativo.

• El dashboard incluye estilos unificados: el mapa implementa 'carto-positron' 
  (tema claro) para maximizar la legibilidad en navegadores, mientras que los 
  gráficos y contenedores usan Glassmorphism con fondos semitransparentes.

• Proyecto alojado y versionado en GitHub:
  → Repositorio oficial: https://github.com/fayderarroyo/datamart-colombia-2026
  → Despliegue en Streamlit Community Cloud leyendo directamente desde la rama 'main'.
  → Las credenciales de Supabase (archivo .env) están excluidas del control de
    versiones (.gitignore) y deben configurarse como "Secrets" en Streamlit.

================================================================================
  "No es donde vive más gente, sino donde crece más rápido el consumidor
   digital." — Datamart Colombia · Planeación Estratégica 2026
================================================================================
