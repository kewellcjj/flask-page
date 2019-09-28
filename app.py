from flask import Flask, render_template, render_template_string
from flask_flatpages import FlatPages, pygments_style_defs
import markdown
from bs4 import BeautifulSoup as bs

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'

app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)

# fix unnested html code
def prettify(html):
    soup = bs(html, 'html.parser')
    return soup.prettify()

# register custom filter in flask app
app.jinja_env.filters['prettify']=prettify

def my_renderer(text):
    """Inject the markdown rendering into the jinga template"""
    rendered_body = render_template_string(text)
    pygmented_body = markdown.markdown(rendered_body, extensions=['codehilite', 'fenced_code', 'tables', 'mdx_math'])
    return pygmented_body

app.config.update({
    'FLATPAGES_EXTENSION': ['.md', '.markdown'],
    'FLATPAGES_MARKDOWN_EXTENSIONS': ['codehilite', 'fenced_code', 'tables', 'mdx_math'],
    'FLATPAGES_HTML_RENDERER': my_renderer,
    'enable_dollar_delimiter': True,
})

@app.route('/')
def index():
    latest = sorted(pages, reverse=True, key=lambda p: p.meta['date'])
    return render_template('index.html', pages=latest)

@app.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    return render_template('page.html', page=latest)

@app.route('/tag/<string:tag>/')
def tag(tag):
    tagged = [p for p in pages if tag in p.meta.get('tags', [])]
    return render_template('tag.html', pages=tagged, tag=tag)

@app.route('/pygments.css')
def pygments_css():
    return pygments_style_defs('tango'), 200, {'Content-Type': 'text/css'}

if __name__ == "__main__":
    app.run()