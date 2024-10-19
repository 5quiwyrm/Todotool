
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

Todos_uncompleted = open("Todos_uncompleted.txt", 'r')
Todos_uncompleted_raw: str = Todos_uncompleted.read()
Todos_uncompleted.close()

Todos_completed = open("Todos_completed.txt", 'r')
Todos_completed_raw: str = Todos_completed.read()
Todos_completed.close()

def valid_date(date_int: int) -> bool:
    year = date_int // 10000
    month = (date_int - year * 10000) // 100
    day = (date_int - year * 10000 - month * 100)
    len_mon = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if year % 4 == 0 or year % 400 not in [100, 200, 300]:
        len_mon[1] = 29
    if -1 < year < 10000 and 0 < month < 13 and day - 1 < len_mon[month - 1]:
        return True
    else: return False

class todo:
    def __init__(self, title: str, setdate: int, duedate: int) -> None:
        self.title: str = title
        if valid_date(setdate): self.setdate: int = setdate
        if valid_date(duedate): self.duedate: int = duedate
    def __str__(self) -> str:
        return f"{self.title}|{self.setdate}|{self.duedate}^"

def to_todo(entry_str: str):
    entry_array = entry_str.split('|')
    try:
        return todo(entry_array[0], int(entry_array[1]), int(entry_array[2]))
    except:
        return todo('Invalid entry', 19700101, 19700101)

def save_todos() -> int:
    try:
        Todos_file = open("Todos_uncompleted.txt", 'w')
        for entry in Todo_uncompleted_list:
            Todos_file.write(str(entry))
        Todos_file.close()
        Todos_file = open("Todos_completed.txt", 'w')
        for entry in Todo_completed_list:
            Todos_file.write(str(entry))
        Todos_file.close()
        return 0
    except:
        return 1

def complete(task) -> int:
    if task in Todo_uncompleted_list:
        Todo_uncompleted_list.remove(task)
        Todo_completed_list.append(task)
        return 0
    else:
        return 1

def delete(task): # You are only allowed to delete completed tasks.
    if task in Todo_completed_list:
        Todo_completed_list.remove(task)
        return 0
    else:
        return 1

def reprise(task):
    if task in Todo_completed_list:
        Todo_completed_list.remove(task)
        Todo_uncompleted_list.append(task)
        return 0
    else:
        return 1

def sortlist() -> None:
    Todo_uncompleted_list.sort(key = lambda x: x.duedate)
    Todo_completed_list.sort(key = lambda x: x.duedate)

def contents(page) -> str:
    sortlist()
    global content_mode, mode
    if content_mode == 0:
        ret = f" Showing entries number {10 * page} to {10 * page + 10}:\n"
        for i in range(len(Todo_uncompleted_list)):
            if 10 * page - 1 < i < 10 + 10 * page - 1:
                tb_appended = f" {i}. {Todo_uncompleted_list[i].title}"
                if len(tb_appended) > 49:
                    tb_appended = tb_appended[:50]
                    tb_appended += '-'
                tb_appended += f" | Due: {Todo_uncompleted_list[i].duedate // 10000}-{Todo_uncompleted_list[i].duedate // 100 % 100}-{Todo_uncompleted_list[i].duedate % 100}\n"
            ret += tb_appended
    elif content_mode == 1:
        i = curr_view + 10 * page
        ret = f" Title: {Todo_uncompleted_list[i].title}\n Due: {Todo_uncompleted_list[i].duedate // 10000}-{Todo_uncompleted_list[i].duedate // 100 % 100}-{Todo_uncompleted_list[i].duedate % 100}\n Set: {Todo_uncompleted_list[i].setdate // 10000}-{Todo_uncompleted_list[i].setdate // 100 % 100}-{Todo_uncompleted_list[i].setdate % 100}"
    elif content_mode == 20:
        ret = f" Title: {tb_added.title}\n Due: {tb_added.duedate // 10000}-{tb_added.duedate // 100 % 100}-{tb_added.duedate % 100}\n Set: {tb_added.setdate // 10000}-{tb_added.setdate // 100 % 100}-{tb_added.setdate % 100}"
    elif content_mode == 21:
        ret = f" Title: {tb_added.title}\n Due: {tb_added.duedate // 10000}-{tb_added.duedate // 100 % 100}-{tb_added.duedate % 100}\n Set: {tb_added.setdate // 10000}-{tb_added.setdate // 100 % 100}-{tb_added.setdate % 100}\n\n\n Are you sure you want to add this to the todos? (y/n)"
    elif content_mode == 30:
        i = curr_view + 10 * page
        ret = f" Task: {Todo_uncompleted_list[i].title}\n Due: {Todo_uncompleted_list[i].duedate // 10000}-{Todo_uncompleted_list[i].duedate // 100 % 100}-{Todo_uncompleted_list[i].duedate % 100}\n Set: {Todo_uncompleted_list[i].setdate // 10000}-{Todo_uncompleted_list[i].setdate // 100 % 100}-{Todo_uncompleted_list[i].setdate % 100}\n has just been completed!"
        content_mode = 0
        mode = ' '
        complete(Todo_uncompleted_list[i])
    ret = f" Mode: {mode}\n" + ret
    return ret

Todo_uncompleted_list = []
for entry in Todos_uncompleted_raw.split('^')[:-1]:
    if to_todo(entry) != todo('Invalid entry', 19700101, 19700101):
        Todo_uncompleted_list.append(to_todo(entry))
Todo_completed_list = []
for entry in Todos_completed_raw.split('^')[:-1]:
    if to_todo(entry) != todo('Invalid entry', 19700101, 19700101):
        Todo_completed_list.append(to_todo(entry))


page = 0
mode = ' '
content_mode = 0
curr_view = 0
tb_added = todo('Invalid entry', 19700101, 19700101)

def loop(cmd, focus_win_name):
    global mode, curr_view, page, content_mode, Todo_uncompleted_list, tb_added
    if 'Todos' in focus_win_name:
        if mode == ' ':
            if cmd == 'd':
                page += 1
            elif cmd == 'u':
                page -= 1
            elif cmd == 's':
                mode = 'r'
            elif cmd == 'x':
                content_mode = 0
            elif cmd == 'w':
                save_todos()
            elif cmd == 'c':
                mode = 'c'
            elif cmd == 'a':
                content_mode = 20
                mode = 'title_req'
            page = page % (len(Todo_uncompleted_list) // 10 + 1)
        elif mode == 'r':
            try:
                if -1 < int(cmd) < 10 and int(cmd) <= len(Todo_uncompleted_list):
                    content_mode = 1
                    curr_view = int(cmd)
                    mode = ' '
            except:
                mode = ' '
                input("After entering select mode, the only recognised commands are integers between 0 and 9 inclusive.")
        elif mode == 'c':
            try:
                if -1 < int(cmd) < 10 and int(cmd) <= len(Todo_uncompleted_list):
                    content_mode = 30
                    mode = 'no_op'
                    curr_view = int(cmd)
            except:
                mode = ' '
                input("After entering select mode, the only recognised commands are integers between 0 and 9 inclusive.")
        elif mode == 'title_req':
            if cmd != '':
                tb_added.title = cmd
            mode = 'setdate_req'
        elif mode == 'setdate_req':
            try:
                if valid_date(int(cmd)):
                    tb_added.setdate = int(cmd)
                    mode = 'duedate_req'
                else:
                    input("Invld: date: must be between 19700101 and 99999999")
                    mode = ' '
                    content_mode = 0
            except:
                content_mode = 0
                mode = ' '
                input("Invld: date: must be int")
        elif mode == 'duedate_req':
            try:
                if valid_date(int(cmd)):
                    tb_added.duedate = int(cmd)
                    mode = 'add_conf'
                    content_mode = 21
                else:
                    input("Invld: date: must be between 19700101 and 99999999")
                    mode = ' '
                    content_mode = 0
            except:
                content_mode = 0
                mode = ' '
                input("Invld: date: must be int")
        elif mode == 'add_conf':
            if cmd == 'y' and tb_added not in Todo_uncompleted_list:
                Todo_uncompleted_list += [tb_added]
            tb_added = todo('Invalid entry', 19700101, 19700101)
            content_mode = 0
            mode = ' '
        else:
            pass
    return contents(page)
    

