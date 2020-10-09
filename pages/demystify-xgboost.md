---
title: 'Demystify XGBoost'
date: 2020-09-14
tags: [machine learning] 
excerpt: 'A breakdown analysis of XGBoost.'
---

XGBoost (eXtreme Gradient Boosting) is a machine learning tool that achieves high prediction accuracies and computation efficiency. Since its initial release in 2014, it has gained huge popularity among academia and industry, becoming one of the most cited machine learning library (nearly 8k paper citation and 20k stars on github). 

I was first introduced to XGBoost by one of my good friend back in 2017, same time as I start to work on some Kaggle competitions. XGBoost quickly became my go-to approach as often times I could achieve reasonable performance without much hyper parameter tuning. In fact, XGBoost is the winningest method in Kaggle and KDDCup competitions during 2015, outperforming second most popular method neural nets [[1]](#1).

Earlier this year, I had a chance to write decision trees and random forests from near scratch. It was amazing that the math behind tree-based methods is so neat and "simple", yet the performance could be very good. I was able to go for an extra mile, managing to build a simple implementation of XGBoost. To do so, I had to study the original paper of XGBoost in depth (kinda, I probably only touched 30% of details). I feel it is a good time to revisit what I have done and go over what I have learned during the process.

Note that various tree boosting methods exist way before the invention of XGBoost. The major contribution of XGBoost is to propose an efficient calculation, parallel tree learning algorithm and system optimizations, which combined together, resulting in a scalable end-to-end tree boosting *system*. The making of XGBoost not only requires understanding in decision tress, boosting and regularization, but also demands knowledge in computer science, particularly high performance computing.

## Part 1: Decision trees and gradient tree boosting

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

## Part 2: An example with logistic regression for binary classification

## Part 3: Parallel algorithms and system design



## References
<a id="1">[1]</a> 
Tianqi Chen and Carlos Guestrin. XGBoost: A Scalable Tree Boosting System. In *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, pages 785–794. ACM, 2016.