from xml.dom.minidom import parse
import xml.dom

dom = parse('episodelist-in.xml')
domTAG = parse('sourceclean.xml')

domTagList = domTAG.getElementsByTagName('tag')
domEpisodeList = dom.getElementsByTagName('number')

property = 'west germany'
tagName = 'country'

propertyTags = [tag for tag in domTagList if tag.firstChild.nodeValue == property]
parentOfTags = [tag.parentNode for tag in propertyTags]

qualMovies = [movie.firstChild.firstChild.nodeValue for movie in parentOfTags]


for movie in qualMovies:
    colorEpisode = [episode.parentNode for episode in domEpisodeList if episode.firstChild.nodeValue == movie]

    episodeNode = colorEpisode[0]   
 
    newElement = dom.createElement(tagName)
    newText = dom.createTextNode(property)
    newElement.appendChild(newText)

    genreElements = episodeNode.getElementsByTagName('genre')
    episodeNode.insertBefore(newElement, genreElements[0])
  
    

with open('episodelist-out.xml', 'w', encoding='utf-8') as f:
  f.write(dom.toxml('utf-8').decode('utf-8'))