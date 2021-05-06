from typing import List, Set
from collections import defaultdict
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk import pos_tag
from string import punctuation
from .utils import memoized
import nltk

nltk.data.path.append('/media/kid/Data/nltk_data')

CONVERT_POS = {
    'J': wordnet.ADJ,
    'V': wordnet.VERB,
    'R': wordnet.ADV
}


def tokenize_text(text: str) -> List[str]:
    return word_tokenize(text, language='english')

@memoized
def preprocess_data(text: str) -> List[str]:
    words: List[str] = tokenize_text(text)
    lemmatized_words: List[str] = __lemmatize_text(words)
    meaningful_words = __remove_stop_words(lemmatized_words)
    meaningful_words = __remove_punctuation(meaningful_words)
    return meaningful_words


def __remove_stop_words(words: List[str]) -> List[str]:
    words_to_remove: Set[str] = set(stopwords.words('english'))
    filtered_words: List[str] = [
        word for word in words if not word in words_to_remove]
    return filtered_words


def __lemmatize_text(words: List[str]) -> List[str]:
    lemmatizer: WordNetLemmatizer = WordNetLemmatizer()
    words_with_pos: List[(str, str)] = __get_postags(words)
    lemmatized_words: List[str] = [
        lemmatizer.lemmatize(word, pos=CONVERT_POS.get(tag[0], wordnet.NOUN)) for word, tag in words_with_pos]
    return lemmatized_words


def __get_postags(words: List[str]) -> List[str]:
    words_with_pos: List[(str, str)] = pos_tag(words)
    return words_with_pos


def __remove_punctuation(words: List[str]) -> List[str]:
    return [word for word in words if not word in punctuation]
