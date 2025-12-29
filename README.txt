
class MyFilter v filter.py, která bude mít minimálně dvě metody: train() a test()
metoda train():
    Vstupy 	Cesta k adresáři s ohodnocenými emaily, tj. adresář musí obsahovat soubor !truth.txt. (Pro jednoduché filtry je to jedno.)
    Výstupy 	Nic.
    Efekty 	Vytvoření a nastavení vnitřních datových struktur třídy, aby byly později využitelné metodou test().

metoda test():
    Vstupy 	Cesta k adresáři s maily. (Adresář nebude obsahovat soubor !truth.txt.)
    Výstupy 	Nic.
    Efekty 	Vytvoří v zadaném adresáři soubor !prediction.txt. 


? Nespoléhejte tedy na to, že všechny emaily budou mít subjekt, nebo další pole!!!

STRATEGIE:
- skore spam-likelihood od [0 OK] do [1 SPAM]
- defaultne to neni spam a pricitame body za spam-like qualities 
- defaultne je to spam od 0.6 (asi nastavit jako variable)
- basic filter:
    - pocet/opakovani overall: 
        - 5 je zaklad, vic nez (delka chars body/200)krat se zvysujou body = 0.1, dalsi 0.05
        - dlouhy vety bez tecek: vic nez 200 znaku mezi teckama (nebrat carky) = zadny 0.10, jinak each 0.05
        - chybi interpunkce skoro kompletne (delka chars body nejaky stovky/200) (i carky) = 0.1, pokud je to 0 nebo 1 tak 0.15
        - konkretni slovo, delsi nez 3 chary (15 a vickrat) = 0.1, ke kazdymu dalsimu nasobit 1.5
        - caps lock v nazvu (vic nez cca jedno slovo) = 0.1
    - pocet blizko u sebe:
        - 2 a vic u sebe tecek, vykricniku, otazniku nebo kombinace = 0.1
        - caps lock: vic nez 20 chars po sobe (mimo mezery) = 0.15
    - lists: (dictionary pro hodnotu kazdyho slova)
        + vzit v potaz mnozstvi celkove
        + rozdelit kategorie (jedno free je ok, jedna sexy single ne)
        - list nejbeznejsich slov co nam neva = nevadi jakykoliv mnozstvi
        - sexy singles explicit atd. = vadi 1 a vic, 0.2 per each
        - reklama/money of some sort: free, penize, cena, kvalita, sleva, dollars... = 5 a vic uz je bad, nasobit 1.2 pak u kazdyho dalsiho
        - divny countries typu Hawaii, Uganda nevim = jakejkoliv mention 0.1
        - urgency, prosby, requests, time left etc. = 2 a vic uz je bad, 0.05
        - duveryhodny domeny po @ [+ body pokud je to neco jinyho, country codes] = 0.2 za divnou domenu
    - vlasnosti:
        - velky pismena na zacatku vety = kdyz nejsou tak 0.15
        - mezi 1 a 5 rano je divny = 0.1 
        - jazyk (?) pokud by nebylo anglicky, hledat znaky = pokud tam nejakej je, tak 0.2
        - zamyslet se: pocet odkazu
        - divny links, http misto https = hodne sus 0.1
    - specificky pro html:
        - barvy: pocet (4+), typ bila/cerna/other = 0.1
        - html mismatched odkaz: odkazuje jinam nez to vypada (html?) = 0.1
    - odkazy projit na konci? pokud vypada sus


moznosti pro ucici filter:
    - hodne jich je odeslanych ze stejne adresy: asi je to spam adresa
    - pokud ma email spam skore pres [neco], tak vsechny dalsi emaily zarad do spamu automaticky
    - pokud ma email spam skore pod [neco], tak vsechny dalsi automaticky nejsou spam
    - pokud se nejaky slovo v jednom emailu objevi vic nez 15x tak ho zarad do listu spam keywords
    - dalsi...?