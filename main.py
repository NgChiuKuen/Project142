from flask import Flask, jsonify, request
import pandas as pd
from demographic_filtering import output
from content_filtering import get_recommendations

articles_data = pd.read_csv('articles.csv')
all_articles = articles_data[['url' , 'title' , 'text' , 'lang' , 'total_events']]
liked_articles = []
not_liked_articles = []

app = Flask(__name__)

def assign_val():
    m_data = {
        "url": all_articles.iloc[0,0],
        "title": all_articles.iloc[0,1],
        "text": all_articles.iloc[0,2] or "N/A",
        "lang": all_articles.iloc[0,3],
        "total_events": all_articles.iloc[0,4]/2
    }
    return m_data

@app.route("/get-article")
def get_article():

    article_info = assign_val()
    return jsonify({
        "data": article_info,
        "status": "success"
    })

@app.route("/liked-article")
def liked_article():
    global all_articles
    article_info = assign_val()
    liked_articles.append(article_info)
    all_articles.drop([0], inplace=True)
    all_articles = all_articles.reset_index(drop=True)
    return jsonify({
        "status": "success"
    })

@app.route("/unliked-article")
def unliked_article():
    global all_articles
    article_info = assign_val()
    not_liked_articles.append(article_info)
    all_articles.drop([0], inplace=True)
    all_articles = all_articles.reset_index(drop=True)
    return jsonify({
        "status": "success"
    })


#'url' , 'title' , 'text' , 'lang' , 'total_events'


# API to return most popular articles.
@app.route("/popular-articles")
def popular_articles():
    article_info = []
    for index, row in output.iterrows():
        i = {
            "url": row['row'],
            "title": row['title'],
            "text": row['text'],
            "lang": row['lang'],
            "total_events": row['total_events']
        }
        article_info.append(i)

    return jsonify({
        "data": article_info,
        "status": "success"
    })

# API to return top 10 similar articles using content based filtering method.
@app.route("/recommended-articles")
def recommended_articles():
    global liked_articles
    var = ["url", "title", "text", "lang", "total_events"]
    var2 = pd.DataFrame(columns = var)

    for i in liked_articles:
        var3 = get_recommendations(i["contentId"])
        var2 = var2.append(var3)
    
    var2.drop_duplicates(subset=["title"], inplace = True)

    var4 = []
    
    for  index2, row in var2.iterrows():
        i = {
            "url": row['row'],
            "title": row['title'],
            "text": row['text'],
            "lang": row['lang'],
            "total_events": row['total_events']
        }
        var4.append(i)

    return jsonify({
        "data": var4,
        "status": "success"
    })

if __name__ == "__main__":
    app.run()