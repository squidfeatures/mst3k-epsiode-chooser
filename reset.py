from xml.dom.minidom import parse
import xml.dom

dom = parse('episodelist-in.xml')

elementsToDelete = ['genre', 'director', 'actor']



for element in elementsToDelete:

    domEpisodeList = dom.getElementsByTagName(element)

    for node in domEpisodeList:

        node.parentNode.removeChild(node)
        node.unlink()

with open('episodelist-out.xml', 'w', encoding='utf-8') as f:
  f.write(dom.toxml('utf-8').decode('utf-8'))