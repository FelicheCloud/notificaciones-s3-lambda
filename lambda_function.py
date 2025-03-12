import json
import boto3

def lambda_handler(event, context):
    sns_client = boto3.client('sns')
    
    # Extraer datos del evento de S3
    s3_event = event['Records'][0]
    bucket_name = s3_event['s3']['bucket']['name']
    object_key = s3_event['s3']['object']['key']
    
    # Mensaje a enviar
    mensaje = f"Se ha subido un nuevo archivo al bucket {bucket_name}.\nArchivo: {object_key}"
    
    # Aquí pegamos el Topic ARN que encontraste
    topic_arn = 'arn:aws:sns:us-east-1:535002863608:NotificacionesFeliche'
    
    # Publica el mensaje en el topic SNS
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
