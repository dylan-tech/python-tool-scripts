# coding:utf-8
import os
import argparse
import re


# 匹配文件中存在key，返回文件名
def getfilename(filename, key):
        abs_path = os.path.abspath(filename)
        search_key = ".*{}.*".format(key)
        if args.ignore:
                pat = re.compile(search_key, re.I|re.M)
        else:
                pat = re.compile(search_key, re.M)
        with open(abs_path, "r") as f:
                match = pat.findall(f.read())
                if match:
                        return filename
        return None


def getabspath(dirname):
        return os.path.abspath(dirname)

def combine(dirname, filename):
        return os.path.join(dirname, filename)

# 遍历目录，如果还有子目录，则递归遍历，遍历times层
def showDirectory(dirname, key):
        current_dir = os.path.abspath(dirname)
        inside_files = os.listdir(current_dir)
        for files in inside_files:
                new_path = combine(current_dir, files)
                if os.path.isdir(new_path):
                        showDirectory(new_path, key)
                else:
                        getfile = getfilename(new_path, key)
                        if getfile:
                                print(getfile)

if __name__ == "__main__":
        current_path = os.getcwd()
        parser = argparse.ArgumentParser()
        parser.add_argument("--path", "-p", help="目录路径", default=current_path)
        parser.add_argument("--key", "-k", help="关键字 必填", required=True)
        parser.add_argument("--ignore", "-i", help="忽略大小写", action="store_true")
        args = parser.parse_args()
        showDirectory(args.path, args.key)