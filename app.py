import sys

from flask import Flask
from flask_frozen import Freezer
from flask import render_template
from flask_flatpages import pygments_style_defs
# from app import app, pages, sorted_dates, sorted_tags

from utils import my_renderer, index_summary, FlatPagesNew

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG

app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPagesNew(app)
freezer = Freezer(app) 

app.config.update({
    'FLATPAGES_EXTENSION': ['.md', '.markdown'],
    'FLATPAGES_MARKDOWN_EXTENSIONS': ['codehilite', 'extra', 'mdx_math', 'toc', 'sane_lists'],
    'FLATPAGES_HTML_RENDERER': my_renderer,
    'FREEZER_DESTINATION_IGNORE': ['.git*'],
    'FREEZER_DESTINATION': 'docs',
})

# collect all tags and dates
sorted_tags, sorted_dates = index_summary(pages)

# from routes import *
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

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "build":
            freezer.freeze()
        else:
            try:
                if int(sys.argv[1])>2000:
                    app.run(port=sys.argv[1])
            except ValueError:
                print("Invalid port number")
    else:
        app.run()