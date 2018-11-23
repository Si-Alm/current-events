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

app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
links = []
class ReusableForm(Form):
    landingPage = TextField('Landing Page:', validators=[validators.required()])

def getLinks(landingPage, newsType, numberOfArticles):
    del links[:]
    page = requests.get(landingPage + "/" + newsType)
    print landingPage + "/" + newsType
    tree = html.fromstring(page.content)
    links0 = tree.xpath('//a[@data-pb-local-content-field="web_headline"]')
    links1 = []
    count = 0
    for i in range(0, numberOfArticles):
        count+=1
        tempNum = randint(0, len(links))
        links1.append("Article " + str(count) + ": " + links0[tempNum].get('href'))
        links0.pop(tempNum)
    return links1


@app.route("/", methods=['GET', 'POST'])
def hello():
    articleOneHead = ""
    articleTwoHead = ""
    articleOneLink = ""
    articleTwoLink = ""
    form = ReusableForm(request.form)
 
    #print form.errors
 
    if request.method == 'POST':
        landingPage = str(request.form.get('landingPage'))
        newsType = str(request.form.get('newsType'))
        numberOfArticles = int(request.form.get('numberOfArticles'))
        print newsType
        links3 = getLinks(landingPage, newsType, numberOfArticles)
        for i in links3:
            links.append(i)
    
        """
        if form.validate():
            # Save the comment here.
            flash(articleOneHead)
            flash(articleOneLink)

            flash(articleTwoHead)
            flash(articleTwoLink)
        else:
            flash('All the form fields are required. ')
        """
    return render_template('article.html', form=form, links=links)
 
if __name__ == "__main__":
    app.run()