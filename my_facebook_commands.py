import re
import my_facebook_support
import os

friend_lists = []
picture_list = []
current_user = None


def log_audit(message):
  audit_file = open("audit.txt", "a")
  audit_file.write(message + "\n")
  audit_file.close()


def log_friend_list(friend):
  friend_list_file = open("friends.txt", "a")
  friend_list_file.write(friend + "\n")
  friend_list_file.close()


def check_friend_list(friend):
  friend_file = open("friends.txt").read()
  if (friend in friend_file):
    return True
  return False


def make_user(name):
  new_user = my_facebook_support.User(name)
  global current_user
  current_user = new_user


def friend_add(args):
  friend_name = args[0][0]
  friend_file = open("friends.txt")
  global current_user

  if check_friend_list(friend_name):
    string = "Cannot add duplicate friends"
    print(string)
    log_audit(string)
    return

  

  # This means this is the first run of this command, so set the currrent user to the first "friend"
  if os.stat("friends.txt").st_size == 0:
    current_user = friend_name
    log_friend_list(friend_name)
    string = f"Added {friend_name} as a friend"
    print(string)
    log_audit(string)

  # the current user must be "root" (the first user in the friend file)
  elif friend_file.readlines()[0].rstrip('\n') == current_user:
    log_friend_list(friend_name)
    string = f"Added {friend_name} as a friend"
    print(string)
    log_audit(string)
    
  else:
    string = "This user cannot add friends"
    print(string)
    log_audit(string)

  friend_file.close()


def view_by(friend_name):
  global current_user
  if (check_friend_list(friend_name[0][0])):
    current_user = friend_name[0][0]
    string = f"viewing as {current_user}"
    print(string)
    log_audit(string)
  else:
    string = f"{friend_name[0][0]} is not a friend"
    print(string)
    log_audit(string)


# takes args but doesn't use them. This is a consequence of how the process_cmd() function works
def logout(args):
  """logs out the current user"""
  global current_user
  string = f"{current_user} logged out"
  current_user = None
  print(string)
  log_audit(string)


def list_add(list_name):
  string = f"Created list: {list_name[0][0]}"
  print(string)
  log_audit(string)


def friend_list_add(args):
  string = f"Added {args[0][0]} to the {args[0][1]} list"
  print(string)
  log_audit(string)


def post_picture(args):
  new_picture = my_facebook_support.Picture(
      args[0][0], current_user, None, None)
  picture_list.append(new_picture)

  open(f"{args[0][0]}", "w").close()  # creates a new file

  string = f"Posted picture: {args[0][0]} with {current_user} as the owner and default permissions"
  print(string)
  log_audit(string)


def chlst(args):
  string = f"Changed the list for {args[0][0]} to {args[0][1]}"
  print(string)
  log_audit(string)


def chmod(args):
  global current_user
  string = f"Changed the permissions for {args[0][0]} to {args[0][1]} by {current_user}"
  print(string)
  log_audit(string)


def chown(args):
  string = f"Changed the owner for {args[0][0]} to {args[0][1]}"
  print(string)
  log_audit(string)


def read_comments(args):
  file_name = args[0][0]
  picture_file = open(file_name, "r")
  next_line = picture_file.readline().rstrip('\n')
  string = f"Reading comments from {file_name}: "
  print(string)
  log_audit(string)

  my_facebook_support.make_blue()
  while next_line:
    print(f"\t{next_line}")
    log_audit(f"\t{next_line}")
    next_line = picture_file.readline().rstrip('\n')
  picture_file.close()
  my_facebook_support.make_white()


def write_comments(args):
  global current_user
  file_name = args[0][0]
  comments = args[0][1]

  picture_file = open(file_name, "a")
  picture_file.write(comments + "\n")
  picture_file.close()

  string = f"Writing comments to {file_name} as {current_user}: "
  print(string)
  log_audit(string)

  my_facebook_support.make_green()
  print(f"\t{comments}")
  log_audit(f"\t{comments}")
  my_facebook_support.make_white()


# takes args but doesn't use them. This is a consequence of how the process_cmd() function works
def end(args):
  """ends the program"""
  string = "Ending program..."
  print(string)
  log_audit(string)
  string = "Writing friends.txt, lists.txt, pictures.txt, and audit.txt..."
  print(string)
  log_audit(string)


COMMAND_DICT = {
    'friendadd': friend_add,
    'viewby': view_by,
    'logout': logout,
    'listadd': list_add,
    'friendlist': friend_list_add,
    'postpicture': post_picture,
    'chlst': chlst,
    'chmod': chmod,
    'chown': chown,
    'readcomments': read_comments,
    'writecomments': write_comments,
    'end': end
}


def parse_command(command_string):
  reg_ex = re.search(
      "^([^\s]+)[ ]?([^\s]+)?[ ]?(.+)?", command_string
  )  # matches the entire command string, splitting it into 3 groups
  cmd = reg_ex.group(1)  # pulls the command portion of the string
  arg1 = reg_ex.group(2)  # pulls the first argument
  arg2 = reg_ex.group(3)  # pulls the second argument

  args = (arg1, arg2)
  process_cmd(cmd, args)


def process_cmd(command, *args):
  if command in COMMAND_DICT:
    COMMAND_DICT[command](args)
  else:
    print(f"Unsupported Command: {command} {args[0]}")
    return
