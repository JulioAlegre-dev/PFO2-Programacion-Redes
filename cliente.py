import requests

BASE_URL = "http://127.0.0.1:5000"

def menu():
    print("\n--- CLIENTE GESTOR DE TAREAS ---")
    print("1. Registrar nuevo usuario")
    print("2. Iniciar sesión")
    print("3. Ver página de bienvenida (/tareas)")
    print("4. Salir")
    return input("Seleccione una opción: ")

def main():
    while True:
        opcion = menu()
        if opcion == "1":
            user = input("Ingrese usuario: ")
            pwd = input("Ingrese contraseña: ")
            res = requests.post(f"{BASE_URL}/registro", json={"usuario": user, "contraseña": pwd})
            print(f"[{res.status_code}] {res.json().get('mensaje')}")

        elif opcion == "2":
            user = input("Ingrese usuario: ")
            pwd = input("Ingrese contraseña: ")
            res = requests.post(f"{BASE_URL}/login", json={"usuario": user, "contraseña": pwd})
            print(f"[{res.status_code}] {res.json().get('mensaje')}")

        elif opcion == "3":
            res = requests.get(f"{BASE_URL}/tareas")
            print(f"[{res.status_code}] Respuesta HTML recibida correctamente.")
            print("Puedes abrir en tu navegador: http://127.0.0.1:5000/tareas")

        elif opcion == "4":
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()