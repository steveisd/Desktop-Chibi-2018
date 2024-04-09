"""
Written 2018.
Edited for clarity and shared for fun 05-31-2023.
Tested in windows since that's the only OS we have (so it may or may not work in others).

Goes with chibi.pyw:
Put in the same directory as chibi.pyw and run to "recompile" chibi.pyw. Useful when adding new scripts as commands and not having to edit the code manually.
Every time chibiselfparse.py is run, the old chibi.pyw file is renamed and moved to a backup folder
and the new chibi file itself is executed

Note: if you're using this script, make sure to sync up the directories between this script and chibi.pyw!
"""

import os, shutil, subprocess
from datetime import datetime

excluded = ["example.py"] #put python files here to not be excluded from chibi's script menu
make, origs, korigs = [], [], []
new_parse = ""

prepend = "/".join(os.path.abspath(__file__).split("\\")[:-1])
backup_dir = "backup" #folder where backups are saved, changed as needed
scripts_dir = "scripts" #folder where scripts are, changed as needed
chibi_file = "chibi.pyw" #chibi files name, changed as needed

#backup old chibi file, just in case
shutil.copy(os.path.join(prepend, chibi_file), os.path.join(prepend, backup_dir, chibi_file.split(".")[0] + " (" + datetime.now().strftime("%m-%d-%Y - %H-%M-%S") + ").pyw"))

#parsing
for file in os.listdir(os.path.join(prepend, scripts_dir)):
    if file.endswith(".py") and not file in excluded:
        make.append(file)

with open(os.path.join(prepend, chibi_file), "r") as f:
    for i in f.readlines():
        if 'self.popup2.add_command(label = "' in i:
            if "MAIN" in i:
                new_parse += i
            elif any(x in i for x in korigs):
                origs.append(i)
        else:
            new_parse += i

with open(os.path.join(prepend, chibi_file), "w") as f:
    f.write(new_parse)

new_parse = ""
make.sort()

with open(os.path.join(prepend, chibi_file), "r") as f:
    for i in f.readlines():
        new_parse += i
        if "self.popup2.add_separator()" in i:
            for j in origs:
                new_parse += j
            for command in make:
                new_parse += '        self.popup2.add_command(label = "' + command.capitalize().replace("_", " ")[:-3] + '", command = lambda: self.deploy(os.path.join(prepend, "' + scripts_dir + '", "' + command + '")))\n'

with open(os.path.join(prepend, chibi_file), "w") as f:
    f.write(new_parse)

#executing the new chibi file
subprocess.call(["cmd.exe", "/c", "START", "pythonw ", os.path.join(prepend, chibi_file)])
