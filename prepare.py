import chardet
filename = './Leetcode-Questions-Scrapper/Qdata/index.txt'

with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

print(lines)


def preprocess(document_text):
    terms=[term.lower() for term in document_text.strip().split()[1:]]
    return terms

documents=[]
vocab={}
for index,line in enumerate(lines):
    tokens=preprocess(line)
    # print(tokens)
    documents.append(tokens)
    tokens=set(tokens)
    for token in tokens:
        if token not in vocab:
            vocab[token]=1
        else:
            vocab[token]+=1
print("Size of vocab ", len(vocab))            
# print(vocab)
vocab = dict(sorted(vocab.items(), key=lambda item: item[1], reverse=True))

with open('bootcamp_tf_idf/tf-idf/vocab.txt','w') as f:
    for keys in vocab.keys():
        f.write("%s\n" % keys)

with open('bootcamp_tf_idf/tf-idf/idf-values.txt','w') as f:
    for keys in vocab.keys():
        f.write("%s\n" % vocab[keys])

with open('bootcamp_tf_idf/tf-idf/document.txt','w') as f:
   for document in documents: 
    f.write("%s\n" % ' '.join(document))

inverted_text={}

for index,document in enumerate(documents):
    for token in document:
        if token not in inverted_text:
            inverted_text[token]=[index]
        else:
            inverted_text[token].append(index)    

with open('bootcamp_tf_idf/tf-idf/inverted_text.txt','w') as f:
   for keys in inverted_text.keys():
       f.write("%s\n" % keys)
       f.write("%s\n" % ' '.join([str(doc_id) for doc_id in inverted_text[keys]]))

