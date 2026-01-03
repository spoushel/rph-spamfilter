import email
import confmat
import quality
import corpus
import os
import dicts as ds
import penalties as ps
import re
import sys

SPAM_TAG = "SPAM"
HAM_TAG = "OK"

class MyFilter:
    def __init__(self):
        self.spam_likelihood = 0
        self.prediction = {}
        self.scores = {}
        
    def train(self, path_to_training_data): #adresar musi obsahovat !truth
        pass
    def test(self, path_to_corpus): # adresar s emails BEZ !truth
        corp = corpus.Corpus(path_to_corpus)
        self.cycle_emails(corp)
        self.create_prediction_file(self.prediction, path_to_corpus)
    
    def cycle_emails(self, corp):
        for file, raw in corp.emails():
            sender_email, time_sent, subject, true_body, reply_flag = self.parse_email(raw)
            self.spam_likelihood = 0 #reset u kazdeho mailu
            if self.general_or_html(true_body):
                self.check_html_colours(true_body)
                self.check_domains(true_body, sender_email)
                true_body = self.normalise_html_body(true_body) # strip do normalni podoby pro basic checks
            #TODO helca stuffs
            self.check_num_interpunction(true_body)
            self.check_double_inter(true_body)
            self.check_caps(subject, 7) 
            self.check_sentence_end(true_body)
            self.check_comma_spaces(true_body)
            self.check_time(time_sent)
            self.check_capitalised_words(true_body)
            self.check_non_ascii_chars(subject, true_body)
            self.check_sender_chars(sender_email)
            self.check_newsletter(subject, true_body)
            self.check_subject(subject)
            #self.check_sus_char(true_body, "%", ps.TOO_MANY_PERC_CHAR_PENALTY, ps.PERC_CHAR_THRESHOLD)
            # ^ lehce zhorsuje skore (o 0.003 v prvni sade, o 0.14 v druhe sade)

            #dict checks
            self.check_dict(true_body, ds.EXPLICIT, ps.DICT_EXPLICIT, ps.NUM_EXPLICIT)
            self.check_dict(true_body, ds.EXPLICIT_S, ps.DICT_EXPLICIT_S, ps.NUM_EXPLICIT_S)
            self.check_dict(true_body, ds.COUNTRIES, ps.DICT_COUNTRIES, ps.NUM_COUNTRIES)
            self.check_dict(true_body, ds.AGRESSION, ps.DICT_AGRESSION, ps.NUM_AGRESSION)
            self.check_dict(true_body, ds.MONEY, ps.DICT_MONEY, ps.NUM_MONEY)
            self.check_dict(true_body, ds.URGENCY, ps.DICT_URGENT, ps.NUM_URGENT)
            self.check_dict(true_body, ds.GOOD_WORDS, ps.GOOD_BONUS, ps.NUM_GOOD)

            if not reply_flag:
                reply_flag = self.is_trusted_domain(sender_email)
            
            if reply_flag == True:
                    self.spam_likelihood = 0 #reset pokud je to reply (100% sure ze je to ok)
            self.scores[file] = self.spam_likelihood #pro better_res script
            self.prediction[file] = self.decide_if_spam_and_tag(self.spam_likelihood)

    def decide_if_spam_and_tag(self, likelihood):
        if likelihood >= ps.SPAM_THRESHOLD:
            return SPAM_TAG
        return HAM_TAG

    def create_prediction_file(self, dictionary, corpus_path): 
        with open(os.path.join(corpus_path, "!prediction.txt"), "w") as f:
            for key in dictionary.keys():
                f.write(key + " " + dictionary[key] +"\n")
        pass

    def general_or_html(self, true_body):
        lower = true_body.lower()
        return any(tag in lower for tag in ("<html>", "<body>", "<br>", "<head", "<div"))
    
    def normalise_html_body(self, true_body):
        text = re.sub(r"<[^>]+>", "", true_body)  # strip anything co je <[sth]>
        text = " ".join(text.split())
        return text

    def parse_email(self, body): #vrati [sender email, time sent, subject, true body]
        sender_email, time_sent, subject, true_body = "", "", "", ""
        reply_flag = False

        text = body.replace("\r\n", "\n").replace("\r", "\n")
        lines = text.split("\n")

        in_headers = True
        body_start_idx = 0

        for idx, line in enumerate(lines):
            if in_headers:
                if line.strip() == "":
                    in_headers = False
                    body_start_idx = idx + 1
                    break

            if line.startswith("From:"): 
                for word in line.split():
                    if '@' in word:
                        sender_email = word.strip('<>"\'()[]')
            if line.startswith("Subject:"): 
                subject = line.split(":", 1)[1].strip() if ":" in line else ""
            if line.startswith("Date:"):
                for word in line.split():
                    if ':' in word:
                        time_sent = word
            low = line.lower()
            if low.startswith("in-reply-to:"): #or line.startswith("References:") or line.startswith("Reply-To:") 
                reply_flag = True


        true_body = "\n".join(lines[body_start_idx:]).lstrip("\n")
        return [sender_email, time_sent, subject, true_body, reply_flag]
    

    def special_punc_case(self, whole_string, punc_index):
        word = self.is_in_word(whole_string, punc_index)

        if word in ds.ABBREVIATION: # ustaleny zkratky
            return True
        if word.startswith("www.") or word.startswith("http"): # odkazy
            return True
        if word.find("@") != -1: # emailovy adresy
            return True
        for ch in word: # datum, cas, vse s cisly
            if (not ch.isnumeric()) and (ch not in ds.INTERPUNCTION):
                break
        else:
                return True
        
        return False
    
    def is_in_word(self, body, char_index): #vrati slovo ve kterem se char nachazi
        index_counter = 0
        for word in body.split():
            body_start = index_counter
            body_end = index_counter + len(word)
            if body_start <= char_index < body_end:
                return word
            index_counter = body_end + 1 # 1 kvuli mezere
        
        return body[char_index]  
    
    ## ACTUAL TESTY

    def check_subject(self, subject):

        for word in ds.AGRESSION:
            if word in subject:
                self.spam_likelihood += ps.SUBJECT_AGRESSION_PENALTY
        for word in ds.EXPLICIT:
            if word in subject:
                self.spam_likelihood += ps.SUBJECT_EXPLICIT_PENALTY
        for word in ds.EXPLICIT_S:
            if word in subject:
                self.spam_likelihood += ps.SUBJECT_EXPLICIT_S_PENALTY
        for word in ds.URGENCY:
            if word in subject:
                self.spam_likelihood += ps.SUBJECT_URGENT_PENALTY


    def check_sus_char(self, body, char, threshold, penalty): # konkretne pro %, mozna prijdem na vice pouziti...
        if body.count(char) >= threshold:
            self.spam_likelihood += penalty


    def check_double_inter(self, body):
        for p in ds.INTERPUNCTION:
            ch_index = 0
            while True:
                ch_index = body.find(p, ch_index)
                if ch_index == -1:
                    break

                if ch_index + 1 <len(body) and body[ch_index + 1] == p:
                    self.spam_likelihood += ps.DOUBLED_INTERPUNCTION_PENALTY
                
                ch_index += 1
    
    def check_caps(self, string, max_allowed): # ted pouzit pro kontrolu predmetu
        caps_counter = 0
        for i in range(len(string)):
            if string[i].isupper():
                caps_counter += 1

        excess = caps_counter - max_allowed
        if excess > 0:
            self.spam_likelihood += ps.TOO_MANY_CAPS_PENALTY * excess 

    def check_capitalised_words(self, body):
        words = body.split()
        cw_count = 0
        total_count = len(words)
        if total_count >= ps.WORDS_FOR_THRESHOLD_MULTIPLIER:
            thr_multiplier = 2
        else:
            thr_multiplier = 1 

        for w in words:
            t_w = w.strip(".,")

            if w.isupper() and len(t_w) > 3: # slova do 3 jsou pravdepodobne zkratky
                cw_count += 1

        if cw_count >= ps.CAPS_THRESHOLD_2 * thr_multiplier:
            #print("first: " + str(total_count))
            self.spam_likelihood += ps.CAP_WORDS_BIG_PENALTY
        elif cw_count >= ps.CAPS_THRESHOLD_1 * thr_multiplier:
            #print("second: " + str(total_count))
            self.spam_likelihood += ps.CAP_WORDS_SMALL_PENALTY


    def check_time(self, time):
        if time[0] == "0" and ps.SUS_TIME_INTERVAL[0] <= int(time[1]) < ps.SUS_TIME_INTERVAL[1]:
            self.spam_likelihood += ps.WEIRD_TIME_PENALTY

    def check_non_ascii_chars(self, subject, body):
        if not subject.isascii() or not body.isascii():
            self.spam_likelihood += ps.NON_ASCII_PENALTY

    def check_sentence_end(self, body): # kontroluje jestli je na konci vety mezera a velke pismeno
        ch_index = 0
        end_interp = [".", "!", "?"]
        for p in end_interp:
            while True:
                ch_index = body.find(p, ch_index)
                if ch_index == -1:
                    break

                if self.special_punc_case(body, ch_index):
                    break

                if ch_index + 1 <len(body) and not body[ch_index + 1].isspace():
                    self.spam_likelihood += ps.MISSING_SPACE_PENALTY 
                    if body[ch_index + 1].islower(): 
                        self.spam_likelihood += ps.MISSING_CAPITALISATION_PENALTY 

                elif ch_index + 2 <len(body) and body[ch_index + 2].islower(): 
                    self.spam_likelihood += ps.MISSING_CAPITALISATION_PENALTY

                ch_index += 1

    def check_comma_spaces(self, body): # kontroluje mezery po , ; :
        ch_index = 0
        punctuation = [",", ";", ":"]
        for p in punctuation:
            while True:
                ch_index = body.find(p, ch_index)
                if ch_index == -1:
                    break

                if self.special_punc_case(body, ch_index):
                    break
                
                if ch_index + 1 <len(body) and not body[ch_index + 1].isspace():
                    self.spam_likelihood += ps.MISSING_SPACE_PENALTY
                ch_index += 1

    def check_domains(self, body, sender):
        words = body.split()
        links = []

        for w in words:
            if w.startswith("www.") or w.startswith("http"):
                links.append(w)

        for not_exp in ds.NOT_EXPLICIT:  
            # at ignoruje napr. hotmail, score se nam ale zhorsilo po teto zmene lol...mozna zkontrolovat znova az budem mit zbytek kontrol
            #TODO jen pripadna kontrola ^
            sender = sender.replace(not_exp, "")

        for explicit in ds.EXPLICIT:
            if explicit in sender:
                self.spam_likelihood += ps.SEXY_SENDER_PENALTY
            for l in links:
                if explicit in l:
                    self.spam_likelihood += ps.SEXY_LINK_PENALTY

        for money in ds.MONEY:
            if money in sender:
                self.spam_likelihood += ps.MONEY_SENDER_PENALTY
            for l in links:
                if money in l:
                    self.spam_likelihood += ps.MONEY_LINK_PENALTY

        for good in ds.GOOD_WORDS:
            for l in links:
                if good in l:
                    self.spam_likelihood += ps.GOOD_BONUS

        


    def is_trusted_domain(self, sender):
        for dom in ds.TRUSTED_DOMAINS:
            if sender.endswith(dom):
                return True
        return False

    def check_sender_chars(self, sender):
        if not sender.isascii():
            self.spam_likelihood += ps.SENDER_NON_ASCII_PENALTY
        for ch in range(len(sender)):
            if sender[ch].isnumeric():
                self.spam_likelihood += ps.SENDER_NUMBER_PENALTY

    def check_newsletter(self, subject, body):
        words_sub = subject.split()
        words_body = body.split()

        for w in (words_sub + words_body):
            t_w = w.strip(".,!?").lower()
            if t_w in ds.GOOD_WORDS:
                self.spam_likelihood -= ps.GOOD_BONUS
                break
    
    def check_html_colours(self, body):
        matches_hex = re.findall(r"#[0-9a-fA-F]{6}(?![0-9a-fA-F])", body)
        ignored_hex = {"#000000", "#ffffff", "#cccccc"}
        filtered_matches = {m.lower() for m in matches_hex} - ignored_hex

        if len(filtered_matches) > 5:
            self.spam_likelihood += ps.HTML_COLOURS_PENALTY

    # dictionaries

    def check_dict(self, body, DICT, PENALTY, PEN_NUM):
        count = 0
        words = [w.strip(".,!?").lower() for w in body.split()]

        for w in words:
            if w in DICT:
                count += 1

        if DICT in (ds.MONEY, ds.URGENCY):
            excess = count - PEN_NUM
            if excess > 0:
                self.spam_likelihood += excess * PENALTY
        elif count >= PEN_NUM:
            self.spam_likelihood += PENALTY

    def check_num_interpunction(self, body):
        l = len(body)
        total = 0
        for p in ds.INTERPUNCTION:
            ch_index = 0
            while True:
                ch_index = body.find(p, ch_index)
                if ch_index == -1:
                    break
                total += 1
                ch_index += 1
        threshold = max(1, l // 200)
        if total < threshold:
            self.spam_likelihood += ps.LITTLE_INTERPUNCTION_PENALTY

    def check_interpunction_gaps(self, body):
        positions = []
        for p in ds.INTERPUNCTION:
            ch_index = 0
            while True:
                ch_index = body.find(p, ch_index)
                if ch_index == -1:
                    break
                positions.append(ch_index)
                ch_index += 1

        positions.sort()

        if not positions:
            if len(body) > 200:
                self.spam_likelihood += ps.LITTLE_INTERPUNCTION_PENALTY
            return

        prev = positions[0]
        for idx in positions[1:]:
            if idx - prev > 200:
                self.spam_likelihood += ps.LITTLE_INTERPUNCTION_PENALTY
                break
            prev = idx



if __name__ == "__main__":
    f = MyFilter()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    corpus_folder = sys.argv[1] if len(sys.argv) > 1 else "1"
    corpus_dir = os.path.join(base_dir, "spamfilter-data", corpus_folder)

    # run and write predictions
    f.test(corpus_dir)  # ensure this calls cycle_emails and then create_prediction_file

    # compute quality from the written files for consistency
    q = quality.compute_quality_for_corpus(corpus_dir)
    print(f"{q:.6f}")
