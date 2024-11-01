import logging
import os
from datetime import datetime
import pytz  # Biblioteca para lidar com fusos horários

# Verifica se a pasta de logs existe, senão cria
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configuração do timezone para o Brasil (Horário de Brasília)
fuso_horario_brasilia = pytz.timezone("America/Sao_Paulo")

# Customizando a formatação de data/hora no estilo brasileiro
class TimezoneFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        # Converte o tempo do log para o fuso horário de Brasília e formata no padrão brasileiro
        dt = datetime.fromtimestamp(record.created, fuso_horario_brasilia)
        return dt.strftime("%d/%m/%Y %H:%M:%S")

# Configuração do logging com a formatação personalizada
formatter = TimezoneFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Configurando o logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Configurando o arquivo de log
file_handler = logging.FileHandler('logs/app.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def registrar_log(mensagem, nivel='info'):
    if nivel == 'info':
        logger.info(mensagem)
    elif nivel == 'error':
        logger.error(mensagem)
    elif nivel == 'warning':
        logger.warning(mensagem)
