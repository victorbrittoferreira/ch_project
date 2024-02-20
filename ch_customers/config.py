from os.path import join, dirname
import environ

dotenv_path = join(dirname(dirname(__file__)), '.env')

class EnvConfig:
    env = environ.Env()
    environ.Env.read_env(dotenv_path)

    @staticmethod
    def get_secret_key() -> str:
        return EnvConfig.env('SECRET_KEY')

    @staticmethod
    def get_debug() -> bool:
        return EnvConfig.env.bool('DEBUG', default=False)
    
    @staticmethod
    def get_db_port() -> int:
        return EnvConfig.env.int('DB_PORT')

    @staticmethod
    def get_db_host() -> str:
        return EnvConfig.env('DB_HOST')
    
    @staticmethod
    def get_db_name() -> str:
        return EnvConfig.env('DB_NAME')
    
    @staticmethod
    def get_db_user() -> str:
        return EnvConfig.env('DB_USER')
    
    @staticmethod
    def get_db_password() -> str:
        return EnvConfig.env('DB_PASSWORD')
    
    @staticmethod
    def get_celery_broker_url() -> str:
        return EnvConfig.env('CELERY_BROKER_URL')