import urllib2
from bs4 import BeautifulSoup

def sp(trueUrl):
    html = urllib2.urlopen(trueUrl).read()
    soup = BeautifulSoup(html)
    mark = 0
    stt = ''
    print (trueUrl)
    for i in soup.find_all('div'):
        if i.has_attr('style'):
            if i['style'] == 'text-align: justify; margin-left: 15px;  margin-right: 15px':
                mark = 1
                stt = i.get_text()
    if mark==0:
        for i in soup.find_all('div'):
            if i.has_attr('class'):
                if 'article_text' in i['class']:
                    stt = i.get_text()
    #get Claim:

#parse itemlist page
def parseItem(surl, murl, status):
    baseUrl = 'http://www.snopes.com'
    #1. determine if in base url
    if len(surl.split('/')) != 1:
        trueUrl = baseUrl + surl
    else:
        trueUrl = murl[0:murl.rfind('/')+1] + surl
    print('Parsing:   ' + trueUrl)

    html = urllib2.urlopen(trueUrl).read()
    soup = BeautifulSoup(html)
    mark = 0
    for i in soup.find_all('div'):
        if i.has_attr('style'):
            if i['style'] == 'text-align: justify; margin-left: 15px;  margin-right: 15px':
                mark = 1
                print (i.get_text())

    if mark==0:
        for i in soup.find_all('div'):
            if i.has_attr('class'):
                if "article_text" in i['class']:
                    print(i.get_text())

#parse subcatagory page
def parseSubCata(url):
    print('Parsing   ' + url)
    baseUrl = 'http://www.snopes.com'
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)

    bulletList = []
    linkList = []
    #find bullets
    for i in soup.find_all('img'):
        if i.has_attr('title'):
            if i['title'].find('bullet') != -1:
                bulletList.append(i['title'])
    for i in soup.find_all('table'):
        if i.has_attr('width') and i.has_attr('align'):
            if (i['width']=='90%'):
                for j in i.find_all('a'):
                    if j.has_attr('href'):
                        linkList.append(j['href'])

    for i in range(0,len(linkList)):
        parseItem(linkList[i], url, bulletList[i+5])


#parse catagory page
def parseCatagory(url,curkey):
    baseUrl = 'http://www.snopes.com/'
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)

    for i in soup.find_all('table'):
        if i.has_attr('align') and i.has_attr('border') and i.has_attr('cellspacing'):
            if i['align'] == 'CENTER' and i['border'] == '0' and i['cellspacing'] == '10':
                tb = i.find_all('a')
                for j in tb:
                    if j.has_attr('href'):
                        #print('Subcatagory page:'+baseUrl + curkey + '/' + j['href'])
                        parseSubCata( baseUrl + curkey + '/' + j['href'])
    return


if __name__=='__main__':
    myList = ['http://www.snopes.com/food/food.asp']
    keys = ['food']
    for i in range(0,len(myList)):
        parseCatagory(myList[i],keys[i])
