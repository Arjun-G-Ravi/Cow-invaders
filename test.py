import pickle

# Example data to be pickled
data_to_pickle = '0' 

# Writing to a file using pickle
with open('h_score.pkl', 'wb') as file:
    pickle.dump(data_to_pickle, file)

# Reading from a file using pickle
with open('data.pkl', 'rb') as file:
    loaded_data = pickle.load(file)

print("Original data:", data_to_pickle)
print("Loaded data:", loaded_data)
