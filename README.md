# kewellcjj.github.io

This is a repository uses Flask to generate static website that can be readily hosted on GitHub. Basic packages can be installed using pip as

```
pip install -r requirements.txt
```

The website uses [Bootstrap](https://getbootstrap.com/) and its [blog template](https://getbootstrap.com/docs/4.3/examples/). Blog posts also uses [github markdown css](https://github.com/sindresorhus/github-markdown-css).

To debug, run ```python app.py```. To generate the website, run ```python app.py build```.

The resulting pages can be found in the `docs` folder and are hosted at https://kewellcjj.github.io. 