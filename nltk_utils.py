import numpy as np
import nltk
import unidecode
# nltk.download('punkt')
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()


def tokenize(sentence):
    """
    split sentence into array of words/tokens
    a token can be a word or punctuation character, or number
    """
    """
    Processes the text to remove accents and special characters,
    converts to lowercase, and then tokenizes
    """
    
     # Paso 1: Eliminar acentos y normalizar caracteres
    sentence = unidecode.unidecode(sentence)
    # Paso 2: Convertir todo a minúsculas
    #sentence = sentence.lower()
    # Paso 3: Tokenizar
    return nltk.word_tokenize(sentence)


def stem(word):
    word = unidecode.unidecode(word.lower())
    """
    stemming = find the root form of the word
    examples:
    words = ["organize", "organizes", "organizing"]
    words = [stem(w) for w in words]
    -> ["organ", "organ", "organ"]
    """
    """
    Apply stemming to already normalized words (without accents and in lowercase).
    """
    return stemmer.stem(word)


def bag_of_words(tokenized_sentence, words):
    """
    return bag of words array:
    1 for each known word that exists in the sentence, 0 otherwise
    example:
    sentence = ["hello", "how", "are", "you"]
    words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
    bog   = [  0 ,    1 ,    0 ,   1 ,    0 ,    0 ,      0]
    """
    # stem each word
    sentence_words = [stem(word) for word in tokenized_sentence]
    # initialize bag with 0 for each word
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in sentence_words: 
            bag[idx] = 1

    return bag
