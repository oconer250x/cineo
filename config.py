class Config:
    SECRET_KEY = 'OCONERELFUKINCRACK250XD'
    DEBUG = True 

class DevelopmentConfig(Config):
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'cineo'

config = {
    'development': DevelopmentConfig

}