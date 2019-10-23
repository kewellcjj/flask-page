from flask import Flask
from flask_frozen import Freezer
import markdown
import sys
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
    'FREEZER_DESTINATION': 'kewellcjj.github.io',
})

# render excerpt as markdown
for p in pages:
    p.meta['excerpt'] = markdown.markdown(p.meta.get('excerpt', ''))

# collect all tags and dates
sorted_tags, sorted_dates = index_summary(pages)

from routes import *

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