#http://www.deanclatworthy.com/imdb/

from xml.dom.minidom import parse
#import xml.dom
from urllib import request
from urllib.parse import quote
from ast import literal_eval
from time import sleep

dom = parse('episodelist-in.xml')
domEpisodeList = dom.getElementsByTagName('episode')

apiNetloc = 'http://www.deanclatworthy.com/imdb/'
keys = ['imdbid', 'country']

for node in domEpisodeList:
  
   titleStr = node.getElementsByTagName('movie')[0].firstChild.data
   ttID = node.getElementsByTagName('id')[0].firstChild.nodeValue
   year = node.getElementsByTagName('year')[0].firstChild.nodeValue
   titleUrl = quote(titleStr)
   
   url = apiNetloc + '?q=' + titleUrl + '&year=' + year
   
   get = request.urlopen(url)
   byteResult = get.read()
   strResult = byteResult.decode()
   dictResult = literal_eval(strResult)

   print(titleStr)
   try:
     dictResult['year']
   except KeyError:
     print('^- key error')
     sleep(120)
     continue
   
   for key in keys:
     
     items = dictResult[key].split(',')

     if key == 'imdbid':

       if ''.join(items) != ttID:
          flag = dom.createElement('unconfirmed')
          node.appendChild(flag)

     else:
        
        for item in items:
          element = dom.createElement(key.lower())
          data = dom.createTextNode(str(item))
          element.appendChild(data)
          insertPoint = node.getElementsByTagName('genre')[0]
          node.insertBefore(element, insertPoint)

   sleep(120)

with open('episodelist-out.xml', 'w', encoding='utf-8') as f:
  f.write(dom.toxml('utf-8').decode('utf-8'))