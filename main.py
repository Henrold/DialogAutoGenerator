#HENROLD
import sys

data = []
with open(f"{sys.argv[1]}.select") as input_file:
    for line in input_file:
        data.append(line.rstrip())

title = data.pop(0)
craw = data.pop(0)
if craw == "default":
    cancel = "goto exit_app"
else:
    cancel = craw

generator = []

for dataline in data:
    generator.append(dataline.split(","))

file = ""

file += "@echo off\ncls\n\n"

# title
file += f"dialog --menu \"{title}\" 15 50 5 ^\n"

for item in generator:
    file += f"  \"{item[0]}\" \"{item[1]}\" ^\n"

file += "  2>ans_stderr.txt\n\ncls\nset ANSWERLEV=%ERRORLEVEL%\nset /p ANSWERERR=<ans_stderr.txt\ndel ans_stderr.txt\n\n"
file += "if \"%ANSWERLEV%\" == \"1\" goto cancel\nif \"%ANSWERLEV%\" == \"255\" goto exit_app\n\n"

for item in generator:
    location = item[0].replace(" ", "_")
    file += f"if \"%ANSWERERR%\" == \"{item[0]}\" goto {location}\n"

file += "EXIT /B 0\n\n"

for item in generator:
    location = item[0].replace(" ", "_")
    file += f":{location}\n{item[2].replace("\\n","\n")}\ngoto exit_app\n\n"

file += f":cancel\n{cancel.replace("\\n","\n")}\n\n:exit_app"

try:
    output_title = sys.argv[2]
except:
    output_title = sys.argv[1]

with open(f"{output_title}.bat", "w") as output_file:
    output_file.write(file)
