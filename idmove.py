from xml.dom.minidom import parse
from urllib import request
from urllib.parse import quote
from ast import literal_eval
from time import sleep
from datetime import datetime

def idRequestUrl(episodeNode):

    apiNetloc = 'http://www.imdbapi.com/'
    imdbID = episodeNode.getElementsByTagName('id')[0].firstChild.nodeValue
    url = apiNetloc + '?i=' + imdbID

    return url


def titleRequestUrl(episodeNode):
    
    title = ''
  
    if episodeNode.hasAttribute('aka'):
        title = getAttribute('aka')
    else:
        title = episodeNode.getElementsByTagName('movie')[0].firstChild.nodeValue

    year = episodeNode.getElementsByTagName('year')[0].firstChild.nodeValue

    apiNetloc = 'http://www.deanclatworthy.com/imdb/'
    titleUrl = quote(title)
    url = apiNetloc + '?q=' + titleUrl + '&year=' + year

    return url


def jsonGet(url):

    get = request.urlopen(url)
    byteResult = get.read()
    strResult = byteResult.decode()

    return strResult


def archive():
  domIN = parse('episodelist-in.xml')
  domOUT = parse('episodelist-out.xml')

  today = datetime.now()
  strDate = today.strftime('%Y-%m-%d-%H%M%S')
  name = str(strDate + '-episodelist.xml')

  with open(name, 'w', encoding='utf-8') as f:
    f.write(domIN.toxml('utf-8').decode('utf-8'))

  with open('episodelist-in.xml', 'w', encoding='utf-8') as f:
    f.write(domOUT.toxml('utf-8').decode('utf-8'))

  domIN.unlink()
  domOUT.unlink()

def writeOut():
  with open('episodelist-out.xml', 'w', encoding='utf-8') as f:
    f.write(dom.toxml('utf-8').decode('utf-8'))


dom = parse('episodelist-in.xml')
domEpisodeList = dom.getElementsByTagName('episode')

keys = ['imdbid', 'country']

for node in domEpisodeList:

    print(node.getElementsByTagName('movie')[0].firstChild.nodeValue)
    
    if node.getElementsByTagName('country').length > 0:
        print('^- already finished')
        continue

    elif node.getElementsByTagName('keyerror').length > 0:
        print('^- not found, skipping')
        continue

    else:
        jsonResult = jsonGet(titleRequestUrl(node))
        dictResult = literal_eval(jsonResult)


    try:
        dictResult[keys[0]]
    except KeyError:
        errorTag = dom.createElement('keyerror')
        node.appendChild(errorTag)
        
        writeOut()
        archive()

        print('^- not found')
 
        sleep(120)
        continue

    for key in keys:
        items = dictResult[key].split(',')

        if key == 'imdbid':
            idElem = node.getElementsByTagName('id')[0]
            idGet = ''.join(items)

            if idGet != idElem.firstChild.nodeValue:
                
                unconf = dom.createElement('unconfCountry')
                node.appendChild(unconf)

            
        else:
            for item in items:
                element = dom.createElement(key.lower())
                data = dom.createTextNode(str(item))
                element.appendChild(data)
                director = node.getElementsByTagName('director')[0]
                node.insertBefore(element, director)
                print('^-added country')


                

    writeOut()
    archive()
    sleep(120)