import csv
import os
import unicodedata

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_CSV = os.path.join(BASE_DIR, "data", "paises.csv")

# -----------------------------
# FUNCIONES DE NORMALIZACIÓN
# -----------------------------

def normalizar(texto):
    texto = texto.strip().lower()
    texto = unicodedata.normalize("NFD", texto).encode("ascii", "ignore").decode("utf-8")
    texto = " ".join(texto.split())  
    return texto

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

    nombre = normalizar(input("Nombre del país: "))
    poblacion = input("Población: ").strip()
    superficie = input("Superficie (km²): ").strip()
    continente = normalizar(input("Continente: "))

    if not nombre or not continente or not poblacion.isdigit() or not superficie.isdigit():
        print("⚠️ Datos inválidos.")
        return

    for pais in paises:
        if normalizar(pais["nombre"]) == nombre:
            print("⚠️ Ese país ya existe en la base de datos.")
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

    nombre = normalizar(input("Ingrese el nombre del país a actualizar: "))

    for pais in paises:
        if normalizar(pais["nombre"]) == nombre:
            nueva_p = input("Nueva población (enter para no cambiar): ").strip()
            nueva_s = input("Nueva superficie (enter para no cambiar): ").strip()
            nuevo_c = input("Nuevo continente (enter para no cambiar): ").strip()

            if nueva_p.isdigit():
                pais["poblacion"] = int(nueva_p)
            if nueva_s.isdigit():
                pais["superficie"] = int(nueva_s)
            if nuevo_c:
                pais["continente"] = normalizar(nuevo_c)

            guardar_paises(paises)
            print("✅ País actualizado.")
            return

    print("⚠️ País no encontrado.")


def buscar_pais(paises):
    print("\n--- BUSCAR PAÍS ---")
    nombre = normalizar(input("Ingrese nombre o parte del nombre: "))

    encontrados = [p for p in paises if nombre in normalizar(p["nombre"])]

    if encontrados:
        for pais in encontrados:
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
        cont = normalizar(input("Ingrese continente: "))
        filtrados = [p for p in paises if normalizar(p["continente"]) == cont]

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

    print("a) Ascendente")
    print("b) Descendente")
    sentido = input("Elija sentido: ")

    reverso = True if sentido.lower() == "b" else False

    if opcion == "1":
        paises.sort(key=lambda x: normalizar(x["nombre"]), reverse=reverso)
    elif opcion == "2":
        paises.sort(key=lambda x: x["poblacion"], reverse=reverso)
    elif opcion == "3":
        paises.sort(key=lambda x: x["superficie"], reverse=reverso)
    else:
        print("⚠️ Opción inválida.")
        return

    guardar_paises(paises)
    print("✅ Países ordenados.")


def mostrar_estadisticas(paises):
    print("\n--- ESTADÍSTICAS ---")

    mayor = max(paises, key=lambda p: p["poblacion"])
    menor = min(paises, key=lambda p: p["poblacion"])

    total_p = sum(p["poblacion"] for p in paises)
    total_s = sum(p["superficie"] for p in paises)

    conteo = {}
    for p in paises:
        cont = p["continente"]
        conteo[cont] = conteo.get(cont, 0) + 1

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
