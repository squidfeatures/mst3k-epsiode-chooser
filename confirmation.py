from xml.dom.minidom import parse
#import xml.dom

dom = parse('episodelist-in.xml')
domTAG = parse('tagsource')

domEpisodeList = domTAG.getElementsByTagName('tag')

for node in domEpisodeList:
  print(node.firstChild.data)
   

#with open('episodelist-out.xml', 'w', encoding='utf-8') as f:
#  f.write(dom.toxml('utf-8').decode('utf-8'))