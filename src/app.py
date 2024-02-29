from flask import Flask
from config import config
from flask_cors import CORS
import os

# Importa tu controlador
from routes.email_controller import main as email_blueprint, configure_mail, initialize_mail

app = Flask(__name__)

CORS(app) 

# Configura la extensión Flask-Mail antes de inicializar la aplicación Flask
configure_mail(app)
initialize_mail(app)

# Registra tu blueprint
app.register_blueprint(email_blueprint, url_prefix='/api/email')

def page_not_found(error):
    return "<h1>Not found page</h1>", 404

app.config.from_object(config['development'])

# Obtener la dirección IP de las variables de entorno
ip_address = os.getenv('IP_ADDRESS', '127.0.0.1')  # Usa localhost como valor predeterminado si no se define IP_ADDRESS

# Obtener el puerto de las variables de entorno
port = os.getenv('PORT', 4000)  # Usa el valor predeterminado 4000 si no se define PORT

if __name__ == '__main__':
    app.run(host=ip_address, port=port)

    #Blueprints
    app.register_error_handler(404, page_not_found)
