from time import gmtime, strftime


def generate_timestamp():
    return strftime("%Y-%m-%d%H:%M:%S", gmtime())


print(generate_timestamp())