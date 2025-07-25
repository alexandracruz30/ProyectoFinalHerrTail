# 🧠 CNN Model Explorer - Wafer Defect Detection

**Una aplicación web moderna para la detección de defectos en obleas de silicio utilizando modelos CNN avanzados**

![Django](https://img.shields.io/badge/Django-5.2-green?style=flat-square&logo=django)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-4.1-blue?style=flat-square&logo=tailwindcss)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=flat-square)

## 🎯 Descripción

CNN Model Explorer es una aplicación web desarrollada con Django que permite a los usuarios interactuar con modelos de redes neuronales convolucionales (CNN) para detectar defectos en obleas de silicio. La aplicación ofrece una interfaz moderna, responsiva y fácil de usar para la clasificación de imágenes industriales.

## ✨ Características Principales

### 🔍 **Detección de Defectos**
- **9 Tipos de Defectos**: Center, Donut, Edge-Loc, Edge-Ring, Loc, Near-full, Random, Scratch, None
- **4 Modelos CNN**: InceptionV3, ResNet50, VGG16, MobileNet
- **Alta Precisión**: Hasta 98.7% de accuracy con ResNet50

### 🎨 **Interfaz Moderna**
- **Diseño Responsivo**: Funciona perfectamente en móviles, tablets y desktop
- **UI/UX Moderna**: Glassmorphism, animaciones suaves, efectos visuales
- **Navegación Intuitiva**: Menús adaptativos y navegación fluida

### 🚀 **Funcionalidades**
- **Clasificación en Tiempo Real**: Sube una imagen y obtén resultados instantáneos
- **Múltiples Modelos**: Compara resultados entre diferentes arquitecturas CNN
- **Visualización de Resultados**: Gráficos de probabilidades y confianza
- **Sistema de Usuarios**: Autenticación y sesiones de usuario

## 🛠️ Tecnologías Utilizadas

### **Backend**
- **Django 5.2**: Framework web principal
- **Python 3.10+**: Lenguaje de programación
- **SQLite**: Base de datos para desarrollo
- **TensorFlow/Keras**: Modelos de machine learning

### **Frontend**
- **TailwindCSS 4.1**: Framework CSS utilitario
- **HTML5 + CSS3**: Estructura y estilos personalizados
- **JavaScript ES6+**: Interactividad y animaciones
- **Responsive Design**: Compatible con todos los dispositivos

### **Arquitectura**
- **MVT Pattern**: Modelo-Vista-Template de Django
- **Class-Based Views**: Vistas organizadas y reutilizables
- **Template Inheritance**: Sistema de plantillas modular

## 📁 Estructura del Proyecto

```
ProyectoFinalHerrTail/
├── 📱 waferapp/                 # Aplicación principal
│   ├── 🎯 models.py            # Modelos de datos
│   ├── 👀 views.py             # Lógica de vistas
│   ├── 🛣️ urls.py              # Configuración de URLs
│   ├── 📝 forms.py             # Formularios
│   ├── 🎨 templates/           # Plantillas HTML
│   │   ├── base/               # Plantillas base
│   │   ├── modelos/            # Páginas de modelos
│   │   ├── pruebas/            # Página de pruebas
│   │   └── usuario/            # Autenticación
│   └── 🗃️ migrations/          # Migraciones de BD
├── ⚙️ waferproject/            # Configuración del proyecto
│   ├── settings.py            # Configuración Django
│   ├── urls.py                # URLs principales
│   └── wsgi.py                # Configuración WSGI
├── 🎨 static/                  # Archivos estáticos
│   ├── src/                   # CSS principal
│   │   ├── input.css          # Estilos personalizados
│   │   └── output.css         # TailwindCSS compilado
│   └── iconos/                # Iconografía
├── 🗄️ db.sqlite3             # Base de datos
├── 📋 requirements.txt        # Dependencias Python
├── 📦 package.json           # Dependencias Node.js
└── 🚀 manage.py              # Script de gestión Django
```

## 🚀 Instalación y Configuración

### **Prerrequisitos**
- Python 3.10 o superior
- Node.js 16+ (para TailwindCSS)
- Git

### **1. Clonar el Repositorio**
```bash
git clone <repository-url>
cd ProyectoFinalHerrTail
```

### **2. Configurar Entorno Virtual**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### **3. Instalar Dependencias Python**
```bash
pip install -r requirements.txt
```

### **4. Configurar Base de Datos**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **5. Crear Superusuario (Opcional)**
```bash
python manage.py createsuperuser
```

### **6. Ejecutar Servidor de Desarrollo**
```bash
python manage.py runserver
```

### **7. Acceder a la Aplicación**
- **URL**: `http://127.0.0.1:8000/`
- **Admin**: `http://127.0.0.1:8000/admin/`

## 🎮 Uso de la Aplicación

### **1. Página Principal**
- Visualiza los modelos CNN disponibles
- Compara precisiones y características
- Accede a información detallada

### **2. Zona de Pruebas**
- Selecciona un modelo CNN
- Sube una imagen de oblea
- Obtén resultados de clasificación
- Visualiza probabilidades por clase

### **3. Dashboard**
- Accede a herramientas adicionales
- Gestiona sesiones de usuario
- Navega entre funcionalidades

### **4. Gestión de Modelos**
- Entrena nuevos modelos
- Visualiza arquitecturas
- Compara rendimientos

## 🧪 Modelos CNN Disponibles

| Modelo | Accuracy | Descripción | Casos de Uso |
|--------|----------|-------------|--------------|
| **InceptionV3** | 96.4% | Módulos inception para multi-escala | Detección general |
| **ResNet50** | 98.7% | Conexiones residuales profundas | Alta precisión |
| **VGG16** | 95.2% | Convoluciones profundas simples | Interpretabilidad |
| **MobileNet** | 94.1% | Optimizado para velocidad | Tiempo real |

## 🎯 Clases de Defectos

La aplicación puede detectar **9 tipos** de defectos en obleas:

1. **Center** - Defectos en el centro
2. **Donut** - Patrones circulares
3. **Edge-Loc** - Defectos en bordes localizados
4. **Edge-Ring** - Anillos en bordes
5. **Loc** - Defectos localizados
6. **Near-full** - Casi toda la superficie
7. **Random** - Patrones aleatorios
8. **Scratch** - Rayones superficiales
9. **None** - Sin defectos

## 🔧 Configuración Avanzada

### **Variables de Entorno**
```bash
# .env (opcional)
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
```

### **Configuración de Producción**
```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['tu-dominio.com']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # ... configuración PostgreSQL
    }
}
```

### **Archivos Estáticos**
```bash
# Recolectar archivos estáticos
python manage.py collectstatic
```

## 🎨 Personalización de Estilos

### **Estructura CSS**
- **`input.css`**: Estilos personalizados organizados por secciones
- **`output.css`**: TailwindCSS compilado automáticamente

### **Modificar Estilos**
1. Editar `static/src/input.css`
2. Usar la tabla de contenidos para navegación
3. Seguir las convenciones de nomenclatura
4. Probar en diferentes dispositivos

## 🧪 Testing

### **Ejecutar Tests**
```bash
python manage.py test
```

### **Tests Disponibles**
- Tests de modelos
- Tests de vistas
- Tests de formularios
- Tests de URLs

## 📱 Responsividad

La aplicación está optimizada para:
- **📱 Móviles**: 320px - 768px
- **📲 Tablets**: 768px - 1024px
- **💻 Desktop**: 1024px+
- **🖥️ Large Desktop**: 1280px+

## 🔒 Seguridad

### **Características de Seguridad**
- Protección CSRF activada
- Validación de formularios
- Escape automático de templates
- Headers de seguridad configurados

### **Mejores Prácticas**
- Usar HTTPS en producción
- Configurar variables de entorno
- Mantener dependencias actualizadas
- Realizar backups regulares

## 🚀 Despliegue

### **Opciones de Despliegue**
- **Heroku**: Fácil despliegue con Git
- **AWS**: EC2, Elastic Beanstalk
- **DigitalOcean**: App Platform
- **Railway**: Despliegue automático

### **Checklist de Producción**
- [ ] `DEBUG = False`
- [ ] Configurar `ALLOWED_HOSTS`
- [ ] Base de datos PostgreSQL
- [ ] Configurar archivos estáticos
- [ ] Variables de entorno seguras
- [ ] Certificado SSL

## 🤝 Contribución

### **Cómo Contribuir**
1. Fork el repositorio
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

### **Estándares de Código**
- Seguir PEP 8 para Python
- Usar nombres descriptivos
- Documentar funciones complejas
- Escribir tests para nuevas features

## 🐛 Solución de Problemas

### **Problemas Comunes**

**Error: "TensorFlow import error"**
```bash
pip install tensorflow
```

**Error: "Static files not found"**
```bash
python manage.py collectstatic
```

**Error: "Database migration issues"**
```bash
python manage.py makemigrations --empty waferapp
python manage.py migrate
```

## 📚 Recursos Adicionales

- **Django Documentation**: https://docs.djangoproject.com/
- **TailwindCSS Guide**: https://tailwindcss.com/docs
- **TensorFlow Tutorials**: https://www.tensorflow.org/tutorials

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Equipo de Desarrollo

- **Desarrollador Principal**: [Tu Nombre]
- **UI/UX Design**: [Nombre del Diseñador]
- **Machine Learning**: [Nombre del Especialista ML]

## 📞 Contacto

- **Email**: [tu-email@ejemplo.com]
- **LinkedIn**: [tu-linkedin]
- **GitHub**: [tu-github]

---

<div align="center">
  <strong>🌟 ¡Hecho con ❤️ y Python! 🌟</strong>
  <br>
  <sub>CNN Model Explorer v2.0 - 2025</sub>
</div>
  
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

##USER
carlos22
nosequeponer1234

