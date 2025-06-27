from math import log
from re import A
from shutil import move
import requests

from ... import LogConfig
import sys
from .. import TMdbSettings
sys.path.insert(0, sys.path[0]+"/../")


import PyQt6

Log_Config = LogConfig("MovieIDGetter")
logger = Log_Config.get_logger()


ConfigManager = TMdbSettings()

# class MovieIDGetter():
    
#     def __init__(self,MovieName:str):
#         self.MovieName = MovieName
#         logger.info(self.MovieName)
        
        
class MovieIDGetter():
    """
    用于根据动漫名称获取TMDB（The Movie Database）上的动漫ID。

    该类提供了一个方法 `get_anime`，用于根据输入的动漫名称和TMDB API密钥，
    从TMDB API获取对应的动漫ID。

    Args:
        MovieName (str): 要查询的动漫名称。
        TMDB_API (str): TMDB API密钥，用于身份验证和访问TMDB数据库。

    Attributes:
        MovieName (str): 存储的动漫名称，用于查询TMDB上的对应ID。
        TMDB_API (str): 存储的TMDB API密钥，用于身份验证。

    Methods:
        FetchMovieID() -> int:
            根据动漫名称查询TMDB上的动漫ID。

            返回:
                int: 查询到的动漫ID，如果查询失败或未找到对应ID，则返回None。
    """
    def __init__(self, MovieName: str) -> None:
        self.MovieName = MovieName
        self.config = ConfigManager
        self.TMDBapi = self.config.GetTmdbApi()
        logger.debug(self.TMDBapi)
        self.Lang = self.config.GetLanguage()
        logger.debug(self.Lang)
        url = f'https://api.themoviedb.org/3/search/multi?api_key={self.TMDBapi}&query={self.MovieName}&language={self.Lang}'
        self.url = url
        response = requests.get(self.url)
        response.raise_for_status()
        data = response.json()
        self.data = data
        # print(self.data)
        MovieNameList = []
        MovieTitleList = []
        self.MovieNameList = MovieNameList
        self.MovieTitleList = MovieTitleList

    def FetchMovieNames(self) -> str:
        try:
            if self.data.get('results'):
                for result in self.data['results']:
                    MovieName_ = result.get('name')
                    MovieTitle_ = result.get('title')
                    if MovieName_  is not None:
                        self.MovieNameList.append(MovieName_)
                        logger.debug(f"获取到的节目名称: %s", MovieName_)
                    elif MovieTitle_ is not None:
                        self.MovieTitleList.append(MovieTitle_)
                        logger.debug(f"获取到的电影名称: %s", MovieTitle_)
                    else:
                        logger.warning(f"没获取到名称")
                logger.debug(f"节目列表：%s",self.MovieNameList)
                logger.debug(f"电影列表: %s",self.MovieTitleList)
                logger.info("成功！")
        except Exception as e:
            # 记录异常信息
            logger.error(f"获取动漫名称列表时发生错误: {e}")

    
    def MovieSelect(self) -> str:
        Mode = ("节目","电影")
        SelectMode = 0
        for ModeName in Mode:
            if ModeName != None :
                print(f"{SelectMode}.{ModeName}")
                SelectMode += 1
        ModeID = int(input("请输入你要选择的模式:"))
        logger.debug(f"已选择：%s",Mode[ModeID])

        if ModeID == 0:
            Number = 0
            for MovieName in self.MovieNameList:
                if MovieName != None :
                    print(f"{Number}.{MovieName}")
                    Number += 1
            MovieID = int(input("请输入你要选择的节目号:"))
            MovieID = self.MovieNameList[MovieID]
            logger.info(MovieID)
            return MovieID
        elif ModeID == 1:
            Number = 0
            for MovieName in self.MovieTitleList:
                if MovieName != None :
                    print(f"{Number}.{MovieName}")
                    Number += 1
            MovieID = int(input("请输入你要选择的电影号:"))
            MovieID = self.MovieTitleList[MovieID]
            logger.info(MovieID)
        
    def FetchMovieID(self) -> str:
        """
        根据动漫名称获取动漫对应的id值
        - 输入:
            - MovieName:动漫名称（通过初始化传入）
            - TMDB_API: TMDB_API密钥（通过初始化传入）
        - 输出：
            - tv_id:查询到的tv_id，如果查询失败或未找到对应ID，则返回None。
        """
        try:
            if self.data.get('results'): 
                tv_id = self.data['results'][0].get('id')
                logger.info(f"找到{self.MovieName}的ID: %s", tv_id)
                return tv_id
            else:
                logger.warning(f"没有找到{self.MovieName}的ID")
                return None
        except requests.RequestException as e:
            logger.error("API请求失败: %s", e)
            return None
