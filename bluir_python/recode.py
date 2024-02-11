import chardet
import codecs
import os
from fact_extractor import list_allfile


# with open(r'F:\AAA研究生资料\Replication-master\bluir_python\demo_srouce.py', 'rb') as f:
#     data = f.read()
#
#     print(chardet.detect(data))

path = "F:\Python_dataset"
path_dir = "F:\Python_dir"
files = os.listdir(path)
files = ["certbot", "compose", "django_rest_framework", "flask", "keras", "mitmproxy", "pipenv", "requests","scrapy", "spaCy", "tornado"]
files = ["requests-master"]
for file in files[:]:
    print(file, end=" ")
    filePath = path+"\\"+file
    for absolutePath in list_allfile(filePath):
        with codecs.open(absolutePath, 'r', 'utf-8') as f:

            data = f.read()

        with codecs.open(absolutePath, 'w', 'gbk') as f:

            f.write(data)

with open(r'F:\java-dir\doc-1', 'rb') as f:
    data = f.read()

    print(chardet.detect(data))

