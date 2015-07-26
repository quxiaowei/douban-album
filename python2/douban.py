import requests as R
from bs4 import BeautifulSoup as BS

def write (pict):
    f = open("./"+pict.rsplit("/", 1)[1], "wb")
    rs = R.get(pict)
    if rs.ok:
        f.write(rs.content)
        rs.close()
    else:
        rs2 = R.get(pict.replace("photo/large","photo/phote"))
        if rs2.ok:
            f.write(rs2.content)
        rs2.close()
    f.close()

def body(url):
    rs = R.get(url)
    if not rs.ok:
        print rs.status
        return "", ""
    soup = BS(rs.content, "lxml")
    _next = soup.find(id="next_photo").get("href")
    _pict = soup.select("a.mainphoto img")[0].get("src")
#    print _next, _pict
    return _next, _pict

if __name__ == "__main__":
    _first = "http://www.douban.com/photos/photo/2019891834/"
    _next = _first
    _pict = ""
    for i in range(1):
        _next, _pict = body(_next)
        if _next == _first or _next == "":
            break
        write(_pict)
    print "End"

