---
title: 'Demystify XGBoost'
date: 2020-09-14
tags: [machine learning] 
excerpt: 'A breakdown analysis of XGBoost.'
---

XGBoost (eXtreme Gradient Boosting) is a machine learning tool that achieves high prediction accuracies and computation efficiency. Since its initial release in 2014, it has gained huge popularity among academia and industry, becoming one of the most cited machine learning library (nearly 8k paper citation and 20k stars on github). 

I was first introduced to XGBoost by one of my good friend back in 2017, same time as I start to work on some Kaggle competitions. XGBoost quickly became my go-to approach as often times I could achieve reasonable performance without much hyper parameter tuning. In fact, XGBoost is the winningest method in Kaggle and KDDCup competitions during 2015, outperforming second most popular method neural nets [[1]](#1).

Earlier this year, I had a chance to write decision trees and random forests from near scratch during my first semester of the Georgia Tech's OMSCS program. It was amazing that the math behind tree-based methods is so neat and "simple", yet the performance could be very good. I was able to go for an extra mile, managing to build a simple implementation of XGBoost. To do so, I had to study the original paper of XGBoost in depth (kinda, I probably only touched 30% of details). I feel it is a good time to revisit what I have done and go over what I have learned during the process.

Note that various tree boosting methods exist way before the invention of XGBoost. The major contribution of XGBoost is to propose an efficient calculation, parallel tree learning algorithm and system optimizations, which combined together, resulting in a scalable end-to-end tree boosting *system*. The making of XGBoost not only requires understanding in decision tress, boosting and regularization, but also demands knowledge in computer science, particularly high performance computing.

## Part 1: Decision trees and tree boosting

Let's begin with a single decision tree.

\begin{equation}
  \hat y_i = \phi(x_i) = \sum_{k=1}^K f_k(x_i), f_k \in \mathcal{F}
  \label{eq:additive}
\end{equation}

## Part 2: An example with logistic regression for binary classification

## Part 3: Parallel algorithms and system design



## References
<a id="1">[1]</a> 
Tianqi Chen and Carlos Guestrin. XGBoost: A Scalable Tree Boosting System. In *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, pages 785–794. ACM, 2016.