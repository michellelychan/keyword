from flask import Flask, render_template
import textrazor


app = Flask(__name__)


textrazor.api_key = "7b177ab63d438808a6fbd9c451b4e492499029cddd0fe02c11cbf016"
client = textrazor.TextRazor(extractors=["entities", "topics"])
response = client.analyze_url("http://www.bbc.co.uk/news/uk-politics-18640916")

api = textrazor.api_key 

@app.route('/')
def home():
	# return textrazor.api_key
	return render_template('index.html', name='Michelle', api=textrazor.api_key )

@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

if __name__ == '__main__':
    app.run(debug=True)