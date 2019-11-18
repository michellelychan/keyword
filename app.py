from flask import Flask, render_template, jsonify, request
# import textrazor, textrazor_tools

import urllib.request, json
import ssl
import textrazor
from newsapi import NewsApiClient

from pytrends.request import TrendReq

# Setup SSL
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

app = Flask(__name__)

# textrazor.api_key = "7b177ab63d438808a6fbd9c451b4e492499029cddd0fe02c11cbf016"
# client = textrazor.TextRazor(extractors=["entities", "topics"])
# response = client.analyze_url("http://www.bbc.co.uk/news/uk-politics-18640916")

# api = textrazor.api_key

# Utils
import re
TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)

@app.route('/')
def home():
    # return textrazor.api_key
    return render_template('index.html')

@app.route('/extract-text/<article_id>')
def extract_text(article_id):
    api_url = "https://cms.scmp.com/api/rest/nodejs/content.json?type=node&token=tyH4YutRToPFg23vW6R4kBQ4LKvZBt38bnNdYZNUK20&keywords=1&id="+article_id

    with urllib.request.urlopen(api_url) as url:
        data = json.loads(url.read().decode())
        print(data)

        print("node_"+article_id)

        title = data.get("node_"+article_id).get("content")[0].get("title")
        print(title)

        topics = data.get("node_"+article_id).get("content")[0].get("topics")

        plain_text_summary = data.get("node_"+article_id).get("content")[0].get("plain_text_summary")
        summary = data.get("node_"+article_id).get("content")[0].get("summary")
        body = remove_tags(data.get("node_"+article_id).get("content")[0].get("body"))
        return jsonify(
            body=body,
            summary=summary,
            title=title,
            topics=topics
    )

@app.route('/extract-keywords/')
def extract_keywords():
    full_text = request.args.get('fulltext')

    textrazor.api_key = "7b177ab63d438808a6fbd9c451b4e492499029cddd0fe02c11cbf016"

    client = textrazor.TextRazor(extractors=["entities", "topics"])
    response = client.analyze(full_text)

    print ("Entity id | Relevance Score | Confidence Score")

    all_entities = response.entities()
    all_entities.sort(key=lambda x: x.relevance_score, reverse=True)


    # Lets construct a return value
    keyword_dict = {}
    for entity in all_entities:
        keyword_dict[entity.id] = entity.relevance_score
        print (entity.id, entity.relevance_score, entity.confidence_score)

    print("----------------------------------------")
    print ("Topic Label | Topic Score")
    response.topics().sort(key=lambda x: x.score, reverse=True)

    for topic in response.topics():
        print (topic.label, topic.score)


    return jsonify(keyword_dict)

# @app.route('/<name>')
# def hello_name(name):
#     return "Hello {}!".format(name)


# Init
@app.route('/newsapi/<keyword>')
def newsapi(keyword):
    newsapi = NewsApiClient(api_key='7d0772b9f7024e80b04e6d2cade69182')

    # /v2/top-headlines
    top_headlines = newsapi.get_top_headlines(q=keyword,
                                              country="us")

    print(top_headlines)

    articles = top_headlines.get('articles')

    result = {}
    for a in articles:
        result[a['title'] + ' ('+ a['source']['name'] +')'] = a

    return result

@app.route('/googletrend/<keyword>')
def googletrend(keyword):
    pytrends = TrendReq(hl='en-US', tz=360) # Related Queries, returns a dictionary of dataframes


    pytrends.build_payload(kw_list=[keyword])
    related_queries_dict = pytrends.related_queries()


    print(related_queries_dict[keyword]['top'])
    print(related_queries_dict[keyword]['rising'])
    return {'top': related_queries_dict[keyword]['top'].to_json(),
    'rising': related_queries_dict[keyword]['rising'].to_json()}

if __name__ == '__main__':
    app.run(debug=True)