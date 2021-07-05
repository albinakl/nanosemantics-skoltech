from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from val import Val
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skoltech.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' & self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/classification')
def clf():
    return render_template("classification.html")


@app.route('/verification')
def verification():
    return render_template("verification.html")


@app.route('/record', methods=['POST', 'GET'])
def record():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/faq')
        except:
            return "Error while creating request"
    else:
        return render_template("record.html")


@app.route('/faq')
def faq():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("faq.html", articles=articles)


@app.route('/faq/<int:id>')
def faq_detail(id):
    article = Article.query.get(id)
    return render_template("faq_detail.html", article=article)

@app.route('/team')
def team():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("team.html", articles=articles)


@app.route('/classification/hhh', methods=['POST', 'GET'])
def asr():
    if request.method == "POST":
        res = []
        for f in request.files:
            if f.startswith('audio_blob'): #and '''проверка формата''':

                predictions_gender, predictions_age, predictions_emotion = Val().predict(request.files[f])

                res.append({
                    'gender': predictions_gender,
                    'age': predictions_age,
                    'emotion': predictions_emotion,
                })
    else:
        return redirect('classification/result')


@app.route('/classification/<path:filename>', methods=['GET'])
def media_file(filename):
    return send_from_directory('./Records', filename, as_attachment=False)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
