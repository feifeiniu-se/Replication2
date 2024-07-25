import subprocess


def retrieve(query_file_path, result_path, index_location):
    indri_path = None

    try:
        with open("Settings.txt", "r") as file:
            line = file.readline().strip()
            if "=" in line:
                indri_path = line.split("=")[1]
    except FileNotFoundError:
        print("Settings File Not Found!")
        return
    except Exception as e:
        print(f"Problems with Settings file! {e}")
        return

    if not all([result_path, index_location, query_file_path]):
        print("You have to provide both the index location, result path, and query file path.")
        return


    topN = 100

    # 构造命令字符串
    command = f"{indri_path}IndriRunQuery {query_file_path} -count={topN} -index={index_location} -trecFormat=true -rule=method:tfidf,k1:1.0,b:0.3"

    # 执行检索命令
    execute_retrieval_command(command, result_path)


def execute_retrieval_command(command, result_path):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True)
        print(result.stdout)  # 打印命令的输出

        with open(result_path, 'w') as f:
            f.write(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(e.stderr)


pro = ["compose", "django_rest_framework", "flask", "keras", "pipenv", "requests", "scrapy", "spaCy", "tornado",
        "certbot"]
pro = ["certbot"]
for project in pro:
    index_path = f"F:\\Python_index\\{project}"
    query_path = f"F:\\Python_query\\{project}\\query"
    result_path = f"F:\\Python_result\\{project}\\result.txt"

    retrieve(query_path, result_path, index_path)

