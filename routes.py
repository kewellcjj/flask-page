from flask import render_template
from flask_flatpages import pygments_style_defs
from app import app, pages, sorted_dates, sorted_tags

@app.route('/')
def index():
    latest = sorted(pages, reverse=True, key=lambda p: p.meta['date'])
    return render_template('index.html', pages=latest, tags=sorted_tags, dates=sorted_dates, list_title="Recent Posts")

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/blog/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    return render_template('index.html', pages=[page], tags=sorted_tags, dates=sorted_dates, list_title="")

@app.route('/blog/tag/<string:tag>/')
def tag(tag):
    tagged = [p for p in pages if tag in p.meta.get('tags', [])]
    tagged = sorted(tagged, reverse=True, key=lambda p: p.meta['date'])
    return render_template('index.html', pages=tagged, tags=sorted_tags, dates=sorted_dates, list_title="Recent Posts Tagged "+tag.title())

@app.route('/blog/archive/<string:date>/')
def archive(date):
    archive = [p for p in pages if date == p.meta.get('date', []).strftime("%B %Y")]
    archive = sorted(archive, reverse=True, key=lambda p: p.meta['date'])
    return render_template('index.html', pages=archive, tags=sorted_tags, dates=sorted_dates, list_title="Posts in "+date.title())

@app.route('/static/css/pygments.css')
def pygments_css():
    return pygments_style_defs('default'), 200, {'Content-Type': 'text/css'}