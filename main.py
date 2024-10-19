
# This will the main entry point of the program, and all other programs will be run from here.

import Render
import os

plugins_file = open("plugins.txt", 'r')
plugins_raw = plugins_file.read()
plugins_file.close()
plugins = plugins_raw[:-1].split(' ')
import_mods = ''
contents_arry: list[str] = []
for plgn in plugins:
    import_mods += f"import {plgn}\n"
exec(import_mods)

plugin_loop = ''
for plgn in plugins:
    plugin_loop += f"contents_arry += [{plgn}.loop(cmd, focus_win_name)]\n"

cont = True

print("Initialising - press any key")
focus_win_no = 0

while cont:
    contents_arry = []
    focus_win_name = Render.wins[focus_win_no].name
    cmd = input("?: ")
    exec(plugin_loop)    
    Render.render(focus_win_name, contents_arry)
    focus_win_no = 0
            
