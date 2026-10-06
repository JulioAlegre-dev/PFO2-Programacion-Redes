# Práctica Formativa Obligatoria 2 (PFO 2) - Programación sobre Redes
## Sistema de Gestión de Tareas con API REST y Persistencia en SQLite

### Descripción del Proyecto
Implementación de una arquitectura cliente-servidor basada en una API REST construida con Flask y persistencia local en SQLite. El servidor gestiona el registro seguro de usuarios aplicando algoritmos criptográficos de hasheo con salt para proteger las contraseñas, valida el inicio de sesión y sirve contenido HTML de bienvenida. La interacción se realiza mediante un cliente de consola interactivo desarrollado en Python.

---

### Estructura de Archivos
* `servidor.py`: API REST con Flask, endpoints `/registro`, `/login`, `/tareas` y persistencia en SQLite.
* `cliente.py`: Cliente interactivo en consola para realizar peticiones HTTP a la API.
* `tareas.db`: Archivo generado automáticamente por SQLite con la tabla de usuarios registrados.
* `README.md`: Documentación técnica, esquema de base de datos, guía de ejecución y respuestas conceptuales.
* `img/Captura pantalla Servidor - Cliente.png`: Evidencia visual de la interacción cliente-servidor y códigos de estado HTTP.
* `img/Captura Bienvenido al Gestor de Tareas.png`: Evidencia de la interfaz HTML servida por la API.

---

### Esquema de Persistencia (SQLite)
Tabla `usuarios`:
* `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
* `usuario` (TEXT, UNIQUE, NOT NULL)
* `contrasena` (TEXT, NOT NULL - Hash criptográfico generado mediante Werkzeug)

---

### Requisitos Previos e Instalación
* Python 3.8 o superior instalado.
* Instalación de librerías requeridas:
  ```bash
  py -m pip install Flask requests
  ```
  *(Nota: `sqlite3` y `werkzeug` vienen incluidos en la biblioteca estándar de Python y junto con Flask respectivamente).*

---

### Instrucciones de Ejecución

1. Iniciar el Servidor API:
   Abrir una terminal en el directorio del proyecto y ejecutar:
   ```bash
   py servidor.py
   ```
   El servidor inicializará la base de datos `tareas.db` (creando la tabla `usuarios` si no existe) y quedará a la escucha en `http://127.0.0.1:5000`.

2. Iniciar el Cliente de Consola:
   Abrir una segunda terminal en el mismo directorio y ejecutar:
   ```bash
   py cliente.py
   ```
   Se desplegará el menú interactivo con las siguientes opciones:
   * **Opción 1:** Registrar un nuevo usuario (POST `/registro`).
   * **Opción 2:** Iniciar sesión y comprobar credenciales hasheadas (POST `/login`).
   * **Opción 3:** Solicitar la vista de bienvenida (GET `/tareas`).
   * **Opción 4:** Salir del cliente interactivo.

3. Visualización Web:
   Abrir un navegador web e ingresar a `http://127.0.0.1:5000/tareas` para comprobar la respuesta visual servida por Flask.

---

### Respuestas Conceptuales

#### 1. ¿Por qué hashear contraseñas?
Las contraseñas nunca deben guardarse en texto plano para garantizar la confidencialidad de los usuarios en caso de filtraciones, accesos no autorizados o brechas de seguridad en la base de datos. 

Un hash criptográfico es una función matemática unidireccional (*one-way*): permite validar si una clave ingresada coincide con la registrada calculando su hash, sin necesidad de que el sistema conozca ni almacene jamás la contraseña original en texto claro. Asimismo, las implementaciones modernas como `werkzeug.security` aplican de forma automática un *salt* (secuencia aleatoria agregada a la contraseña antes de procesarla), lo cual mitiga ataques basados en tablas precalculadas (*rainbow tables*) y fuerza bruta masiva por diccionario.

#### 2. Ventajas de usar SQLite en este proyecto
* **Arquitectura Serverless:** No requiere de un motor ni de un proceso servidor independiente de base de datos (como PostgreSQL o MySQL); el motor corre embebido en el mismo proceso de Python.
* **Persistencia Monolítica en un Archivo:** Toda la base de datos, esquema e información reside en el archivo único `tareas.db`, facilitando enormemente la portabilidad, el backup y las pruebas en entornos de desarrollo.
* **Cero Configuración y Compatibilidad Nativa:** Se integra directamente a través del módulo estándar `sqlite3` de Python, asegurando que el proyecto no dependa de controladores o servicios externos adicionales para persistir la información.

---

### Evidencias de Pruebas Exitosas

#### Interacción Servidor - Cliente
![Prueba Servidor Cliente](img/Captura%20pantalla%20Servidor%20-%20Cliente.png)

#### Vista Web de Bienvenida
![Bienvenida al Gestor de Tareas](img/Captura%20Bienvenido%20al%20Gestor%20de%20Tareas.png)
