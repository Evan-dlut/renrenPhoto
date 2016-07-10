#!/user/bin/python
# -*- coding: utf-8 -*- 

import urllib   
import urllib2   
import cookielib   
import re
import os

def mkdir(path):
	path=path.strip()
	path=path.rstrip("\\")
	isExists=os.path.exists(path)
	if not isExists:
		print (path+' create success')
		os.makedirs(path)
		return True
	else:
		print (path+' create fail')
		return False

def do_regex(content, str):
	pattern = re.compile(str)
	return pattern.findall(content)

def get_content_from_url(url):
	req = urllib2.Request(url)
	res = urllib2.urlopen(req)  
	content = res.read()
	return content, res

def init_urllib2():
	cj = cookielib.CookieJar()   
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))   
	opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)')]   
	urllib2.install_opener(opener)