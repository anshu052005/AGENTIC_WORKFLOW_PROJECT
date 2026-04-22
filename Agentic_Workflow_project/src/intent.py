import re
from typing import Dict


class IntentConfig:
    """
    Stores all intent-related keywords and configuration.
    Easily extendable for future projects.
    """

    GREETING_KEYWORDS = [
    "hi", "hello", "hey", "hii", "helo",
    "good morning", "good evening",
    "yo", "wassup"
]

    INQUIRY_KEYWORDS = [
        "price", "cost", "plan", "feature",
        "refund", "support", "details"
    ]

    HIGH_INTENT_KEYWORDS = [
        "buy", "purchase", "subscribe",
        "sign up", "get started", "try",
        "start using"
    ]


class TextPreprocessor:
    """
    Handles text cleaning and normalization.
    """

    @staticmethod
    def clean(text: str) -> str:
        text = text.lower()
        text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
        return text.strip()


class IntentClassifier:
    """
    Main Intent Classification Engine.
    Rule-based for reliability and speed.
    """

    def __init__(self, config: IntentConfig = IntentConfig()):
        self.config = config

    def _contains_keyword(self, text: str, keywords: list) -> bool:
        return any(keyword in text for keyword in keywords)

    def detect(self, user_input: str) -> Dict:
        """
        Returns:
        {
            "intent": str,
            "confidence": float
        }
        """

        text = TextPreprocessor.clean(user_input)

        # 1. Greeting
        if self._contains_keyword(text, self.config.GREETING_KEYWORDS):
            return {"intent": "greeting", "confidence": 0.9}

        # 2. High Intent (priority over inquiry)
        if self._contains_keyword(text, self.config.HIGH_INTENT_KEYWORDS):
            return {"intent": "high_intent", "confidence": 0.95}

        # 3. Inquiry
        if self._contains_keyword(text, self.config.INQUIRY_KEYWORDS):
            return {"intent": "inquiry", "confidence": 0.85}

        # 4. Default fallback
        return {"intent": "inquiry", "confidence": 0.6}