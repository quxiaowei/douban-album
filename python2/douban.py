#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import requests as R
from bs4 import BeautifulSoup as BS
#from exceptions import StopIteration

def write (pict):
    '''
    download picture to directory
    :param pict: the url of picture
    '''

    f = open("./"+pict.rsplit("/", 1)[1], "wb")

#   try to get url of the large version pic
    rs = R.get(pict)
    if rs.ok:
        f.write(rs.content)
        rs.close()
    else:
#       get url of normal-size picture
        pict = pict.replace("photo/large", "photo/photo")
        rs2 = R.get(pict)
        if rs2.ok:
            f.write(rs2.content)
        rs2.close()
    
    f.close()

def url(url):
    '''
    delete anchor in url
    '''
    return url.split("#")[0]

def body(first):
    '''
    parse page, return a pic-url generator
    :param url: url of page
    :param _pict: url of picture
    '''

    if not first:
        return #raise StopIteration("empty url!")

    first = url(first)
    _next = first
    _i = 0
    while True:
	_i = _i + 1
        try:
            rs = R.get(_next)
        except Exception as e:
            print(e)
            return
        
        if not rs.ok:
            return #raise StopIteration("request failed!")

        _soup = BS(rs.content, "html.parser")
        _next = _soup.find(id="next_photo").get("href")
        _pict = _soup.select("a.mainphoto img")[0].get("src")
        rs.close()
        
        yield _i, _pict

        _next = url(_next)
        if _next == first:
            return #raise StopIteration("normal end!")

if __name__ == "__main__":
    print("Start.")

#   [notice]
#   replace the url below with url of any page within the album
    _first = "http://www.douban.com/photos/photo/2180595358/"
    _n, _y = 0, 0
    for _i, _pict in body(_first):
        try:
            write(_pict)
        except Exception as e:
            print("#%3d Failed:  %s"%(_i, _pict))
            _n = _n + 1
        else:
            print("#%3d Success: %s"%(_i, _pict))
            _y = _y + 1

    print("End. %d downloaded, %d failed"%(_y, _n))
