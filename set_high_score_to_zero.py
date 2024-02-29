# Run me to set the high score to 0
import pickle
data_to_pickle = '0' 
with open('h_score.pkl', 'wb') as file:
    pickle.dump(data_to_pickle, file)