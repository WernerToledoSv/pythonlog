import re
from datetime import datetime
from collections import Counter
from tkinter import Tk, filedialog

#severidades que podrian existir cualquiera que no este aqui no sera tomada en cuenta
SEVERIDADES = ("INFO", "WARNING", "ERROR")

#estos fueron sugeridos por la iA
#en caso no se cumplan estos patrones mostrara un mensaje de malformateo
#patron para validar la fecha
PATRON_FECHA = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")

#patron para validar la severidad
PATRON_SEVERIDAD = re.compile(
    r"^\s*\[([A-Za-z]+)\]\s*"
)

#funcion para buscar y abrir el archivo log de txt
#se creo por separado para segmentar las responsabilidades 
def BuscarArchivo():
    ventana = Tk()
    ventana.withdraw()

    archivo = filedialog.askopenfilename(   
        title = "Seleccionar archivo log en formato txt",
        filetypes = [("Archivos de texto", "*.txt")] 
    )
    ventana.destroy()
    return archivo

#Logica para contabilizar los eventos log
#los contadores fueron desididos en base a lo requerido
def ResumenEventos(archivo):
    totalLineasValidas = 0
    totalEventos = 0
    totalEventosInfo = 0
    totalEventosWar = 0
    totalEventosErr = 0
    totalFechaValida = 0
    totalFechaInvalida = 0
    totalSinFecha = 0
    totaLineaMalFormateada = 0
    detalles = []
    

    with open(archivo, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    for numeroLinea, linea in enumerate(lineas, start=1):
        totalLineasValidas += 1  
        linea = linea.strip()

        if not linea:
            totaLineaMalFormateada += 1

            detalles.append({
                "numero": numeroLinea,
                "linea": "(Línea vacía)",
                "problemas": ["La línea está vacía"]
            })

            continue
        totalEventos += 1

        lineaAnalizada = AnalizarLinea(linea)

        #contar severidad
        match lineaAnalizada["severidad"]:
            case "INFO":
                totalEventosInfo += 1

            case "WARNING":
                totalEventosWar += 1

            case "ERROR":
                totalEventosErr += 1

            case _:
                totaLineaMalFormateada += 1

        if lineaAnalizada["fecha_valida"]:
            totalFechaValida += 1
        elif not lineaAnalizada["fecha"]:
            totalSinFecha += 1  
        else:
            totalFechaInvalida += 1

        if lineaAnalizada["problemas"]:
            totaLineaMalFormateada += 1

            detalles.append({
                "numero": numeroLinea,
                "linea": linea,
                "problemas": lineaAnalizada["problemas"]
            })
        
    return {
        "totalLineasValidas": totalLineasValidas,
        "totalEventos": totalEventos,
        "totalEventosInfo": totalEventosInfo,
        "totalEventosWar": totalEventosWar,
        "totalEventosErr": totalEventosErr,
        "fechaValida": totalFechaValida,
        "fechaInvalida": totalFechaInvalida,
        "sinFecha": totalSinFecha,
        "lineaMalFormateada": totaLineaMalFormateada,
        "detalles": detalles
    }

#logica para analizar los parametros de cada linea en este caso fecha, severidad y mensaje
def AnalizarLinea(linea):
    resultado = {
        "severidad": None,
        "fecha": None,
        "fecha_valida": False,
        "mensaje": "",
        "problemas": []
    }

    # 1. Identificar la severidad
    patronServeridad = PATRON_SEVERIDAD.match(linea)

    if patronServeridad:
        severidad = patronServeridad.group(1).upper()

        if severidad in SEVERIDADES:
            resultado["severidad"] = severidad
        else:
            resultado["problemas"].append(
                f"Severidad desconocida: {severidad}"
            )

        contenido = linea[patronServeridad.end():]
    else:
        resultado["problemas"].append(
            "Falta la severidad o está mal formateada"
        )
        contenido = linea

    # 2. Buscar y validar la fecha
    patronFecha = PATRON_FECHA.search(contenido)

    if patronFecha:
        fecha = patronFecha.group()
        resultado["fecha"] = fecha

        if validar_fecha(fecha):
            resultado["fecha_valida"] = True
        else:
            resultado["problemas"].append(
                f"Fecha inválida: {fecha}"
            )

        # Quitar la fecha para obtener el mensaje
        contenido = (
            contenido[:patronFecha.start()]
            + contenido[patronFecha.end():]
        ).strip()
    else:
        resultado["problemas"].append("Falta la fecha")

    # 3. Validar que exista un mensaje
    resultado["mensaje"] = contenido.strip()

    if not resultado["mensaje"]:
        resultado["problemas"].append("Falta el mensaje")

    return resultado

#esta funcion fue sugeria por la IA
#logica para validar que sea una fecha existente
def validar_fecha(fecha_texto):
    """Comprueba el formato y la validez real de la fecha."""
    try:
        datetime.strptime(fecha_texto, "%Y-%m-%d")
        return True
    except ValueError:
        return False
    

#logica para mostar los datos recolectados
def ImprimirResumen(resumen):
    print("\n===== RESUMEN DE EVENTOS =====")
    print(f"{'Total de líneas leídas:':<28} {resumen['totalLineasValidas']}")
    print(f"{'Total de eventos:':<28} {resumen['totalEventos']}")
    print(f"{'Eventos INFO:':<28} {resumen['totalEventosInfo']}")
    print(f"{'Eventos WARNING:':<28} {resumen['totalEventosWar']}")
    print(f"{'Eventos ERROR:':<28} {resumen['totalEventosErr']}")

    print("\n===== RESUMEN DE FECHAS =====")
    print(f"Fechas válidas:         {resumen['fechaValida']}")
    print(f"Fechas inválidas:       {resumen['fechaInvalida']}")
    print(f"Eventos sin fecha:      {resumen['sinFecha']}")

    print("\n===== VALIDACIÓN =====")
    print(f"Líneas mal formateadas: {resumen['lineaMalFormateada']}")

    print("\n========== DETALLES DE ERRORES ==========")

    if resumen["detalles"]:
        for i, detalle in enumerate(resumen["detalles"], start=1):
            print(f"\n----------- ERROR #{i} -----------")
            print(f"Número de línea: {detalle['numero']}")
            print(f"Contenido:       {detalle['linea']}")

            print("Problemas detectados:")

            for problema in detalle["problemas"]:
                print(f"  - {problema}")

            print("----------------------------------")
    else:
        print("No se encontraron errores.")

    print("=========================================")


#metodo main para centralizar el codigo y tener un orden 
def main():
    print("==Sistema de procesamiento de logs==")

    #llamado de funcion y validacion que no venga null
    archivo = BuscarArchivo()
    if not archivo:
        print("No se ha seleccionado el archivo")

    try:
        ImprimirResumen(ResumenEventos(archivo))
    except OSError as error:
        print(f"Error al leer el archivo: {error}")

    print("==si se pudó, si se pudó!!!!==")

if __name__ == "__main__":
    main()