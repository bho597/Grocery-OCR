import pickle
from pprint import pprint

with open('temp.pkl', 'rb') as file:
    data = pickle.load(file)

# Now 'data' contains the unpickled dictionary
pprint(data.pages)