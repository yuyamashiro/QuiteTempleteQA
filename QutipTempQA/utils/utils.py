
def filename_from(N, T, param, names):
    filename = "N{}T{}".format(N,T)
    for key in names:
        filename += key+str(param[key]).replace(".","_")
    return filename