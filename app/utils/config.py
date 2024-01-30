from starlette.config import Config

from dotenv import load_dotenv

load_dotenv()
config = Config(".env")

REDIS_HOST = config('REDIS_HOST', str, '0.0.0.0')
REDIS_PORT = config('REDIS_PORT', int, 6379)
REDIS_DB = config('REDIS_DB', int, 0)
REDIS_KEY_PREFIX = config('REDIS_KEY_PREFIX', str, 'fastapi_pydiator:')

DISTRIBUTED_CACHE_IS_ENABLED = config("DISTRIBUTED_CACHE_IS_ENABLED", bool, True)
CACHE_PIPELINE_IS_ENABLED = config("CACHE_PIPELINE_IS_ENABLED", bool, False)
LOG_PIPELINE_IS_ENABLED = config("LOG_PIPELINE_IS_ENABLED", bool, True)


