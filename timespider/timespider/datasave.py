import pymongo

# 配置数据库信息
MONGO_URl = 'localhost'
MONGO_DB = 'taobao' # 数据库名
MONGO_TABLE = 'iphonex_url' # 表名

# 连接数据库
client = pymongo.MongoClient(MONGO_URl)
db = client[MONGO_DB]

# 存入数据库
def save_url_to_Mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('存储到MongoDB成功', result)
    except Exception:
        print('存储到MongoDb失败', result)
