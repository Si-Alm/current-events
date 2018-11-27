from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from lxml import html
import requests
import os.path
from random import randint

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)

app.config['SECRET_KEY'] = 'x983mhwoadx85m37g94pwdskgdb69h'
links = []
class ReusableForm(Form):
    landingPage = TextField('Landing Page:', validators=[validators.required()])


@app.route("/articletext")
def textScrape():
    return render_template('articletext.html')

@app.route("/articletext", methods=['GET', 'POST'])
def getText():
    articleHead = "Article: "
    articleBody = ""
    form = ReusableForm(request.form)
    if request.method == 'POST':
        landingPage = str(request.form.get('articleLink'))
        page = requests.get(landingPage)
        tree = html.fromstring(page.content)
        text = tree.xpath("//p/text()")
        for i in text:
            articleBody += i
    return render_template('articletext.html', articleText=articleBody, articleHead=articleHead)


def getLinks(landingPage, newsType, numberOfArticles):
    del links[:]
    pageLink = landingPage + "/" + newsType
    if landingPage == "https://www.foxnews.com" and newsType =="business":
        pageLink = "https://www.foxbusiness.com"

    page = requests.get(pageLink)
    tree = html.fromstring(page.content)
    links0 = []
    exLinks0 = []
    if landingPage=="https://www.washingtonpost.com":
        links0 = tree.xpath('//a[@data-pb-local-content-field="web_headline"]')
    elif "https://www.foxnews.com" in pageLink:
        links0 = tree.xpath('//h4[@class="title"]/a')
        exLinks0 = tree.xpath('//h5[@class="title"]/a')
        links0 = links0+exLinks0
    elif pageLink == "https://www.foxbusiness.com":
        links0 = tree.xpath('//h3[@data-v-7cf20f0a=""]/a')
    links1 = []
    for i in range(0, numberOfArticles):
        tempNum = randint(0, (len(links0)-1))
        if landingPage=="https://www.foxnews.com":
            if "https://" in links0[tempNum].get('href'):
                links1.append(links0[tempNum].get('href'))
            else:
                if "https://www.foxnews.com" in pageLink:
                    links1.append("https://www.foxnews.com" + links0[tempNum].get('href'))
                elif pageLink == "https://www.foxbusiness.com":
                    links1.append("https://www.foxbusiness.com" + links0[tempNum].get('href'))
            links0.pop(tempNum)
        elif landingPage=="https://www.washingtonpost.com":
            links1.append(links0[tempNum].get('href'))
            links0.pop(tempNum)
        
    return links1


@app.route("/", methods=['GET', 'POST'])
def main():
    articleOneHead = ""
    articleTwoHead = ""
    articleOneLink = ""
    articleTwoLink = ""
    form = ReusableForm(request.form)
 
 
    if request.method == 'POST':
        landingPage = str(request.form.get('landingPage'))
        newsType = str(request.form.get('newsType'))
        numberOfArticles = int(request.form.get('numberOfArticles'))
        links3 = getLinks(landingPage, newsType, numberOfArticles)
        for i in links3:
            links.append(i)
    
    return render_template('article.html', form=form, links=links)
 
if __name__ == "__main__":
    app.run()
