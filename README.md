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
    |--- bluir_python/      Implementation of code structure component on python dataset.
    |--- cache/             Implementation of version history component.
    |--- cache_python/      Implementation of version history component on python dataset.
    |--- data/              Example of the data set.
    |--- data_processing/   Read data from SQLite.
    |--- evaluation/        Evaluation metrics, including MAP, MRR, Top K.
    |--- repication/        Preprocessing on extended data set.
    |--- repication_python/ Preprocessing on python dataset.
    |--- tracescore/        Implementation of TraceScore.
    |--- box.py             Draw box-plot for the paper.
    |--- ks-test.py         ks-test for the paper.

<h2 id="2"> Data set </h2>
The extended dataset include two additional datasets: SEOSS 33 dataset for Java bug localization [3] and Python projects in BuGL dataset [4] for cross-language bug localization.
Here is the data model for the SEOSS 33 dataset. For each project, the data set includes information as follows [3]:

![avatar](dataset.png)

<h2 id="3"> Requirements </h2>
python 3.7  <br>   


We have 6 dependencies below:<br>
scikit-learn >= 1.3.2<br>
matplotlib >= 2.0.1<br>
numpy >= 1.16.1<br>
scipy >= 0.19.1<br>
imbalanced-learn >= 0.7.1<br>
pandas >= 0.25.3<br>

<h2 id="4"> How to run </h2>
<h3>Clone this repository</h3>
Clone the repository by using the following command:<br>

$ git clone https://github.com/feifeiniu-se/Replication2.git

If you don't have git,you can visit the Git website (https://git-scm.com/download) or use Git for Windows download links (e.g. https://gitforwindows.org/), choose the installation package that matches your Windows system to download.<br>

<h3>Install python</h3>
We used python 3.7. (If you have python 3.7 in your computer, please skip this section.)<br>

To install Python 3.7 on a Windows VM, visit the Python website (https://www.python.org). On the home page, move the mouse button to "Downloads" and select a Windows version. After the download is complete, double-click the downloaded installation package file (such as python-3.7.x-amd64.exe) to start the installation process.

<h3>Usage of ablots package</h3>
Run the main file of the ablots package to get how the original-java dataset and the extended-java dataset perform in different composer.
Run the main_python file of the ablots package to see how the extended-python dataset perform in different composer.

Different methods correspond to different components: <br>

calculate: This method corresponds to integrated strategies based on training and can select different models in classifier.py, such as decision trees, random forests, multi-layer perceptrons, logistic regression, etc. <br>
calculate_fixed: Fixed weight component. <br>
calculate_overlap: Use the CombSUM method based on overlap. <br>
calculate_bias: Use the CombSUM method based on bias. <br>
calculate_combanz: Use the CombANZ method. <br>
calculate_combmnz: Use the CombMNZ method. <br>
calculate_corr: Use a correlation-based method. <br>
calculate_borda: Use the boda counts method. <br>

<h3>Usage of bluir_python package</h3>

The bluir_python package is an implementation of the code structure component, where the first four files are used to extract the code structure , build the index, build the query document, and retrieve. Build indexing and retrieval using the indri toolkit (https://downloads.sourceforge.net/project/lemur/lemur/indri-5.21/indri-5.21.tar.gz).

*1_fact_extractor.py: This file is used to extract the code structure (using python's ast module),The path parameter indicates the path to the python dataset, the path_dir parameter indicates the storage path of the code structure file collection, and the files parameter indicates the name of the project in the dataset from which the code structure needs to be extracted.<br>
*2_index_builder.py:To execute this file, you need to change the contents of Settings.txt to the bin folder path of your Indri, source_path and index_path are your code structure file collection path and index store path, respectively.<br>
*3_query_extractor.py:To execute this file requires changing the outputPath parameter in the extractSumDesField method to your query document storage path and the url parameter to your sql database document path.<br>
*4_retrieve.py:To execute this file, change the index_path parameter to your index storage path, the query_path parameter to your query document path, and the result_path parameter to your code structure score storage path.<br>
*5_bluir_insert.py:To execute this file, you need to change the path parameter in the read_indriQueryResult method to your code structure score store path and the path parameter in the insert_database method to your database store path.<br>

Refer to https://hub.nuaa.cf/exatoa/Bench4BL for the implementation of the code structure component.

<h3>Run previous package on PyCharm</h3>
We chose to run the package using PyCharm.If you also want to run it on PyCharm, please follow next sequence:<br>

*Before running the package, you need to make sure that PyCharm is configured with the correct Python interpreter.<br>
*If you have already cloned the package, you can open it directly in PyCharm. Click on the "File" menu and select "Open..." (Opens...) Then navigate to the package folder and select it.<br>
*Enter the 'pip install package name' in the terminal or command prompt to install the required package. For example, to install the NumPy package, type 'pip install numpy'.<br>
*Click the green triangle icon in the Run/Debug Configuration drop-down menu (or Ctrl + Shift + F10 (Windows) /Cmd + Shift + F10 (Mac)) to run the package.<br>
*PyCharm will display the output of the package in the "Run" window (or "Terminal" window, depending on your Settings) at the bottom.<br>

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
