# Proyecto Final HerrTail - CNN Model Explorer

## Descripción
Este proyecto es una aplicación web desarrollada con Django que utiliza Tailwind CSS para el diseño. Es una plataforma especializada en la exploración y prueba de modelos de Redes Neuronales Convolucionales (CNN) para la clasificación de imágenes de wafers semiconductores. La aplicación incluye funcionalidades como autenticación de usuarios, gestión de modelos CNN, pruebas interactivas, visualización de datos y un dashboard completo.

## Funcionalidades Principales
- **Clasificación de Wafers**: Utiliza modelos CNN preentrenados para clasificar defectos en wafers semiconductores
- **Autenticación de Usuarios**: Sistema completo de registro, login y logout
- **Interfaz Interactiva**: Permite subir imágenes y obtener predicciones en tiempo real
- **Dashboard**: Visualización de métricas y estadísticas de los modelos
- **Guía de Uso**: Documentación integrada para el usuario
- **Arquitectura Visual**: Representación gráfica de la arquitectura del modelo CNN

## Estructura Detallada del Proyecto

### Archivos de Configuración Principal
- **`db.sqlite3`**: Base de datos SQLite que almacena la información de los modelos CNN registrados, usuarios y sesiones
- **`manage.py`**: Script principal de Django para ejecutar comandos como `runserver`, `migrate`, `createsuperuser`, etc.
- **`package.json`**: Configuración de Node.js que define las dependencias de JavaScript:
  - `tailwindcss`: Framework CSS para estilos
  - `autoprefixer`: Plugin para compatibilidad CSS
  - `postcss`: Procesador CSS
- **`requirements.txt`**: Lista extensa de dependencias de Python (461 líneas) que incluye:
  - Django para el framework web
  - TensorFlow/Keras para machine learning
  - PIL (Pillow) para procesamiento de imágenes
  - NumPy para computación científica
  - Muchas otras librerías científicas y de desarrollo

### Carpetas Estáticas
- **`static/`**: Archivos estáticos servidos por Django
  - **`entrenapng/`**: Imágenes de ejemplo del proceso de entrenamiento:
    - `original.png`: Imagen original del wafer
    - `reconstruida.png`: Imagen reconstruida por el modelo
    - `ruido.png`: Imagen con ruido aplicado
    - `wCenter.png`, `wDonut.png`, `wEdgeLoc.png`: Ejemplos de diferentes tipos de defectos
  - **`iconos/`**: Íconos para la interfaz de usuario:
    - `principal.png`: Logo principal de la aplicación
    - `modelos.png`, `dataset.png`, `arquitectura.png`: Íconos de navegación
    - `brain-networking.png`, `LLM.png`: Íconos relacionados con AI
    - `guiauso.png`, `test.png`, `data.png`: Íconos funcionales
  - **`src/`**: Archivos CSS procesados por Tailwind:
    - `input.css`: Archivo CSS de entrada
    - `output.css`: Archivo CSS compilado y optimizado

### Aplicación Principal (waferapp/)
- **`models.py`**: Define el modelo `ModeloCNN` para la base de datos:
  - `nombre`: CharField para el nombre del modelo
  - `accuracy`: CharField para almacenar la precisión del modelo
  - `descripcion`: TextField para la descripción detallada
  
- **`views.py`**: Contiene toda la lógica de las vistas (160 líneas):
  - `HomeView`: Vista principal que muestra modelos registrados
  - `DashboardView`: Vista del dashboard con métricas
  - `procesoModeloView`: Vista para mostrar el proceso de entrenamiento
  - `SignUpView`: Vista para registro de usuarios
  - `UserLoginView` y `UserLogoutView`: Vistas de autenticación
  - `EntrenamientoView`: Vista para el proceso de entrenamiento
  - `DetallesUsoView`: Vista con detalles de uso del modelo
  - `PruebasView`: Vista principal para pruebas con imágenes (incluye lógica de predicción con TensorFlow)
  
- **`urls.py`**: Configuración de rutas de la aplicación:
  - `/`: Página principal
  - `/signup/`, `/login/`, `/logout/`: Rutas de autenticación
  - `/proceso-entrenamiento/`: Página de entrenamiento
  - `/detalles-uso/`: Guía de uso
  - `/zona-pruebas/`: Área de pruebas interactivas
  - `/dashboard/`: Panel de control
  
- **`forms.py`**: Formularios de Django:
  - `ModeloCNNForm`: Formulario para crear/editar modelos CNN
  - `LLMChatForm`: Formulario para interacción con chat (funcionalidad futura)
  
- **`admin.py`**: Configuración del panel de administración (actualmente vacío)
- **`apps.py`**: Configuración de la aplicación Django
- **`tests.py`**: Archivo para pruebas unitarias

### Plantillas HTML (templates/)
- **`base/`**: Plantillas base del sitio
  - `base.html`: Plantilla base con navegación completa, header con "CNN Model Explorer", menú de navegación con íconos y estructura general
  - `index.html`: Página principal que extiende la plantilla base
  
- **`dash/`**: Dashboard
  - `dash.html`: Interfaz del dashboard con métricas y visualizaciones
  
- **`modelos/`**: Gestión de modelos
  - `add_modelo.html`: Formulario para agregar nuevos modelos
  - `detalles.html`: Página con detalles de uso del modelo
  - `entrena.html`: Página del proceso de entrenamiento
  - `procesoModelo.html`: Visualización del proceso del modelo
  
- **`pruebas/`**: Área de pruebas
  - `pruebas.html`: Interfaz para subir imágenes y obtener predicciones
  
- **`usuario/`**: Autenticación
  - `login.html`: Página de inicio de sesión
  - `signup.html`: Página de registro de usuarios

### Configuración del Proyecto (waferproject/)
- **`settings.py`**: Configuración principal de Django:
  - Configuración de aplicaciones instaladas (Django, waferapp, tailwind)
  - Configuración de base de datos SQLite
  - Configuración de archivos estáticos
  - Configuración de plantillas
  - Middleware de seguridad
  
- **`urls.py`**: Configuración de rutas globales del proyecto
- **`wsgi.py`** y **`asgi.py`**: Configuración para servidores web

## Tecnologías y Dependencias

### Backend
- **Django 5.2**: Framework web principal
- **Python 3.10+**: Lenguaje de programación
- **SQLite**: Base de datos integrada
- **TensorFlow/Keras**: Para machine learning y CNN
- **Pillow (PIL)**: Procesamiento de imágenes
- **NumPy**: Computación científica y manejo de arrays

### Frontend
- **Tailwind CSS 4.1.11**: Framework CSS utilitario
- **HTML5**: Estructura de páginas
- **JavaScript**: Interactividad (partículas de fondo)
- **PostCSS**: Procesamiento CSS
- **Autoprefixer**: Compatibilidad CSS cross-browser

### Clasificación de Wafers
El sistema puede clasificar 9 tipos diferentes de defectos en wafers semiconductores:
1. **Center**: Defectos en el centro
2. **Donut**: Defectos en forma de anillo
3. **Edge-Loc**: Defectos localizados en el borde
4. **Edge-Ring**: Defectos en anillo en el borde
5. **Loc**: Defectos localizados
6. **Near-full**: Defectos que cubren casi todo el wafer
7. **Random**: Defectos aleatorios
8. **Scratch**: Arañazos
9. **None**: Sin defectos

## Instalación y Configuración

### Requisitos Previos
- Python 3.10 o superior
- Node.js (para Tailwind CSS)
- Git

### Pasos de Instalación
1. **Clona el repositorio**:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd ProyectoFinalHerrTail
   ```

2. **Crea un entorno virtual**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # En Windows
   # source venv/bin/activate  # En Linux/Mac
   ```

3. **Instala las dependencias de Python**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Instala las dependencias de Node.js**:
   ```bash
   npm install
   ```

5. **Compila los estilos CSS**:
   ```bash
   npx tailwindcss -i ./static/src/input.css -o ./static/src/output.css --watch
   ```

6. **Configura la base de datos**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Crea un superusuario (opcional)**:
   ```bash
   python manage.py createsuperuser
   ```

8. **Inicia el servidor de desarrollo**:
   ```bash
   python manage.py runserver
   ```

## Uso de la Aplicación

### Navegación Principal
- **Modelos**: Visualiza y gestiona modelos CNN registrados
- **Dataset**: Información sobre el conjunto de datos utilizado
- **Arquitectura**: Visualización de la arquitectura del modelo CNN
- **Guía de uso**: Documentación detallada para el usuario
- **Pruebas**: Interfaz interactiva para subir imágenes y obtener predicciones
- **Dashboard**: Métricas y estadísticas del sistema

### Funcionalidades Clave
1. **Registro y Login**: Los usuarios pueden crear cuentas y autenticarse
2. **Subida de Imágenes**: Sube imágenes de wafers para clasificación
3. **Predicciones en Tiempo Real**: Obtén resultados instantáneos del modelo CNN
4. **Visualización de Probabilidades**: Ve las probabilidades de cada clase
5. **Gestión de Modelos**: Administra diferentes modelos CNN

### Estructura de Archivos del Modelo
- El modelo CNN debe estar ubicado en `modelos/mi_modelo.h5`
- Las imágenes deben ser de 26x26 píxeles para el procesamiento
- Formatos soportados: PNG, JPG, JPEG

## Desarrollo y Contribución

### Estructura del Código
- **Separación de Responsabilidades**: Modelos, vistas, formularios y plantillas están claramente separados
- **Arquitectura MTV**: Sigue el patrón Model-Template-View de Django
- **Responsive Design**: Utiliza Tailwind CSS para diseño responsivo
- **Manejo de Errores**: Implementa manejo robusto de errores en las predicciones

### Mejoras Futuras
- Integración con LLM para chat interactivo
- Soporte para más tipos de modelos de machine learning
- API REST para integraciones externas
- Sistema de métricas avanzado
- Almacenamiento en la nube para imágenes

### Contribuir al Proyecto
1. Fork el repositorio
2. Crea una nueva rama: `git checkout -b feature/nueva-funcionalidad`
3. Realiza tus cambios y commitea: `git commit -m "Descripción del cambio"`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

## Resolución de Problemas

### Problemas Comunes
1. **Modelo no encontrado**: Asegúrate de que el archivo `mi_modelo.h5` esté en la carpeta `modelos/`
2. **Errores de CSS**: Ejecuta `npx tailwindcss` para recompilar los estilos
3. **Dependencias faltantes**: Verifica que todas las dependencias estén instaladas con `pip install -r requirements.txt`

### Logs y Debugging
- Los errores de predicción se muestran en la interfaz de usuario
- Los logs de Django se pueden ver en la consola del servidor
- Para debugging, activa `DEBUG = True` en `settings.py` (solo en desarrollo)

## Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

## Contacto
Para preguntas o sugerencias sobre el proyecto, puedes contactar al equipo de desarrollo.
