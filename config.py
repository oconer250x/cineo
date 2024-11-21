class Config:
    SECRET_KEY = 'OCONERELFUKINCRACK250XD'
    DEBUG = True 

class DevelopmentConfig(Config):
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'mysql'
    MYSQL_DB = 'cineo'


    #pythonanywhere
    '''MYSQL_HOST = 'cineo.mysql.pythonanywhere-services.com'
    MYSQL_USER = 'cineo'
    MYSQL_PASSWORD = 'oconerelcrack'
    MYSQL_DB = 'cineo$cineo' '''

class MailConfig(Config):
    MAIL_SERVER         = 'smto.gmail.com'
    MAIL_PORT           = 587
    MAIL_USE_TLS        = True
    MAIL_USE_SSL        = False
    MAIL_USENAME        = 'mateo.bermejo5809@alumnos.udg.mx'
    MAIL_PASSWORD       = 'yzcd mlwq jhiz njxj'
    MAIL_ASCII_ATTACHMENTS = True
    MAIL_DEFAULT_SENDER = 'mateo.bermejo5809@alumnos.udg.mx'

config = {
    'development': DevelopmentConfig,
    'mail'       : MailConfig

}