

"""
This file runs the Streamlit web version of Celestial Guide.
It creates the user interface, collects astrology questions,
and displays the chatbot's final response in the browser.
"""

import streamlit as st

from intent import IntentClassifier
from responses import load_zodiac_data, combined_response, clarification_message


@st.cache_resource
def load_classifier():
    classifier = IntentClassifier()
    classifier.train()
    return classifier

@st.cache_data
def load_data():
    return load_zodiac_data()


def get_response(user_input, classifier, zodiac_data):
    intent, sign, confidence = classifier.predict_intent(user_input)

    lowered = user_input.lower()

    if "horoscope" in lowered or "guidance" in lowered or "advice" in lowered:
        intent = "horoscope"
    elif "trait" in lowered or "personality" in lowered:
        intent = "traits"
    elif "compatible" in lowered or "compatibility" in lowered or "match" in lowered:
        intent = "compatibility"
    elif "planet" in lowered:
        intent = "ruling_planet"
    elif "element" in lowered:
        intent = "element"

    if intent == "unknown":
        return clarification_message(sign, ["traits", "compatibility"])

    return combined_response(intent, sign, zodiac_data)


def main():
    st.set_page_config(
        page_title="Celestial Guide",
        page_icon="✨🔮",
        layout="centered"
    )

    st.title("✨🔮 Celestial Guide")
    st.write(
        "Ask about zodiac traits, compatibility, ruling planets, or elements. "
        "Celestial Guide will return a mystical astrology-inspired response."
    )

    zodiac_data = load_data()
    classifier = load_classifier()

    with st.form("celestial_form", clear_on_submit=False):
        user_input = st.text_input(
            "Ask the stars a question:",
            placeholder="Example: What is Aries like?"
        )

        submitted = st.form_submit_button("Reveal My Reading")

    if submitted:
        if not user_input.strip():
            st.warning("Please enter a question first.")
        else:
            response = get_response(user_input, classifier, zodiac_data)

            st.subheader("Celestial Guide")
            st.write(response)


if __name__ == "__main__":
    main()
