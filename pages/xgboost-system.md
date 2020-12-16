---
title: 'XGBoost: System'
date: 2020-12-12
tags: [machine learning, gradient boosting, HPC] 
excerpt: "An overview of XGBoost system optimization."
---

Obligatory disclaimer. This post is based on my very limited knowledge in High Performance Computing (HPC) related topics. My understanding is mainly based on the paper and the author's presentations. While I have checked the source code, I could have overlooked or even misinterpreted some details as I was not too familiar with c++. So take my summary with a huge grain of salt lol...
{: .alert .alert-info role='alert' }

# Data block

|   |x1 |x2 |x3 |
|---|---|---|---|
| 0 |6  |100|30 |
| 1 |1  |np.nan|10|
| 2 |np.nan|40|0|

# Sparsity-aware split finding

# Distributed approximate algorithm

# Cache-aware access

# Out-of-core computation

# Other