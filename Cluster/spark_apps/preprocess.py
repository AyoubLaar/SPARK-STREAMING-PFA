import preprocessor  as p
import re
from string import punctuation
from wordcloud import STOPWORDS
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
import nltk
from nltk.stem import PorterStemmer

nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

p.set_options(p.OPT.URL,p.OPT.MENTION,p.OPT.RESERVED,p.OPT.EMOJI,p.OPT.SMILEY,p.OPT.NUMBER)
contractions_dict = {"ain't": "are not","'s":" is","aren't": "are not"}
contractions_re=re.compile('(%s)' % '|'.join(contractions_dict.keys()))
lemmatizer = WordNetLemmatizer()
ps = PorterStemmer()
MAX_SEQUENCE_LENGTH = 280
VOCAB_SIZE = 10000

def lemmatize_stem_words(text):
    tokens = text.split(" ")
    tagged_tokens = nltk.pos_tag(tokens)
    return " ".join([ps.stem(lemmatizer.lemmatize(word,penn_to_wn(pos))) for word,pos in tagged_tokens])

def penn_to_wn(tag):
    if tag.startswith('J'):
        return wn.ADJ
    elif tag.startswith('N'):
        return wn.NOUN
    elif tag.startswith('R'):
        return wn.ADV
    elif tag.startswith('V'):
        return wn.VERB
    return "n"

def expand_contractions(text,contractions_dict=contractions_dict):
    def replace(match):
        return contractions_dict[match.group(0)]
    return contractions_re.sub(replace, text)


def split_camel_case(word):
    # Regular expression to match camel case patterns, including acronyms
    split_words = re.sub('([a-z0-9])([A-Z])', r'\1 \2', word)
    split_words = re.sub('([A-Z])([A-Z][a-z])', r'\1 \2', split_words)
    return " ".join(split_words.split())

def preprocess(text):
    text = p.clean(text)
    text = re.sub(f'[{re.escape(punctuation)}]', '' , str(text))
    text = split_camel_case(text)
    text = expand_contractions(text)
    text = text.lower()
    text = ' '.join([word for word in text.split(' ') if word not in STOPWORDS])
    text = lemmatize_stem_words(text)
    return text