#http://www.deanclatworthy.com/imdb/

from xml.dom.minidom import parse
#import xml.dom
from urllib import request
from urllib.parse import quote
from ast import literal_eval


dom = parse('episodelist-in.xml')
domEpisodeList = dom.getElementsByTagName('episode')

apiNetloc = 'http://www.imdbapi.com/'
keys = ['Title', 'Year', 'Genre', 'Director', 'Actors', 'ID']

for node in domEpisodeList:
  
   titleStr = node.getElementsByTagName('movie')[0].firstChild.data
   titleUrl = quote(titleStr)
   
   url = apiNetloc + '?t=' + titleUrl
   
   get = request.urlopen(url)
   byteResult = get.read()
   strResult = byteResult.decode()
   dictResult = literal_eval(strResult)

   for key in keys:
     
     items = dictResult[key].split(', ')     

     if key == 'Title':

       if ''.join(items) != titleStr:

          flag = dom.createElement('unconfirmed')
          alternate = dom.createElement('altMovieTitle')
          alternateName = dom.createTextNode(''.join(items))
          
          alternate.appendChild(alternateName)
          node.insertBefore(alternate, node.getElementsByTagName('movie')[0].nextSibling)
          node.appendChild(flag)
      
     else:
        
        for item in items:
          element = dom.createElement(key.lower())
          data = dom.createTextNode(str(item))
          element.appendChild(data)
          node.appendChild(element)

with open('episodelist-out.xml', 'w', encoding='utf-8') as f:
  f.write(dom.toxml('utf-8').decode('utf-8'))