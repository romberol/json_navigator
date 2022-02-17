"""
This module can be used to navigate through json file.
"""

from importlib.resources import path
import json
import copy

def ind_input(n_sections):
    """
    Gets user's input and validate it.
    Must be an integer.
    """
    while True:
        try:
            inp = int(input("\nEnter section number to open\nIf you want to go back enter 0\nIf you want ot exit enter -1: "))       
        except ValueError:
            print("Please, enter valid section number")
            continue
        else:
            if int(inp)>n_sections or int(inp)<-1:
                print("Please, enter valid section number")
                continue
            return int(inp)     

def get_data(path):
    """
    Opens json file and returns data from it.
    """
    with open(file_path, encoding="utf-8") as file:
        data = json.load(file)
        return data


def print_json(json_path, data=None):
    """
    Provide text interface to navigate through json file.
    Navigation keys:
    0 - go back
    -1 - exit program
    """
    if not data: data = get_data(json_path)
    tmp_data = copy.copy(data)
    sections = json_path.split('/')[1:]
    for section in sections:
        if section[0]=="<" and section[-1]==">" and section[1:-1].isdigit():
            tmp_data = tmp_data[int(section[1:-1])-1]
        else: tmp_data = tmp_data.get(section)
    print(f"\nCurrently you are at: {json_path}")
    if isinstance(tmp_data, (str, int)) or tmp_data == None:
        print("Data from this section:\n")
        print(tmp_data)
        inp = input("\nTo go back type 0/To exit type -1:")
        while inp!="0" and inp!="-1":
            inp = input("Incorrect input!\n")
        if inp=="0": 
            json_path = "/".join(json_path.split("/")[:-1]) if json_path.count("/")>0 else json_path
            print_json(json_path, data=data)
        if inp=="-1": quit()
    else:
        print(f"There is {len(tmp_data)} section(s) to choose.\n")
    if isinstance(tmp_data, dict):
        for ind, key in enumerate(tmp_data.keys()):
            if isinstance(tmp_data[key], (list, dict)): print(f"{ind+1} - {key} -> ...")
            else: 
                if isinstance(tmp_data[key], str):
                    if len(tmp_data[key])>100: 
                        print(f"{ind+1} - {key} -> <TOO LONG TO DISPLAY>")
                        continue
                print(f"{ind+1} - {key} -> {tmp_data[key]}")
        next_section = ind_input(len(tmp_data.keys()))
        if next_section==-1: quit()
        elif next_section==0:
            json_path = "/".join(json_path.split("/")[:-1]) if json_path.count("/")>0 else json_path
        else: json_path = json_path+"/"+list(tmp_data.keys())[next_section-1]
    else:
        for ind, el in enumerate(tmp_data):
            if isinstance(el, (list, dict)): print(f"{ind+1} -> ...")
            else: 
                if isinstance(el, str):
                    if len(el)>100: 
                        print(f"{ind+1} -> <TOO LONG TO DISPLAY>")
                        continue
                print(f"{ind+1} - {el}")
        next_section = ind_input(len(tmp_data))
        if next_section==-1: quit()
        elif next_section==0: 
            json_path = "/".join(json_path.split("/")[:-1]) if json_path.count("/")>0 else json_path
        else: json_path = f"{json_path}/<{next_section}>"
    print_json(json_path, data=data)

if __name__=="__main__":
    file_path = ["frienfs_list_Obama.json", "user_timeline_obama.json", "kved.json"][0] #<-----FILES EXAMPLES
    file_path = input("Enter the path to json file: ")
    print("\nNAVIGATION:\n... - list or dictionary\n<TOO LONG TO DISPLAY> - open this section to see full content")
    print_json(file_path)
