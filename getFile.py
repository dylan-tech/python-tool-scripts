import datetime
import re
import time
import wget
from ucloud.client import Client
from getApiCsv import ssh_scp_get
from getSlowLog import gettimestamp, createslowlog, getlogdownloadurl, getslowloglist, getslowlogid, move, uncompresstgz
from dingding import ding_text



DOAMIN = "xxx"          # 访问域名，IP亦可
DATE = datetime.datetime.date(datetime.datetime.now())

# dingding api
ding_api = "xxx"        # 钉钉群机器人webhook

# API CSV 配置
PORT = 22
USER = 'root'
IP = "xxx"              # api文件所在服务器IP
PASSWORD = "xxx"        

date = time.strftime("%Y%m%d")
api_filename = "XXX/xxx{date}.csv".format(date=date)         # api源路径
local_filename = "XXX/xxx{date}.csv".format(date=date)       # 保存的路径


# slowlog 配置
REGION = "XXX"          # 所在地区
PROJECT_ID = "XXX"      # 项目ID， 可以通过Ucloud UAPI示例代码查询
PUBLIC_KEY = "xxx"      # ucloud api 公钥
PRIVATE_KEY = "xxx"     # ucloud api 私钥
DBID = "xxx"            # UDB 资源Id
ZONE = "xxx"            # 所有区域
DIR = "xxx"             # 目标保存位置 

# 获取api csv
try:
    print("正在获取今天api csv文件")
    ssh_scp_get(ip=IP, port=PORT, user=USER, password=PASSWORD, remote_file=api_filename, local_file=local_filename)
except Exception as e:
    print(e)
else:
    print("api csv文件已保存")

# 获取slowlog
try:
    print("开始执行slowlog日志打包下载")
    client = Client({
            "region": REGION,
            "project_id": PROJECT_ID,
            "public_key": PUBLIC_KEY,
            "private_key": PRIVATE_KEY,
        })

    START_TIME, END_TIME = gettimestamp()
    LOG_NAME = "slowlog-{}.log".format(date)

    createslowlog(client, db_id=DBID, start_time=START_TIME, finish_time=END_TIME, log_name=LOG_NAME)
    resp = getslowloglist(client, zone=ZONE, offset=0, limit=50, log_type=None)
    package_id = getslowlogid(resp, backup_name=LOG_NAME, db_id=DBID)
    url = getlogdownloadurl(client, zone=ZONE, db_id=DBID, backup_id=package_id)
    time.sleep(5)
    wget.download(url)
    downloaded_filename = re.split(r'[/?]', url)[4]
    uncompresstgz(downloaded_filename)
    move(downloaded_filename, dst=DIR, new_name="ymcore-slowlog-{}.log".format(date))
except Exception as e:
    print(e)
else:
    print("下载当天slowlog日志成功")
    
    
# 发送链接到钉钉群
api_download_url = "http://{domain}/api/api_ec_youmobi_com.access_log-{date}.csv".format(domain=DOMAIN, date=date)
slow_download_url = "http://{domain}/slow/ymcore-slowlog-{date}.log".format(domain=DOMAIN, date=date)
content = "{DATE} api csv文件: \n{api_url}\n{DATE} slowlog文件: \n{slow_url}".format(DATE=DATE, api_url=api_download_url, slow_url=slow_download_url)
ding_text(ding_api, content)

