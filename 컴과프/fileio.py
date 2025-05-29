import pickle
from data import lost_item_list, found_item_list

def save_data(filename='savedata.txt'):
    with open(filename, 'wb') as f:
        pickle.dump({'lost': lost_item_list, 'found': found_item_list}, f)

def load_data(filename='savedata.txt'):
    try:
        with open(filename, 'rb') as f:
            data = pickle.load(f)
            lost_item_list.clear()
            found_item_list.clear()
            lost_item_list.extend(data.get('lost', []))
            found_item_list.extend(data.get('found', []))
    except (EOFError,FileNotFoundError):
        pass
