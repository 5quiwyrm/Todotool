
import os

# This will use a config file in the style of:
# window-title: (attribute=int ) * n\n
# The config file will also have the name config.txt
# All attributes of windows will be assumed to be the default if not specified.
# The order in which the windows are rendered (even if there are intersects) will the the same as the order in which they are defined in the config.

class window:
    def __init__(self, name, width, height, border_type, x, y, contents):
        self.name = name
        self.width = width
        self.height = height
        self.border_type = border_type
        self.x = x
        self.y = y
        self.contents = contents # This refers to the name of the function that returns the contents
    def __str__(self):
        return f"--------------\nwin name: {self.name}\nwidth | height: {self.width} | {self.height}\nborder type: {self.border_type}\nlocation: {x}, {y}\ncontents: {contents}\n"

config_file = open("config.txt", 'r')
config_file_raw = config_file.read()
config_file.close()
wins_raw = config_file_raw.split('\n')[:-1]
wins: list[window] = []
  
for win in [x.split(' ') for x in wins_raw][:-1]:
    name = ''
    width = 120
    height = 27
    border_type = 0
    x = 0
    y = 0
    contents = ''
    for attribute in win:        
        if attribute[-1] == ':':
            name = attribute[:-1]
        else:
            optn_attr = attribute.split('=')
            if len(optn_attr) != 2:
                raise Exception("Invalid config: format of attribute must be [attr]=[num]")
            if optn_attr[0] == 'width':
                try:
                    if int(optn_attr[1]) < 120:
                        width = int(optn_attr[1])
                    else:
                        raise Exception(f"Invalid config: width of {name} cannot be more than 120")
                except:
                    raise Exception(f"Invalid config: width value {optn_attr[1]} is not recognised")
            elif optn_attr[0] == 'height':
                try:
                    if int(optn_attr[1]) < 26:
                        height = int(optn_attr[1])
                    else:
                        raise Exception(f"Invalid config: height of {name} cannot be more than 27")
                except:
                    raise Exception(f"Invalid config: height value {optn_attr[1]} is not recognised")
            elif optn_attr[0] == 'border_type':
                try:
                    if int(optn_attr[1]) < 1:
                        border_type = int(optn_attr[1])
                    else:
                        raise Exception(f"Invalid config: border_type of {name} cannot be more than 1")
                except:
                    raise Exception(f"Invalid config: border_type {optn_attr[1]} is not recognised")
            elif optn_attr[0] == 'x':
                try:
                    if int(optn_attr[1]) < 26:
                        x = int(optn_attr[1])
                    else:
                        raise Exception(f"Invalid config: x location of {name} cannot be more than 1")
                except:
                    raise Exception(f"Invalid config: x location {optn_attr[1]} is not recognised")
            elif optn_attr[0] == 'y':
                try:
                    if int(optn_attr[1]) < 120:
                        y = int(optn_attr[1])
                    else:
                        raise Exception(f"Invalid config: y location of {name} cannot be more than 120")
                except:
                    raise Exception(f"Invalid config: y location {optn_attr[1]} is not recognised")
            elif optn_attr[0] == 'contents':
                try:
                    if type(eval(optn_attr[1])) is str:
                        contents = optn_attr[1]
                    else:
                        raise Exception(f"Invalid config: contents function of {name} doesn't return a str type object")
                except:
                    raise Exception(f"Invalid config: contents {optn_attr[1]} is not recognised: may contain an error")
            else:
                raise Exception(f"Invalid config: {optn_attr[0]} is not a valid field")
            
    wins.append(window(name, width, height, border_type, x, y, contents)) 

def render(focused_win_name: str, contents_arry: list[str]):
    os.system("cls")
    screen = [[' '] * 120 for i in range(27)]
    for win in wins:
        contents = ' Win ' + str(wins.index(win)) + '\n\n' + contents_arry[eval(eval(win.contents))] + ' '
        line_broken = False
        ptr = 0
        for x in range(win.x, win.x + win.height):
            for y in range(win.y, win.y + win.width):
                if x < 27 and y < 120:
                    if x in [win.x, win.x + win.height - 1] or y in [win.y, win.y + win.width - 1]:
                        screen[x][y] = ('*' if win.name == focused_win_name else '.')
                    else:
                        if contents[ptr] == '\n':
                             line_broken = True
                             ptr += 1
                        if line_broken == False:
                             screen[x][y] = contents[ptr]
                             if ptr != len(contents) - 1: 
                                 ptr += 1
            line_broken = False
    for i in range(27):
        print(i, end = '')
        if i < 10:
            print(' ', end = '')
        print('|', end = '')
        print(*screen[i], sep = '')
