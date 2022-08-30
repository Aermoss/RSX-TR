from rsharp.tools import *

create_library("rsxtrio")

@create_function("VOID", {"text": "STRING"})
def yaz(environment):
    if environment["args"]["text"] == None: print("null", end = "", flush = True)
    else: print(environment["args"]["text"], end = "", flush = True)

@create_function("STRING", {})
def iste(environment):
    return input()

@create_function("STRING", {})
def bitir(environment):
    return "\n"

rsxtrio = pack_library()