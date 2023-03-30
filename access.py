import sys
import os
import my_facebook_commands

cwd = os.getcwd()  #current working directory


def check_file_exists():
  if (os.path.exists(cwd + "/audit.txt")):
    open("audit.txt", "w").close()  #clears out the txt file
  if (os.path.exists(cwd + "/friends.txt")):
    open("friends.txt", "w").close()
  if (os.path.exists(cwd + "/lists.txt")):
    open("lists.txt", "w").close()
  if (os.path.exists(cwd + "/pictures.txt")):
    open("pictures.txt", "w").close()
  


check_file_exists()

file_argument = sys.argv[1]  #get command line argument

input_file = open(f"{cwd}/{file_argument}", 'r')  #open the command file

while (input_file):
  command_line = input_file.readline().strip()  #read a line from the file

  if command_line:
    my_facebook_commands.parse_command(command_line)
  else:
    break
