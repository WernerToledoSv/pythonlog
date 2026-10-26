# Analizador de logs en Python

> **Proyecto académico:** lectura, validación y resumen de archivos de registro (`.txt`).

## Descripción

Este programa permite seleccionar un archivo de texto desde una ventana de Windows y analizar sus líneas para generar un resumen de eventos. Identifica las severidades admitidas, revisa las fechas y registra detalles de las líneas que presentan errores o inconsistencias.

**Autor:** [Escribe tu nombre]  
**Curso:** [Escribe el nombre del curso]  
**Fecha:** [Escribe la fecha de entrega]

## Funcionalidades

- Seleccionar un único archivo `.txt` mediante el explorador de archivos de Windows.
- Contar las líneas leídas y los registros no vacíos.
- Clasificar los eventos por severidad: `INFO`, `WARNING` y `ERROR`.
- Detectar fechas válidas, fechas inválidas y registros sin fecha.
- Detectar registros sin severidad válida, sin mensaje o con otros problemas de formato.
- Registrar los errores junto con el número de línea y una descripción del problema.
- Mostrar un resumen organizado en la consola.

## Requisitos

- Python **3.10 o superior**, porque el programa utiliza `match/case`.
- Windows para utilizar el selector gráfico de archivos tal como está configurado.
- `tkinter`, normalmente incluido en la instalación de Python para Windows.

El programa utiliza módulos de la biblioteca estándar de Python; no necesita instalar paquetes externos adicionales.

## Cómo ejecutar el programa

1. Descarga o clona este repositorio.
2. Abre una terminal en la carpeta del proyecto.
3. Ejecuta el script principal:

   ```powershell
   python PythonLogs.py
   ```

4. Cuando aparezca la ventana, selecciona un archivo `.txt`.
5. Revisa el resumen y los detalles de errores que se muestran en la consola.

Si tu archivo principal tiene otro nombre, reemplaza `PythonLogs.py` en el comando por el nombre correspondiente.

## Formato esperado de un registro

El formato general de una línea es:

```text
[SEVERIDAD] AAAA-MM-DD Mensaje del evento
```

Ejemplos:

```text
[INFO] 2025-01-10 User logged in successfully
[WARNING] 2025-01-11 Invalid password attempt
[ERROR] 2025-01-12 Failed to connect to database
```

Las severidades reconocidas son:

- `INFO`
- `WARNING`
- `ERROR`

La fecha debe respetar el formato `AAAA-MM-DD` y corresponder a una fecha real del calendario. La línea también debe contener un mensaje.

## Archivos del proyecto

| Archivo | Descripción |
|---|---|
| `PythonLogs.py` | Script principal que selecciona y analiza el archivo, y muestra el resumen. |
| `logs_exitoso_50.txt` | Archivo de prueba con 50 líneas de registros bien formados. |
| `logs_con_errores_20.txt` | Archivo de prueba de 20 líneas que contiene errores e inconsistencias. |

## Pruebas realizadas

Se utilizan dos archivos para comprobar el comportamiento del analizador.

### 1. Archivo bien formado: `logs_exitoso_50.txt`

**Resultado esperado:** 50 líneas leídas, 50 eventos con contenido, fechas válidas en todos los registros y ningún detalle de error.

**Resultado obtenido con la versión corregida:**

| Métrica | Resultado |
|---|---:|
| Líneas leídas | 50 |
| Eventos con contenido | 50 |
| Eventos `INFO` | 30 |
| Eventos `WARNING` | 10 |
| Eventos `ERROR` | 10 |
| Fechas válidas | 50 |
| Fechas inválidas | 0 |
| Eventos sin fecha | 0 |
| Líneas mal formateadas | 0 |

### 2. Archivo con errores: `logs_con_errores_20.txt`

Incluye una línea vacía, una severidad no admitida, fechas inválidas, registros sin fecha, una severidad sin corchetes y registros sin mensaje o con formato incorrecto.

**Resultado esperado:** el programa debe leer las 20 líneas, contar los registros no vacíos y señalar las líneas que no cumplen el formato.

**Resultado obtenido con la versión corregida:**

| Métrica | Resultado |
|---|---:|
| Líneas leídas | 20 |
| Eventos con contenido | 19 |
| Eventos `INFO` | 6 |
| Eventos `WARNING` | 3 |
| Eventos `ERROR` | 5 |
| Fechas válidas | 14 |
| Fechas inválidas | 2 |
| Eventos sin fecha | 3 |
| Líneas mal formateadas | 11 |
| Detalles de error registrados | 11 |

> **Nota:** estos resultados corresponden a la versión corregida del analizador. Si se cambia la lógica de validación o los archivos de prueba, se deben volver a ejecutar las pruebas y actualizar esta sección.

## Organización del código

- `BuscarArchivo()`: abre el selector de archivos y devuelve la ruta seleccionada.
- `ResumenEventos(archivo)`: recorre el archivo, acumula las estadísticas y devuelve los resultados en un diccionario.
- `AnalizarLinea(linea)`: identifica la severidad, localiza y valida la fecha y comprueba que exista un mensaje.
- `validar_fecha(fecha_texto)`: comprueba que la fecha exista en el calendario.
- `ImprimirResumen(resumen)`: imprime las estadísticas y el detalle de los problemas.
- `main()`: coordina la ejecución del programa.

## Uso de IA durante el desarrollo

La IA se utilizó como apoyo para proponer y explicar partes del código, revisar errores y sugerir formas de validar y presentar los datos. Las propuestas se revisaron y ajustaron durante el desarrollo; el programa y sus resultados deben ser comprendidos y verificados por el estudiante.

### Ejemplo de una sugerencia de IA que se mejoró

La IA sugirió utilizar una ventana de Windows para seleccionar el archivo que se iba a analizar. Sin embargo, la primera propuesta no incluía un filtro para limitar los tipos de archivo, por lo que se podían seleccionar documentos distintos de `.txt`. Esto podía provocar errores al intentar leer o procesar un archivo con un formato no esperado.

Identifiqué este problema y modifiqué la función `BuscarArchivo()` para utilizar el parámetro `filetypes=[("Archivos de texto", "*.txt")]`. Con este cambio, el explorador filtra los archivos para seleccionar documentos de texto con extensión `.txt`. También agregué una validación para comprobar si se seleccionó un archivo o si el usuario canceló la operación.

Esta experiencia me enseñó que las sugerencias de la IA pueden servir como punto de partida, pero es necesario probar el código y verificar si contempla las condiciones del proyecto. La decisión de incorporar el filtro y la validación se tomó después de identificar el problema y comprobar la necesidad de corregirlo.

## Reflexión personal: 
La IA me ayudó a generar un codigo mas limpio el cual tiene la capacidad de ser escalable debido a la forma en la cual esta creado ademas de centralizar la ejecucion en un solo lugar, esto ayuda a que mas adelante se puedan seguir escalando y agregando funcionalidades. 

## Limitaciones conocidas

- El programa procesa archivos de texto plano (`.txt`); no analiza directamente formatos como JSON o CSV.
- La validación depende del formato de registro descrito en este documento.
- Una línea puede tener más de un problema, pero el contador de líneas mal formadas debe registrar esa línea una sola vez.

## Licencia

[Indica la licencia si el proyecto requiere una, o elimina esta sección si no aplica.]
