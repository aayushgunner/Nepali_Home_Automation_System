import os


file_path = "D:\Voice\Project\TurnOff/"

i = 10

for filename in os.listdir(file_path):
    file_name = os.path.join(file_path, filename)
    num_1, ext = os.path.splitext(filename)
    
    if True:
        i += 1
        new_name = os.path.join(file_path, str(i) + ext)
        os.rename(file_name, new_name)
        

        
 