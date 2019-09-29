from xml.dom.minidom import parse
from urllib import request
from urllib.parse import quote
from ast import literal_eval


def idRequestUrl(episodeNode):

    apiNetloc = 'http://www.imdbapi.com/'
    imdbID = episodeNode.getElementsByTagName('id')[0].firstChild.nodeValue
    url = apiNetloc + '?i=' + imdbID

    return url


def titleRequestUrl(title, year):

    apiNetloc = 'http://www.deanclatworthy.com/imdb/'
    titleUrl = quote(title)
    url = apiNetloc + '?q=' + titleUrl + '&year=' + year

    return url


def jsonGet(url):

    get = request.urlopen(url)
    byteResult = get.read()
    strResult = byteResult.decode()

    return strResult


dom = parse('episodelist-in.xml')
domEpisodeList = dom.getElementsByTagName('episode')

keys = ['Title', 'Director', 'Actors', 'Genre']

for node in domEpisodeList:
    if node.getElementsByTagName('director').length > 0:
        continue

    jsonResult = jsonGet(idRequestUrl(node))
    dictResult = literal_eval(jsonResult)



    for key in keys:
        items = dictResult[key].split(', ')

        if key == 'Title':
            movieElem = node.getElementsByTagName('movie')[0]
            titleGet = ''.join(items)

            if titleGet != movieElem.firstChild.nodeValue:
                attribute = 'aka'
                alsoKnownAs = dom.createAttribute(attribute)
                movieElem.setAttributeNode(alsoKnownAs)
                movieElem.setAttribute(attribute, titleGet)

            
        else:
            for item in items:
                element = dom.createElement(key.lower())
                data = dom.createTextNode(str(item))
                element.appendChild(data)
                node.appendChild(element)

with open('episodelist-out.xml', 'w', encoding='utf-8') as f:
  f.write(dom.toxml('utf-8').decode('utf-8'))