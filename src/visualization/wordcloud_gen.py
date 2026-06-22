"""Generador de word clouds."""

from __future__ import annotations

from collections import Counter

import pandas as pd

import config


def extract_word_frequencies(texts: list[str], top_n: int = 50) -> pd.DataFrame:
    words = []
    stop = {"de", "la", "que", "el", "en", "y", "a", "los", "un", "por", "con", "no", "una", "su", "para", "es", "del", "se", "las"}
    for text in texts:
        for word in str(text).lower().split():
            if len(word) > 3 and word not in stop:
                words.append(word)
    counter = Counter(words)
    rows = [{"word": w, "count": c} for w, c in counter.most_common(top_n)]
    return pd.DataFrame(rows)


def generate_wordcloud_image(texts: list[str]):
    try:
        from wordcloud import WordCloud
        import matplotlib.pyplot as plt

        text = " ".join(str(t) for t in texts)
        wc = WordCloud(
            width=800, height=400,
            background_color=config.THEME["card"],
            colormap="Blues",
            max_words=100,
        ).generate(text)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        fig.patch.set_facecolor(config.THEME["background"])
        return fig
    except ImportError:
        return None
