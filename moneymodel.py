from mesa import Model, Agent


class MoneyAgent(Agent):
    '''An agent with fixed initial wealth.'''
    def __init__(self, unique_id):
        self.unique_id = unique_id
        self.wealth = 1


class MoneyModel(Model):
    '''A model with some number of agents.'''
    def __init__(self, N):
        self.num_agents = N
        self.create_agents()

    def create_agents(self):
        '''Method to create all the agents.'''
        for i in range(self.num_agents):
            a = MoneyAgent(i)
            
            
