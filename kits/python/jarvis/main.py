from agent import Agent
from utilities import read_turn_updates

if __name__ == "__main__":
    turn_updates = read_turn_updates()
    initial_game_state = next(turn_updates)
    agent = Agent(initial_game_state)
    agent.take_turn()

    for update in turn_updates:
        agent.take_turn(turn_data=update)
