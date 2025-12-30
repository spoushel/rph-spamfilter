INTERPUNCTION = {".", ",", "?", "!", ";"}

ABBREVIATION = {"a.m", "p.m", "P.S", "e.g", "i.e", "N.B", "q.v"}


# dictionary pro hodnotu kazdyho slova, jak moc ho penalizujem
# vzit v potaz mnozstvi celkove
# rozdelit kategorie (jedno free je ok, jedna sexy single ne)
# list nejbeznejsich slov co nam neva = nevadi jakykoliv mnozstvi


# sexy singles explicit atd. = vadi 1 a vic, 0.2 per each
EXPLICIT = {"sexy", "single", "singles", "hot"}

# nejcastejsich 60 slov v anglictine podle wikipedie
IGNORED = {"the", "be", "to", "of", "and", "a", "in", "that", "have", "i", 
           "it", "for", "not", "on", "with", "he", "as", "you", "do", "at", 
           "this", "but", "his", "by", "from", "they", "we", "say", "her", 
           "she", "or", "an", "will", "my", "one", "all", "would", "there",
           "their", "what", "so", "up", "out", "if", "about", "who", "get",
           "which", "go", "me", "when", "make", "can", "like", "time", "no", 
           "just", "him", "know", "take"}

# reklama/money of some sort: free, penize, cena, kvalita, sleva, dollars... 
# 5 a vic uz je bad, nasobit 1.2 pak u kazdyho dalsiho
MONEY = {"free", "money", "sale", "gift", "dollar", "dollars", "USD", "million"}

# divny countries typu Hawaii, Uganda nevim = jakejkoliv mention 0.1
# nevim jaky vsechny zaradit, zkusim najit nejaky lists
COUNTRIES = {"Uganda", "Hawaii", "Nigeria", "Morocco"} 

URGENCY = {"please", "give", "send", "beg", "begging", "urgent", "important", 
           "crucial", "immediately", "asap", "soon", "need"}
# urgency, prosby, requests, time left etc. = 2 (3?) a vic uz je bad, 0.05

GOOD_DOMAINES = {"gmail.com"} #lol actuall nevim :3
# duveryhodny domeny po @ [+ body pokud je to neco jinyho, country codes] = 0.2 za divnou domenu