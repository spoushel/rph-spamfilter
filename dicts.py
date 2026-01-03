INTERPUNCTION = {".", ",", "?", "!", ";"}

ABBREVIATION = {"a.m", "p.m", "P.S", "e.g", "i.e", "N.B", "q.v"}

EXPLICIT = {"sexy", "sex", "porn", "single", "singles", "freaky", "adult",
            "slut", "sluts", "whore", "nude", "sexual",}

EXPLICIT_S = {"girlfriend", "boyfriend", "cigarettes", "cigarette", "tobacco", "hot"
                "alcohol", "cams", "sneaky", "fat", "diet", "dieting", "wrinkle", "weight"}

NOT_EXPLICIT = {"hotmail"}

AGRESSION = {"war", "crime", "protect", "protected", "criminal", "protecting"}

# nejcastejsich 60 slov v anglictine podle wikipedie
IGNORED = {"the", "be", "to", "of", "and", "a", "in", "that", "have", "i", 
           "it", "for", "not", "on", "with", "he", "as", "you", "do", "at", 
           "this", "but", "his", "by", "from", "they", "we", "say", "her", 
           "she", "or", "an", "will", "my", "one", "all", "would", "there",
           "their", "what", "so", "up", "out", "if", "about", "who", "get",
           "which", "go", "me", "when", "make", "can", "like", "time", "no", 
           "just", "him", "know", "take"}

MONEY = {"free", "money", "sale", "gift", "dollar", "dollars", "USD", "million", 
        "insurance", "rate", "rates", "pay", "financial", "savings", "save",
        "affordable", "value", "quote", "merchant", "debt", "credit", "debit", "income", "wealth", "marketing", "pricing", "price",
        "cash", "fee", "fees", "offer", "ad", "lottery", "jackpot", "inheritance", "donation",
        "bank", "transfer", "sales", "employment", "jon"}

COUNTRIES = {"Uganda", "Hawaii", "Nigeria", "Morocco", "Ghana", "Cameron", "Senegal", "prince", "king", "queen"} 
#japan

URGENCY = {"please", "give", "send", "beg", "begging", "urgent", "important", 
           "crucial", "immediately", "asap", "soon", "need", "minute", "minutes"
           "safety", "chance", "help", "needs"}

GOOD_WORDS = {"java", "linux", "c++", "thanks", "javascript", "tech"
              "intel", "techs", "windows", "CNET", "IT", "news", "edu"}

TRUSTED_DOMAINS = {".edu", ".gov", ".mil",  ".int"}