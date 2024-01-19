import os
def check_path(path):
    if os.path.isdir(path):
        print(path+"是文件夹")
        return 1
    elif os.path.isfile(path):
        print(path+"是文件")
        return 0
    else:
        print ("获取不到文件类型")
        return 1

def get_dir(path,name=".pdf"):
    path_list = []
    paths = os.walk(path)
    for path, dir_lst, file_lst in paths:
        for file_name in file_lst:
            file = os.path.join(path, file_name)
            if(check_pdf(file,name)):
                path_list.append(file)
                print(file)

    return path_list
def check_pdf(path,name='.pdf'):
    if(path.endswith(name)):
        return 1
    else:
        return 0