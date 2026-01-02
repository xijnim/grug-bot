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

os.mkdir("mods")
os.mkdir("mods/THE_MOD")

with open("mods/THE_MOD/about.json", "w", encoding="utf-8") as f:
    f.write(about)

with open("mods/THE_MOD/code-Script.grug", "w", encoding="utf-8") as f:
    f.write(code)

from grug.packages import grug_stdlib, grug_numpy

state = grug.init(
    packages=[
        grug_stdlib.get(),
        grug_numpy.get(),
    ]
)

try:
    file = state.compile_grug_file("THE_MOD/code-Script.grug")
    script = file.create_entity()
    script.on_exec()
except Exception as e:
    print(e)

