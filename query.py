import math

def load_vocab():
    vocab={}
    with open('bootcamp_tf_idf/tf-idf/vocab.txt','r') as f:
        vocab_terms=f.readlines()   
    with open('bootcamp_tf_idf/tf-idf/idf-values.txt','r') as f:
        idf_values=f.readlines()

    for (term,id_value)in zip(vocab_terms,idf_values):
       vocab[term.strip()]=int(id_value.strip())
    return vocab

def load_documents():
    documents={}
    with open('bootcamp_tf_idf/tf-idf/document.txt','r') as f:
        documents=f.readlines()
    documents=[document.strip().split() for document in documents]
    print("Number of Documents ",len(documents))
    print("Sample Document ",documents[0])
    return documents

def load_inverted_index():
    inverted_index={}
    with open('bootcamp_tf_idf/tf-idf/inverted_text.txt','r') as f:
        inverted_index_items=f.readlines()

    for row in range (0,len(inverted_index_items),2):
        terms=inverted_index_items[row].strip()
        document=inverted_index_items[row+1].strip().split()
        inverted_index[terms]=document
    return inverted_index    

vocab_idf_values = load_vocab()
documents = load_documents()
inverted_index = load_inverted_index()

def get_tf_dictionary(term):
    tf_values={}
    if term in inverted_index:
        for document in inverted_index[term]:
            if document not in tf_values:
                tf_values[document]=1
            else:
                tf_values[document]+=1
    for document in tf_values:
        tf_values[document]/=len(documents[int(document)])
    return tf_values
def get_idf_values(term):
    return math.log(len(documents)/vocab_idf_values[term])                 


def calculate_sorted_order_of_documents(query_terms):
    potential_documents={}
    for term in query_terms:
        if vocab_idf_values[term]==0:
            continue
        tf_values_by_document=get_tf_dictionary(term)
        idf_value=get_idf_values(term)
        for document in tf_values_by_document:
            if document not in potential_documents:
                potential_documents[document]=tf_values_by_document[document]*idf_value
            potential_documents[document]+=tf_values_by_document[document]*idf_value
    print(potential_documents)
    for docuent in potential_documents:
        potential_documents[document]/=len(query_terms)
    
    potential_documents = dict(sorted(potential_documents.items(), key=lambda item: item[1], reverse=True))

    for document_id in potential_documents:
        print('Documents :',documents[int(document_id)],'Score :',potential_documents[document_id])


query_string = input('Enter your query: ')
query_terms = [term.lower() for term in query_string.strip().split()]

print(query_terms)
calculate_sorted_order_of_documents(query_terms)

