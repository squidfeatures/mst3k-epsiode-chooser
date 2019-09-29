from random import choice
from xml.dom.minidom import parse
import xml.dom

dom = parse('episodelist-out.xml')

mostRecent = dom.getElementsByTagName('mostRecent').item(0).firstChild.data
print(mostRecent)
domEpisodeList = dom.getElementsByTagName('episode')


idList = []
titleList = []
tagSetList = []


for node in domEpisodeList:

	if node.hasAttributes:
	
		episodeID = node.getAttribute('number')

	idList.append(episodeID)
	
	listOfMovieNodes = node.getElementsByTagName('movie')
	titleList.append(listOfMovieNodes.item(0).firstChild.data)
	
	listOfTagNodes = node.getElementsByTagName('tag')
	
	tagList = []
	
	for tag in listOfTagNodes:
		tagText = tag.firstChild.data
		tagList.append(tagText)
		tagSet = set(tagList)
		tagSetList.append(tagSet)
	
tagDict = dict(zip(idList,tagSetList))
titleDict = dict(zip(idList,titleList))

print(idList)
mostRecentTags = tagDict[mostRecent]
idList.remove(mostRecent)

matchList = []

for id in idList:
	comparitor = tagDict[id]
	match = len(mostRecentTags.intersection(comparitor))
	#mash = []
	#mash.extend(comparitor)
	#mash.extend(mostRecentTags)
	#tagSet = len(set(mash))
	n = len(mostRecentTags)
	m = len(comparitor)
	#totalTags = n + m
	#tagDiff = abs(n - m)

	#print(id, ':', 2*(tagSet / totalTags)-1, ':', 1 - ( tagDiff / totalTags))
	#print(id, ':', (2*(tagSet / totalTags)-1) * (1 - ( tagDiff / totalTags)))
	#print(id, ':', (2*(tagSet / totalTags)-1) - tagDiff / totalTags)
	#print(id, ':', (min(n,m) / tagSet))
	print(id, ':', (1 - (match / min(n,m))))
	
#control = max(matchList) + 1
#probAmount = [control-x for x in matchList]

#probMap = dict(zip(idList,probAmount))

#probPool = []

#for id in idList:
#	i = probMap[id]
#	for n in range(i):
#		probPool.append(id)

#suggestedChoice = choice(probPool)
#suggestedMovie = titleDict[suggestedChoice]
#recentMovie = titleDict[mostRecent]
		
#print('Last Watched: ', mostRecent, ' - ', recentMovie, '\n',  \
#'Suggested: ', suggestedChoice, ' - ', suggestedMovie)


#recentNodes = dom.getElementsByTagName('mostRecent')

#for episode in recentNodes:
#	episode.childNodes = [dom.createTextNode(suggestedChoice)]

#f = open('episodelist.xml', 'w')
#dom.writexml(f)

#dom.unlink()
