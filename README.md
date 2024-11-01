# Enpoint para Carga y Gestión de Archivos

### Implementacion
Configurar la ruta para cargar archivos (POST /upload).
![imagen](https://github.com/user-attachments/assets/41dd75e9-a52a-487e-8cfa-3265c361e1d2)
![imagen](https://github.com/user-attachments/assets/08e41956-7c50-47ef-bc67-997747d50fc2)

Validar el tipo de archivo (por ejemplo, solo permitir imágenes o PDFs).
![imagen](https://github.com/user-attachments/assets/a409c470-5639-4c99-b2fc-525227ceb95f)

Guardar los archivos en un directorio en el servidor o depende el tipo seria la gestion.
![imagen](https://github.com/user-attachments/assets/36c0ad93-94d3-46a8-9741-e17ed85631da)
![imagen](https://github.com/user-attachments/assets/8ce83873-d426-4e67-ac75-de6f5beb8b75)

Implementar una ruta para descargar o acceder a los archivos almacenados.
![imagen](https://github.com/user-attachments/assets/8a44ea53-3413-45b6-8aab-b30cb2169454)

Implementar lógica de control de errores para evitar cargas fallidas, archivos corruptos o repetidos.
![imagen](https://github.com/user-attachments/assets/fc20168f-6555-4cae-9cfe-fcc71167f9ef)
![imagen](https://github.com/user-attachments/assets/02f77873-1041-4e53-be93-d0c0b45c979d)

### Pruebas y Resultados

Si vamos a localhost/upload en el navegador obtenemos un error ya que al acceder estamos utilizando el metodo GET en lugar de POST.
![imagen](https://github.com/user-attachments/assets/4ad2061f-f64f-4c2e-92f8-fba58eda6b83)

Entramos a POSTMAN y realizamos una POST request a localhost/upload, con un body dando la ruta del archivo que se desea enviar, en este caso la imagen ensenada.jpg
![imagen](https://github.com/user-attachments/assets/fd560f6b-9a5f-42a2-9ed6-1ab4d35082e3)
la realizamos y vemos que el archivo se cargo correctamente:
![imagen](https://github.com/user-attachments/assets/d2482d89-d913-4cc8-991a-ddbf8395bb27)

Entramos al contenedor de Flask en Docker y vemos el archivo en la carpeta ./uploads que preparamos:
![imagen](https://github.com/user-attachments/assets/8229636d-0d36-4657-9a7a-7234667ecd4f)

Comprobamos el manejo de errores:
Si intentamos enviar de nuevo el mismo archivo
![imagen](https://github.com/user-attachments/assets/9b5544a9-461e-475b-a3c1-7fa9fd0befce)
Si intentamos enviar un archivo con una extension no permitida, en este caso ensenada.exe
![imagen](https://github.com/user-attachments/assets/bc068e34-b660-4e94-bb99-f430a22419fc)

Y finalmente podemos descargar el archivo enviado usando el endpoint /download/ensenada.jpg, como se trata de un metodo GET, podemos entrar desde el navegador donde se descargara automaticamente el archivo:
![imagen](https://github.com/user-attachments/assets/e8cff161-c383-4290-b281-fd02d42f1ccc)
