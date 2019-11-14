import textrazor

textrazor.api_key = "7b177ab63d438808a6fbd9c451b4e492499029cddd0fe02c11cbf016"

client = textrazor.TextRazor(extractors=["entities", "topics"])
response = client.analyze_url("http://www.bbc.co.uk/news/uk-politics-18640916")

for entity in response.entities():
    print entity.id

    # entity.relevance_score, entity.confidence_score, entity.freebase_types 