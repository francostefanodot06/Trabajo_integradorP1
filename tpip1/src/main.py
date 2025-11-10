import csv
import os

RUTA_CSV = "data/paises.csv"

# Crea la carpeta en caso de no existir:
os.makedirs("data", exist_ok=True)

# -----------------------------
# FUNCIONES DE ARCHIVOS
# -----------------------------

def cargar_paises():
    paises = []

    if not os.path.exists(RUTA_CSV):
        print(f"⚠️ No se encontró el archivo {RUTA_CSV}. Se creará al guardar datos.")
        return paises

    with open(RUTA_CSV, "r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            # Validación numérica sin try-except
            if fila["poblacion"].isdigit() and fila["superficie"].isdigit():
                fila["poblacion"] = int(fila["poblacion"])
                fila["superficie"] = int(fila["superficie"])
                paises.append(fila)

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

    nombre = " ".join(input("Nombre del país: ").strip().split())
    poblacion = input("Población: ").strip()
    superficie = input("Superficie (km²): ").strip()
    continente = " ".join(input("Continente: ").strip().split())

    if not nombre or not continente or not poblacion.isdigit() or not superficie.isdigit():
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
            nueva_p = input("Nueva población (enter para no cambiar): ").strip()
            nueva_s = input("Nueva superficie (enter para no cambiar): ").strip()

            if nueva_p and nueva_p.isdigit():
                pais["poblacion"] = int(nueva_p)

            if nueva_s and nueva_s.isdigit():
                pais["superficie"] = int(nueva_s)

            guardar_paises(paises)
            print("✅ País actualizado.")
            return

    print("⚠️ País no encontrado.")


def buscar_pais(paises):
    print("\n--- BUSCAR PAÍS ---")
    nombre = input("Ingrese nombre o parte del nombre: ").strip().lower()

    resultados = []
    for p in paises:
        if nombre in p["nombre"].lower():
            resultados.append(p)

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

    if opc == "1":
        cont = input("Ingrese continente: ").strip().lower()
        filtrados = [p for p in paises if p["continente"].lower() == cont]

    elif opc == "2":
        min_p = input("Población mínima: ").strip()
        max_p = input("Población máxima: ").strip()
        if not min_p.isdigit() or not max_p.isdigit():
            print("⚠️ Debe ingresar valores numéricos.")
            return
        min_p, max_p = int(min_p), int(max_p)
        filtrados = [p for p in paises if min_p <= p["poblacion"] <= max_p]

    elif opc == "3":
        min_s = input("Superficie mínima: ").strip()
        max_s = input("Superficie máxima: ").strip()
        if not min_s.isdigit() or not max_s.isdigit():
            print("⚠️ Debe ingresar valores numéricos.")
            return
        min_s, max_s = int(min_s), int(max_s)
        filtrados = [p for p in paises if min_s <= p["superficie"] <= max_s]

    else:
        print("⚠️ Opción inválida.")
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
    opcion = input("Elija una opción: ")

    if opcion == "1":
        paises.sort(key=lambda x: x["nombre"])
    elif opcion == "2":
        paises.sort(key=lambda x: x["poblacion"])
    elif opcion == "3":
        paises.sort(key=lambda x: x["superficie"])
    else:
        print("⚠️ Opción inválida.")
        return

    guardar_paises(paises)
    print("✅ Países ordenados.")


def mostrar_estadisticas(paises):
    print("\n--- ESTADÍSTICAS ---")

    mayor = paises[0]
    menor = paises[0]

    total_p = 0
    total_s = 0
    conteo = {}

    for p in paises:
        total_p += p["poblacion"]
        total_s += p["superficie"]
        if p["poblacion"] > mayor["poblacion"]:
            mayor = p
        if p["poblacion"] < menor["poblacion"]:
            menor = p
        conteo[p["continente"]] = conteo.get(p["continente"], 0) + 1

    print(f"Mayor población: {mayor['nombre']} ({mayor['poblacion']})")
    print(f"Menor población: {menor['nombre']} ({menor['poblacion']})")
    print(f"Promedio de población: {total_p // len(paises)}")
    print(f"Promedio de superficie: {total_s // len(paises)} km²")
    print("\nPaíses por continente:")
    for cont, cant in conteo.items():
        print(f"- {cont}: {cant}")


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
