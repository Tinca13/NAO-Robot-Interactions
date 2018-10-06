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
    dance_dict = {"thriller": "new_thriller-40424e/new_thriller",
                           "disco": "disco-dd565c/disco",
                           "arm dance": "arm_dance-074ba5/arm_dance",
                           "tai chi": "taichi-cd9975/GangnamStyle",
                           "gangnam style": "gangnam_style-2b4c5b/GangnamStyle (1)",
                           "caravan palace": "canavanplacemusic-16a6c1/CanavanPlace music"}
    # store_list(dance_dict, 'robot_behaviours.pkl', 'H:\\Programming\\RemoteSandbox\\NAO-Robot-Interactions\\pkl_sources')