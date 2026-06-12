# Celestial Guide NLP Chatbot

Celestial Guide is a retrieval-based learning chatbot that answers astrology related questions about zodiac traits, compatibility, ruling planets, elements, and horoscope style guidance. The chatbot uses NLP preprocessing, machine learning intent classification, a JSON zodiac knowledge base, and a mystical response generation layer called the AstroNarrative Engine. Emojis were included in the Streamlit interface to make the chatbot feel more engaging and aligned with its entertainment based astrology theme. They do not affect the chatbot’s NLP process, intent classification, or response selection.

## Project Files

- `main.py`: Terminal version of the chatbot.
- `app.py`: Streamlit interface web version of the chatbot.
- `intent.py`: Handles text preprocessing, zodiac sign detection, TF-IDF vectorization, and Logistic Regression intent classification.
- `responses.py`: Loads zodiac data and generates final Celestial Guide responses.
- `training_data.py`: Contains expanded training examples used to train the intent classifier.
- `z_data.json`: Structured zodiac knowledge base.

## Requirements

This project requires Python 3 and the following packages:

```bash
streamlit
spacy
scikit-learn
