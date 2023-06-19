from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import math

def preprocess(document_text):
    terms = [term.lower() for term in document_text.strip().split()[1:]]
    return terms
documents = {}
documents_head = {}
vocab = {}
links = {}
filename = 'Leetcode-Questions-Scrapper/Qdata/index.txt'
with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for index, line in enumerate(lines):
    tokens = preprocess(line)
    if index not in documents_head:
        documents_head[index + 1] = tokens
filename = 'Leetcode-Questions-Scrapper/Qdata/Qindex.txt'
with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()
# print(lines)    
for index, line in enumerate(lines):
    if index not in documents_head:
        links[index + 1] = line

# print(documents_head)
for index in range (1, 2406):
    filename = 'Leetcode-Questions-Scrapper/Qdata/'
    with open(filename + str(index) + "/" + str(index) + ".txt", 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    example_index = next((i for i, line in enumerate(lines) if "Example 1" in line), None)
    
    # Extract the content until "Example 1"
    if example_index is not None:
        content = ''.join(lines[:example_index])
        lines = lines[:example_index]
    else:
        content = ''.join(lines)  # If "Example 1" is not found, use the entire content
        
    # print(content)  
    if index not in documents:
        documents[index] = str(content)    
    for id, line in enumerate(lines):
        tokens = preprocess(line)
        tokens = set(tokens)
        for token in tokens:
           if token not in vocab:
              vocab[token] = 1
           else:
              vocab[token] += 1

vocab = dict(sorted(vocab.items(), key=lambda item: item[1], reverse=True))
# print(vocab)    
# print(document)
with open('tf-idf/vocab.txt', 'w') as f:
    for keys in vocab.keys():
        f.write("%s\n" % keys)
with open('tf-idf/idf-values.txt', 'w') as f:
    for keys in vocab.keys():
        f.write("%s\n" % vocab[keys])        

with open('tf-idf/document.txt', 'w') as f:
   for document in documents_head: 
    f.write("%s\n" % ' '.join(documents_head[document]))

inverted_text = {}
for index in documents:
    for token in [term.lower() for term in documents[index].strip().split()[1:]]:
        if token not in inverted_text:
            inverted_text[token] = [index]
        else:
            inverted_text[token].append(index)   
# print(inverted_text)

for index in documents:
    documents[index] = [term.lower() for term in documents[index].strip().split()[1:]]
    # print(index,documents[index]) 

with open('tf-idf/inverted_text.txt', 'w') as f:
   for keys in inverted_text.keys():
       f.write("%s\n" % keys)
       f.write("%s\n" % ' '.join([str(doc_id) for doc_id in inverted_text[keys]]))


def load_inverted_index():
    inverted_index = {}
    with open('tf-idf/inverted_text.txt', 'r') as f:
        inverted_index_items = f.readlines()

    for row in range (0, len(inverted_index_items), 2):
        terms = inverted_index_items[row].strip()
        document = inverted_index_items[row + 1].strip().split()
        inverted_index[terms] = document
    return inverted_index


inverted_text = load_inverted_index()   


def get_tf_dictionary(term):
    tf_values = {}
    if term in inverted_text:
        for document in inverted_text[term]:
            if document not in tf_values:
                tf_values[document] = 1
            else:
                tf_values[document] += 1
    for document in tf_values:
        try:
          tf_values[document] /= len(documents[int(document)])
        except (ZeroDivisionError, ValueError, IndexError) as e:
            print(e)
            print(document)

    return tf_values


# print(len(documents))
def get_idf_values(term):
    return math.log(len(documents) / vocab[term])     


def calculate_sorted_order_of_documents(query_terms):
    potential_documents = {}
    for term in query_terms:
        if term not in vocab :
            continue
        tf_values_by_document = get_tf_dictionary(term)
        idf_value = get_idf_values(term)
        for document in tf_values_by_document:
            if document not in potential_documents:
                potential_documents[document] = tf_values_by_document[document] * idf_value
            potential_documents[document] += tf_values_by_document[document] * idf_value
    # print(potential_documents)
    for document in potential_documents:
        potential_documents[document] /= len(query_terms)
    
    potential_documents = dict(sorted(potential_documents.items(), key=lambda item: item[1], reverse=True))

    link_list = []
    score_list = []
    for document_id in potential_documents:
    # Check if the document_id is present in documents_head, otherwise provide a default value of an empty list
       document_head = documents_head.get(int(document_id), [])
       link = links.get(int(document_id), [])
       if document_head != [] and links != []:
        # print('Document: ',document_head,'Score :',potential_documents[document_id],'link :' ,link) 
        link_list.append({"Question Link":link, "Score":potential_documents[document_id]})    
    return link_list

# query_string = input('Enter your query: ')
# query_terms = [term.lower() for term in query_string.strip().split()]


# print(query_terms)
# ans=calculate_sorted_order_of_documents(query_terms) 
# print(ans)   
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'


class SearchForm(FlaskForm):
    search = StringField('Enter your query term', validators=[DataRequired()])
    submit = SubmitField('Search')


@app.route('/', methods=['GET', 'POST'])
def home():
    form = SearchForm()
    result = []
    if form.validate_on_submit():
        query = form.search.data
        query_ = [term.lower() for term in query.strip().split()]
        result = calculate_sorted_order_of_documents(query_)
        result = result[:15]
    return render_template('index.html', form=form, result=result)    