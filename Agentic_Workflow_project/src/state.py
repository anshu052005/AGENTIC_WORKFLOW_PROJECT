class AgentState:
    def __init__(self):
        self.intent = None
        self.name = None
        self.email = None
        self.platform = None
        self.lead_stage = None

        # ✅ MEMORY (IMPORTANT)
        self.history = []  # stores last conversations