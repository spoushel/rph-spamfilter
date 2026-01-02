#FINALNI IMPORTANT FILE !!!
import email
import quality
import corpus
import confmat
import os
import dicts as ds
import penalties as ps
import re

SPAM_TAG = "SPAM"
HAM_TAG = "OK"

SPAM_THRESHOLD = 0.6
CAPS_THRESHOLD_1 = 2 #vcetne
CAPS_THRESHOLD_2 = 6 #vcetne
SUS_TIME_INTERVAL = 1, 5


class MyFilter:
    def __init__(self):
        self.spam_likelihood = 0
        self.prediction = {}
        
    def train(self, path_to_training_data): #adresar musi obsahovat !truth
        pass
        #Vytvoření a nastavení vnitřních datových struktur třídy, aby byly později využitelné metodou test()
    def test(self, path_to_corpus): # adresar s emails BEZ !truth
        corp = corpus.Corpus(path_to_corpus)
        self.cycle_emails(corp)
        self.create_prediction_file(self.prediction, path_to_corpus)
        #output nic
    
    def cycle_emails(self, corp):
        for file, raw in corp.emails():
            sender_email, time_sent, subject, true_body = self.parse_email(raw)
            self.spam_likelihood = 0 #reset u kazdeho mailu
            if self.general_or_html(true_body):
                # TODO: add html specific checks here
                self.check_domains(true_body, sender_email)
                true_body = self.normalise_html_body(true_body) # strip do normalni podoby pro basic checks\

            self.check_double_inter(true_body)
            self.check_caps(subject, 7) 
            self.check_sentence_end(true_body)
            self.check_comma_spaces(true_body)
            self.check_time(time_sent)
            self.check_capitalised_words(true_body)
            self.check_non_ascii_chars(subject, true_body)
            self.check_sender_chars(sender_email)
            # TODO tu dalsi kontroly...
            # ...
            #if 
            #print(self.spam_likelihood) # < pak vymazat
            self.prediction[file] = self.decide_if_spam_and_tag(self.spam_likelihood)

    def decide_if_spam_and_tag(self, likelihood):
        if likelihood >= SPAM_THRESHOLD:
            return SPAM_TAG
        return HAM_TAG

    def create_prediction_file(self, dictionary, corpus_path): #TODO vytvori txt soubor z dict
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

        true_body = "\n".join(lines[body_start_idx:]).lstrip("\n")
        return [sender_email, time_sent, subject, true_body]
    

    def special_punc_case(self, whole_string, punc_index):
        word = self.is_in_word(whole_string, punc_index)

        if word in ds.ABBREVIATION: # ustaleny zkratky
            return True
        if word.startswith("www.") or word.startswith("http"): # odkazy
            return True
        if word.find("@") != -1: # emailovy adresy
            return True
        for i in range(len(word)): # datum, cas, vse s cisly
            if (not word[i].isnumeric()) and (word[i] not in ds.INTERPUNCTION):
                break
            if i == range(len(word)):
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

            if (caps_counter > max_allowed):
                self.spam_likelihood += ps.TOO_MANY_CAPS_PENALTY # per cap
                #caps_counter = 0

    def check_capitalised_words(self, body):
        words = body.split()
        w_count = 0

        for w in words:
            t_w = w.strip(".,")

            if w.isupper() and len(t_w) > 3: # slova do 3 jsou pravdepodobne zkratky
                w_count += 1
                if w_count >= CAPS_THRESHOLD_2:
                    self.spam_likelihood += ps.CAP_WORDS_BIG_PENALTY
                elif w_count >= CAPS_THRESHOLD_1:
                    self.spam_likelihood += ps.CAP_WORDS_SMALL_PENALTY


    def check_time(self, time):
        if time[0] == "0" and SUS_TIME_INTERVAL[0] <= int(time[1]) < SUS_TIME_INTERVAL[1]:
            self.spam_likelihood += ps.WEIRD_TIME_PENALTY

    def check_non_ascii_chars(self, subject, body):
        if not subject.isascii() or not body.isascii():
            self.spam_likelihood + ps.NON_ASCII_PENALTY



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


    def check_sender_chars(self, sender):
        if not sender.isascii():
            self.spam_likelihood += ps.SENDER_NON_ASCII_PENALTY
        for ch in range(len(sender)):
            if sender[ch].isnumeric():
                self.spam_likelihood += ps.SENDER_NUMBER_PENALTY


                    



if __name__ == "__main__":
    filter = MyFilter()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, "spamfilter-data", "2")
    filter.test(path) #testovani na mini corpusu
    quality_score = quality.compute_quality_for_corpus(os.path.join(base_dir, "spamfilter-data", "2"))
    print(quality_score)
