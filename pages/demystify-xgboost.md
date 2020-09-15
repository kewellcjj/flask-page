---
title: Demystify XGBoost
date: 2020-09-14
tags: [machine learning] 
excerpt: 'A breakdown analysis of XGBoost: a popular scalable tree boosting system.'
---

XGBoost (eXtreme Gradient Boosting) is a machine learning tool that achieves high prediction accuracies and computation efficiency. Since its initial release in 2014, it has gained huge popularity among academia and industry, becoming one of the most cited machine learning library (7k+ paper citation and 19k+ stars on github). 

I was first introduced to XGBoost by one of my good friend back in 2017, same time as I start to work on some Kaggle competitions. XGBoost quickly became my go-to approach as often times I could achieve reasonable performance without much hyper parameter tuning. In fact, XGBoost is the winningest method in Kaggle and KDDCup competitions during 2015, outperforming second most popular method neural nets [[1]](#1).

Earlier this year, I started my journey in Georgia Tech's OMSCS programing taking Artificial Intelligence as my first course. During the semester, I had a chance to write decision trees and random forests from near scratch to tackle classification problems. It was amazing that the math behind tree-based methods is so neat and "simple", yet the performance could be very good. I went for an extra mile managing to build a simple implementation of XGBoost. 

## References
<a id="1">[1]</a> 
Tianqi Chen and Carlos Guestrin. XGBoost: A Scalable Tree Boosting System. In *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, pages 785–794. ACM, 2016.