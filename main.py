from langchain.agents import create_agent,AgentState
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.utils.uuid import uuid7
from pydantic import BaseModel
import os
import requests

load_dotenv()


def get_current_weather(city: str) -> str:
    """
    获取指定城市的实时天气。
    
    Args:
        city: 城市名称，建议带国家代码以提高准确性，例如 "Beijing,CN" 或 "London,UK"。
    
    Returns:
        一句话描述当前天气和温度；如果查询失败，返回错误提示。
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "错误：未配置 OPENWEATHER_API_KEY 环境变量。"
    
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "zh_cn"      
    }
    
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
    
class Weather(BaseModel):
    desc:str
    temp:float
    feels_like:str
    humidity:int

class MyState(AgentState):
    user_id:str

agent = create_agent(
    model="deepseek:deepseek-v4-flash",
    tools=[get_current_weather],
    system_prompt="你是一名乐于助人的助手",
    checkpointer=InMemorySaver()

)
config = {"configurable": {"thread_id": str(uuid7())}}

while True:
    print("1--new chat\n2--continue chat\n3--exit")
    if input()=="1":
        city = input("请输入城市名称：")

        result = agent.invoke(
            {"messages": [{"role": "user", "content": f"{city} 天气怎么样？"}]},
            config=config
        )
        print(result["messages"][-1].content)
        continue
    
    elif input()=="2":
        question = input("还想问...：")
        result = agent.invoke(
            {"messages": [{"role": "user", "content": f"{question}"}]},
            config=config
        )
        print(result["messages"][-1].content)
        continue

    elif input()=="3":
        break 
    else:
        print("invalid input")
        continue