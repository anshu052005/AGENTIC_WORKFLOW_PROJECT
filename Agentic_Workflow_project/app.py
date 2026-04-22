from src.agent import Agent

agent = Agent()

while True:
    user_input = input("You: ")
    response = agent.handle_input(user_input)
    print("Bot:", response)