# chci aby to vzalo file name z !better_res.txt ktery nefunguje a vyhodilo to score analysis for it
import os
import sys
import corpus
from filter import MyFilter

def analyze_email(corpus_dir, email_id):
    corp = corpus.Corpus(corpus_dir)
    filter = MyFilter()

    filter.cycle_emails(corp)
    
    if email_id not in filter.scores:
        print(f"{email_id} not found")
        return

    score = filter.scores[email_id]
    
    out_path = os.path.join(corpus_dir, "!score_analysed.txt")
    with open(out_path, "w", encoding="utf-8") as file:
        file.write(f"Score analysis for {email_id}\n")
        file.write(f"Final score: {score:.3f}\n\n")
        for label, delta in filter.all_logs.get(email_id, []):
            file.write(f"{label:40s} {delta:+.3f}\n")
    
if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    corpus_folder = sys.argv[1] if len(sys.argv) > 1 else "1"
    corpus_dir = os.path.join(base_dir, "spamfilter-data", corpus_folder)
    email_id = sys.argv[2] if len(sys.argv) > 1 else "00002.9438920e9a55591b18e60d1ed37d992b"
    analyze_email(corpus_dir, email_id)

