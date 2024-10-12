import requests
from json import dumps as jsonDumps
import time
import json
import os

address = os.environ['QINGLONG_URL']
env_api="/open/envs"
# 获取token的api
get_token_api="/open/auth/token"
# 启用变量
enable_env="/open/envs/enable"




 
def login(address, client_id, client_secret):
    print("开始获取token")
    url = f"{address}{get_token_api}"
    response = requests.get(url, params={"client_id": client_id, "client_secret": client_secret})
    print(response.text)
    response = response.json()
    if response["code"] != 200:
        print("获取token失败")
        return
    token = response["data"]["token"]
    return token;

 
def update_env(token, data):
    url = f"{address}{env_api}"

    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}'
    }

  # 获取当前时间戳
    timestamp = int(time.time() * 1000)

  # 将时间戳添加到 URL 中
    url = f"{url}?t={timestamp}"

    response = requests.put(url, json=data, headers=headers)

    if response.status_code == 200:
        print("环境变量更新成功！")
        print(response.text)
    else:
        print("环境变量更新失败！")
        print(f"状态码: {response.status_code}")
        print(response.text)


def extract_pt_key_pt_pin(cookie_string):
  """
  从 cookie 字符串中提取 pt_key 和 pt_pin 的值，并以指定格式输出。

  Args:
    cookie_string: cookie 字符串。

  Returns:
    包含 pt_key 和 pt_pin 的字符串，格式为 "pt_key=xxx;pt_pin=yyy;"。
  """

  pt_key = None
  pt_pin = None

  for part in cookie_string.split(';'):
    if 'pt_key=' in part:
      pt_key = part.split('=')[1]
    if 'pt_pin=' in part:
      pt_pin = part.split('=')[1]

  return f"pt_key={pt_key};pt_pin={pt_pin};"



def get_token():
    client_id = os.environ['CLIENT_ID'] 
    client_secret = os.environ['CLIENT_SECRET'] 
    return login(address, client_id, client_secret)


def update_cookie(jd_cookie):
    token= get_token()
    update_env(token, jd_cookie)

def update_jd_cookie(cookie_string,id):
    jdhucookie=extract_pt_key_pt_pin(cookie_string)
    jd_cookie ={
    "name": "JD_COOKIE",
    "value": jdhucookie,
    "id": id
    }
    update_cookie(jd_cookie)
    enable_envs(id)
    return "更新成功"


# 仅通过cookie更新jd_cookie
def update_jd_cookie_only_by_cookie(cookie_string):
    id=get_envid_by_cookstring(cookie_string)
    if id is None:
        return "不存在该cookie,请先添加"
    return update_jd_cookie(cookie_string,id)

def get_pin_by_cookie(cookie_string):
     pt_pin = None
     for part in cookie_string.split(';'):
        if 'pt_pin=' in part:
            pt_pin = part.split('=')[1]

     return pt_pin

# 通过cookie获取envid
def get_envid_by_cookstring(cookie_string):
    pin=get_pin_by_cookie(cookie_string)
    if pin is None:
        return None
    return get_envid_by_pin(pin)

# 启用环境变量
def enable_envs(id):
    url = f"{address}{enable_env}"
    token=get_token()

    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}'
    }
    data=[id]
  # 获取当前时间戳
    timestamp = int(time.time() * 1000)

  # 将时间戳添加到 URL 中
    url = f"{url}?t={timestamp}"

    response = requests.put(url, json=data, headers=headers)
    print(response.text)

def get_envid_by_pin(pin):
    token=get_token()

    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}'
    }
    # 获取当前时间戳
    timestamp = int(time.time() * 1000)
    url = f"{address}{env_api}?t={timestamp}"
    response = requests.get(url, params={"searchValue": pin},headers=headers)
    json_data = response.json()
    id_list=json_data['data']
    if len(id_list)==0:
        return None
    else:
        return id_list[0]['id']

#添加jd_cookie
""" 
1,检查之前是否有这个jd_cookie
2,如果没有则添加
""" 
def add_jd_cookie(cookie_string):
    id=get_envid_by_cookstring(cookie_string)
    if id is not None:
        return "已经存在"
    else:
        jdhucookie=extract_pt_key_pt_pin(cookie_string)
        add_envs(jdhucookie)
        return "添加成功"



# 添加环境变量
def add_envs(data):
    token=get_token()
     # 获取当前时间戳
    timestamp = int(time.time() * 1000)
    url = f"{address}{env_api}?t{timestamp}"
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}'
    }
    env_value=[{
        "value":data,
        "name":"JD_COOKIE"
    }]
    response = requests.post(url, json=env_value, headers=headers)
    print(response.text)

