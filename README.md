# Table of Contents

* [General info](#1)
* [Overview of the replication package](#7)
* [Data set](#2)
* [Requirements](#3)
* [How to run](#4)
* [How to cite this paper](#5)
* [Reference](#6)

<h2 id="1"> General info </h2>
This repository contains the replication package for paper with the title "An Extensive Replication Study of the ABLoTS Approach for Bug Localization". This paper extends our previous work: "The Ablots Approach for Bug Localization: is it replicable and generalizable?" [1], which was granted the "Distinguished Paper Award" at the 2023 IEEE/ACM 20th International Conference on Mining Software Repositories (MSR). 
The original paper is a replication study of the original paper "Analyzing requirements and traceability information to improve bug localization" by Rath et al.[2].


<h2 id="7"> Overview of the replication package </h2>

    /
    .
    |--- ablots/            Implementation of composer component.	
    |--- cache/             Implementation of version history component.
    |--- data/              Example of the data set.
    |--- data_processing/   Read data from SQLite.
    |--- evaluation/        Evaluation metrics, including MAP, MRR, Top K.
    |--- repication/        Preprocessing on extended data set.
    |--- tracescore/        Implementation of TraceScore.
    |--- box.py             Draw box-plot for the paper.
    |--- ks-test.py         ks-test for the paper.

<h2 id="2"> Data set </h2>
The extended dataset include two additional datasets: SEOSS 33 dataset for Java bug localization [3] and Python projects in BuGL dataset [4] for cross-language bug localization.
Here is the data model for the SEOSS 33 dataset. For each project, the data set includes information as follows [3]:

![avatar](dataset.png)

<h2 id="3"> Requirements </h2>
python 3.7

<h2 id="4"> How to run </h2>

<h2 id="5"> How to  cite this paper </h2>

To be known...

<h2 id="6">Reference</h2>

[1]F. Niu, C. Mayr-Dorn, W.K. Assunc ̧ ̃ao, L. Huang, J. Ge, B. Luo, A. Egyed,
"The ABLoTs Approach for Bug Localization: is it replicable and generalizable?," 
in proceedings of the 20th International Conference on Mining Software 
Repositories (MSR), 2023, pp. 576–587.

[2]M. Rath, D. Lo, and P. M ̈ader, "Analyzing requirements and traceability
information to improve bug localization," in Proceedings of the 15th
International Conference on Mining Software Repositories, 2018, pp.
442–453.

[3]M. Rath and P. M ̈ader, "The seoss 33 dataset—requirements, bug reports,
code history, and trace links for entire projects," Data in brief, vol. 25,
p. 104005, 2019.

[4] S. Muvva, A.E. Rao, S. Chimalakonda, "Bugl -- a cross-language dataset for bug localization," arXiv preprint arXiv:2004.08846 (2020).
