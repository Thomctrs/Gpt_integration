import pyttsx3

def speak_text(text, rate=150):
    """
    Fonction de synthèse vocale qui lit un texte à voix haute
    
    Args:
        text (str): Le texte à lire
        rate (int, optional): La vitesse de lecture. Défaut à 150.
    """
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()
