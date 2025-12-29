import corpus

class TrainingCorpus(corpus.Corpus):
    def get_class(file_name):
    # Třídu vybavte metodou get_class(), jejímž vstupem bude název souboru s emailem a výstupem buď kód OK nebo SPAM.

# Váš filtr musí v adresáři testovacího korpusu vytvořit soubor !prediction.txt, v němž pro každý soubor s emailem v 
# testovacím korpusu uvede řádek nazevsouboru OK, jedná-li se (podle mínění filtru) o korektní email, nebo nazevsouboru SPAM, 
# jedná-li se (podle mínění filtru) o spam. 