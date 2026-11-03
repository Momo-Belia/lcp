import requests
import os
def get_weather(city:str):
    key = os.getenv("OPENWEATHER_API_KEY")
    if not key:
        raise ValueError("环境变量 WEATHER_KEY 未设置")

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q":city,
        "appid":key, 
        "units": "metric",
        "lang": "zh_cn"  
    }
    resp = requests.get(url,params=params)
    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            desc = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            return f"{city} 当前天气：{desc}，气温 {temp}°C，体感 {feels_like}°C，湿度 {humidity}%。"
        elif resp.status_code == 404:
            return f"未找到城市“{city}”的天气数据，请检查城市名称。"
        else:
            return f"天气查询失败，HTTP 状态码：{resp.status_code}"
    except requests.RequestException as e:
        return f"请求天气服务时出错：{e}"

city = input("pleast type city name: ")

response = get_weather(city)

print(response)