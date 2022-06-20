import pymysql
from module.config import config
from module.logger import *

# 连接数据库
db = pymysql.connect(
        host=config["db_host"],
        user=config["db_user"],
        password=config["db_password"],
        database=config["database"]
)
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
logger.debug("数据库版本 : %s " % data)


async def sql_run(sql=None):
    try:
        # 执行sql语句
        if sql is not None:
            cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        logger.info("[数据库]命令执行成功~")
        return 0
    except:
        # 如果发生错误则回滚
        db.rollback()
        logger.error("[数据库]数据库发生错误，执行失败")
        return -1

# 创建数据表
if cursor.execute("show tables") != 6:
    logger.error("数据表丢失，正在修复")
    create_tables = """CREATE TABLE IF NOT EXISTS whitelist (
        id float(5) PRIMARY KEY AUTO_INCREMENT,
        QQ char(16) UNIQUE not null,
        player_name char(16) UNIQUE not null
    );
    CREATE TABLE IF NOT EXISTS wait(
        id float(5) PRIMARY KEY AUTO_INCREMENT,
        QQ char(16) UNIQUE not null,
        player_name char(20) UNIQUE not null,
        pass boolean,
        pass_info char(50) 
    );
    CREATE TABLE IF NOT EXISTS banlist(
        player_name char(16) UNIQUE not null,
        reason char(30)
    );
    CREATE TABLE IF NOT EXISTS usedbot(
        id float(5) PRIMARY KEY AUTO_INCREMENT,
        QQ char(16) not null,
        bot_name char(20) UNIQUE not null,
        isused boolean not null,
        purpose char(30) not null
        time DATETIME not null DEFAULT NOW()
    );"""
    cursor.execute(create_tables)
    db.commit()
    logger.debug("数据表创建完成")