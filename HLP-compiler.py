#! /bin/python
#-*- encoding: utf-8 -*-

# imports
import sys
import os

# dev space

## check file
if len(sys.argv) < 2 :
    sys.exit("No file specified")

elif "-h" in sys.argv :
    print("Usage:")
    print("\tHLP -h               'Call help'")
    print("\tHLP -l               'list instructions'")
    print("\tHLP [file-path]      'File-path is the file name or file path of file to compile'")
    sys.exit()

elif "-l" in sys.argv :
    print("Instructions:")
    print("\t 👉: moves the memory pointer to the next cell")
    print("\t 👈: moves the memory pointer to the previous cell")
    print("\t 👆: increment the memory cell at the current position")
    print("\t 👇: decreases the memory cell at the current position.")
    print("\t 🤜: if the memory cell at the current position is 0,\n\t     jump just after the corresponding fist_left")
    print("\t 🤛: if the memory cell at the current position is not 0,\n\t     jump just after the corresponding fist_right")
    print("\t 👊: Display the current character represented by the\n\t     ASCII code defined by the current position.")
    sys.exit()

elif not(os.path.exists(sys.argv[1])):
    sys.exit("The file '" + str(sys.argv[1]) + "' does not exist!!")

## function

def execute_hpl_file():
    '''
    Execute the input file from instructions
    '''
    # read
    path_file = sys.argv[1]
    content = ''
    with open(path_file, mode='r') as file:
        content = file.read()

    #
    env = [0]
    loop_stack = []
    memory_pointer = 0
    ignore=0
    content_pointer = 0
    output = ""
    # debug vars
    column = 0
    row = 0


    while content_pointer < len(content):
        column +=1
        if content[content_pointer] == '\n':
            row +=1
            column =0
        else:
            memory_pointer,content_pointer, ignore,output =  evaluate_char(ignore,\
                                                            content[content_pointer],\
                                                            env,\
                                                            memory_pointer,\
                                                            content_pointer,\
                                                            loop_stack,\
                                                            column,\
                                                            row,\
                                                            output)
        content_pointer +=1


    # read Bucle
    # for content_pointer in range(len(content)):
    #     column +=1
    #     if content[content_pointer] == '\n':
    #         row +=1
    #         column =0
    #     else:
    #         memory_pointer,content_pointer =  evaluate_char(ignore,\
    #                                         content[content_pointer],\
    #                                         env,\
    #                                         memory_pointer,\
    #                                         content_pointer,\
    #                                         loop_stack,\
    #                                         column,\
    #                                         row)
    #         content_pointer = -2


def evaluate_char(ignore, str_hand, env, memory_pointer, content_pointer, loop_stack, column, row, output):
    # print("--Enter-- ["+ output + "]")
    # print("strh", str_hand)
    # print("content pointer", content_pointer)
    # print("ENV: ", env)
    # print("Momory pointer:", memory_pointer)
    # print("loop stack", loop_stack)
    # print("==========================")
    # input()

    if str_hand == '👉' and not(ignore):
        memory_pointer+=1
        if len(env) <= memory_pointer:
            env.append(0)
    elif str_hand == '👈' and not(ignore):
        if memory_pointer == 0:

            sys.exit("ERROR!!: -- memory overflow on col:" + \
                         str(column) + \
                         " row:" +\
                         str(row) +\
                         " --")
        memory_pointer -=1
    elif str_hand == '👆' and not(ignore):
        env[memory_pointer] = (env[memory_pointer] + 1) %256

    elif str_hand == '👇' and not(ignore):
        env[memory_pointer] = (env[memory_pointer] - 1) %256 
    elif str_hand == '🤜':
        # verify ignore
        if ignore :
            ignore +=1
        else:
            # verify loop pointer
            if not(loop_stack) or loop_stack[-1] != content_pointer:
                # init loop
                # save content + 1, couse jump just after the corresponding fist_right
                loop_stack.append(content_pointer)

            # verify memory pointer
            if env[memory_pointer] == 0:
                ignore+=1

        pass
    elif str_hand == '🤛':
        if ignore:
            ignore -=1
        if not(ignore):
            if env[memory_pointer] == 0:
                #pop
                loop_stack.pop()
            else:
                content_pointer = loop_stack[-1]
        pass
    elif str_hand == '👊':
        # print(env[memory_pointer], end='')
        output += chr(env[memory_pointer])
        print(chr(env[memory_pointer]), end='')

    return memory_pointer, content_pointer, ignore, output

## calls
execute_hpl_file()
print()
