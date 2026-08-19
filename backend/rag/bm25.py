import re
from collections import Counter

def tokenizer(text):
    return re.findall(r"\w+",text.lower())

documents = ["Muscle growth, happens through resistance training!"]

tokenized_documents = []
for doc in documents:
    token = tokenizer(doc)
    tokenized_documents.append(token)

print(tokenized_documents)

term_freq = []
for token in tokenized_documents:
    tf = Counter(token)
    term_freq.append(tf)
    
print(term_freq[0])


