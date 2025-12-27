v dir funkce-testy jsou confmat, corpus, quality, utils (takovy, ze to proslo basic odevzdanim :P) 
+ testy na ne kdybychom je jeste potrebovaly

final soubor (filter.py) s tridou MyFilter bych asi vlozila primo do tohohle main folderu, vsechny ty
jiny kroky do subfolders (treba to simple-filters)

specifikace:
Abychom umožnili pozdější automatické testování vašeho finálního filtru, budeme vyžadovat, aby se třída 
vašeho filtru jmenovala MyFilter a byla umístěna v modulu filter.py. 

třídou, která bude mít minimálně dvě metody: train() a test()
metoda train():
    Vstupy 	Cesta k adresáři s ohodnocenými emaily, tj. adresář musí obsahovat soubor !truth.txt. (Pro jednoduché filtry je to jedno.)
    Výstupy 	Nic.
    Efekty 	Vytvoření a nastavení vnitřních datových struktur třídy, aby byly později využitelné metodou test().

metoda test():
    Vstupy 	Cesta k adresáři s maily. (Adresář nebude obsahovat soubor !truth.txt.)
    Výstupy 	Nic.
    Efekty 	Vytvoří v zadaném adresáři soubor !prediction.txt. 
