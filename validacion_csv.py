import csv

YEAR_MIN = 1900
YEAR_MAX = 2100
FIELD_COUNT = 19
FILE = r".\archivos\test.csv"


def leer_archivo(archivo: str):
    """Abre el archivo CSV en la ruta `archivo`, lee y lo convierte
    a una lista de listas de strings donde cada fila es un registro
    y cada columna un campo
    """

    # Comprueba que sea un archivo csv
    if not archivo.endswith(".csv"):
        raise RuntimeError("El archivo no es un CSV.")

    try:
        # Abre el archivo y retorna la lista
        with open(archivo, mode="r", newline="") as ar:
            archivoCSV = csv.reader(ar, delimiter=",", quotechar='"')
            return [registro for registro in archivoCSV][1:]
    except:
        raise FileNotFoundError("No existe el archivo: " + archivo)


def validar_numero_campos(registros: list[list[str]], limite: int):
    """Comprueba si el numero de campos de cada registro en `registros`
    no supera el `limite`.
    """
    for i, registro in enumerate(registros):
        if len(registro) > limite:
            # Si el registro actual supera el numero de campos
            # especificado, levanta un error indicando en qué
            # registro sucede y los campos excedentes
            raise RuntimeError(
                "el registro "
                + str(i + 2)
                + " tiene uno o más campos extras -> "
                + ";".join(registro[limite:])
            )


def validar_fecha(registros: list[list[str]], campo: int):
    """Comprueba si el número en el `campo` en cada registro en
    `registros` cumple el formato de fecha 'AAAAMMDD'.
    """
    for i, registro in enumerate(registros):
        valor = registro[campo - 1]

        # Valida la longitud del campo
        if len(valor) != 8:
            raise RuntimeError(
                "en el registro "
                + str(i + 2)
                + ", la fecha del campo "
                + str(campo)
                + " no cumple con el formato 'AAAAMMDD' -> '"
                + valor
                + "'"
            )

        # Valida el valor del año
        try:
            year = int(valor[0:4])
        except:
            raise RuntimeError(
                "en el registro "
                + str(i + 2)
                + ", el año de la fecha del campo "
                + str(campo)
                + " no es un número entero -> '"
                + valor
                + "'"
            )

        # Valida el rango del año
        if year < YEAR_MIN or year > YEAR_MAX:
            raise RuntimeError(
                "en el registro "
                + str(i + 2)
                + ", el año de la fecha del campo "
                + str(campo)
                + " no está en el rango permitido ["
                + YEAR_MIN
                + ", "
                + YEAR_MAX
                + "] -> "
                + valor
            )

        # Valida el valor del mes
        try:
            mes = int(valor[4:6])
        except:
            raise RuntimeError(
                "en el registro "
                + str(i + 2)
                + ", el mes de la fecha del campo "
                + str(campo)
                + " no es un número entero -> '"
                + valor
                + "'"
            )

        # Valida el rango del mes
        if mes < 1 or mes > 12:
            raise RuntimeError(
                "en el registro "
                + str(i + 2)
                + ", el mes de la fecha del campo "
                + str(campo)
                + " no está en el rango permitido -> "
                + valor
            )

        # Valida el valor del día
        try:
            dia = int(valor[6:8])
        except:
            raise RuntimeError(
                "en el registro "
                + str(i + 2)
                + ", el día de la fecha del campo "
                + str(campo)
                + " no es un número entero -> '"
                + valor
                + "'"
            )

        diasMes = [
            31,
            28 if not biciesto(year) else 29,
            31,
            30,
            31,
            30,
            31,
            31,
            30,
            31,
            30,
            31,
        ]
        # Valida el rango del día
        if dia < 1 or dia > diasMes[mes - 1]:
            raise RuntimeError(
                "en el registro "
                + str(i + 2)
                + ", el día de la fecha del campo "
                + str(campo)
                + " no está en el rango permitido -> "
                + valor
            )


def validar_mes(registros: list[list[str]], campo: int):
    """Comprueba si el valor en el `campo` en cada registro en
    `registros` es un mes válido.
    """
    for i, registro in enumerate(registros):
        valor = registro[campo - 1]

        # Valida el valor del mes
        try:
            mes = int(valor)
        except:
            raise RuntimeError(
                "en el registro "
                + str(i + 2)
                + ", el valor del campo "
                + str(campo)
                + " no es un número entero -> '"
                + valor
                + "'"
            )

        # Valida el rango del mes
        if mes < 1 or mes > 12:
            raise RuntimeError(
                "en el registro "
                + str(i + 2)
                + ", el valor del campo "
                + str(campo)
                + " no es un mes válido -> "
                + valor
            )


def validar_entero(registros: list[list[str]], campo: int):
    """Comprueba si el valor en el `campo` en cada registro en
    `registros` es un número entero.
    """
    for i, registro in enumerate(registros):
        valor = registro[campo - 1]

        # Intenta convertir el valor del campo del registro
        # actual en entero
        try:
            entero = int(valor)
        except:
            # En caso de no poder convertir, levanta un error
            # indicando en qué registro sucede y el contenido
            # del campo que levantó el error
            raise RuntimeError(
                "en el registro "
                + str(i + 2)
                + ", el valor del campo "
                + str(campo)
                + " no es un número entero -> '"
                + valor
                + "'"
            )

        # Comprueba que sea positivo
        if entero < 0:
            raise RuntimeError(
                "en el registro "
                + str(i + 2)
                + ", el valor del campo "
                + str(campo)
                + " no es un número entero positivo -> "
                + valor
            )


def validar_flotante(registros: list[list[str]], campo: int):
    """Comprueba si el valor en el `campo` en cada registro en
    `registros` es un número decimal.
    """
    for i, registro in enumerate(registros):
        valor = registro[campo - 1].replace(",", "")

        # Intenta convertir el valor del campo del registro
        # actual en flotante
        try:
            float(valor)
        except:
            # En caso de no poder convertir, levanta un error
            # indicando en qué registro sucede y el contenido
            # del campo que levantó el error
            raise RuntimeError(
                "en el registro "
                + str(i + 2)
                + ", el valor del campo "
                + str(campo)
                + " no es un número flotante -> '"
                + valor
                + "'"
            )


def validar_si_no(registros: list[list[str]], campo: int):
    """Comprueba si el valor en el `campo` en cada registro en
    `registros` es un 'SI' o 'NO' sin distinguir mayúsculas y
    minúsculas.
    """
    permitidos = ["SI", "NO"]

    for i, registro in enumerate(registros):
        valor = registro[campo - 1].upper()

        if not valor in permitidos:
            # En caso de que el valor del campo del registro
            # actual no sea ni 'SI' ni 'NO', levanta un error
            # indicando el registro actual y el contenido del
            # campo que levantó el error
            raise RuntimeError(
                "en el registro "
                + str(i + 2)
                + ", el valor del campo "
                + str(campo)
                + " no pertenece al conjunto {'SI', 'NO'} -> '"
                + valor
                + "'"
            )


def biciesto(year):
    """Comprueba si el año es biciesto."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


registros = leer_archivo(FILE)
validar_numero_campos(registros, FIELD_COUNT)
validar_fecha(registros, 1)
validar_entero(registros, 2)
validar_mes(registros, 3)
validar_entero(registros, 5)
validar_entero(registros, 7)
validar_entero(registros, 9)
validar_entero(registros, 11)
validar_flotante(registros, 14)
validar_flotante(registros, 15)
validar_entero(registros, 16)
validar_si_no(registros, 19)

print(f"Validación completada")
