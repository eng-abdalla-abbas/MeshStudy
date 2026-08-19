import FreeCAD as App
import json
import os 

user_dir = App.getUserAppDataDir()
save_dir = os.path.join(user_dir, "Mod", "MeshStudyWorkbench", "services")
os.makedirs(save_dir, exist_ok=True)
file_path = os.path.join(save_dir, "service_signals.json")
data = []

def send(signal):
    global data

    with open(file_path, "r")as f:
            data = json.load(f)
            
    with open(file_path, "w") as f:
            data[0][signal] = True
            json.dump(data, f)


def get_signal(signal):
    global data
    with open(file_path, "r")as f:
        data =json.load(f)
    
    return  data[0][signal]

def reset_signal(): 
    reset =  [{"STOP":False}]
    with open(file_path, "w") as f:
        json.dump(reset,f)
