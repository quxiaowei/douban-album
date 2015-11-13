#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import requests as R
from bs4 import BeautifulSoup as BS

def write(pict):
    '''
    download picture to directory
    :param pict: the url of picture
    '''
    with open("./"+pict.rsplit("/", 1)[1], "wb") as f:
		# try to get url of the large version pic
		rs = R.get(pict)
		if rs.ok:
			f.write(rs.content)
			rs.close()
		else:
			# get url of normal-size picture
			pict = pict.replace("photo/large", "photo/photo")
			rs2 = R.get(pict)
			if rs2.ok:
				f.write(rs2.content)
			rs2.close()
    
def url(url):
    '''
    delete anchor in url
    '''
    return url.split("#")[0]

def body(start):
    '''
    parse page, return a pic-url generator
    :param url: url of page
    :param _pict: url of picture
    '''
    if not start: return

    _start = url(start)
    _next = _start
    while True:
        try:
            rs = R.get(_next)
        except Exception as e:
            print(e)
            return
        
    	if not rs.ok: return

        _soup = BS(rs.content, "html.parser")
        _next = _soup.find(id="next_photo").get("href")
        _pict = _soup.select("a.mainphoto img")[0].get("src")
        rs.close()
        
        yield _pict

        _next = url(_next)
        if _next == _start: return

if __name__ == "__main__":
    print("Start.")

    # replace the url below with url of any page within the album
    start = "http://www.douban.com/photos/photo/2180595358/"
    success, fail, total = 0, 0, 0
    for pict in body(start):
	total = total + 1
        try:
            write(pict)
        except Exception as e:
            print("#%3d Failed:  %s"%(total, pict))
            fail = fail + 1
        else:
            print("#%3d Success: %s"%(total, pict))
            success = success + 1

    print("End. %d downloaded, %d failed"%(success, fail))
