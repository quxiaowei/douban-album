# -*- coding: UTF-8 -*-

import logging
import requests as R
from bs4 import BeautifulSoup as BS
#from exceptions import StopIteration

def write (pict):
    '''
    download picture to directory
    :param pict: the url of picture
    '''

    f = open("./"+pict.rsplit("/", 1)[1], "wb")

#   try large one
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
    parse page, get urls of picture
    :param url: url of page
    :param _pict: url of picture
    '''

    if not first:
        return #raise StopIteration("empty url!")

    first = url(first)
    _next = first
    while True:
        rs = R.get(_next)
        if not rs.ok:
            return #raise StopIteration("request failed!")

        _soup = BS(rs.content, "lxml")
        _next = _soup.find(id="next_photo").get("href")
        _pict = _soup.select("a.mainphoto img")[0].get("src")

        yield _pict
        rs.close()

        _next = url(_next)
        if _next == first:
            return #raise StopIteration("normal end!")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info("Starting...")

    _first = "http://www.douban.com/photos/photo/2019891834/"

    for i in body(_first):
        write(i)

    print "End"

