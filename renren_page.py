# -*- coding: utf-8 -*- 
from base import *
import time
import json

album_id_pattern = '"albumName":"([^"]+)","albumId":"([\d]+)"'
photo_id_pattern = 'photoId":"([\d]+)'
api_ids_pattern = "requestToken : '([\d]+)',[\s]+_rtk : '([^']+)'"
root_path = os.getcwd()+"/"

def renren_do_login(user_email, password):
	req = urllib2.Request("http://www.renren.com/PLogin.do",
		urllib.urlencode({"email":user_email,"password":password}))
	resp = urllib2.urlopen(req, timeout=2)  
	home_url = resp.geturl()
	pattern = re.compile(r'\d+')
	match = pattern.search(home_url) 
	if match :
		return match.group()

def load_user_info():
	file = open("login.dat","r")
	data = file.readline()
	return data.split(" ")

def json_dict_to_photo(dict):
	for x in dict['list']:
		title = str(long(x["id"]))
		file = open("photo.dat","a+")
		file.write(title)
		file.write("|$---$|")
		file.write(x["originTitle"].encode('utf-8'))
		file.write("|$---$|")
		file.write(x["share"]["largeurl"].encode('utf-8'))
		file.write("|$---$|")
		file.write(x["date"].encode('utf-8'))
		file.write("\n")
		
		img_content,res = get_content_from_url(x["share"]["largeurl"])
		img=open(title+".jpg", "wb")
		if img_content :
			img.write(img_content)

def download_photo(content, renren_id):
	mkdir("photo")
	album_ids = do_regex(content, album_id_pattern)
	result = do_regex(content,api_ids_pattern)
	psource = 2
	requestToken = result[0][0]
	_rtk = result[0][1]
	for name_to_id in (album_ids):
		name = name_to_id[0]
		album_id = name_to_id[1]
		os.chdir(root_path)
		mkdir("photo/"+name)
		os.chdir("photo/"+name)
		album_url = 'http://photo.renren.com/photo/'+renren_id+'/album-'+album_id+'/v7'
		aContent, res = get_content_from_url(album_url)
		photo_ids = do_regex(aContent, photo_id_pattern)
		if not photo_ids[0]:
			continue
		api='http://photo.renren.com/photo/'+renren_id+'/photo-'+photo_ids[0]+'/layer?psource=2&requestToken='+requestToken+'&_rtk='+_rtk
		print("api", api)
		photo_detail_content, res = get_content_from_url(api)
		photo_detail_content_dict = json.loads(photo_detail_content.decode('utf-8'))
		json_dict_to_photo(photo_detail_content_dict)

index_file = open("index.html","r+w+")
user_email, passwd = load_user_info()
init_urllib2()
renren_id = renren_do_login(user_email.strip(), passwd.strip())
content = index_file.read()
if not content or content=='':
	content, res_photo = get_content_from_url('http://photo.renren.com/photo/'+renren_id+'/albumlist/v7?showAll=1#')
	index_file.write(content)
download_photo(content, renren_id)
