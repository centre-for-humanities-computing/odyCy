import json
from pathlib import Path
import pandas as pd


METRICS_DIR = 'metrics/'
md = Path(METRICS_DIR)


keys_of_interest = [
    'token_acc', 'token_p', 'token_r', 'token_f',
    'tag_acc', 'pos_acc', 'morph_acc', 
    'sents_p', 'sents_r', 'sents_f',
    'dep_uas', 'dep_las', 
    'lemma_acc', 'ents_p', 'ents_f',
    'speed'
    ]


results = []
for model_dir in md.iterdir():
    # last element of path is model name
    model_name = model_dir.parts[-1]
    # iterate through versions
    for version_dir in model_dir.iterdir():
        model_version = version_dir.parts[-1]
        # iterate though evaluation corpora
        for corpus_dir in version_dir.iterdir():
            eval_corpus = corpus_dir.parts[-1]
            # iterture thourgh model checkpoints
            for metric_file in corpus_dir.iterdir():
                # checkpoint name
                checkpoint_name = metric_file.stem
                # load file
                with open(metric_file) as fin:
                    metrics = json.load(fin)
                
                # initialize thing
                out = {
                    'model': model_name,
                    'version': model_version,
                    'corpus': eval_corpus,
                    'checkpoint': checkpoint_name,
                }

                # append metrics
                for key in keys_of_interest:
                    if key in metrics.keys():
                        out.update({key: metrics[key]})
                    else:
                        out.update({key: None})

                results.append(out)


results_table = pd.DataFrame(results)
results_table.to_csv('results.csv')
