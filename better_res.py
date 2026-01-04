#script na porovnani co mame spatne, se spam likelihood, nahore co je FP potom FN (pridat i do predictions)
from filter import MyFilter
import corpus 
import os
import quality
import sys

TAGS = {"SPAM", "OK"}

def load_info_file(path_to_file):
    out = {}
    with open(path_to_file, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                key, tag = parts[0], parts[1].upper()
                if tag in TAGS:
                    out[key] = tag
    return out

def create_better_results(path_to_corpus, path_to_training_corpus):
    pred = load_info_file(os.path.join(path_to_corpus, "!prediction.txt"))
    truth = load_info_file(os.path.join(path_to_corpus, "!truth.txt"))

    corp = corpus.Corpus(path_to_corpus)
    f = MyFilter()
    f.train(path_to_training_corpus)
    f.cycle_emails(corp)
    scores = f.scores
    pred = f.prediction
    try:
        f.create_prediction_file(pred, path_to_corpus)
    except Exception:
        pass

    wrong_spam = []
    wrong_ok = []
    common = pred.keys() & truth.keys()
        
    for k in sorted(common):
        if pred[k] != truth[k]:
            if pred[k] == "SPAM" and truth[k] == "OK":
                wrong_spam.append(k)
            elif pred[k] == "OK" and truth[k] == "SPAM":
                wrong_ok.append(k)
    score = quality.compute_quality_for_corpus(path_to_corpus)

    out_path = os.path.join(path_to_corpus, "!better_res.txt")
    with open(out_path, "w", encoding="utf-8") as f_out:
        f_out.write(f"Quality score: {score:.3f}\n")
        f_out.write("\n")
        for k in wrong_spam:
            s = float(scores.get(k, 0.0))
            f_out.write(f"{k} | score: {s:.3f} | wrong: SPAM, ma byt: OK\n")
        f_out.write("\n")
        for k in wrong_ok:
            s = float(scores.get(k, 0.0))
            f_out.write(f"{k} | score: {s:.3f} | wrong: OK, ma byt: SPAM\n")
    

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    corpus_folder = sys.argv[1] if len(sys.argv) > 1 else "1"
    corpus_dir = os.path.join(base_dir, "spamfilter-data", corpus_folder)

    training_corpus_folder = sys.argv[2] if len(sys.argv) > 2 else "2"
    training_corpus_dir = os.path.join(base_dir, "spamfilter-data", training_corpus_folder)

    create_better_results(corpus_dir, training_corpus_dir)
