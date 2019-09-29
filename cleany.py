from xml.dom.minidom import parse
import xml.dom

def remove_whitespace_nodes(node, unlink=False):

  remove_list = []

  for child in node.childNodes:
    if child.nodeType == xml.dom.Node.TEXT_NODE and \
      not child.data.strip():
       remove_list.append(child)
    elif child.hasChildNodes():
      remove_whitespace_nodes(child, unlink)
  for node in remove_list:
    node.parentNode.removeChild(node)
    if unlink:
      node.unlink()

dom1 = parse('tagsource.xml')
domEpisodeList = dom1.getElementsByTagName('episode')


for node in domEpisodeList:

  remove_whitespace_nodes(node)      

f = open('sourceclean.xml', 'w')
dom1.writexml(f)



dom1.unlink()