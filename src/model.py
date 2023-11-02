import numpy as np
import pandas as pd


class History():
    def __init__(self, model):
        self.model = model 
        self.state_history = [] 
        self.state_numbers = []


    def update(self):
        self.state_history.append(self.model.node_states.copy())
        state_numbers_dict = {
            s: (self.model.node_states == s).sum()
            for s in self.model.states 
        }
        self.state_numbers.append(state_numbers_dict)

    def to_df(self, include_node_states=False):
        df1 = pd.DataFrame(self.state_numbers)
        df1.columns = self.model.state_strings
        if not include_node_states:
            return df1
        
        df2 = pd.DataFrame(self.state_history, columns=self.model.G.node_numbers)
        return pd.concat([df1, df2], axis=1)
        
class BaseModel():

    def __init__(self, states, state_strings, state_func_dict):
        self.states = states
        self.state_strings = state_strings
        self.state_func_dict = state_func_dict
        self.G = None

        self.history = History(self)
        
    def set_graph(self, G):
        self.G = G
        
    def setup(self, initial_state):
        self.node_states= np.full(self.G.n_nodes, initial_state)
        self.new_states = np.empty(self.G.n_nodes)

        self.time_in_state = np.ones(self.G.n_nodes)

        self.history.update()
        
    def iterate(self):
        self.new_states[:] = self.node_states

        for state, func in self.state_func_dict.items():
            nodes = self.G.nodes[self.node_states == state]
            func(nodes)
            
        same_state = self.new_states == self.node_states
        self.node_states[:] = self.new_states
        self.time_in_state[same_state] += 1
        self.time_in_state[same_state == False] = 1
        self.history.update()

    def inform(self):
        for state in self.states:
            num = (self.node_states == state).sum()
            print(f"{self.state_strings[state]} ..... {num}")
        print()


    def history_to_df(self, include_node_states=False):
        return self.history.to_df(include_node_states=include_node_states)
    
