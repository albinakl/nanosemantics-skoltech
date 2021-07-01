from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
