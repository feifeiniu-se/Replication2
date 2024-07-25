import subprocess
import os


def execute_index_command(command):
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Command execution failure: {e}")

#构建索引
def index(docs_location, index_location):
    indri_path = ''
    try:
        with open("Settings.txt", "r") as file:
            line = file.readline()
            indri_path = line.split("=")[1].strip()

        if not os.path.exists(index_location):
            os.makedirs(index_location)

        command = f"{indri_path}IndriBuildIndex -corpus.path={docs_location} -corpus.class=trectext -index={index_location} -memory=2000M -stemmer.name=Krovetz stopwords fields"

        execute_index_command(command)
        print("Index creation success")
    except FileNotFoundError:
        print("Configuration file not found")


pro = ["compose", "django_rest_framework", "flask", "keras", "pipenv", "requests", "scrapy", "spaCy", "tornado",
        "certbot"]
pro = ["certbot"]
for project in pro:
    index_path = f"F:\\Python_index\\{project}"
    source_path = f"F:\\Python_dir\\{project}"

    index(source_path, index_path)