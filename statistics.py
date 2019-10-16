#!/usr/bin/python3.6
import re
import csv
import argparse
import datetime


parser = argparse.ArgumentParser()
parser.add_argument("--file", "-f", help="日志文件")
parser.add_argument("--start", "-s", help="指定开始时间段", default=0)
parser.add_argument("--end", "-e", help="指定结束时间段", default=24)

args = parser.parse_args()
logfile = args.file
start_time = int(args.start)
end_time = int(args.end)
infos = {}


def averageTime(time_list):
    sum = 0
    for i in time_list:
        sum += float(i)
    return round(sum / len(time_list), 5)


def timeIndex(time_list):
    time_index = {
        "less_than_a_second": 0,
        "between_one_to_two": 0,
        "between_two_to_three": 0,
        "between_three_to_five": 0,
        "more_than_five":0
    }
    for i in time_list:
        if float(i) < 1:
            time_index["less_than_a_second"] += 1
        elif float(i) < 2:
            time_index["between_one_to_two"] += 1
        elif float(i) < 3:
            time_index["between_two_to_three"] += 1
        elif float(i) < 5:
            time_index["between_three_to_five"] += 1
        else:
            time_index["more_than_five"] += 1
    return time_index


with open(logfile, 'r') as f:
    lines = f.readlines()


for line in lines:
    hour = line.split(":")[1]
    if start_time > int(hour) or end_time < int(hour):
        continue

    uri_string = line.split()[6]
    uri_pat = re.compile("/v1.*\?")
    uri_tmp = uri_pat.search(uri_string)

    # 获取uri, method, infos
    if uri_tmp is  None:
        continue
    uri = uri_tmp.group(0).split("?")[0]
    method = line.split()[5].split('"')[1]
    time = line.split()[2]

    try:
        infos[uri][method].append(time)
    except KeyError:
        infos[uri] = {}
        if method == "POST":
            try:
                infos[uri]["POST"].append(time)
            except KeyError:
                infos[uri]["POST"] = [time]
        elif method == "GET":
            try:
                infos[uri]["GET"].append(time)
            except KeyError:
                infos[uri]["GET"] = [time]

# 保存成csv文件，保存位置与logfile相同
header = ["请求方法", "请求链接uri", "最大请求时长", "最小请求时长", "累计次数", "平均请求时长", "1秒内请求次数", "1-2秒内请求次数", "2-3秒内请求次数", "3-5秒内请求次数", "5秒以上请求次数"]

with open(logfile +".csv", "w", newline="", encoding="utf-8-sig") as f:
    f_csv = csv.writer(f)
    f_csv.writerow([datetime.datetime.date(datetime.datetime.now())])
    f_csv.writerow(header)
    for uri in infos.keys():
        for method in infos[uri].keys():
            time_index = timeIndex(infos[uri][method])
            f_csv.writerow([method, uri, max(infos[uri][method]), min(infos[uri][method]), len(infos[uri][method]), averageTime(infos[uri][method]), time_index["less_than_a_second"],
            time_index["between_one_to_two"], time_index["between_two_to_three"], time_index["between_three_to_five"], time_index["more_than_five"]])