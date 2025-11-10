import csv

# Ruta del archivo CSV
RUTA_CSV = "data/paises.csv"

# -----------------------------
# FUNCIONES DE ARCHIVOS
# -----------------------------

def cargar_paises():
    paises = []
    try:
        with open(RUTA_CSV, "r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                fila["poblacion"] = int(fila["poblacion"])
                fila["superficie"] = int(fila["superficie"])
                paises.append(fila)
    except FileNotFoundError:
        print(f"⚠️ No se encontró el archivo {RUTA_CSV}.")
    return paises


def guardar_paises(paises):
    with open(RUTA_CSV, "w", newline="", encoding="utf-8") as archivo:
        campos = ["nombre", "poblacion", "superficie", "continente"]
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        for pais in paises:
            escritor.writerow(pais)

# -----------------------------
# FUNCIONES PRINCIPALES
# -----------------------------

def agregar_pais(paises):
    print("\n--- AGREGAR PAÍS ---")
    nombre = input("Nombre del país: ").strip()
    poblacion = input("Población: ").strip()
    superficie = input("Superficie (km²): ").strip()
    continente = input("Continente: ").strip()

    if not nombre or not poblacion.isdigit() or not superficie.isdigit() or not continente:
        print("⚠️ Datos inválidos.")
        return

    paises.append({
        "nombre": nombre,
        "poblacion": int(poblacion),
        "superficie": int(superficie),
        "continente": continente
    })

    guardar_paises(paises)
    print("✅ País agregado correctamente.")


def actualizar_pais(paises):
    print("\n--- ACTUALIZAR PAÍS ---")
    nombre = input("Ingrese el nombre del país a actualizar: ").strip().lower()

    for pais in paises:
        if pais["nombre"].lower() == nombre:
            nueva_poblacion = input("Nueva población (enter para no cambiar): ").strip()
            nueva_superficie = input("Nueva superficie (enter para no cambiar): ").strip()

            if nueva_poblacion:
                if nueva_poblacion.isdigit():
                    pais["poblacion"] = int(nueva_poblacion)
                else:
                    print("⚠️ Población inválida.")
            if nueva_superficie:
                if nueva_superficie.isdigit():
                    pais["superficie"] = int(nueva_superficie)
                else:
                    print("⚠️ Superficie inválida.")

            guardar_paises(paises)
            print("✅ País actualizado correctamente.")
            return

    print("⚠️ No se encontró el país.")


def buscar_pais(paises):
    print("\n--- BUSCAR PAÍS ---")
    nombre = input("Ingrese nombre o parte del nombre: ").lower()

    resultados = [p for p in paises if nombre in p["nombre"].lower()]

    if resultados:
        for pais in resultados:
            print(f"{pais['nombre']} | Población: {pais['poblacion']} | Superficie: {pais['superficie']} | Continente: {pais['continente']}")
    else:
        print("⚠️ No se encontraron coincidencias.")


def filtrar_paises(paises):
    print("\n--- FILTRAR PAÍSES ---")
    print("1) Por continente")
    print("2) Por rango de población")
    print("3) Por rango de superficie")
    opc = input("Elija una opción: ")

    try:
        if opc == "1":
            cont = input("Ingrese continente: ").lower()
            filtrados = [p for p in paises if p["continente"].lower() == cont]

        elif opc == "2":
            min_p = int(input("Población mínima: "))
            max_p = int(input("Población máxima: "))
            filtrados = [p for p in paises if min_p <= p["poblacion"] <= max_p]

        elif opc == "3":
            min_s = int(input("Superficie mínima: "))
            max_s = int(input("Superficie máxima: "))
            filtrados = [p for p in paises if min_s <= p["superficie"] <= max_s]

        else:
            print("⚠️ Opción inválida.")
            return
    except ValueError:
        print("⚠️ Ingrese valores numéricos.")
        return

    if filtrados:
        for pais in filtrados:
            print(f"{pais['nombre']} | Población: {pais['poblacion']} | Superficie: {pais['superficie']} | Continente: {pais['continente']}")
    else:
        print("⚠️ No se encontraron resultados.")


def ordenar_paises(paises):
    print("\n--- ORDENAR PAÍSES ---")
    print("1) Nombre")
    print("2) Población")
    print("3) Superficie")
    criterio = input("Elija una opción: ")

    if criterio not in ["1", "2", "3"]:
        print("⚠️ Opción inválida.")
        return

    orden = input("Ascendente (A) o Descendente (D)?: ").upper()
    reverse = (orden == "D")

    claves = {"1": "nombre", "2": "poblacion", "3": "superficie"}
    paises.sort(key=lambda x: x[claves[criterio]], reverse=reverse)

    guardar_paises(paises)
    print("✅ Países ordenados.")


def mostrar_estadisticas(paises):
    print("\n--- ESTADÍSTICAS ---")
    mayor = max(paises, key=lambda p: p["poblacion"])
    menor = min(paises, key=lambda p: p["poblacion"])
    prom_poblacion = sum(p["poblacion"] for p in paises) / len(paises)
    prom_superficie = sum(p["superficie"] for p in paises) / len(paises)

    print(f"Mayor población: {mayor['nombre']} ({mayor['poblacion']})")
    print(f"Menor población: {menor['nombre']} ({menor['poblacion']})")
    print(f"Promedio de población: {int(prom_poblacion)}")
    print(f"Promedio de superficie: {int(prom_superficie)} km²")

    conteo = {}
    for p in paises:
        conteo[p["continente"]] = conteo.get(p["continente"], 0) + 1

    print("\nPaíses por continente:")
    for c, cant in conteo.items():
        print(f" - {c}: {cant}")


def mostrar_todos(paises):
    print("\n--- LISTA DE PAÍSES ---")
    for p in paises:
        print(f"{p['nombre']} | Población: {p['poblacion']} | Superficie: {p['superficie']} | Continente: {p['continente']}")

# -----------------------------
# MENÚ PRINCIPAL
# -----------------------------

def menu():
    paises = cargar_paises()

    while True:
        print("\n========================================")
        print("      SISTEMA DE GESTIÓN DE PAÍSES 🌍")
        print("========================================")
        print("1) Agregar país")
        print("2) Actualizar país")
        print("3) Buscar país")
        print("4) Filtrar países")
        print("5) Ordenar países")
        print("6) Ver estadísticas")
        print("7) Mostrar todos")
        print("0) Salir")

        opcion = input("Ingrese una opción: ")

        if opcion == "1": agregar_pais(paises)
        elif opcion == "2": actualizar_pais(paises)
        elif opcion == "3": buscar_pais(paises)
        elif opcion == "4": filtrar_paises(paises)
        elif opcion == "5": ordenar_paises(paises)
        elif opcion == "6": mostrar_estadisticas(paises)
        elif opcion == "7": mostrar_todos(paises)
        elif opcion == "0":
            print("Chau!")
            break
        else:
            print("⚠️ Opción inválida.")


if __name__ == "__main__":
    menu()
