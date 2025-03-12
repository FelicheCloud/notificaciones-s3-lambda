# Notificaciones Automáticas de Subidas a S3 con AWS Lambda y SNS

Este proyecto implementa una función Lambda en AWS que envía notificaciones por correo electrónico cada vez que se sube un archivo a un bucket de Amazon S3.

## 📌 Arquitectura

1. **Amazon S3**:
   - Bucket: `felicheprueba`
   - Evento: Cuando se sube un archivo (PutObject)

2. **AWS Lambda**:
   - Función: `Feliche-notificacion-subida-s3`
   - Runtime: Python 3.12
   - Se activa cuando S3 recibe un nuevo archivo.
   - Extrae el nombre del archivo y el bucket.

3. **Amazon SNS**:
   - Topic: `NotificacionesFeliche`
   - Envía un correo electrónico de notificación al destinatario suscrito.

---

## ⚙️ Cómo funciona

1. Se sube un archivo al bucket `felicheprueba`.
2. S3 activa la función Lambda `Feliche-notificacion-subida-s3`.
3. Lambda genera un mensaje con el nombre del bucket y el archivo subido.
4. Lambda publica el mensaje en el topic SNS `NotificacionesFeliche`.
5. SNS envía una notificación al correo electrónico suscrito.

---

## 💻 Código Lambda (Python)

```python
import json
import boto3

def lambda_handler(event, context):
    sns_client = boto3.client('sns')
    
    s3_event = event['Records'][0]
    bucket_name = s3_event['s3']['bucket']['name']
    object_key = s3_event['s3']['object']['key']
    
    mensaje = f"Se ha subido un nuevo archivo al bucket {bucket_name}.\nArchivo: {object_key}"
    
    topic_arn = 'arn:aws:sns:us-east-1:535002863608:NotificacionesFeliche'
    
    response = sns_client.publish(
        TopicArn=topic_arn,
        Subject='Notificación de subida a S3',
        Message=mensaje
    )
    
    print(f"Mensaje enviado: {mensaje}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Notificación enviada correctamente')
    }
