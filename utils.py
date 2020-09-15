from flask import render_template_string
from flask_flatpages import FlatPages, Page
import markdown
from werkzeug.utils import import_string
from itertools import takewhile

# from bs4 import BeautifulSoup as bs

# fix unnested html code, and register to the jinja filter
# @app.template_filter('prettify')
# def prettify(html):
#     soup = bs(html, 'html.parser')
#     return soup.prettify()

class FlatPagesNew(FlatPages):
    def _parse(self, content, path):
        """Parse a flatpage file, i.e. read and parse its meta data and body.
        :return: initialized :class:`Page` instance.
        """

        lines = content.split('\n')
        assert lines[0] == '---' and lines.count('---') >= 2, "Use '---' to indicate the start and end of the page meta"

        lines = iter(lines[1:])
        # Read lines until an empty line is encountered.
        meta = '\n'.join(takewhile(lambda s: s != "---", lines))
        # The rest is the content. `lines` is an iterator so it continues
        # where `itertools.takewhile` left it.
        content = '\n'.join(lines)

        # Now we ready to get HTML renderer function
        html_renderer = self.config('html_renderer')

        # If function is not callable yet, import it
        if not callable(html_renderer):
            html_renderer = import_string(html_renderer)

        # Make able to pass custom arguments to renderer function
        html_renderer = self._smart_html_renderer(html_renderer)

        # Initialize and return Page instance
        return Page(path, meta, content, html_renderer)

def my_renderer(text):
    """Inject the markdown rendering into the jinga template"""
    rendered_body = render_template_string(text)
    extension_configs = {
        'codehilite': {
            # 'linenums': 'True',
            'guess_lang': False,
        },
        'mdx_math': {
            'enable_dollar_delimiter': True,
        },
        'toc': {
            'baselevel': 2,
            'toc_depth': "2-2",
            # 'title': "Table of Contents",
        },
    }
    pygmented_body = markdown.markdown(rendered_body, extensions=['codehilite', 'extra', 'mdx_math', 'toc', 'sane_lists'],
                        extension_configs = extension_configs)
    return pygmented_body

def index_summary(pages):  
    tags = {}
    dates = {}

    for p in pages:

        # render excerpt as markdown
        p.meta['excerpt'] = markdown.markdown(p.meta.get('excerpt', ''))

        #collect all tags
        for tag in p.meta.get('tags', []):
            if tag not in tags:
                tags[tag] = 1
            else:
                tags[tag] += 1

        #collect publish dates
        mmyyyy = p.meta.get('date','').strftime("%B %Y")
        if mmyyyy not in dates:
            dates[mmyyyy] = 1
        else:
            dates[mmyyyy] += 1

    sorted_tags = sorted(tags.items(), reverse = True, key = lambda x: x[1])
    sorted_dates = sorted(dates.items(), reverse = False, key = lambda x: x[1])

    return sorted_tags, sorted_dates