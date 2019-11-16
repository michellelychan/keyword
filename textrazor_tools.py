import textrazor

textrazor.api_key = "7b177ab63d438808a6fbd9c451b4e492499029cddd0fe02c11cbf016"

client = textrazor.TextRazor(extractors=["entities", "topics"])


response = client.analyze_url("https://www.scmp.com/sport/martial-arts/mixed-martial-arts/article/3037656/hong-kongs-ufc-academy-star-ramona-pascual")
# response = client.analyze_url("https://www.scmp.com/news/hong-kong/politics/article/3038049/pla-soldiers-sent-streets-hong-kong-first-time-protests")


print "Entity id | Relevance Score | Confidence Score"

response.entities().sort(key=lambda x: x.relevance_score, reverse=True)

for entity in response.entities():
    print entity.id, entity.relevance_score, entity.confidence_score

print"----------------------------------------"
print "Topic Label | Topic Score"
response.topics().sort(key=lambda x: x.score, reverse=True)

for topic in response.topics(): 
	print topic.label, topic.score


# entity.freebase_types  