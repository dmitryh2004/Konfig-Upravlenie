# This is a sample Python script.
import sys
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from zipfile import ZipFile
import argparse

Current_Directory = ""  # can be changed only by "change_directory_start" func
ROOT_PATH = "FileSystem/"  # constant


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('ziploc')
    parser.add_argument('-s', '--script', nargs='?')

    return parser


def show_directory(zipfile, dirpath):  # ls command
    ziplist = zipfile.infolist()
    level = dirpath.count('/')
    print("==============================")
    print("Content of directory " + dirpath + ":")
    print("==============================")
    if not dirpath == ROOT_PATH:
        print("../")
    for entry in ziplist:
        if entry.filename.count('/') == level + 1 and entry.filename.find(dirpath) != -1 and entry.is_dir():
            tmp = entry.filename
            temp_int = 0
            for i in range(0, len(tmp)):
                if (tmp[i] == '/'):
                    if tmp[i+1:].count('/') == 1:
                        temp_int = i+1
                        break
            print(entry.filename[temp_int:])
    for entry in ziplist:
        if entry.filename.count('/') == level and entry.filename.find(dirpath) != -1 and not entry.is_dir():
            tmp = entry.filename
            temp_int = 0
            for i in range(0, len(tmp)):
                if (tmp[i] == '/'):
                    if tmp[i + 1:].count('/') == 0:
                        temp_int = i+1
                        break
            print(entry.filename[temp_int:])
    print("==============================")


def go_to_dir(zipfile, cd, direction, add):  # cd command stuff
    ziplist = zipfile.infolist()
    level = (ROOT_PATH + cd).count('/')
    if direction == "up":
        if level == 1: return cd
        last = len(cd)
        for i in range(last - 2, -1, -1):
            if cd[i] == '/':
                last = i
                break
            if i == 0:
                return ""
        temp = ""
        for i in range(0, last + 1):
            temp += cd[i]
        return temp
    else:
        for entry in ziplist:
            if entry.filename.count('/') == level + 1 and entry.filename.find(ROOT_PATH + cd) != -1 and entry.is_dir():
                if (ROOT_PATH + cd + add) == entry.filename:
                    temp = entry.filename[len(ROOT_PATH):]
                    return temp
        return "Directory not found"


def change_directory_start(zipfile, newdir):  # cd command
    level = Current_Directory.count('/')
    cd = Current_Directory
    nd = newdir
    temp = ""
    cut = 0
    while len(nd) > 0:
        temp = ""
        for i in range(0, len(nd)):
            temp += nd[i]
            if nd[i] == "/":
                cut = i
                break
        if temp == "../":
            cd = go_to_dir(zipfile, cd, "up", None)
        else:
            tmp = go_to_dir(zipfile, cd, "down", temp)
            if tmp != "Directory not found":
                cd = tmp
            else:
                print("Invalid path to new directory")
                return Current_Directory
        nd = nd[cut + 1:]
    return cd


def pwd():
    return ROOT_PATH + Current_Directory


def cat(zipfile, filepath):
    ziplist = zipfile.infolist()
    level = pwd().count('/')
    for entry in ziplist:
        if entry.filename.count('/') == level and entry.filename == pwd() + filepath and not entry.is_dir():
            with zipfile.open(entry.filename, "r") as file:
                print("==============================")
                print("File " + filepath + ":")
                print("==============================")
                for line in file.readlines():
                    print(line.decode("utf-8").replace('\r', '').replace('\n', ''))
                print("==============================")
            return
    print("File " + filepath + " not found")


def executecmd(root, cmd_line):
    global Current_Directory
    if cmd_line == "exit":
        return "exit"
    elif cmd_line.count('|') > 0:
        cmds = cmd_line.split('|')
        for cmd1 in cmds:
            cmd1 = cmd1.lstrip().rstrip()
            if cmd1 == "exit":
                break
            elif cmd1 == "pwd":
                print(pwd())
            elif cmd1 == "ls":
                show_directory(root, pwd())
            elif cmd1.find('cd') != -1:
                tmp = cmd1[3:]
                Current_Directory = change_directory_start(root, tmp)
            elif cmd1.find('cat') != -1:
                tmp = cmd1[4:]
                cat(root, tmp)
            elif cmd1 == "help":
                print("Список поддерживаемых команд:\nls - текущая директория\npwd - вывести путь к"
                      "текущей директории\ncd <newdir> - смена директории\ncat <filepath> - прочесть файл"
                      "в текущей директории\n"
                      "exit - выход\n<command1> | <command2> [| <command3> ...] - выполнить цепочку команд")
            else:
                print("Incorrect command at index " + str(cmd_line.find(cmd1)) + " of the command chain")
                break
    elif cmd_line == "pwd":
        print(pwd())
    elif cmd_line == "ls":
        show_directory(root, pwd())
    elif cmd_line.find('cd') != -1:
        tmp = cmd_line[3:]
        Current_Directory = change_directory_start(root, tmp)
    elif cmd_line.find('cat') != -1:
        tmp = cmd_line[4:]
        cat(root, tmp)
    elif cmd_line == "help":
        print("Список поддерживаемых команд:\nls - текущая директория\npwd - вывести путь к"
              "текущей директории\ncd <newdir> - смена директории\ncat <filepath> - прочесть файл"
              "в текущей директории\n"
              "exit - выход\n<command1> | <command2> [| <command3> ...] - выполнить цепочку команд")
    else:
        print("Incorrect command")


def execute_vshell():
    global ROOT_PATH
    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])
    zip_path = args.ziploc
    with ZipFile(zip_path, "r") as root:
        if not root:
            pass
        else:
            ziplist = root.infolist()
            temp = ziplist[0].filename
            temp_split = temp.split("/")
            ROOT_PATH = temp_split[0] + "/"
            if args.script is not None:
                with open(args.script, "r") as script_file:
                    for cmdline in script_file.readlines():
                        if executecmd(root, cmdline.replace('\r', '').replace('\n', '')) == "exit": return
            while True:
                cmd = str(input())
                if executecmd(root, cmd) == "exit": return


if __name__ == '__main__':
    execute_vshell()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
