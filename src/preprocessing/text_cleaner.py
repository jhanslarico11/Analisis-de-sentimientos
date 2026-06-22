"""Preprocesamiento NLP optimizado para español."""

from __future__ import annotations

import re
import unicodedata
from typing import Optional

import pandas as pd

try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import SnowballStemmer
    from nltk.tokenize import word_tokenize

    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False

try:
    import spacy

    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False

from src.utils.helpers import logger

SPANISH_STOPWORDS = {
    "de", "la", "que", "el", "en", "y", "a", "los", "del", "se", "las", "por", "un", "para",
    "con", "no", "una", "su", "al", "lo", "como", "más", "mas", "pero", "sus", "le", "ya",
    "o", "fue", "este", "ha", "si", "porque", "esta", "entre", "cuando", "muy", "sin", "sobre",
    "también", "tambien", "me", "hasta", "hay", "donde", "quien", "desde", "todo", "nos",
    "durante", "todos", "uno", "les", "ni", "contra", "otros", "ese", "eso", "ante", "ellos",
    "e", "esto", "mí", "mi", "antes", "algunos", "qué", "unos", "yo", "otro", "otras", "otra",
    "él", "tanto", "esa", "estos", "mucho", "quienes", "nada", "cada", "cual", "poco", "ella",
    "ser", "son", "dos", "fueron", "había", "habia", "siendo", "sido", "tiene", "tienen",
}


def _ensure_nltk() -> None:
    if not NLTK_AVAILABLE:
        return
    resources = ["punkt", "punkt_tab", "stopwords"]
    for res in resources:
        try:
            nltk.data.find(f"tokenizers/{res}" if "punkt" in res else f"corpora/{res}")
        except LookupError:
            try:
                nltk.download(res, quiet=True)
            except Exception:
                pass


class TextPreprocessor:
    """Pipeline completo de limpieza y normalización de texto."""

    def __init__(self, use_lemma: bool = True, use_stem: bool = False):
        _ensure_nltk()
        self.use_lemma = use_lemma and SPACY_AVAILABLE
        self.use_stem = use_stem and NLTK_AVAILABLE
        self.stemmer = SnowballStemmer("spanish") if self.use_stem else None
        self._nlp = None
        if self.use_lemma:
            try:
                self._nlp = spacy.load("es_core_news_sm", disable=["parser", "ner"])
            except OSError:
                logger.warning("spaCy es_core_news_sm no disponible. Usando normalización básica.")
                self.use_lemma = False

    @staticmethod
    def to_lowercase(text: str) -> str:
        return text.lower() if text else ""

    @staticmethod
    def remove_urls(text: str) -> str:
        return re.sub(r"https?://\S+|www\.\S+", " ", text)

    @staticmethod
    def remove_emojis(text: str) -> str:
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"
            "\U0001F300-\U0001F5FF"
            "\U0001F680-\U0001F6FF"
            "\U0001F1E0-\U0001F1FF"
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+",
            flags=re.UNICODE,
        )
        return emoji_pattern.sub(" ", text)

    @staticmethod
    def remove_hashtags(text: str) -> str:
        return re.sub(r"#\w+", " ", text)

    @staticmethod
    def remove_mentions(text: str) -> str:
        return re.sub(r"@\w+", " ", text)

    @staticmethod
    def remove_special_chars(text: str) -> str:
        text = unicodedata.normalize("NFKD", text)
        text = re.sub(r"[^\w\sáéíóúüñÁÉÍÓÚÜÑ]", " ", text)
        return text

    @staticmethod
    def normalize(text: str) -> str:
        text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
        return re.sub(r"\s+", " ", text).strip()

    def tokenize(self, text: str) -> list[str]:
        if NLTK_AVAILABLE:
            try:
                return word_tokenize(text, language="spanish")
            except Exception:
                pass
        return text.split()

    def remove_stopwords(self, tokens: list[str]) -> list[str]:
        if NLTK_AVAILABLE:
            try:
                stops = set(stopwords.words("spanish"))
            except Exception:
                stops = SPANISH_STOPWORDS
        else:
            stops = SPANISH_STOPWORDS
        return [t for t in tokens if t not in stops and len(t) > 1]

    def lemmatize(self, text: str) -> str:
        if self._nlp is not None:
            doc = self._nlp(text)
            return " ".join(token.lemma_ for token in doc if not token.is_space)
        return text

    def stem(self, tokens: list[str]) -> list[str]:
        if self.stemmer:
            return [self.stemmer.stem(t) for t in tokens]
        return tokens

    def clean(self, text: Optional[str], full: bool = True) -> str:
        if not text or not isinstance(text, str):
            return ""
        result = self.to_lowercase(text)
        result = self.remove_urls(result)
        result = self.remove_emojis(result)
        result = self.remove_hashtags(result)
        result = self.remove_mentions(result)
        result = self.remove_special_chars(result)
        if full:
            if self.use_lemma:
                result = self.lemmatize(result)
            tokens = self.tokenize(result)
            tokens = self.remove_stopwords(tokens)
            if self.use_stem:
                tokens = self.stem(tokens)
            result = " ".join(tokens)
        result = self.normalize(result)
        return result

    def process_dataframe(self, df: pd.DataFrame, text_col: str = "text", out_col: str = "clean_text") -> pd.DataFrame:
        out = df.copy()
        out[out_col] = out[text_col].fillna("").astype(str).apply(self.clean)
        return out
