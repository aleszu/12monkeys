from flask import Flask, request
from goose import Goose
from pattern.vector import Document, Model, TFIDF
import json
import tweepy
from flask.ext.cors import CORS
from bs4 import BeautifulSoup
import requests
import do_auth

CONSUMER_KEY = do_auth.c_k
CONSUMER_SECRET = do_auth.c_s
ACCESS_TOKEN = do_auth.a_k
ACCESS_TOKEN_SECRET = do_auth.a_s
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

g = Goose()

app = Flask(__name__)
cors = CORS(app)

@app.route("/")
def hello():
	tgt_url = "http://www.washingtonpost.com/blogs/the-fix/wp/2015/07/11/in-south-carolina-a-bizarre-dismount-for-the-confederate-flag/"
	tgt_obj = get_keywords(tgt_url)
	keywords = map(lambda x: x[1], tgt_obj['keywords'])
	article_objs = get_articles(keywords)
	return json.dumps(compare(tgt_obj, article_objs))

@app.route("/post", methods=["POST"])
def post():
	if request.method == 'POST':
		tgt_url = request.form['url']
		tgt_obj = get_keywords(tgt_url)
		keywords = map(lambda x: x[1], tgt_obj['keywords'])
		article_objs = get_articles(keywords)
		return json.dumps(compare(tgt_obj, article_objs))


def compare(origin_article_obj, tgt_article_objs):
	tgt_paragraph_docs = []
	tgt_grafs = []

	for obj in tgt_article_objs:
		if obj['paragraphs'] is not None:
			for graf in obj['paragraphs']:
				tgt_grafs.append({
					'text': graf,
					'url': obj['url'],
					'img': obj['img_src'],
					'title': obj['title']
				})
				tgt_paragraph_docs.append(Document(graf, description=obj['url']))

	origin_graf_doc = Document(' '.join(origin_article_obj['paragraphs']), description='origin')

	m = Model(documents=tgt_paragraph_docs+[origin_graf_doc], weight=TFIDF)

	tgts_by_dist = sorted(range(len(tgt_paragraph_docs)), key=lambda i: m.similarity(origin_graf_doc, tgt_paragraph_docs[i]))

	furthest = map(lambda i: tgt_grafs[i], tgts_by_dist)

	furthest_unique = []
	for entry in furthest[::-1]:
		if any([obj['url'] == entry['url'] or obj['text'] == entry['text'] for obj in furthest_unique]):
			pass
		else:
			furthest_unique.append(entry)

	if len(furthest_unique) >= 10:
		return furthest_unique[:10]
	else:
		return furthest_unique


def get_keywords(url):
	output = {}

	try:
		art = g.extract(url=url)
	except:
		pass
	try:
		art_text = art.cleaned_text

		if not art_text:
			r = requests.get(url)
			soup = BeautifulSoup(r.text, 'lxml')
			art_text = ''.join([p.string for p in soup.find_all('p') if p.string is not None])

		output['paragraphs'] = filter(lambda x: x, art_text.split('\n'))
	except:
		output['paragraphs'] = None
	try:
		output['img_src'] = art.top_image.src
	except:
		output['img_src'] = None
	try:
		output['description'] = art.meta_description
	except:
		output['description'] = None
	try:
		output['keywords'] = Document(art_text).keywords(top=4)
	except:
		output['keywords'] = None

	return output


def get_articles(query_term_list):
	max_tweets = 300

	searched_tweets = [status for status in tweepy.Cursor(api.search, q=query_term_list).items(max_tweets)]

	searched_tweet_urls = []
	for tweet in searched_tweets:
		try:
			searched_tweet_urls.append(tweet.entities['urls'])
		except:
			pass

	tgt_urls = []
	for urls in searched_tweet_urls:
		for url in urls:
			tgt_urls.append(url['expanded_url'])

	tgt_urls = list(set(tgt_urls))

	print tgt_urls

	articles = [dict() for url in tgt_urls]

	for i in range(len(tgt_urls)):
		articles[i]['url'] = tgt_urls[i]
		try:
			art = g.extract(url=tgt_urls[i])
		except:
			pass
		try:
			articles[i]['paragraphs'] = filter(lambda x: x, art.cleaned_text.split('\n'))
		except:
			articles[i]['paragraphs'] = None
		try:
			articles[i]['img_src'] = art.top_image.src
		except:
			articles[i]['img_src'] = None
		try:
			articles[i]['description'] = art.meta_description
		except:
			articles[i]['description'] = None
		try:
			articles[i]['title'] = art.title
		except:
			articles[i]['title'] = None

	return articles



if __name__ == "__main__":
    app.run()
