from evaluation.evaluation import evaluation

def BF(test_bugs):
    for issue in test_bugs:
        files = {}
        for i in range(len(issue.artifacts)-1, -1, -1):
            files_set = set(f.new_filePath for f in issue.artifacts[i].files if f.new_filePath!="/dev/null" and f.new_filePath is not None)
            source_len = len(files_set)
            for f in files_set:
                if (f in files.keys()):
                    files[f] = files[f] + issue.artif_sim[i] / source_len
                else:
                    files[f] = issue.artif_sim[i] / source_len

        sorted_files = sorted(files.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        # issue.predict_bf = [x[0] for x in sorted_files if x[0] in issue.source_files]
        issue.predict_bf = [x[0] for x in sorted_files if x[0] in issue.source_files]

    # evaluation
    ground_truth = [set(f.new_filePath for f in issue.files if f.new_filePath!="/dev/null" and f.new_filePath is not None) for issue in test_bugs]
    predict_result = [issue.predict_bf for issue in test_bugs]

    evaluation(ground_truth, predict_result)



