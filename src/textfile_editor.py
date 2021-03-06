# if txt file is not exist , this function would make it. and then write text.
def make_file_and_add_text(path: str, text):
    f = open(path, 'a')
    f.writelines(text)
    f.close()

    
def clear_old_text_and_write_text(path: str, text):
    f = open(path, 'x', encoding="utf-8")
    f.writelines(text, encoding="utf-8")
    f.close()


def write_to_unwritten_txt_file(path: str, text):
    if is_unwritten_txt_file_or_not_exist(path):
        make_file_and_add_text(path, text)


def is_written(path: str):
    if(is_exist(path)):
        data = read_txt_file(path)
        if(data != ""):
            return True
    else:
        return False


def is_exist(path: str):
    import os.path
    return os.path.isfile(path)


def is_unwritten_txt_file_or_not_exist(path: str):
    if not is_written(path):
        return True
    if not is_exist(path):
        return True
    else:
        return False


# read
def read_txt_file(path: str):
    f = open(path, 'r', encoding="utf-8", errors='ignore')
    data = f.read()
    f.close()
    return data
