#!/usr/bin/python3

import os
import sys
class colors: 
    reset='\033[0m'
    bold='\033[01m'
    disable='\033[02m'
    underline='\033[04m'
    reverse='\033[07m'
    strikethrough='\033[09m'
    invisible='\033[08m'
    class fg: 
        black='\033[30m'
        red='\033[31m'
        green='\033[32m'
        orange='\033[33m'
        blue='\033[34m'
        purple='\033[35m'
        cyan='\033[36m'
        lightgrey='\033[37m'
        darkgrey='\033[90m'
        lightred='\033[91m'
        lightgreen='\033[92m'
        yellow='\033[93m'
        lightblue='\033[94m'
        pink='\033[95m'
        lightcyan='\033[96m'
    class bg: 
        black='\033[40m'
        red='\033[41m'
        green='\033[42m'
        orange='\033[43m'
        blue='\033[44m'
        purple='\033[45m'
        cyan='\033[46m'
        lightgrey='\033[47m'

def do_header(filename, header, first):
    if (header == False):
        header = True
        if (first == True):
            print("")
        else:
            first = True
        print(colors.fg.purple+'['+os.path.normpath(filename)+'] :')
    return(header, first)

def check_handler(fichier, filename, header, first):
    count = 0
    if (fichier.readline().strip() != "/*"):
        header,first = do_header(filename, header, first)
        print(colors.fg.red+colors.bold+'    ['+os.path.normpath(filename)+'] Missing or corrupted header'+colors.reset)
        count = 1
    elif (fichier.readline()[0:20] != "** EPITECH PROJECT, "):
        header,first = do_header(filename, header, first)
        print(colors.fg.red+colors.bold+'    ['+os.path.normpath(filename)+'] Missing or corrupted header'+colors.reset)
        count = 2
    elif (fichier.readline()[0:3] != "** "):
        header,first = do_header(filename, header, first)
        print(colors.fg.red+colors.bold+'    ['+os.path.normpath(filename)+'] Missing or corrupted header'+colors.reset)
        count = 3
    elif (fichier.readline().strip() != "** File description:"):
        header,first = do_header(filename, header, first)
        print(colors.fg.red+colors.bold+'    ['+os.path.normpath(filename)+'] Missing or corrupted header'+colors.reset)
        count = 4
    elif (fichier.readline()[0:3] != "** "):
        header,first = do_header(filename, header, first)
        print(colors.fg.red+colors.bold+'    ['+os.path.normpath(filename)+'] Missing or corrupted header'+colors.reset)
        count = 5
    elif (fichier.readline().strip() != "*/"):
        header,first = do_header(filename, header, first)
        print(colors.fg.red+colors.bold+'    ['+os.path.normpath(filename)+'] Missing or corrupted header'+colors.reset)
        count = 6
    if (count != 0 and count < 6):
        while (count < 6):
            fichier.readline()
            count = count + 1
    return(header,first)

def check_coma(fichier, filename, line_str, line, header, first):
    position = 0
    remenber = 0
    while (position != -1):
        try:
            position = line_str.index(',',remenber + 1)
        except:
            position = -1
            continue
        remenber = position
        if (line_str[position+1] != ' '):
            header,first = do_header(filename, header, first)
            print(colors.fg.green+'    ['+os.path.normpath(filename)+':'+str(line)+'] Missing space after comma'+colors.reset)
    return(header,first)

def check_return(fichier, filename, line_str, line, header, first):
    position = line_str.find("return")
    if (position != -1):
        if (line_str[position + 6] != ' ' and line_str[position + 6] == '('):
            header,first = do_header(filename, header, first)
            print(colors.fg.green+'    ['+os.path.normpath(filename)+':'+str(line)+'] Missing space after keyword \'return\''+colors.reset)
    return(header,first)

def check_if(fichier, filename, line_str, line, header, first):
    position = line_str.find("if")
    if (position != -1):
        if (line_str[position + 2] != ' ' and line_str[position + 2] == '('):
            header,first = do_header(filename, header, first)
            print(colors.fg.green+'    ['+os.path.normpath(filename)+':'+str(line)+'] Missing space after keyword \'if\''+colors.reset)
    return(header,first)

def check_while(fichier, filename, line_str, line, header, first):
    position = line_str.find("while")
    if (position != -1):
        if (line_str[position + 5] != ' ' and line_str[position + 5] == '('):
            header,first = do_header(filename, header, first)
            print(colors.fg.green+'    ['+os.path.normpath(filename)+':'+str(line)+'] Missing space after keyword \'while\''+colors.reset)
    return(header,first)

def check_training(fichier, filename, line_str, line, header, first):
    if (line_str.endswith(" \n") or line_str.endswith("\t\n") or line_str.endswith(" ")):
        header,first = do_header(filename, header, first)
        print(colors.fg.green+'    ['+os.path.normpath(filename)+':'+str(line)+'] Trailing space(s) at the end of the line'+colors.reset)
    return(header,first)

def count_line(filename):
    num_lines = 0
    with open(filename, 'r') as f:
        for lined in f:
            num_lines += 1
    return (num_lines)

def check_space_after_word(fichier, filename, line_str, line, header, first):
    header,first = check_coma(fichier, filename, line_str, line, header, first)
    header,first = check_while(fichier, filename, line_str, line, header, first)
    header,first = check_if(fichier, filename, line_str, line, header, first)
    header,first = check_return(fichier, filename, line_str, line, header, first)
    return(header,first)

def not_in_quote(line_str, position_find):
    position_first = 0
    remenber = 0
    while (position_first != -1 or position_first > position_find):
        try:
            position_first = line_str.index('"',remenber + 1)
        except:
            position_first = -1
            continue
        position_last = line_str.index('"',position_first + 1)
        remenber = position_last
        if (position_last > position_find and position_first < position_find):
            return False
    return True

def check_equal(fichier, filename, line_str, line, header, first):
    position = 0
    remenber = 0
    while (position != -1):
        try:
            position = line_str.index('=',remenber + 1)
        except:
            position = -1
            continue
        remenber = position
        if (line_str[position+1] == '='):
            remenber = remenber + 1
            if (not_in_quote(line_str, position) and (line_str[position+2] != ' ' or line_str[position-1] != ' ')):
                header,first = do_header(filename, header, first)
                print(colors.fg.green+'    ['+os.path.normpath(filename)+':'+str(line)+'] Misplaced space(s) around \'==\' sign'+colors.reset)
        elif ((line_str[position+1] != ' ' or (line_str[position-1] != ' ' and line_str[position-1] != '!' and line_str[position-1] != '>' and line_str[position-1] != '<' and line_str[position-1] != '+' and line_str[position-1] != '-' and line_str[position-1] != '/' and line_str[position-1] != '%' and line_str[position-1] != '*')) and line_str[position+1] != '\'' and line_str[position-1] != '\'' and not_in_quote(line_str, position)):
            header,first = do_header(filename, header, first)
            print(colors.fg.green+'    ['+os.path.normpath(filename)+':'+str(line)+'] Misplaced space(s) around \'=\' sign'+colors.reset)
    return(header,first)

def check_sup(fichier, filename, line_str, line, header, first):
    position = 0
    remenber = 0
    while (position != -1):
        try:
            position = line_str.index('>',remenber + 1)
        except:
            position = -1
            continue
        remenber = position
        if (line_str[position+1] == '='):
            remenber = remenber + 1
            if (not_in_quote(line_str, position) and (line_str[position+2] != ' ' or line_str[position-1] != ' ')):
                header,first = do_header(filename, header, first)
                print(colors.fg.green+'    ['+os.path.normpath(filename)+':'+str(line)+'] Misplaced space(s) around \'>=\' sign'+colors.reset)
        elif ((line_str[position+1] != ' ' or line_str[position-1] != ' ') and line_str[position+1] != '\'' and line_str[position-1] != '\'' and not_in_quote(line_str, position)):
            header,first = do_header(filename, header, first)
            print(colors.fg.green+'    ['+os.path.normpath(filename)+':'+str(line)+'] Misplaced space(s) around \'>\' sign'+colors.reset)
    return(header,first)

def check_inf(fichier, filename, line_str, line, header, first):
    position = 0
    remenber = 0
    while (position != -1):
        try:
            position = line_str.index('<',remenber + 1)
        except:
            position = -1
            continue
        remenber = position
        if (line_str[position+1] == '='):
            remenber = remenber + 1
            if (not_in_quote(line_str, position) and (line_str[position+2] != ' ' or line_str[position-1] != ' ')):
                header,first = do_header(filename, header, first)
                print(colors.fg.green+'    ['+os.path.normpath(filename)+':'+str(line)+'] Misplaced space(s) around \'<=\' sign'+colors.reset)
        elif ((line_str[position+1] != ' ' or line_str[position-1] != ' ') and line_str[position+1] != '\'' and line_str[position-1] != '\'' and not_in_quote(line_str, position)):
            header,first = do_header(filename, header, first)
            print(colors.fg.green+'    ['+os.path.normpath(filename)+':'+str(line)+'] Misplaced space(s) around \'<\' sign'+colors.reset)
    return(header,first)

def check_dif(fichier, filename, line_str, line, header, first):
    position = 0
    remenber = 0
    while (position != -1):
        try:
            position = line_str.index('!',remenber + 1)
        except:
            position = -1
            continue
        remenber = position
        if (line_str[position+1] == '='):
            remenber = remenber + 1
            if (not_in_quote(line_str, position) and (line_str[position+2] != ' ' or line_str[position-1] != ' ')):
                header,first = do_header(filename, header, first)
                print(colors.fg.green+'    ['+os.path.normpath(filename)+':'+str(line)+'] Misplaced space(s) around \'!=\' sign'+colors.reset)
    return(header,first)

def check_comp_signe(fichier, filename, line_str, line, header, first, signe):
    position = 0
    remenber = 0
    while (position != -1):
        try:
            position = line_str.index(signe,remenber + 1)
        except:
            position = -1
            continue
        remenber = position + 1
        if (not_in_quote(line_str, position) and ((line_str[position+2] != ' ' and line_str[position+2] != '\n') or line_str[position-1] != ' ')):
            header,first = do_header(filename, header, first)
            print(colors.fg.green+'    ['+os.path.normpath(filename)+':'+str(line)+'] Misplaced space(s) around \''+signe+'\' sign'+colors.reset)
    return(header,first)

def check_math_signe(fichier, filename, line_str, line, header, first, signe):
    position = 0
    remenber = 0
    while (position != -1):
        try:
            position = line_str.index(signe,remenber + 1)
        except:
            position = -1
            continue
        remenber = position
        if (line_str[position+1] == '='):
            remenber = remenber + 1
            if (not_in_quote(line_str, position) and (line_str[position+2] != ' ' or line_str[position-1] != ' ')):
                header,first = do_header(filename, header, first)
                print(colors.fg.green+'    ['+os.path.normpath(filename)+':'+str(line)+'] Misplaced space(s) around \''+signe+'=\' sign'+colors.reset)
        elif (line_str[position:position+2] == "++" or line_str[position:position+2] == "--"):
            remenber = remenber + 1
            if (not_in_quote(line_str, position) and ((line_str[position+2] != ' ' and line_str[position+2] != ';') or line_str[position-1] == ' ')):
                header,first = do_header(filename, header, first)
                print(colors.fg.green+'    ['+os.path.normpath(filename)+':'+str(line)+'] Misplaced space(s) around \''+signe+signe+'\' sign'+colors.reset)
        elif ((line_str[position+1] != ' ' or line_str[position-1] != ' ') and line_str[position+1] != '\'' and line_str[position-1] != '\'' and not_in_quote(line_str, position)):
            header,first = do_header(filename, header, first)
            print(colors.fg.green+'    ['+os.path.normpath(filename)+':'+str(line)+'] Misplaced space(s) around \''+signe+'\' sign'+colors.reset)
    return(header,first)

def check_space_with_math_char(fichier, filename, line_str, line, header, first):
    header,first = check_equal(fichier, filename, line_str, line, header, first)
    header,first = check_sup(fichier, filename, line_str, line, header, first)
    header,first = check_inf(fichier, filename, line_str, line, header, first)
    header,first = check_dif(fichier, filename, line_str, line, header, first)
    header,first = check_comp_signe(fichier, filename, line_str, line, header, first, '||')
    header,first = check_comp_signe(fichier, filename, line_str, line, header, first, '&&')
    header,first = check_math_signe(fichier, filename, line_str, line, header, first, '+')
    header,first = check_math_signe(fichier, filename, line_str, line, header, first, '-')
    header,first = check_math_signe(fichier, filename, line_str, line, header, first, '/')
    header,first = check_math_signe(fichier, filename, line_str, line, header, first, '*')
    header,first = check_math_signe(fichier, filename, line_str, line, header, first, '%')
    return(header,first)

def start(folder_path, first):
    line = 0
    nbr_max = 0
    com = False
    for path, dirs, files in os.walk(folder_path):
        for filename in files:
            if (filename[-2] == "." and (filename[-1] == "h" or filename[-1] == "c")):
                filename = os.path.join(path, filename)
                fichier = open(filename, "r")
                nbr_max = count_line(filename) + 1
                header = False
                header,first = check_handler(fichier, filename, header, first)
                line = 7
                while line < nbr_max:
                    line_str = fichier.readline()
                    if (line_str.find("/*") != -1):
                        com = True
                        header,first = do_header(filename, header, first)
                        print(colors.fg.green+'    ['+os.path.normpath(filename)+':'+str(line)+'] You have leave(s) some comment(s)'+colors.reset)
                    elif (line_str.strip()[0:2] == "**" or line_str.strip()[0:2] == "//"):
                        header,first = do_header(filename, header, first)
                        print(colors.fg.green+'    ['+os.path.normpath(filename)+':'+str(line)+'] You have leave(s) some comment(s)'+colors.reset)
                    if (com == False and line_str.strip()[0:2] != "**" and line_str.strip()[0:2] != "//"):
                        header,first = check_space_after_word(fichier, filename, line_str, line, header, first)
                        header,first = check_space_with_math_char(fichier, filename, line_str, line, header, first)
                        header,first = check_training(fichier, filename, line_str, line, header, first)
                    elif (line_str.find("*/") != -1):
                        com = False
                    line = line + 1

first = False
if (len(sys.argv) == 1):
    start(".", first)
##elif (sys.argv[1] == "-h"):
else:
    count = 1
    while (count < len(sys.argv)):
        start(sys.argv[count], first)
        count = count + 1