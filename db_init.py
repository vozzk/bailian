import pymysql
import json
import pymysql.cursors

class MySQLCRUD:
    def __init__(self):
        self.connection = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='697925',
            port=3306,
            db='test',
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor
        )
        # self.connection = pymysql.connect(
        #     host='172.16.200.236',
        #     user='ovit_sdxl',
        #     password='ovit_sdxl',
        #     port=23307,
        #     db='ovit_web3d_test',
        #     charset='utf8',
        #     cursorclass=pymysql.cursors.DictCursor
        # )
        self.cursor = self.connection.cursor()


    def create(self, query, data):
        self.cursor.execute(query, data)
        self.connection.commit()

    def read(self, query, data=None):
        self.cursor.execute(query, data)
        return self.cursor.fetchall()

    def update(self, query, data):
        self.cursor.execute(query, data)
        self.connection.commit()

    def delete(self, query, data):
        self.cursor.execute(query, data)
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()

if __name__ == "__main__":
    db = MySQLCRUD()
    # typename = db.read("SELECT distinct typename FROM gim_pkgt_mod_attr_dtl where modtype='wire'")
    # print(typename)
    # 用于存储所有提取到的 'type' 值的列表
    all_type_values = [] 

    try:
        # 读取数据
        modtype_results = db.read("SELECT pub_attr FROM gim_pkgt_mod_attr_dtl where typename='灌注桩单桩基础'")
        
        # 遍历查询结果
        for row_dict in modtype_results:
            json_string_data = row_dict['pub_attr']
            
            try:
                # 将 JSON 字符串解析成 Python 字典
                parsed_json = json.loads(json_string_data)
                
                # 提取 'type' 字段的 'value'
                if 'type' in parsed_json and 'value' in parsed_json['type']:
                    type_value = parsed_json['type']['value']
                    all_type_values.append(type_value) # 将提取到的值添加到列表中
                else:
                    print("JSON 数据中未找到 'type' 或其内部的 'value' 字段。")
            except json.JSONDecodeError as e:
                print(f"解析 JSON 字符串失败: {e}. 原始字符串: {json_string_data}")
            except KeyError as e:
                print(f"尝试访问 JSON 数据的键错误: {e}. 确保键存在。")

        # 对收集到的所有 'type' 值进行去重
        # 先转换为 set 自动去重，再转换回 list
        unique_type_values = list(set(all_type_values))
        
        print("所有唯一的 'type' 值为:")
        # for val in unique_type_values:
        #     print(val)
        print(unique_type_values)
    except pymysql.Error as e:
        print(f"数据库操作错误: {e}")
    finally:
        db.close()