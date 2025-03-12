# notificaciones-s3-lambda

Este proyecto es una función Lambda en AWS que se activa automáticamente cuando se sube un archivo a un bucket S3. Al detectar un nuevo objeto, la Lambda envía una notificación por correo electrónico utilizando el servicio SNS de AWS.

---

## 🚀 Pasos para desplegarlo

1. **Crear un bucket en S3** si aún no tienes uno.
2. **Crear una función Lambda** en AWS Lambda:
   - Elige el entorno de ejecución Python 3.x.
   - Copia y pega el código de la función desde este repositorio.
3. **Configurar los permisos de IAM**:
   - La Lambda debe tener permisos para leer el bucket S3 y publicar en el SNS Topic.
4. **Configurar el trigger del bucket S3**:
   - En el bucket, añade una notificación para eventos de `ObjectCreated` que invoque la función Lambda.
5. **Crear un Topic en SNS**:
   - Añade las suscripciones (por ejemplo, tu correo electrónico).
6. **Agregar variables de entorno** en la Lambda si es necesario (por ejemplo, el ARN del Topic SNS).
7. **Probar la integración**:
   - Sube un archivo al bucket y verifica que llegue el correo de notificación.

---

## 📋 Requisitos

- Cuenta de AWS con acceso a los servicios Lambda, S3 y SNS.
- Permisos suficientes para crear roles de IAM y asignarlos.
- Python 3.8 o superior para el código de la función (en caso de probarlo localmente antes de desplegar).

---

## 📝 Notas

- La Lambda solo se activa con eventos `ObjectCreated` en el bucket S3 configurado.
- La notificación enviada por SNS incluye el nombre del archivo subido.
- Puedes ampliar el comportamiento de la Lambda para realizar otras tareas (procesamiento de archivos, mover datos, etc.).
- Revisa los límites de tamaño para eventos de S3 y SNS.

---

## 📚 Lo que aprendí

- Cómo crear y desplegar una función Lambda en AWS.
- Cómo configurar eventos en un bucket S3 para invocar Lambda automáticamente.
- Cómo integrar Lambda con SNS para enviar notificaciones por correo electrónico.
- Cómo gestionar permisos con IAM para que los servicios se comuniquen de forma segura.

---

## 💻 Código de la función Lambda (Python)

```python
import json
import boto3
import os

sns_client = boto3.client('sns')

def lambda_handler(event, context):
    # Obtiene el nombre del bucket y del objeto desde el evento
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    
    # Crea el mensaje
    message = f"Se ha subido un nuevo archivo al bucket S3.\n\nBucket: {bucket_name}\nArchivo: {object_key}"
    
    # Obtiene el ARN del SNS Topic desde la variable de entorno
    sns_topic_arn = os.environ['SNS_TOPIC_ARN']
    
    # Publica el mensaje en el SNS Topic
    response = sns_client.publish(
        TopicArn=sns_topic_arn,
        Message=message,
        Subject='Nuevo archivo en S3'
    )
    
    # Respuesta de la publicación
    return {
        'statusCode': 200,
        'body': json.dumps('Notificación enviada correctamente.')
    }
