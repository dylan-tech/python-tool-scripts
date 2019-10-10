import wget
import time
import re
from ucloud.client import Client
from getApiCsv import ssh_scp_get
from getSlowLog import gettimestamp, createslowlog, getlogdownloadurl, getslowloglist, getslowlogid, move, uncompresstgz


# API CSV 配置
PORT = 22
USER = 'root'
IP = "107.150.96.108"
PASSWORD = "jqowzohwo!1"

date = time.strftime("%Y%m%d")
api_filename = "/var/log/nginx/api_ec_youmobi_com.access_log-{date}.csv".format(date=date)
local_filename = "C:/Users/Administrator/Desktop/analysis/api_ec_youmobi_com.access_log-{date}.csv".format(date=date)

# api_filename = "/var/log/nginx/api_ec_youmobi_com.access_log-20191009.csv"
# local_filename = "C:/Users/Administrator/Desktop/analysis/api_ec_youmobi_com.access_log-20191009.csv"

# slowlog 配置
REGION = "us-ca"
PROJECT_ID = "org-27257"
PUBLIC_KEY = "1UfzNpviWgrjvICMiho6sS0TEoGlind9/pkkOaN9v2DeQMemvHt1B+Xtyp0="
PRIVATE_KEY = "mm/L+ymhzLoJOGcrUkbzPQPHgN8GifmqY0jzUfGQRNuiYrugX8nH1Xjvv1SHjEnh"
DBID = "udbha-fwvtmj"
ZONE = "us-ca-01"
DIR = "C:/Users/Administrator/Desktop/analysis"

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

