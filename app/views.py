from elasticsearch import RequestError
from flask import render_template, request, redirect, url_for
from app import app, db
from .models import Text
from .search import add_to_index, query_index, remove_from_index


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        rubrics = request.form['rubrics']
        file = request.files['file']
        date = request.form['date']

        text_b = file.read()
        text = text_b.decode('utf-8')
        file.close()

        text_object = Text(rubrics=rubrics, text=text, created_date=date)
        db.session.add(text_object)
        db.session.commit()

        add_to_index(text_object)
        return redirect(url_for('search'), 302)
    else:
        return render_template('index.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_request = str(request.form['search'])
        try:
            ids = query_index(search_request)
        except RequestError as re:
            print('truble', re)

        text_obj = Text.query.filter(Text.id.in_(ids)).order_by('created_date').all()

        return render_template('search.html', text_obj=text_obj)
    else:
        return render_template('search.html')


@app.route('/search/text/<int:id>', methods=['GET', 'POST'])
def text(id):
    text = Text.query.get(id)
    return render_template('text.html', text=text)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        id = int(request.form['id'])

        text_obj = Text.query.get(id)

        remove_from_index(text_obj)
        db.session.delete(text_obj)
        db.session.commit()

        return render_template('index.html')
    else:
        ids = Text.query.all()
        return render_template('delete.html', ids=ids)
