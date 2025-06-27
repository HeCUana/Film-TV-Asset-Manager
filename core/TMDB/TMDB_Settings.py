import json

from .. import LogConfig


log_config = LogConfig("TMdb_Settings")
logger = log_config.get_logger()

class TMdbSettings():
    ''' 
    用于配置TMDB的API密钥和语言
    '''
    def __init__(self) -> None:
        self.config = json.load(open('config.json'))
        self.TMDB_API = self.config['TMDB']['TMDB_API']
        self.language = self.config['TMDB']['language']

    def GetTmdbApi(self):
        if self.TMDB_API == "Tmdb_Api_Key":
            logger.error(f"TMDB_API is not set {self.TMDB_API}")
        else :
            logger.info(f"TMDB_API is set to {self.TMDB_API}")
            return self.TMDB_API

    def GetLanguage(self):
        if self.language == "Language":
            logger.error(f"Language is not set {self.language}")
        else:
            logger.info(f"Language is set to {self.language}")
            return self.language

