import gensim as gs
import numpy as np
stopwords = frozenset({"ourselves", "hers", "between", "yourself", "but", "again", "there", "about", "once", "during", "out", "very", "having", "with", "they", "own", "an", "be", "some", "for", "do", "its", "yours", "such", "into", "of", "most", "itself", "other", "off", "is", "s", "am", "or", "who", "as", "from", "him", "each", "the", "themselves", "until", "below", "are", "we", "these", "your", "his", "through", "don", "nor", "me", "were", "her", "more", "himself", "this", "down", "should", "our", "their", "while", "above", "both", "up", "to", "ours", "had", "she", "all", "no", "when", "at", "any", "before", "them", "same", "and", "been", "have", "in", "will", "on", "does", "yourselves", "then", "that", "because", "what", "over", "why", "so", "can", "did", "not", "now", "under", "he", "you", "herself", "has", "just", "where", "too", "only", "myself", "which", "those", "i", "after", "few", "whom", "t", "being", "if", "theirs", "my", "against", "a", "by", "doing", "it", "how", "further", "was", "here", "than"})
model = gs.models.KeyedVectors.load_word2vec_format('../../data/GoogleNews-vectors-negative300.bin', binary=True)
lda_model = None
id2word = None
corpus = None

vectors = []
file = open("test.txt")
content = file.read()

print("done loading model")
def split_paragraphs(raw_text):
    paras = raw_text.splitlines()
    paras = [p.strip() for p in paras]
    paras = [p for p in paras if p != '']
    return paras

pars = split_paragraphs(content)
def tokenize(raw_para):#return  list of strings
    sentences = gs.summarization.textcleaner.split_sentences(raw_para) # list of sentences
    lemmatized = [gs.utils.lemmatize(s,stopwords = stopwords) for s in sentences]# lemmatizes and tokenizes, return list of list of tokens
    for i in range(len(lemmatized)):
        for j in range(len(lemmatized[i])):
            lemmatized[i][j] = lemmatized[i][j].decode('ascii')[:-3]
    return lemmatized

def cons_tokenize(raw_para):
    sentences = gs.summarization.textcleaner.split_sentences(raw_para) # list of sentences
    lemmatized = [gs.utils.lemmatize(s) for s in sentences]# lemmatizes and tokenizes, return list of list of tokens
    for i in range(len(lemmatized)):
        for j in range(len(lemmatized[i])):
            lemmatized[i][j] = lemmatized[i][j].decode('ascii')[:-3]
    return lemmatized

def preprocess(raw_text):
    paras = split_paragraphs(raw_text)#list of paragraphs
    tokens = [tokenize(p) for p in paras] #list (paragraphs) of list(sentences) of list (per word) of tokens
    phrases = gs.models.phrases.Phrases(sentences = [sentence for paragraph in tokens for sentence in paragraph], delimiter = b'_', common_terms = stopwords)
    gram = [[]]
    for i in range(len(tokens)):
        gram.append([])
        gram[i].extend([phrases[s] for s in tokens[i]])# list(sentences) of list(per word) of bigrams
    gram = list(filter(lambda x: x!=[], gram))
    return gram #list (paragraphs) of list(sentences) of list (per word) of bigrams

def vectorize(word):
    return model[word]

def mass_vectorize(grams):
    global vectors
    global id2word
    global corpus
    flattened = []
    for paragraph in grams:
        flattened.append([gram for sentence in paragraph for gram in sentence])
    id2word = gs.corpora.Dictionary(flattened)
    # Create Corpus
    texts = flattened
    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]
    vectors = []
    for i in range(len(grams)):
        paragraph = grams[i]
        vectors.append([])
        for j in range(len(paragraph)):
            sentence = paragraph[j]
            vectors[i].append([])
            for k in range(len(sentence)):
                word = sentence[k]
                vectors[i][j].append(vectorize(word))


def train_lda():
    global lda_model
    lda_model = gs.models.LdaModel(corpus = corpus, id2word = id2word, num_topics = 3)

def kill_dims(vectors):
    return [word for paragraph in vectors for sentence in paragraph for word in sentence]

def do_lda(grams):
    doc_grams = [gram for paragraph in grams for sentence in paragraph for gram in sentence]
    corpus = id2word.doc2bow(doc_grams)
    topic_dist, topics_per_word, phis = lda_model.get_document_topics(bow = corpus, per_word_topics = True)
    return topic_dist, topics_per_word, phis

def decompose_bigram(gram, topics_per_word):
    unigrams = gram.split(separator = '_')
    words = []
    for unigram in unigrams:
        id = id2word.token2id[unigram]
        words.append(Word("null", unigram, id, topics_per_word[id][1][0]))
    return words

def stable_matching(raw_para, grams, topics_per_word):
    input = cons_tokenize(raw_para) #postlemma
    fixed_grams = []
    word_list = []
    for j in grams:
        if j.contains("_"):
            fixed_grams.extend(decompose_bigram(j,topics_per_word))
        else:
            fixed_grams.append(j)

    for i in range(len(input)):
        if input[i].lower()==fixed_grams[i].lower():
            word_list.append(Word(raw_para[i],input[i],fixed_grams[i].id,fixed_grams[i].topic))
        elif:
            word_list.append(Word(input[i],input[i],None,None))
    return word_list

class Word:
    def __init__(self, prelemma,postlemma, id, topic):
        self.prelemma = prelemma
        self.postlemma = postlemma
        self.id = id
        self.topic = topic
