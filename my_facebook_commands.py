import re
import my_facebook_support
import os

list_of_friend_lists = []
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
  friend_file = open("friends.txt")
  for line in friend_file.readlines():
    if friend == line.rstrip('\n'):
      return True
  return False

def is_root():
  global current_user
  friend_file = open("friends.txt")
  return friend_file.readlines()[0].rstrip('\n') == current_user #if the first line of the friend file is the current user, return true


def make_user(name):
  new_user = my_facebook_support.User(name)
  global current_user
  current_user = new_user
  
# def parse_perms(perm_string):
#   reg_ex = re.search("(^[r-])([w-]$)", perm_string)

#   read_perm = reg_ex.group(0)  #can only be 'r' or '-'
#   write_perm = reg_ex.group(1)  #can only be 'w' or '-'


# def parse_perms(perm_string):
#   perm_string_list = perm_string.split(" ") #access with indexes 0 for owner, 1 for the list, 2 for others
#  return perm_string_list

def find_picture(picture_name):
  global picture_list
  for picture in picture_list:
    if picture.name == picture_name:
      return picture
  return None

def has_read_perms(perm_string, picture_name):
  global current_user
  perm_string_list = perm_string.split(" ") #access with indexes 0 for owner, 1 for the list, 2 for others
  
  picture = find_picture(picture_name)
  
  if current_user == picture.owner and perm_string_list[0][0] == "r":
    return True
  elif current_user in picture.friend_list and perm_string_list[1][0] == "r":
    return True
  elif perm_string_list[2][0] == "r":
    return True

def has_write_perms(perm_string, picture_name):
  global current_user
  perm_string_list = perm_string.split(" ") #access with indexes 0 for owner, 1 for the list, 2 for others
  
  picture = find_picture(picture_name)
  
  if current_user == picture.owner and perm_string_list[0][1] == "w":
    return True
  elif current_user in picture.friend_list and perm_string_list[1][1] == "w":
    return True
  elif perm_string_list[2][1] == "w":
    return True

def friend_add(args):
  friend_name = args[0][0]
  friend_file = open("friends.txt")
  global current_user

  if check_friend_list(friend_name):
    string = f"Cannot add duplicate friends. {friend_name} is already a friend"
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
  elif is_root():
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
  if current_user == None or is_root():
    if check_friend_list(friend_name[0][0]):
      current_user = friend_name[0][0]
      string = f"Viewing as {current_user}"
      print(string)
      log_audit(string)
    else:
      string = f"{friend_name[0][0]} is not a friend"
      print(string)
      log_audit(string)
  else:
    string = "Duplicate logins not allowed"
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


def list_add(args):
  global list_of_friend_lists
  if is_root():
    if args[0][0] not in list_of_friend_lists and args[0][0] != "nil": #duplicate names are not allowed and nil is a reserved name
      new_list = []
      new_list.append(args[0][0]) #make the first index the name of the list
      list_of_friend_lists.append(new_list)  #add the list to list_of_friend_lists
      string = f"Created list: {args[0][0]}"
      print(string)
      log_audit(string)
  else:
    string = "Only the profile owner can create new lists"
    print(string)
    log_audit(string)

def find_friend_list(list_name):
  global list_of_friend_lists
  for friend_list in list_of_friend_lists:
    if friend_list[0] == list_name:
      return friend_list
  return None

def friend_list_add(args):
  global list_of_friend_lists
  if is_root():
    valid_flag = False
    for friend_list in list_of_friend_lists: #look through all the lists
      #list name matches the list name given by args and the friend exists in the friends file
      if friend_list[0] == args[0][1] and check_friend_list(args[0][0]): 
        friend_list.append(args[0][0]) #add the friend to the list
        valid_flag = True
    if not valid_flag:
      string = "Friend does not exist or list does not exist"
      print(string)
      log_audit(string)
    
    string = f"Added {args[0][0]} to the {args[0][1]} list"
    print(string)
    log_audit(string)
  else:
    string = "Only the profile owner can add friends to lists"
    print(string)
    log_audit(string)
  


def post_picture(args):
  if is_root() or check_friend_list(current_user):
    if args[0][0] not in picture_list:
      new_picture = my_facebook_support.Picture(args[0][0], current_user, ["nil"], ["rw", "--", "--"])
      picture_list.append(new_picture)

      new_file = open(f"{args[0][0]}", "w")  # creates a new file
      name = f"{args[0][0]}"
      new_file.write(f"{name}\n")  # writes the name of the picture to the file

      string = f"Posted picture: {args[0][0]} with {current_user} as the owner and default permissions"
      print(string)
      log_audit(string)
    else:
      string = f"{args[0][0]} already exists and duplicates cannot be created"
      print(string)
      log_audit(string)
  else:
    string = "Only the profile owner or friends can post pictures"
    print(string)
    log_audit(string)


def chlst(args):
  global current_user
  picture = find_picture(args[0][0])
  desired_list = find_friend_list(args[0][1])
  if picture != None and desired_list != None:
    if is_root() or current_user == picture.owner:
      if current_user in desired_list or desired_list == "nil" or is_root():
        picture.friend_list = desired_list
        string = f"Changed the list for {args[0][0]} to {desired_list[0]} by {current_user}"
        print(string)
        log_audit(string)
    else:
      string = "Only the profile owner or the picture owner can change the list"
      print(string)
      log_audit(string)
  else:
    string = "Picture or list does not exist"
    print(string)
    log_audit(string)

def chmod(args):
  global current_user
  picture = find_picture(args[0][0])
  if picture != None:
    if is_root() or current_user == picture.owner:
      perms_list = args[0][1].split(" ")
      picture.perms = perms_list
      string = f"Changed the permissions for {args[0][0]} to {args[0][1]} by {current_user}"
      print(string)
      log_audit(string)
    else:
      string = "Only the profile owner or the picture owner can change the permissions"
      print(string)
      log_audit(string)
  else:
    string = f"The picture {args[0][0]} does not exist"
    print(string)
    log_audit(string)


def chown(args):
  picture = find_picture(args[0][0])
  if picture != None and check_friend_list(args[0][1]):
    if is_root():
      picture.owner = args[0][1]
      string = f"Changed the owner for {args[0][0]} to {args[0][1]}"
      print(string)
      log_audit(string)
    else:
      string = "Only the profile owner can change the owner of pictures"
      print(string)
      log_audit(string)
  else:
    string = "Picture or new owner does not exist"
    print(string)
    log_audit(string)


def read_comments(args):
  global current_user
  picture = find_picture(args[0][0])
  allow_flag = False
  if is_root() or check_friend_list(current_user):
    if current_user == picture.owner and picture.perms[0][0] == "r": #The owner has permission to read
      allow_flag = True
    elif current_user in picture.friend_list and picture.perms[1][0] == "r": #The user is in the friend list and has permission to read
      allow_flag = True
    elif picture.perms[2][0] == "r": #Everyone has permission to read
      allow_flag = True
    
    if allow_flag:
      file_name = args[0][0]
      picture_file = open(file_name, "r")
      next(picture_file)
      next_line = picture_file.readline().rstrip('\n')
      string = f"Reading comments from {file_name} as {current_user}: "
      print(string)
      log_audit(string)

      my_facebook_support.make_blue()
      while next_line:
        print(f"\t{next_line}")
        log_audit(f"\t{next_line}")
        next_line = picture_file.readline().rstrip('\n')
      picture_file.close()
      my_facebook_support.make_white()
    else:
      string = f"{current_user} does not have permission to read comments from {args[0][0]}"
      print(string)
      log_audit(string)
  else:
    string = f"{current_user} is not a friend"
    print(string)
    log_audit(string)


def write_comments(args):
  global current_user
  if is_root or check_friend_list(current_user):
    if find_picture(args[0][0]) != None:
      picture = find_picture(args[0][0])
      allow_flag = False
      
      if current_user == picture.owner and picture.perms[0][1] == "w": #The owner has permission to write
        allow_flag = True
      elif current_user in picture.friend_list and picture.perms[1][1] == "w": #The user is in the friend list and has permission to write
        allow_flag = True
      elif picture.perms[2][1] == "w": #Everyone has permission to write
        allow_flag = True
      
      if allow_flag:
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
      else:
        string = f"{current_user} does not have permission to write comments to {args[0][0]}"
        print(string)
        log_audit(string)
    else:
      string = f"{args[0][0]} does not exist"
      print(string)
      log_audit(string)
  else:
    string = f"{current_user} is not a friend"
    print(string)
    log_audit(string)

def log_lists():
  list_file = open("lists.txt", "a")
  pictures_file = open("pictures.txt", "a")
  picture_name_list = []

  for list in list_of_friend_lists:
    list_file.write(f"{list[0]}: ")
    list_file.write(', '.join(list[1:]))
    #list_file.write("\n")
  
  for picture in picture_list:
    picture_name_list.append(picture.name)
  pictures_file.write("Pictures: ")
  pictures_file.write(', '.join(picture_name_list))

# takes args but doesn't use them. This is a consequence of how the process_cmd() function works
def end(args):
  """ends the program"""
  string = "Ending program..."
  print(string)
  log_audit(string)
  string = "Writing friends.txt, lists.txt, pictures.txt, and audit.txt..."
  log_lists()
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
    COMMAND_DICT[command](args) #calls the function associated with the given command in the command dictionary
  else:
    print(f"Unsupported Command: {command} {args[0]}")
    return
