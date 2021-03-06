import six


def print_txt(file):
    if isinstance(file, six.string_types):
        file = open(file)
    str = ''
    for line in file.readlines():
        str += line
    print(str)
