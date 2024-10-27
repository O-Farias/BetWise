import logging
import os

# Verifica se a pasta de logs existe, senão cria
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configuração básica do logging
logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def registrar_log(mensagem, nivel='info'):
    if nivel == 'info':
        logging.info(mensagem)
    elif nivel == 'error':
        logging.error(mensagem)
    elif nivel == 'warning':
        logging.warning(mensagem)
