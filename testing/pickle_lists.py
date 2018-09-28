import pickle

PKL_EXT = ".pkl"

def store_list(list_in, f_name, _dir = ''):
    """
    Stores an input list in a given file

    Keyword arguments:
    list_in -- the list or dictionary to be pickled
    f_name -- the name of the pickled list file (can be with or without .pkl extension)
    _dir -- the parent directory's path of the file, default assumes relative path
    """
    f_path = find_path(f_name, _dir)
    with open(f_path, 'ab') as pkl_f:
        pickle.dump(list_in, pkl_f)

def get_list(f_name, _dir = ''):
    """
    Opens a given pickle file and returns the serialised list contained there

    Keyword arguments:
    f_name -- the name of the pickled list file (can be with or without .pkl extension)
    _dir -- the parent directory's path of the file, default assumes relative path

    Yields:
    A generator that must be looped over to get the different containers from the file
    """
    f_path = find_path(f_name, _dir)
    yield_lists = True
    with open(f_path, 'rb') as pkl_f:
        while yield_lists:
            try:
                yield pickle.load(pkl_f)
            except EOFError:
                print("Found end of file, stopping pickling")
                break

def find_path(f_name, _dir):
    """
    Used to setup the full .pkl file path and check whether the name has been
    passed with or without a file extension

    Keyword arguments:
    f_name -- the name of the pickled list file (can be with or without .pkl extension)
    _dir -- the parent directory's path of the file, default assumes relative path

    Returns:
    f_path -- the full path of the pickled file
    """
    if PKL_EXT in f_name:
        f_path = "{0}\\{1}".format(_dir, f_name)
    else:
        f_path = "{0}\\{1}{2}".format(_dir, f_name, PKL_EXT)
    
    return f_path

if __name__ == "__main__":
    com_dict = {"speech": 
                    {"hello robbie", "fire the trebuchet", "what is the time",
                    "how are you", "where are we", "what is this department",
                    "what is your favourite pathway"},
                "movement": 
                    {"can you sit down", "stand", "can you walk forward",
                    "come over here robbie", "can you walk backwards", 
                    "are you tired robbie"},
                "behaviours": 
                    {"do you feel like dancing", "show me your best dance moves",
                    "can you play the guitar", "why don't you do some exercise",
                    "bless you", "do you know thriller"},
                "stop": {"it is time to stop", "can you please stop that movement"} 
                }   
    # store_list(com_dict, 'robot_commands.pkl', 'F:\\Programming\\RemoteSandbox\\NAO-Robot-Interactions\\pkl_sources')
    # items = get_list('robot_commands.pkl', 'F:\\Programming\\RemoteSandbox\\NAO-Robot-Interactions\\pkl_sources')