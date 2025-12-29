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
        #TODO vytvoří v zadaném adresáři soubor !prediction.txt
        self.create_prediction_file(self.prediction)
        #print docasnej, jen testuju, pujde to do funkce ^ az bude hotova
        print(self.prediction)
        #output nic
    
    def cycle_emails(self, corp):
        for file, raw in corp.emails():
            sender_email, time_sent, subject, true_body = self.parse_email(raw)
            self.spam_likelihood = 0 #reset u kazdeho mailu
            if self.general_or_html(true_body):
                # TODO: add html specific checks here
                true_body = self.normalise_html_body(true_body) # strip do normalni podoby pro basic checks\

            self.check_double_inter(true_body)
            self.check_caps(true_body)
            # TODO tu dalsi kontroly...
            # ...
            if 
            self.prediction[file] = self.decide_if_spam_and_tag(self.spam_likelihood)

    def decide_if_spam_and_tag(self, likelihood):
        if likelihood >= SPAM_THRESHOLD:
            return SPAM_TAG
        return HAM_TAG

    def create_prediction_file(self, dictionary): #TODO vytvori txt soubor z dict
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
    
    def check_caps(self, body):
        caps_counter = 0
        for i in range(len(body)):
            if body[i].isupper():
                caps_counter += 1
            elif body[i].isspace() is False:
                caps_counter = 0
            if (caps_counter > 20):
                self.spam_likelihood += ps.TOO_MANY_CAPS_PENALTY
                caps_counter = 0

if __name__ == "__main__":
    filter = MyFilter()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, "funkce-testy", "simple_corpus")
    filter.test(path) #testovani na mini corpusu
