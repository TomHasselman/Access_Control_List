import sys


class User:

  def __init__(self, name):
    self.name = name


class Picture:

  def __init__(self, name, owner, friend_list, perms):
    self.name = name
    self.owner = owner
    self.friend_list = friend_list
    self.perms = perms


def make_blue():
  sys.stdout.write("\u001b[34m")


def make_green():
  sys.stdout.write("\u001b[32m")


def make_white():
  sys.stdout.write("\u001b[37m")
