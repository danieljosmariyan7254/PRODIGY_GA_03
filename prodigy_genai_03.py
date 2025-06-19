from random import choices
import numpy as np

class MarkovChain:
    def __init__(self):
        self.transition_table = {}
        pass

    def add_transition(self, current_state, next_state):
        if current_state not in self.transition_table.keys():
            self.transition_table[current_state]={}
        if next_state not in self.transition_table[current_state].keys():
            self.transition_table[current_state][next_state]=0
        self.transition_table[current_state][next_state]+=1
        pass

    def generate_states(self, initial_state, num_states):
        if num_states<1:
            return []
        initial_state = initial_state.lower()
        states_list=[initial_state]
        for i in range(1, num_states):
            initial_state = self._get_next_state(initial_state)
            states_list.append(initial_state)
        return states_list

    def _get_next_state(self, current_state):
        possible_next_states = list(self.transition_table[current_state].keys())
        probabilities = list(self.transition_table[current_state].values())
        total = np.sum(probabilities)
        for i in range(len(probabilities)):
            probabilities[i]/=total
        return choices(possible_next_states, probabilities)[0]


if __name__ == "__main__":
    markov_chain = MarkovChain()

    text = "In a land far away, there lived a wise old owl. The owl loved to share stories. These stories were not just any tales; they were reflections of the wisdom the owl had gained over the years. Every evening, creatures from all around the land would gather to listen to the owl's tales. The tales spoke of adventures, lessons, and the mysteries of the land. Among the listeners were a curious rabbit, a brave fox, and a cautious deer. The rabbit, known for its endless curiosity, would always ask questions about the tales. The fox, brave and cunning, would ponder how to use the lessons in life. The deer, cautious and gentle, would reflect on the morals of the stories. Together, they learned much from the wise old owl and looked forward to each new tale with great anticipation."

    words = text.split(' ')
    for i in range(len(words)):
        last_char = words[i][-1]
        if not(last_char>='a' and last_char<='z' or last_char>='A' and last_char<='Z'):
            words[i] = words[i][:len(words[i])-1]
        words[i] = words[i].lower()
    
    for i in range(len(words)-1):
        markov_chain.add_transition(words[i], words[i+1])

    markov_chain.add_transition(words[-1], words[0])

    words_list = []
    for word in words:
        if word not in words_list:
            words_list.append(word)

    table = np.zeros([len(words_list), len(words_list)])

    def index(s):
        i = 0
        while words_list[i]!=s:
            i+=1
        return i

    for i in range(len(words)-1):
        table[index(words[i])][index(words[i+1])]+=1
    table[index(words[-1])][index(words[0])]+=1

    for i in range(len(words_list)):
        sum=0
        for j in range(len(words_list)):
            sum+=table[i][j]
        for j in range(len(words_list)):
            table[i][j]/=sum

    for word in words_list:
        print(",",end='')
        print(word,end='')
    print("")
    for i in range(len(words_list)):
        print(words_list[i],end='')
        for j in range(len(words_list)):
            print(",",end='')
            print(table[i][j],end='')
        print("")

    initial_state = "In"
    num_states = 15  
    generated_sequence = markov_chain.generate_states(initial_state, num_states)
    print("Generated Text:", " ".join(generated_sequence))