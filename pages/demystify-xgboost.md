---
title: 'Demystify XGBoost'
date: 2020-09-14
tags: [machine learning, gradient boosting] 
excerpt: 'A breakdown analysis of XGBoost.'
---

XGBoost (eXtreme Gradient Boosting) is a machine learning tool that achieves high prediction accuracies and computation efficiency. Since its initial release in 2014, it has gained huge popularity among academia and industry, becoming one of the most cited machine learning library (nearly 8k paper citation and 20k stars on github). 

I was first introduced to XGBoost by one of my good friend back in 2017, same time as I start to work on some Kaggle competitions. XGBoost quickly became my go-to approach as often times I could achieve reasonable performance without much hyper parameter tuning. In fact, XGBoost is the winningest method in Kaggle and KDDCup competitions during 2015, outperforming second most popular method neural nets [[1]](#1).

Earlier this year, I had a chance to write decision trees and random forests from near scratch. It was amazing that the math behind tree-based methods is so neat and "simple", yet the performance could be very good. I was able to go for an extra mile, managing to build a simple implementation of XGBoost. To do so, I had to study the original paper of XGBoost in depth (kinda, I probably only touched 30% of details). I feel it is a good time to revisit what I have done and go over what I have learned during the process.

Note that various tree boosting methods exist way before the invention of XGBoost. The major contribution of XGBoost is to propose an efficient calculation, parallel tree learning algorithm and system optimizations, which combined together, resulting in a scalable end-to-end tree boosting *system*. The making of XGBoost not only requires understanding in decision tress, boosting and regularization, but also demands knowledge in computer science, particularly high performance computing.

# Decision trees and gradient tree boosting

We will follow the notation from the paper. Consider a data set with $n$ examples and $m$ features $\mathcal{D} = \{({\bf x}_i, y_i)\} (|\mathcal{D}|=n, {\bf x}_i \in \mathbb{R}^m, y_i \in \mathbb{R})$. Let $\mathcal{F} = \{f({\bf x})=\mathcal{w}_{q({\bf x})}\}(q: \mathbb{R}^m \rightarrow T, \mathcal{w} \in \mathbb{R}^T)$ denote the space of regression trees, where $T$ is the number of leaves in the tree, $q$ represents a possible structures of the tree that maps ${\bf x}$ to the corresponding leaf index, $\mathcal{w}$ is the leaf weight given the observation ${\bf x}$ and a tree structure $q$. A key step of any decision tree algorithms is to determine the best structure $q$ by continuously splitting the leaves (binary partition) according to certain criterion, such as sum of squared errors for regression trees, gini index or cross-entropy for classification trees. Finding the best split is also the key algorithm for XGBoost. In fact, all algorithms listed in the paper are related to split finding. The resulting split points will partition the input space into disjoint regions $R_j=\{  {\bf x} | q({\bf x}) = j\}$ as represented by leaf $j$. A constant $\mathcal{w}_j$ is assigned to leaf $j$, that is $${\bf x} \in R_j \Rightarrow f({\bf x}) = \mathcal{w}_j.$$
Thus $f({\bf x})$ can also be expressed as $f({\bf x}) = \sum_{j=1}^T \mathcal{w}_j I(q({\bf x}) = j)$ which is equivalent to $f({\bf x})=\mathcal{w}_{q({\bf x})}$.

Now we can represent a tree ensemble model as a sum of $K$ additive tree functions: 
\begin{equation}
  \hat y_i = \phi({\bf x}_i) = \sum_{k=1}^K f_k({\bf x}_i), \quad f_k \in \mathcal{F},
  \label{eq:additive}
\end{equation}
where each $f_k$ corresponds to an independent tree structure $q$ and leaf weight $\mathcal{w}$. The optimal tree structures and weights are then learned by minimizing the following object.
\begin{equation}
  \mathcal{L}(\phi) = \sum_{i} l(\hat y_i, y_i) + \sum_k \Omega(f_k),
  \label{eq:object}
\end{equation}
where $\Omega(f) = \gamma T + \frac{1}{2} \lambda ||\mathcal{w}||^2$ is a regularization term to penalize complex models with exceedingly large number of leaves and fluctuant weights to avoid over-fitting.

The boosting tree model can be trained in a forward stagewise manner [[2]](#2). Let $\hat y_i^{(t)}$ denote the prediction of instance ${\bf x}_i$ at the $t$-th iteration, one need to solve $f_t$ to minimize the following:
\begin{equation}
\mathcal{L}^{(t)} = \sum_{i=1}^n l(y_i, \hat y_i^{(t-1)} + f_t({\bf x}_i)) + \Omega(f_t).
\label{eq:stagewise}
\end{equation}
It is quit straightforward to calculate the $\mathcal{w}_j$ given the regions $R_j$. On the contrary, finding the best $R_j$ which minimize $\eqref{eq:stagewise}$ could be a very difficult task for general loss functions. To find an approximate yet reasonably good solution, we first need to find a more convenient ("easy") criterion. Here is where numerical optimization via gradient boosting comes into play. A second-order approximation of loss function was used to show that the AdaBoost algorithm is equivalent to a forward stagewise additive modeling procedure with exponential loss [[3]](#3). The XGBoost paper borrowed this idea to approximate the objective $\eqref{eq:stagewise}$ by
\begin{equation}
\tilde{\mathcal{L}}^{(t)} \simeq \sum_{i=1}^n [g_i f_t({\bf x}_i) + \frac{1}{2} h_i f_t^2({\bf x}_i)] + \Omega(f_t),
\label{eq:stagewise1}
\end{equation}
where $g_i=\partial_{\hat y_i^{(t-1)}} l(y_i, \hat y_i^{(t-1)})$ and $h_i=\partial_{\hat y_i^{(t-1)}}^2 l(y_i, \hat y_i^{(t-1)})$ are first and second order gradient, and the constant term $l(y_i, \hat y_i^{(t-1)})$ is omitted.

Given $R_j$ or equivalently $q$, the paper shows the optimal weight $\mathcal{w}_j^*$ can be expressed as
\begin{equation}
\mathcal{w}_j^* = -\frac{\sum_{i \in R_j} g_j}{\sum_{i \in R_j} h_j + \lambda},
\label{eq:w}
\end{equation}
and the corresponding optimal value is
\begin{equation}
\tilde{\mathcal{L}}^{(t)} (q) = -\frac{1}{2}\sum_{j=1}^T \frac{(\sum_{i \in R_j} g_j)^2}{\sum_{i \in R_j} h_j + \lambda} + \gamma T.
\label{eq:obj}
\end{equation}

Another difficulty for finding the optimal tree structure $q$ is that the possible ways of partition the input space is numerous. Hence, the second approximation is to use a greedy algorithm that starts from a single leaf and iteratively adds branches to the tree is used instead. This is a very common approach same as the recursive binary partitions adopted in CART [[2]](#2). Let $\tilde{\mathcal{L}}^{(t)} (R_j) = \frac{(\sum_{i \in R_j} g_j)^2}{\sum_{i \in R_j} h_j + \lambda} + \gamma$, $\eqref{eq:obj}$ can be decomposed as $\tilde{\mathcal{L}}^{(t)} (q) = -\frac{1}{2}\sum_{j=1}^T \tilde{\mathcal{L}}^{(t)} (R_j)$ which means the splitting can be processed independently across all leaves. Consider $R_L$ and $R_R$ as the disjoint left and right regions after splitting region $R$. Then the loss **reduction** after the split is given by
\begin{align}
\mathcal{L}_{split} = & \frac{1}{2}\left[{\mathcal{L}}^{(t-1)} (R) - {\mathcal{L}}^{(t)} (R_L) - {\mathcal{L}}^{(t)} (R_R) \right]\nonumber\\
= & \frac{1}{2}\left[ \frac{\sum_{i \in R_L} g_j}{\sum_{i \in R_L} h_j + \lambda} + \frac{\sum_{i \in R_R} g_j}{\sum_{i \in R_R} h_j + \lambda} - \frac{\sum_{i \in R} g_j}{\sum_{i \in R} h_j + \lambda} \right] - \gamma.
\label{eq:split}
\end{align}
The best split point will then be the one resulting in the largest value of $\eqref{eq:split}$.  

Notice the XGBoost algorithm is different from the Gradient Tree Boosting Algorithm MART [[4]](#4) showed in the ESL book. The MART is also used in the $\texttt{R gbm}$ package [[2]](#2). Let's take a closer look at the weight udpate equation $\eqref{eq:w}$. Define $I_j=\{i|{\bf x}_i \in R_j\}$ as the instance set of leaf $j$ and $|I_j|$ as the cardinality of $I_j$. Ignoring the regularization term, we can express $\eqref{eq:w}$ as
\begin{equation*}
\mathcal{w}_j^* = -\frac{\frac{1}{|I_j|}\sum_{i \in I_j} g_j}{\frac{1}{|I_j|}\sum_{i \in I_j} h_j}.
\end{equation*}
The nominator and denominator can be considered as the estimated first and second order gradient over $R_j$ with respect to $\hat y^{(t-1)}$, the latest (accumulated) leaf weight. Does this formulation look familiar? It resembles the Newton's method in convex optimization where the update is subtracting first order gradient divided by the Hessian matrix. The MART method is using a steepest gradient descent with only first order approximation. As a result, we can expect XGBoost has a better quadratic approximation and have a better convergence rate to find the optimal weight (in theory).
{: .alert .alert-info role='alert' }

Besides the regularized objective mentioned above, two additional techniques are used to further prevent overfitting. The first technique is to shrink the weight update in $\eqref{eq:w}$ by a factor $\eta$, often times also called as learning rate. Recall the benefits of shrinkage methods such as ridge regression or Lasso? The second technique is column (feature) subsampling, a technique used in Random Forest to improve the variance reduction of bagging by reducing the correlation between the trees. The dropout technique for neural networks work the same way.


# An example with logistic regression for binary classification

# Parallel algorithms and system design

<div class="algorithm">
<pre id="quicksort" style="display:hidden;">
    % This quicksort algorithm is extracted from Chapter 7, Introduction to Algorithms (3rd edition)
    \begin{algorithm}
    \caption{Quicksort}
    \begin{algorithmic}
    \PROCEDURE{Quicksort}{$A, p, r$}
        \IF{$p < r$} 
            \STATE $q = $ \CALL{Partition}{$A, p, r$}
            \STATE \CALL{Quicksort}{$A, p, q - 1$}
            \STATE \CALL{Quicksort}{$A, q + 1, r$}
        \ENDIF
    \ENDPROCEDURE
    \PROCEDURE{Partition}{$A, p, r$}
        \STATE $x = A[r]$
        \STATE $i = p - 1$
        \FOR{$j = p$ \TO $r - 1$}
            \IF{$A[j] < x$}
                \STATE $i = i + 1$
                \STATE exchange
                $A[i]$ with $A[j]$
            \ENDIF
            \STATE exchange $A[i]$ with $A[r]$
        \ENDFOR
    \ENDPROCEDURE
    \end{algorithmic}
    \end{algorithm}
</pre>
</div>

## References
<a id="1">[1]</a> 
Tianqi Chen and Carlos Guestrin. XGBoost: A Scalable Tree Boosting System. In *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, pages 785–794. ACM, 2016.

<a id="2">[2]</a> 
Hastie, T., Tibshirani, R., & Friedman, J. H. (2009). The elements of statistical learning: data mining, inference, and prediction. 2nd ed. New York: Springer.

<a id="3">[3]</a> 
J. Friedman, T. Hastie, and R. Tibshirani. Additive logistic
regression: a statistical view of boosting. *Annals of
Statistics*, pages 337–407, 2000.

<a id="4">[4]</a>
Friedman, Jerome H. Greedy function approximation: A gradient boosting machine. *Annals of
Statistics*, 29 (2001), 1189--1232.

<script>
    pseudocode.renderElement(document.getElementById("quicksort"),
    { lineNumber: true });
</script>