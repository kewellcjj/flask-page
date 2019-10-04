title: Markdown Math Support
date: 2019-09-27
tags: [markdown] 

Below is a quick illustration of math support in markdown using [mdx_math](https://github.com/mitya57/python-markdown-math) extension. However, the equation link will be broken if we truncated the equation off the front page. 
{: .alert .alert-warning role="alert"}
```
In equation $\eqref{eq:sample}$, we find the value of an
interesting integral:

\begin{equation}
  \int_0^\infty \frac{x^3}{e^x-1}\,dx = \frac{\pi^4}{15}
  \label{eq:sample}
\end{equation}
```

In equation $\eqref{eq:sample}$, we find the value of an
interesting integral:

\begin{equation}
  \int_0^\infty \frac{x^3}{e^x-1}\,dx = \frac{\pi^4}{15}
  \label{eq:sample}
\end{equation}