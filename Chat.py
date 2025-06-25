import json
from my_logger import MyLogger
from db_init import MySQLCRUD
import os
from openai import OpenAI

log=MyLogger().logger
db = MySQLCRUD()

def query_from_db(project_id:str):
    '''
    从数据库获取工程信息
    '''
    log.info(f"查询工程信息，工程ID：{project_id}")
    res = db.read(f"SELECT * FROM flask_db.projects WHERE project_id='{project_id}'")
    if res:
        log.info(f"查询成功，工程信息：{res[0]}")
        return res[0]
    else:
        return None

def query_from_knowledge_base(kws:list):
    '''
    从知识库获取相关信息
    '''
    # mock_from_ragflow()
    return "mock_from_ragflow"

tools={
    "query_from_db":query_from_db,
    "query_from_knowledge_base":query_from_knowledge_base,
}


class LLM_predict:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"),
                             base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
        log.info("初始化LLM模型")

    def _get_tool_definition(self):
        '''
        定义工具功能
        '''
        tool_definitions = []

        tool_definitions.append({
            "type":"function",
            "function":{
                "name":"query_from_db",
                "description":"公司内部数据库获取工程项目的结构化信息，如项目名称、高度、材料、地点、截止日期等。需要提供工程的唯一标识ID（如塔号、工程编号）。",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "project_id":{
                            "type":"string",
                            "description":"工程唯一标识，如N23，P34等"
                        }
                    },
                    "required":["project_id"]
                },
            },
        })

        tool_definitions.append({
            "type": "function",
            "function": {
                "name": "query_from_knowledge_base",
                "description": "从私有知识库（RAG系统）中检索与用户查询相关的非结构化文本信息，如施工规范、安全协议、历史施工方案、技术文档、物料清单、机械设备要求等。需要提供具体的关键词列表以提高检索精度。",
                "parameters": { # 这里的键名是 "parameters"，而不是 "input_params"
                    "type": "object",
                    "properties": {
                        "kws": {
                            "type": "array",
                            "items": {"type": "string"}, # 列表元素的类型是字符串
                            "description": "用于知识库检索的关键词列表，例如：['高空作业安全', '塔吊安装', '混凝土浇筑规范', 'A项目方案']。"
                        }
                    },
                    "required": ["kws"] # 必须包含此参数
                }
            },
        })
        return tool_definitions
    
    def predict(self, msg:list):
        my_tools = self._get_tool_definition()

        try:
            completion = self.client.chat.completions.create(
                model='qwen-plus',
                messages=msg,
                tools=my_tools,
                tool_choice='auto'
            )

            response_msg = completion.choices[0].message
            return response_msg

        except:
            pass


    
if __name__ == '__main__':
    llm = LLM_predict()
    messages_1 = [{"role": "user", "content": "请帮我查询N12工程的基本信息。"}]

    response_1 = llm.predict(messages_1)
    print(f"\nLLM 响应: {response_1}")