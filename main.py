from core import *


log_config = LogConfig("main")
logger = log_config.get_logger()

if __name__ == "__main__":
    tmdb_settings = TMdbSettings() 
    tmdb_api = tmdb_settings.GetTmdbApi()
    language = tmdb_settings.GetLanguage()
    anime_getter = MovieIDGetter(MovieName="名侦探柯南")
    b = anime_getter.FetchMovieNames()
    a = anime_getter.FetchMovieID()
    c = anime_getter.MovieSelect()



