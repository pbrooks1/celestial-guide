
"""
This file runs the command-line version of Celestial Guide.
It loads the zodiac data, trains the intent classifier, accepts user input,
and returns a single astrology themed chatbot response.
"""

from intent import IntentClassifier, preprocess_text
from responses import load_zodiac_data, combined_response, clarification_message

# Confidence hidden unless DEBUG_MODE is set to True.
DEBUG_MODE = False


def two_intents(classifier, user_input):
    processed = preprocess_text(user_input)
    X_input = classifier.vectorizer.transform([processed])
    probabilities = classifier.model.predict_proba(X_input)[0]

    ranked = sorted(
        zip(classifier.model.classes_, probabilities),
        key=lambda x: x[1],
        reverse=True
    )

    if len(ranked) >= 2:
        return [ranked[0][0], ranked[1][0]]
    elif len(ranked) == 1:
        return [ranked[0][0]]
    else:
        return ["traits", "compatibility"]


def main():
    print("Welcome to Celestial Guide.")
    print("Ask about zodiac traits, compatibility, ruling planets, or elements.")
    print("Type 'quit' to exit.\n")

    zodiac_data = load_zodiac_data()

    classifier = IntentClassifier()
    classifier.train()

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["quit", "exit", "bye"]:
            print("\nCelestial Guide: Farewell, seeker. May the stars guide your path.")
            break

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


        if DEBUG_MODE:
            print(f"\nPredicted intent: {intent}")
            print(f"Detected sign: {sign}")
            print(f"Confidence: {confidence:.2f}")

        if intent == "unknown":
            top_intents = two_intents(classifier, user_input)
            response = clarification_message(sign, top_intents)
        else:
            response = combined_response(intent, sign, zodiac_data)

        # Final user response.
        print(f"\nCelestial Guide: {response}\n")


if __name__ == "__main__":
    main()
