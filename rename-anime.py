import requests
from guessit import guessit
import os
import re
import shutil


# 获取动漫id
def get_anime(dir_path: str, api: str) -> int:
    """
    根据动漫文件夹的名称获取动漫对应的id值
    - 输入:
        - dir_name:动漫文件夹的绝对路径
        - api: api密钥
    - 输出：
        - 动漫id
    """
    url = f'https://api.themoviedb.org/3/search/multi?api_key={api}&query={os.path.basename(dir_path)}'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    if data.get('results'):
            # 打印完整的搜索结果，用于调试
        tv_id = data['results'][0].get('id')
            # 打印完整的搜索结果，用于调试
        print(f"找到的TV节目的ID: {tv_id}")
        return tv_id


# 遍历文件夹
def traverse_the_folder(dir_path: str) -> list:
    """
    根据输入的动漫文件夹路径，获取其中每个动漫视频的剧集信息
    - 输入：
        - dir_path:动漫文件夹路径
    - 输出：
        - 一个列表，里面包含每一个动漫视频的剧集信息字典
            - 字典的键为'file_name','season','episode'
    """
    list_file = []
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        for file_name in os.listdir(dir_path):
            if not os.path.isdir(file_name):
                # 检查文件是否为视频文件
                if file_name.endswith(('.mp4', '.mkv', '.avi', '.mov','.ass','.srt','.txt')):
                    print(f"找到视频文件: {file_name}")
                    list_file.append(
                        {
                            'file_name': file_name ,
                            'season': guessit(file_name).pop('season', None),
                            'episode': guessit(file_name).pop('episode', None)
                        }
                )
    return list_file

# 获取剧集名称
def get_episode_name(api: str, get_tvid: int, list_file: list, language: str = 'zh-CN') -> list:
    '''
    根据输入的动漫id和剧集信息列表，获取每个视频文件对应的剧集名称
    - 输入：
        - api: api密钥
        - get_tvid: 动漫id
        - list_file:一个列表，里面包含每一个动漫视频的剧集信息字典
            - 字典的键为'file_name','season','episode'
        - language: 语言
    - 输出：
        - 一个列表，里面包含每一个动漫视频的剧集信息字典
            - 字典的键为'file_name','season','episode'
    '''
    list_episode_data = []
    for file in list_file:
        try:
            url = f'https://api.themoviedb.org/3/tv/{get_tvid}/season/{file['season']}/episode/{file['episode']}?api_key={api}&language={language}'
            episode_response = requests.get(url)
            episode_response.raise_for_status()
            episode_data = episode_response.json()
            file['file_name'] = episode_data.get('name')
            list_episode_data.append(file)
            if file['file_name']:
                print(f"这一集的 {language} 名字是: {file['file_name']}")
        except requests.RequestException as e:
            print(f"请求集信息出错: {e}")
    return list_episode_data

# 创建文件夹
def Create_folders(dir_path: str, list_episode_data: str):
    # 创建目录
    for file in list_episode_data:
        # 检查是否存在Special目录，如果不存在则创建
        if os.path.exists(dir_path+"/Special") == False :
            # 检查季数是否为0，如果是则创建Special目录
            if file['season'] == 00:
                # 创建Special目录
                if not os.path.exists(os.path.join(dir_path, "Special")):
                    os.mkdir(os.path.join(dir_path, "Special"))
                print(f"已创建目录: Special")    
        # 检查季数是否大于等于1，如果是则创建Season目录 
        if file['season'] <= 1:
            # 创建Season目录
            if not os.path.exists(os.path.join(dir_path, f"Season {file['season']:02d}")):
                os.mkdir(os.path.join(dir_path, f"Season {file['season']:02d}"))
                print(f"已创建目录: Season {file['season']:02d}")  
    return print("创建完成"),
    
def Move_Reanme_Episode_FileName(dir_path: str, list_episode_data: str):
    '''
    根据输入的动漫文件夹路径和剧集信息列表，对每个视频文件进行重命名
    - 输入：
        - dir_path:动漫文件夹路径
        - list_episode_data:一个列表，里面包含每一个动漫视频的剧集信息字典
            - 字典的键为'file_name','season','episode'
    - 输出：
        - 无
    '''
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
       list_file_name = [file_name for file_name in os.listdir(dir_path)]
       # 确保索引不越界，取两列表长度的最小值
       
       for i in range(min(len(list_file_name), len(list_episode_data))):
           # 检查当前索引是否有效
           if i >= len(list_episode_data):
               print(f"警告：list_episode_data中缺少第{i+1}项数据，跳过文件{list_file_name[i]}")
               continue
           # 用正则表达式替换非法字符
           episode_name = re.sub(r'[\\/:*?"<>|]', '', list_episode_data[i]['file_name'])
           # 构建新文件名
           new_filename = f"S{list_episode_data[i]['season']:02d}E{list_episode_data[i]['episode']:02d}-{episode_name}{os.path.splitext(list_episode_data[i]['file_name'])[1]}"
           # 构建新文件路径,不包含后缀名
           new_file_path = os.path.join(dir_path, new_filename)
        # 确保新文件名使用原文件的后缀名
           original_ext = os.path.splitext(list_file_name[i])[1]
           # 构建新文件路径，使用原文件的后缀名
           new_filename_with_ext = os.path.splitext(new_file_path)[0] + original_ext
           # 新的文件路径，包含正确的后缀名
           new_file_path_with_correct_ext = os.path.join(dir_path, new_filename_with_ext)
           # 重命名文件
           os.rename(os.path.join(dir_path, list_file_name[i]), new_file_path_with_correct_ext)
           print(f"文件 {list_file_name[i]} 重命名为 {new_filename}")
           # 将季数为0的文件移动到Special目录中
           if list_episode_data[i]['season'] == 0 :
                # 移动文件到Special目录中
                # shutil.move(源文件路径, 目标文件路径)
                 # os.path.join(目录拼接：目录名，文件名)
                shutil.move(new_file_path_with_correct_ext, os.path.join(dir_path,"Special") )
                print(f"已将文件 {new_filename} 移动到 Special 目录中")
        # 将季数大于等于1的文件移动到Season目录中
           elif list_episode_data[i]['season'] >= 1 :
                # 移动文件到Special目录中
                # shutil.move(源文件路径, 目标文件路径)
                # os.path.join(目录拼接：目录名，文件名)
                shutil.move(new_file_path_with_correct_ext,os.path.join(dir_path,f"Season {list_episode_data[i]['season']:02d}"))
                print(f"已将文件 {new_filename} 移动到 Season {list_episode_data[i]['season']:02d} 目录中")

    return print("重命名完成"),


# 主函数
def main():
    # 输入文件路径
    dir_path = r"D:\Movie\紫云寺家的兄弟姐妹"
    # api密钥
    api = "32731ff2961c65563b06e4b87654a0b2"
    #获取动漫id
    get_tvid = get_anime(dir_path, api)
    # 获取每个视频文件的剧集信息
    list_file = traverse_the_folder(dir_path)
    # 获取每个视频文件的剧集名称
    list_episode_data = get_episode_name(api, get_tvid, list_file)
   # 创建文件夹
    Create_folders(dir_path, list_episode_data)
    # 重命名文件
    Move_Reanme_Episode_FileName(dir_path, list_episode_data)
    # 输出
    print("完成")

# 主函数
if __name__ == "__main__":
    main()

