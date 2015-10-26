import urllib2
from bs4 import BeautifulSoup

def stringPurify(str):
    while '\n\n' in str:
        str = str.replace('\n\n','\n')
    while '   ' in str:
        str = str.replace('   ', '  ')
    return str

def outputFile(claim, status, example, origins, sources, url):
    example = stringPurify(example)
    origins = stringPurify(origins)
    sources = stringPurify(sources)
    fset = url.split('/')
    fileName = 'output/' + fset[-3] + '-' + fset[-2] + '-' + fset[-1][0:len(fset[-1])-4] + '.txt'
    f = open(fileName,'w')
    f.write('@@@begin_claim@@@\n')
    f.write(claim.encode('utf8'))
    f.write('\n@@@end_claim@@@\n')
    f.write('@@@begin_status@@@\n')
    f.write(status.encode('utf8'))
    f.write('\n@@@end_status@@@\n')
    f.write('@@@begin_example@@@\n')
    f.write(stringPurify(example.encode('utf8')))
    f.write('\n@@@end_example@@@\n')
    f.write('@@@begin_origins@@@\n')
    f.write(stringPurify(origins.encode('utf8')))
    f.write('\n@@@end_origins@@@\n')
    f.write('@@@begin_sources@@@\n')
    f.write(stringPurify(sources.encode('utf8')))
    f.write('\n@@@end_sources@@@\n')
    f.close()
    print('Writing done:' + fileName)

def parseItem(surl, murl, status):
    baseUrl = 'http://www.snopes.com'
    #1. determine if in base url
    if len(surl.split('/')) != 1 and surl[0] == '/':
        #go to domain and read
        trueUrl = baseUrl + surl
    else:
        #to current and read
        trueUrl = murl[0:murl.rfind('/')+1] + surl
    print('Parsing:   ' + trueUrl)
    try:
        html = urllib2.urlopen(trueUrl).read()
    except:
        return
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

    #debug
    print (stt.find('var CasaleArgs = new Object();'))
    print (stt.find('CasaleArgs.version = 2;'))
    stt = stt.replace('var CasaleArgs = new Object();', '\n')
    stt = stt.replace('CasaleArgs.version = 2;', '\n')
    stt = stt.replace('CasaleArgs.adUnits = "4";', '\n')
    stt = stt.replace('CasaleArgs.casaleID = 159339;', '\n')
    #print stt

    #parsing:
    #1. get Claim:
    sClaim = ''
    st = stt
    sts = st.split('\n')
    for i in sts:
        if len(i)>6:
            sClaim = i[9:len(i)-1]
            break
    #print("Claim--" + sClaim)

    #2. example
    testSplit = stt.split('Examples:')
    if len(testSplit) == 1:
        testSplit = stt.split('Example:')
    if len (testSplit) != 1:
        sExample = testSplit[1].split('Origins:')[0]
    else:
        sExample = ' '
    #print("Example--" + sExample)

    #3. origins
    if len (stt.split('Origins:')) == 1:
        sOrigins = ' '
    else:
        sOrigins = stt.split('Origins:')[1].split('Additional information:')[0]
        sOrigins = sOrigins.split('Source')[0]
    #print("Origins--" + sOrigins)

    #4. sourses
    sourseTable = soup.find_all('dl')
    if len(sourseTable) == 0:
        sSource = ' '
    else:
        sSource = sourseTable[0].get_text()
    #print("Sourses--" + sSource)

    if len(sClaim) > 2 and len(sOrigins) > 2 and len(sSource) > 2 and len(sExample)> 2:
        print ("Information retrieved")
    outputFile(sClaim, status, sExample, sOrigins, sSource, trueUrl)
'''
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
'''

#parse subcatagory page
def parseSubCata(url):
    print('Parsing   ' + url)
    baseUrl = 'http://www.snopes.com'
    try:
        html = urllib2.urlopen(url).read()
    except:
        return
    soup = BeautifulSoup(html)

    bulletList = []
    linkList = []
    #find bullets

    type = 0
    for i in soup.find_all('img'):
        if i.has_attr('title') or i.has_attr('alt'):
            if i['src'].find('common') != -1:
                if '/common/green.gif' in i['src']:
                    bulletList.append('TRUE')
                elif '/common/red.gif' in i['src']:
                    bulletList.append('FALSE')
                elif '/common/multi.gif' in i['src']:
                    bulletList.append('MULTIPLE TRUTH VALUES')
                elif '/common/yellow.gif' in i['src']:
                    bulletList.append('UNDETERMINED')
                elif '/common/white.gif' in i['src']:
                    bulletList.append('UNCLASSIFIABLE VERACITY')
                '''
                if i['title']=='Green bullet':
                    bulletList.append('TRUE')
                elif i['title']=='Red bullet':
                    bulletList.append('FALSE')
                elif i['title']=='Multiple status bullet' \
                        or i['title'] == 'Multi bullet' \
                        or i['title'] == 'Multi-colored bullet' \
                        or i['title'] == 'Multi-status bullet':
                    bulletList.append('MULTIPLE TRUTH VALUES')
                elif i['title']== 'Yellow bullet':
                    bulletList.append('UNDETERMINED')
                elif i['title']=='White bullet':
                    bulletList.append('UNCLASSIFIABLE VERACITY')
                #bulletList.append(i['title'])
                '''
                type = 1
    if type==0:
        for i in soup.find_all('img'):
            if i.has_attr('src'):
                if i['src'] == '/images/green.gif':
                    bulletList.append('TRUE')
                elif i['src'] == '/images/yellow.gif':
                    bulletList.append('UNDETERMINED')
                elif i['src'] == '/images/legend.gif':
                    bulletList.append('LEGEND')
                elif i['src'] == '/images/red.gif':
                    bulletList.append('FALSE')
                elif i['src'] == '/images/mostlyfalse.gif':
                    bulletList.append('PROBABLY FALSE')
                elif i['src'] == '/images/mostlytrue.gif':
                    bulletList.append('PARTLY TRUE')
                elif i['src'] == '/images/mixture.gif':
                    bulletList.append('MIXTURE')
    for i in soup.find_all('table'):
        if i.has_attr('width') and i.has_attr('align'):
            if (i['width']=='90%'):
                print('Find Table')
                for j in i.find_all('a'):
                    #print('Find link')
                    if j.has_attr('href'):
                        linkList.append(j['href'])

    if (len(linkList) < len(bulletList)):
        bulletList = bulletList[len(bulletList)-1-len(linkList):len(bulletList)-1]
        print("table adjusted")
    print len(linkList)
    print len(bulletList)
    print(linkList)
    print(bulletList)
    print(url)
    for i in range(0,len(linkList)):
        parseItem(linkList[i], url, bulletList[i])


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
    #sp('http://www.snopes.com/business/alliance/procter.asp')
    #parseSubCata('http://www.snopes.com/autos/law/law.asp')

    myList = ['http://www.snopes.com/college/college.asp']
    keys = ['college']
    for i in range(0,len(myList)):
        parseCatagory(myList[i],keys[i])
