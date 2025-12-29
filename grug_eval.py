import grug
import sys
import os
import tempfile
import shutil

with open("mod_api.json", "r", encoding="utf-8") as f:
    mod_api = f.read()

with open("about.json", "r", encoding="utf-8") as f:
    about = f.read()

idx = 0
while True:
    path = os.path.join(
        tempfile.gettempdir(),
        f"grug-eval-context-{idx}"
    )
    if not os.path.exists(path):
        break
    idx += 1

os.mkdir(path)
os.chdir(path)

with open("mod_api.json", "w", encoding="utf-8") as f:
    f.write(mod_api)

os.mkdir("dll")
os.mkdir("mods")
os.mkdir("mods/THE_MOD")

with open("mods/THE_MOD/about.json", "w", encoding="utf-8") as f:
    f.write(about)

code = sys.argv[1]
with open("mods/THE_MOD/code-Script.grug", "w", encoding="utf-8") as f:
    f.write(code)

state = grug.init()

@state.game_fn
def println(code: str):
    print(code)

@state.game_fn
def number_to_string(code: float) -> str:
    return str(code)

try:
    file = state.compile_grug_file("THE_MOD/code-Script.grug")
    script = file.create_entity()
    script.on_exec()
except Exception as e:
    print(e)

shutil.rmtree(path)

