import re
from src.intent import IntentClassifier
from src.rag import RAGPipeline
from src.state import AgentState
from src.tools import mock_lead_capture


class Agent:
    def __init__(self):
        self.intent_model = IntentClassifier()
        self.rag = RAGPipeline("data/knowledge.json")
        self.state = AgentState()
    
    def handle_input(self, user_input):
        # Store user message.
        self.state.history.append({
            "role": "user",
            "content": user_input
        })

        # Continue lead flow if already in progress.
        if self.state.lead_stage is not None and self.state.lead_stage != "done":
            response = self.handle_lead_flow(user_input)
        else:
            # Detect intent for new turn.
            result = self.intent_model.detect(user_input)
            intent = result["intent"]
            self.state.intent = intent

            if intent == "greeting":
                response = "Hey! 👋 I can help you with AutoStream pricing, features, or getting started."
            elif intent == "high_intent":
                response = self.handle_lead_flow(user_input)
            elif intent == "inquiry":
                response = self.rag.query(user_input, self.state)
            else:
                response = "I'm not sure how to help with that."

        # Store bot response.
        self.state.history.append({
            "role": "bot",
            "content": response
        })

        # Keep last 6 full conversation turns (user+bot = 12 messages).
        self.state.history = self.state.history[-12:]
        return response

    def is_valid_email(self, email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def handle_lead_flow(self, user_input):
        # Start
        if self.state.lead_stage is None:
            self.state.lead_stage = "name"
            return "Awesome choice 🚀 Let's get you started.\nWhat's your name?"

        # Name
        if self.state.lead_stage == "name":
            self.state.name = user_input.strip()
            self.state.lead_stage = "email"
            return f"Nice to meet you, {self.state.name}!\nPlease share your email."

        # Email
        if self.state.lead_stage == "email":
            if not self.is_valid_email(user_input):
                return "That doesn't look like a valid email. Please enter a correct one."

            self.state.email = user_input.strip()
            self.state.lead_stage = "platform"
            return "Which platform do you create content on? (YouTube/Instagram)"

        # Platform
        if self.state.lead_stage == "platform":
            self.state.platform = user_input.strip()

            # TOOL CALL
            mock_lead_capture(
                self.state.name,
                self.state.email,
                self.state.platform
            )

            self.state.lead_stage = "done"
            return "🎉 You're all set! Our team will contact you soon."
    
