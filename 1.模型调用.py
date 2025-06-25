import os 
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {'role':'system','content':'你是一个数学高手'},
        {'role':'user','content':'你是谁？'}
    ]
)

print(completion)