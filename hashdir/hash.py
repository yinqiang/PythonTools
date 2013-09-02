#!/usr/bin/env python
# -*- encoding:utf8 -*-
# hash.py
# 创建一个Lua数据文件。
# 文件内包括：
# 一个version字段：表示数据版本；
# 一个list字段：表示指定文件夹中所有文件的md5值（包括子文件夹内文件）。
#
# Copyright (c) 2013 , 朱垠强 (Zhu Yinqiang) yinqiang.zhu@gmail.com
# All rights reserved.


import sys, os, time, hashlib

h = {}


def get_file_md5(file):
	f = open(file, 'rb')
	md5 = hashlib.md5()
	md5.update(f.read())
	f.close()
	return md5.hexdigest()


def get_all(dir):
	if dir[-1] != '/':
		dir = dir + '/'

	for filename in os.listdir(dir):
		path = dir + filename
		if os.path.isdir(path):
			get_all(path)
		else:
			h[path] = get_file_md5(path)


def save(dir, version):
	n = len(dir) + 1
	l = sorted(h.keys())
	buf = '-- Generated By hash.py Do not Edit\n'
	buf += 'data = {\n'
	buf += '\tversion = "' + version + '",\n'
	buf += '\tlist = {\n'
	for k in l:
		buf += '\t\t{ path = "' + k[n:] + '" , h = "' + h[k] + '" },\n'
	buf += '\t}\n}\nreturn data\n'
	f = open('update.lua', 'w')
	f.write(buf)
	f.close()


def main():
	dir = len(sys.argv) > 1 and sys.argv[1] or 'assets'
	version = len(sys.argv) > 2 and sys.argv[2] or time.strftime('%Y%m%d%H%M', time.localtime())
	print('scan ' + dir)
	get_all(dir)
	print('saving...')
	save(dir, version)
	print('output: update.lua')
	print('done')


if __name__ == '__main__':
	main()
