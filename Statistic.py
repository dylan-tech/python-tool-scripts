import re

logfile = "tmp.log"
statistics = {}
times = {}


def averageTime(time_list):
    sum = 0
    for i in time_list:
        sum += float(i)
    return round(sum / len(time_list), 5)


with open(logfile, 'r') as f:
    lines = f.readlines()


for line in lines:
    uri_pat = re.compile("/v1.*\?")
    uri_tmp = uri_pat.search(line)

    # 获取uri, method, times
    uri = uri_tmp.group(0).split("?")[0]
    method = line.split()[5].split('"')[1]
    time = line.split()[2]
    try:
        times[uri][method].append(time)
    except KeyError:
        times[uri] = {}
        if method == "POST":
            try:
                times[uri]["POST"].append(time)
            except KeyError:
                times[uri]["POST"] = [time]
        elif method == "GET":
            try:
                times[uri]["GET"].append(time)
            except KeyError:
                times[uri]["GET"] = [time]


for uri in times.keys():
    for method in times[uri].keys():
        statistics[uri] = {"uri": {"请求方法": method,
                                   "最大请求时间": max(times[uri][method]),
                                   "最小请求时间": min(times[uri][method]),
                                   "累计次数": len(times[uri][method]),
                                   "平均请求时长": averageTime(times[uri][method])
                                   },
                           }

print(statistics)
