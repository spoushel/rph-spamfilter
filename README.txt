
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
        *- HELCA: dlouhy vety bez tecek: vic nez 200 znaku mezi teckama (nebrat carky) = zadny 0.10, jinak each 0.05
        *- HELCA: chybi interpunkce skoro kompletne (delka chars body nejaky stovky/200) (i carky) = 0.1
        *- NELA: caps lock v nazvu (vic nez cca jedno slovo) = 0.015 
        *- NELA: pocet slov caps lockem - 2 - 5 = 0.15, vice jak 6 0.25
    - lists: (dictionary pro hodnotu kazdyho slova)
        *- HELCA: vsechny dicts do separate funkci podle zavaznosti
        *- NELA: domeny projet podle dict 
    - vlasnosti:
        *- NELA: mezi 1 a 5 rano je divny = 0.1 
        *- NELA: jazyk (?) pokud by nebylo anglicky, hledat znaky = pokud tam nejakej je, tak 0.2
        *- NELA: projet odkazy podle dict, final check
    - specificky pro html:
        *- HELCA: barvy: pocet (5+ mimo cerna, bila), typ bila/cerna/other = 0.1 (jestli to pujde)
    - pozitivni vlastnosti:
        *- HELCA: in-reply-to:, Reply-To: - automaticky HAM
        *- HELCA: pozitivni slova (newsletter) - odecist 0.3


moznosti pro ucici filter:
    -? pokud ma email spam skore pres [neco], tak vsechny dalsi emaily zarad do spamu automaticky
    - pokud maj aspon tri email spam skore pod [neco], tak vsechny dalsi automaticky nejsou spam (CNET?)
    - dicts spatnych slov a dobrych slov
        - slova ktery jsou hlavne ve spamu + kolikrat a v ok zpravach ne : pak s nima pracovat jako s tema dalsima
    - nejlepsi kombinace hodnot
