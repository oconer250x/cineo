class Config:
    SECRET_KEY = 'OCONERELFUKINCRACK250XD'
    DEBUG = True 

class DevelopmentConfig(Config):
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'mysql'
    MYSQL_DB = 'cineo'

        #pythonanywhere
        MYSQL_HOST = 'localhost'
        MYSQL_USER = 'root'
        MYSQL_PASSWORD = 'oconerelcrack'
        MYSQL_DB = 'cineo$cineo'

config = {
    'development': DevelopmentConfig

}