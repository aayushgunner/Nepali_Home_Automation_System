import os


file_path = "D:\Voice\Project\Audio_data/"

i = 142

for filename in os.listdir(file_path):
    file_name = os.path.join(file_path, filename)
    num_1, ext = os.path.splitext(filename)
    
    if "-" in num_1:
        i += 1
        new_name = os.path.join(file_path, str(i) + ext)
        os.rename(file_name, new_name)
        

        
 