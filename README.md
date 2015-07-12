### Hacking Journalism, July 11-12, 2015

1. Overview
2. How it works 
3. Scenario 
4. Future work

![alt tag](http://i.imgur.com/eAaOoKS.jpg)

### Overview 
If you are reading one story, this application will help you find stories that are on similar topics, but with dissimilar ideas.

####Backend Specs
Full story is a [Flask application] (http://flask.pocoo.org/docs/0.10/quickstart/) using [Goose extraction] (https://pypi.python.org/pypi/goose-extractor/)  to identify keywords in an (original) article and through [Twitter's API] (https://dev.twitter.com/overview/documentation), identify articles on the same topic. Using the Python Pattern library to compute inverse cosine similarity of paragraphs to the original document, it extracts paragraphs from articles that are the most different from the original article.

####Human-centered design 
Pam is a 20-year-old college student in D.C.
She consumes news as it comes to her, has no allegiance to any particular news outlets, and feels she's rarely getting the full story. 
Test scenario: Her friends are all talking about Charleston confederate flag but she can't add much to the conversation. Does she sit in silence?
When she goes back to her dorm, she goes to Facebook and starts reading the first Confederate flag article she finds, but she doesn't understand it. 
Does she have to go read other articles? She doesn't have the time. 
How does she do it? Full Story.

#### How this helps journalists
- Full Story can show journalists what they're missing or how the issue has grown over time.

#### Future work
- Chrome plugin
- Perhaps help contextualize corporate funding sources, flagging sponsored content

#### Challenges
- What is a news outlet and what is not? Highly contentious issues would return a lot of op-eds and tendentious viewpoints. 

#### List of possible 1st articles

http://www.usatoday.com/story/news/nation/2015/07/10/south-carolina-confederate-flag/29952953/

http://www.nbcnews.com/storyline/confederate-flag-furor/confederate-flag-lowered-forever-south-carolina-capitol-n389996

http://www.washingtonpost.com/news/post-nation/wp/2015/07/10/watch-live-as-the-confederate-flag-comes-down-in-south-carolina/

http://www.motherjones.com/mojo/2015/07/south-carolina-lowers-confederate-flag-once-and-all

http://www.nydailynews.com/news/national/confederate-flag-fans-critics-gather-s-statehouse-article-1.2287700


####Team: 
Aleszu Bajak, Amelia Winger-Bearskin, Erik Reyna, Igor Motor, Maria Chiu, Ralph Wilson, Ross Goodwin, Sandhya Kambhampati 







