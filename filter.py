#FINALNI IMPORTANT FILE !!!
import email
import quality
import corpus
import confmat
import os
#tokenizace str.
#email.message_from_string(), email.message_from_file() umožní vytvořit objekt třídy Message z řetězce či přímo ze souboru.
#metoda Message.walk() pak umožní systematicky email procházet po jednotlivých částech.

SPAM_TAG = "SPAM"
HAM_TAG = "OK"

INTERPUNCTION = {".", ",", "?", "!", ";"}
SPAM_THRESHOLD = 0.6
DOUBLED_INTERPUNCTION_PENALTY = 0.1
TOO_MANY_CAPS_PENALTY = 0.15


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

# zakladnejsi funkce here, a pak je vyuzit do modulu? 

#counter = Counter(tokens)
#fce sorted()
    
    def cycle_emails(self, corp):
        for file, body in corp.emails():
            self.spam_likelihood = 0 #reset u kazdeho mailu
            self.check_double_inter(body)
            self.check_caps(body)
            # TODO tu dalsi kontroly...
            # ...
            self.prediction[file] = self.decide_if_spam_and_tag(self.spam_likelihood)

        
    def decide_if_spam_and_tag(self, likelihood):
        if likelihood >= SPAM_THRESHOLD:
            return SPAM_TAG
        return HAM_TAG

    def create_prediction_file(self, dictionary): #TODO vytvori txt soubor z dict
        pass


    def check_double_inter(self, body):
        for p in INTERPUNCTION:
            ch_index = 0
            while True:
                ch_index = body.find(p, ch_index)
                if ch_index == -1:
                    break

                if ch_index + 1 <len(body) and body[ch_index + 1] == p:
                    self.spam_likelihood += DOUBLED_INTERPUNCTION_PENALTY
                
                ch_index += 1
    
    def check_caps(self, body):
        caps_counter = 0
        for i in range(len(body)):
            if body[i].isupper():
                caps_counter += 1
            elif body[i].isspace() is False:
                caps_counter = 0
            if (caps_counter > 20):
                self.spam_likelihood += TOO_MANY_CAPS_PENALTY
                caps_counter = 0

if __name__ == "__main__":
    filter = MyFilter()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, "funkce-testy", "simple_corpus")
    filter.test(path) #testovani na mini corpusu
