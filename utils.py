from flask import render_template_string
import markdown
# from bs4 import BeautifulSoup as bs

# fix unnested html code, and register to the jinja filter
# @app.template_filter('prettify')
# def prettify(html):
#     soup = bs(html, 'html.parser')
#     return soup.prettify()

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
    #collect all tags
    tags = {}
    for p in pages:
        for tag in p.meta.get('tags', []):
            if tag not in tags:
                tags[tag] = 1
            else:
                tags[tag] += 1
    sorted_tags = sorted(tags.items(), reverse=True, key=lambda x: x[1])
    #collect publish dates
    dates = {}
    for p in pages:
        mmyyyy = p.meta.get('date','').strftime("%B %Y")
        if mmyyyy not in dates:
            dates[mmyyyy] = 1
        else:
            dates[mmyyyy] += 1
    sorted_dates = sorted(dates.items(), reverse=True, key=lambda x: x[1])

    return sorted_tags, sorted_dates