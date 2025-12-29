import utils
import confmat
import os

def quality_score(tp, tn, fp, fn):
    score = (tp+tn)/(tp+tn+10*fp+fn)
    return score

# q=(TP+TN)/(TP+TN+10⋅FP+FN) 

def compute_quality_for_corpus(corpus_dir):
    truth_file = os.path.join(corpus_dir, "!truth.txt") 
    truth_dict = utils.read_classification_from_file(truth_file)
    prediction_file = os.path.join(corpus_dir, "!prediction.txt")
    prediction_dict = utils.read_classification_from_file(prediction_file)
    pos_tag="SPAM"
    neg_tag="OK"

    confmat_fc = confmat.BinaryConfusionMatrix(pos_tag, neg_tag)
    confmat_fc.compute_from_dicts(truth_dict, prediction_dict)
    matrix = confmat_fc.as_dict()
    score = quality_score(matrix["tp"], matrix["tn"], matrix["fp"], matrix["fn"])
    return score