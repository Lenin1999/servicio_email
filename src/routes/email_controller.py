from flask import Blueprint, request, jsonify, current_app
from flask_mail import Mail, Message
import openai
from dotenv import load_dotenv
import os

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Define tu blueprint
main = Blueprint('main', __name__)

# Configura la API de OpenAI
api_key = os.getenv('OPENAI_API_KEY')

# Configura Flask-Mail
mail = Mail()

# Función para inicializar la extensión Flask-Mail con la aplicación Flask
def initialize_mail(app):
    mail.init_app(app)

# Configuración del correo electrónico
def configure_mail(app):
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', '587'))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

# Ruta para generar el reporte
@main.route('/reporte', methods=['POST'])
def generar_reporte():
    # Obtener datos de la solicitud 
    data = request.json
    
    paciente = data["paciente"]["nombre"]
    email = data["paciente"]["email"]
      # Tomando la fecha del primer resultado, podría ser diferente dependiendo del contexto
    
    prompt = (
        "Obtuve estos resultados después de realizar un análisis de tuberculosis en la fecha de cada examen como esta en los datos " 
        " Es un examen pulmonar con radiografías de tórax utilizando un modelo de CNN al paciente " + str(paciente) +
        
        " Datos obtenidos: " + str(data) + " Realizame un reporte que contenga: " +
        " Nombre paciente " +
        " Análisis de resultados con fechas " +
        " Dame algun analisis de los resultados detallando un poco pero no recomendaciones"
    )



    # Llamar a la API de OpenAI para generar texto
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
      
    )

    generated_text = response['choices'][0]['message']['content']
    print(generated_text)

    # Enviar el mensaje por correo electrónico
    msg = Message('Reporte de OpenAI', sender=current_app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = f'Hola {paciente},\n\nAquí está el reporte generado por OpenAI:\n\n{generated_text}'
    mail.send(msg)

    return jsonify({'generated_text': generated_text})
