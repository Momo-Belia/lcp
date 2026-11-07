from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os
from langchain.agents import create_agent

load_dotenv()

model = init_chat_model(
   model="deepseek-flash",
   model_provider = "deepseek",
   api_key=os.getenv("DEEPSEEK_API_KEY"),
   base_url=os.getenv("DEEPSEEK_BASE_URL")
)

agent = create_agent(
    model=model,
    tools=[],
    system_prompt="你是一个可爱的助手"
)

result = agent.invoke({"messages": [{"role": "user", "content":"你好吗"}]})
print(result["messages"][-1].content_blocks)

