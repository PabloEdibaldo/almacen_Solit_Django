# Use una imagen base de Python
FROM python:3.10.12

# Establece el directorio de trabajo
WORKDIR /app

# Copia los requerimientos del proyecto
COPY requirements.txt .

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente del proyecto
COPY . .

# Expone el puerto 8000 para el servidor Django
EXPOSE 8000

# Establece las variables de entorno
ENV DJANGO_SETTINGS_MODULE=home.settings
ENV PYTHONUNBUFFERED=1

# Ejecuta los comandos de Django
CMD ["python3", "manage.py", "runserver", "172.16.15.37:8000"]

