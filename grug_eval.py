import math
import grug
import sys
import os

with open("mod_api.json", "r", encoding="utf-8") as f:
    mod_api = f.read()

with open("about.json", "r", encoding="utf-8") as f:
    about = f.read()

code = sys.argv[1]
path = sys.argv[2]

os.mkdir(path)
os.chdir(path)

with open("mod_api.json", "w", encoding="utf-8") as f:
    f.write(mod_api)

os.mkdir("dll")
os.mkdir("mods")
os.mkdir("mods/THE_MOD")

with open("mods/THE_MOD/about.json", "w", encoding="utf-8") as f:
    f.write(about)

with open("mods/THE_MOD/code-Script.grug", "w", encoding="utf-8") as f:
    f.write(code)


state = grug.init()

@state.game_fn
def print_string(code: str):
    print(code)

@state.game_fn
def number_to_string(code: float) -> str:
    return str(code)

@state.game_fn
def print_number(code: float):
    print(code)

@state.game_fn
def ceil(n: float) -> float:
    return math.ceil(n)

try:
    file = state.compile_grug_file("THE_MOD/code-Script.grug")
    script = file.create_entity()
    script.on_exec()
except Exception as e:
    print(e)

