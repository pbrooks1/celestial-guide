"""
This file creates Celestial Guide's responses.
It loads zodiac information from the JSON file and formats the retrieved
information into a mystical astrology style response.
"""

import json
import random
from pathlib import Path

def get_sign_data(sign, data):
    if sign is None:
        return None, None

    sign_clean = sign.strip().lower()

    for key, value in data.items():
        if key.strip().lower() == sign_clean:
            return key, value

    return sign, None

def load_zodiac_data(filename="z_data.json"):
    base_dir = Path(__file__).resolve().parent
    file_path = base_dir / filename

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def generate_retrieval_response(intent, sign, data):
    if sign is None:
        return "Please mention a zodiac sign so I can help guide the reading."

    sign, sign_data = get_sign_data(sign, data)
    if not sign_data:
        return f"I could not find a reading for {sign}."

    if intent == "horoscope":
        traits = ", ".join(sign_data["traits"][:3])
        strengths = ", ".join(sign_data["strengths"][:2])
        weaknesses = ", ".join(sign_data["weaknesses"][:2])
        return (
            f"{sign}'s horoscope guidance is connected to {traits}. "
            f"Strengths include {strengths}, while challenges may include {weaknesses}."
        )
    if intent == "traits":
        traits = ", ".join(sign_data["traits"])
        strengths = ", ".join(sign_data["strengths"])
        weaknesses = ", ".join(sign_data["weaknesses"])
        return (
            f"{sign} is often associated with {traits}. "
            f"Its strengths include {strengths}, while its challenges may include {weaknesses}."
        )

    if intent == "compatibility":
        compatibility = ", ".join(sign_data["compatibility"])
        return f"{sign} is often considered most compatible with {compatibility}."

    if intent == "ruling_planet":
        return f"The ruling planet of {sign} is {sign_data['ruling_planet']}."

    if intent == "element":
        return f"{sign} belongs to the {sign_data['element']} element."

    return "The message is unclear, and I cannot answer that yet."


def astro_narrative_engine(intent, sign, data):
    if sign is None:
        return "Speak your sign and let the stars reveal what is hidden."

    sign, sign_data = get_sign_data(sign, data)
    if not sign_data:
        return "The stars are clouded, and the vision is not yet clear."

    traits = ", ".join(sign_data["traits"][:3])
    strengths = ", ".join(sign_data["strengths"][:2])
    weaknesses = ", ".join(sign_data["weaknesses"][:2])
    compatibility = ", ".join(sign_data["compatibility"][:2])
    planet = sign_data["ruling_planet"]
    element = sign_data["element"]

    openings = [
        "The stars whisper this truth:",
        "I sense a message coming through:",
        "The cosmic veil parts for a moment:",
        "A strong energy surrounds this reading:"
    ]

    planet_meanings = {
        "Sun": "confidence, identity, vitality, and the need to shine with purpose",
        "Moon": "emotion, intuition, memory, and the need for emotional safety",
        "Mercury": "communication, analysis, learning, and careful observation",
        "Venus": "love, beauty, comfort, loyalty, and connection to what feels valuable",
        "Mars": "courage, action, passion, and the instinct to move forward",
        "Jupiter": "growth, wisdom, optimism, and the search for wider meaning",
        "Saturn": "discipline, patience, responsibility, and long-range focus",
        "Uranus": "change, originality, independence, and sudden insight",
        "Neptune": "dreams, intuition, imagination, and spiritual sensitivity",
        "Pluto": "transformation, power, rebirth, and hidden emotional depth"
    }

    opening = random.choice(openings)
    planet_energy = planet_meanings.get(
        planet,
        "personal growth, inner direction, and the deeper path ahead"
    )

    if intent == "traits":
        return (
            f"{opening} {sign} carries an aura of {traits}. "
            f"This sign often shines through {strengths}, but the stars also reveal lessons around {weaknesses}. "
            f"Your energy is not accidental. It moves with purpose, presence, and a path still unfolding."
        )

    if intent == "compatibility":
        return (
            f"{opening} {sign} is often drawn toward {compatibility}. "
            f"These connections are rarely random. They may carry emotional understanding, natural harmony, "
            f"and a sense of recognition that feels familiar from the beginning."
        )

    if intent == "ruling_planet":
        return (
            f"{opening} The force guiding {sign} is {planet}. "
            f"For {sign}, {planet} brings themes of {planet_energy}."
        )

    if intent == "element":
        return (
            f"{opening} {sign} belongs to the {element} element. "
            f"This element shapes how {sign} feels, reacts, connects, and reveals its deeper nature to the world."
        )

    if intent == "horoscope":
        return (
            f"{opening} Today, {sign}, your energy is colored by {traits}. "
            f"Lean into {strengths}, but stay mindful of {weaknesses}. "
            f"The stars suggest a moment of reflection, steady choices, and trust in your inner timing."
        )

    return f"{opening} There are still secrets around {sign} waiting to be revealed."


def clarification_message(sign, top_intents):
    if not top_intents:
        return "I am not fully certain what you seek. Are you asking about traits, compatibility, ruling planet, or element?"

    if len(top_intents) == 1:
        if sign:
            return f"I am not fully certain. Are you asking about {sign}'s {top_intents[0]}?"
        return f"I am not fully certain. Are you asking about {top_intents[0]}?"

    pretty_intents = " or ".join(top_intents[:2])

    if sign:
        return f"I am not fully certain. Are you asking about {sign}'s {pretty_intents}?"
    return f"I am not fully certain what you seek. Are you asking about {pretty_intents}?"


def combined_response(intent, sign, data):
    return astro_narrative_engine(intent, sign, data)