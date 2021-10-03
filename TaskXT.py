import colorama
from colorama import Fore, Style
from os import system, name, remove
from time import sleep

# clear the console
def clear():
  # for windows
  if name == 'nt':
      _ = system('cls')
  # for mac and linux(here, os.name is 'posix')
  else:
      _ = system('clear')

# to give to key of sorted function, transform task
# to order the lists by year, then month, then day and 
# the name of the task at the end
def transform_task(task):
  task, date = task[0].split("$")[0:2]
  day, month, year = list(map(int, date.split("-")))
  return year, month, day, task

# print a subtask with a symbol
def print_subtask(subtask, symbol, priority):
  sub, state = subtask.strip().split("$")
  if state == "1":
    print(Fore.GREEN + ("    * " if symbol == "a" else "    " + str(priority) + " ") + sub + Fore.RED)
  else:
    print(("    * " if symbol == "a" else "    " + str(priority) + " ") + sub)

# to print tasks 
# tasks -> list of the tasks ordered by date
# name -> if is TO DO or COMPLETED
def print_tasks(tasks, name, symbol):
  print((Fore.RED if name == "TO DO" else Fore.GREEN) + name)
  priority = 1
  for task, subtask in tasks:
    task = task.split("$")
    print((Fore.RED if name == "TO DO" else Fore.GREEN) + str(priority) + "\\ " + task[1] + " " + task[0])
    priority += 1
    sub_priority = 1
    for sub in subtask:
      print_subtask(sub, symbol, sub_priority)
      sub_priority += 1

def obtain_tasks():
  try:
    read_tasks = open("tasks.txt", "r")
  except:
    read_tasks = open("tasks.txt", "w")
    read_tasks.close()
    os.mkdir("./tasks")
    read_tasks = open("tasks.txt", "r")
  menu = {"0": {}, "1": {}}
  # for each task search the subtasks
  for task in read_tasks:
    task = task.strip()
    try:
      read_task = open("tasks/" + task.split("$")[0] + ".txt", "r")
    except:
      read_task = open("tasks/dummy", "r")
    menu[task[-1]][task] = []
    for subtask in read_task:
      menu[task[-1]][task].append(subtask.strip())
    menu[task[-1]][task].sort()
    read_task.close()
  read_tasks.close()

  return menu

# search for all the tasks and show them
def open_tasks():
  menu = obtain_tasks()  

  # sort by date
  todo = list(menu["0"].items())
  todo = sorted(todo, key = transform_task)

  # show the tasks for todo
  print_tasks(todo, "TO DO", "a")

  completed = list(menu["1"].items())
  completed = sorted(completed, key = transform_task)

  # show the tasks completed
  print_tasks(completed, "COMPLETED", "a")

def add_task():
  name = input("Name of the task: ")
  date = input("DeadLine: ")

  # add the task in the principal txt
  write_in_tasks = open("tasks.txt", "a")
  write_in_tasks.write(name + "$" + date + "$0\n")
  write_in_tasks.close()

  # adding subtask, creating a txt for the task
  add_subtask = input("Have subtask [y/n]: ")
  if add_subtask == "y":
    write_subtasks = open("tasks/" + name + ".txt", "w")
    while(1):
      subtask = input("Subtask: ")
      write_subtasks.write(subtask + "$0\n")
      add_subtask = input("Have another subtask [y/n]: ")
      if add_subtask == "n":
        break
    write_subtasks.close()

  clear()

def delete_task():
  clear()
  open_tasks()

  while(1):
    to_delete = input(Fore.WHITE + "Task to delete (only the name) or if you don't want to delete something press enter: ")
    
    if to_delete == "":
      print("Nothing deleted!")
      break

    # searching for the task to delete
    read_tasks = open("tasks.txt", "r")
    tasks = []
    found = 0
    for task in read_tasks:
      if to_delete in task:
        found = 1
        continue
      tasks.append(task)
    read_tasks.close()

    if found == 0:
      print(Fore.RED + "The task doesn't exist, try again")
      continue
    # re write the file tasks.txt
    write_tasks = open("tasks.txt", "w")
    for task in tasks:
      write_tasks.write(task)
    write_tasks.close()

    try:
      remove("tasks/" + to_delete + ".txt")
    except:
      found = 0

    break
  print(Fore.GREEN + "Task removed!!!")
  sleep(1)
  clear()

def edit_task():
  clear()

  menu = obtain_tasks() 

  # sort by date
  todo = list(menu["0"].items())
  todo = sorted(todo, key = transform_task)

  # show the tasks for todo
  print_tasks(todo, "TO DO", "n")
  while(1):
    edit = input(Fore.WHITE + "Task to edit (only the name) or if you don't want to delete something press enter: ")

    if edit == "":
      break


    try:
      read_subtasks = open("tasks/" + edit +".txt", "r")
    except:
      print("Task to edit not found, try again")
      continue

    clear()
    print("Actual subtasks of " + edit)
    for subtask in read_subtasks:
      print("* " + subtask.strip().split("$")[0])    
    read_subtasks.close()

    # adding subtask, creating a txt for the task
    add_subtask = input("Erase all subtask and new ones? [y/n]: ")
    if add_subtask == "y":
      write_subtasks = open("tasks/" + edit + ".txt", "w")
      while(1):
        subtask = input("Subtask: ")
        write_subtasks.write(subtask + "$0\n")
        add_subtask = input("Have another subtask [y/n]: ")
        if add_subtask == "n":
          break
      write_subtasks.close()

  clear()

def complete_task():
  clear()

  menu = obtain_tasks()  

  # sort by date
  todo = list(menu["0"].items())
  todo = sorted(todo, key = transform_task)

  # show the tasks for todo
  print_tasks(todo, "TO DO", "n")

  while(1):
    what = input(Fore.WHITE + "Complete a task or subtask [t/s] or if you don't want to complete something press enter: ")
    if what == "t":
      while(1):
        task_to_complete = input("Task to complete (only the name) or if you don't want to complete something press enter: ")

        if task_to_complete == "":
          break

        read_tasks = open("tasks.txt", "r")
        tasks = []
        found = 0
        for task in read_tasks:
          if task_to_complete in task:
            task = list(task)
            task[-2] = "1"
            task = "".join(task)
            found = 1
          tasks.append(task)
        read_tasks.close()

        if found == 0:
          print(Fore.RED + "The task doesn't exist, try again" + Fore.WHITE)
          continue

        try:
          read_subtasks = open("tasks/" + task_to_complete +".txt", "r")
          subtasks = []
          for subtask in read_subtasks:
            subtask = list(subtask)
            subtask[-2] = "1"
            subtask = "".join(subtask)
            subtasks.append(subtask)
          read_subtasks.close()

          # re write the file .txt of the task
          write_subtasks = open("tasks/" + task_to_complete + ".txt", "w")
          for subtask in subtasks:
            write_subtasks.write(subtask)
          write_subtasks.close()
        except:
          nothing = 1

        # re write the file tasks.txt
        write_tasks = open("tasks.txt", "w")
        for task in tasks:
          write_tasks.write(task)
        write_tasks.close()

        print("Task completed!!!")
        sleep(1)
        break
    elif what == "s":
      while(1):
        task = input("Task of the subtask to complete (only the name) or if you don't want to complete something press enter: ")

        if task == "":
          break

        num = input("Number of the subtask to complete of the task (only the name) or if you don't want to complete something press enter: ")

        if num == "":
          break
        
        read_subtasks = open("tasks/" + task +".txt", "r")
        subtasks = []
        i = 1
        found = 0
        for subtask in read_subtasks:
          if num == str(i):
            subtask = list(subtask)
            subtask[-2] = "1"
            subtask = "".join(subtask)
            found = 1
          i += 1
          subtasks.append(subtask)
        read_subtasks.close()

        if found == 0:
          print(Fore.RED + "The subtask doesn't exist, try again" + Fore.WHITE)
          continue

        # re write the file .txt of the task
        write_subtasks = open("tasks/" + task + ".txt", "w")
        for subtask in subtasks:
          write_subtasks.write(subtask)
        write_subtasks.close()

        print("Subtask completed!!!")
        sleep(1)
        break
    else:
      break
  clear()

def __main__():
  clear()
  while(1):
    open_tasks()

    print(Fore.WHITE)
    print("[1] add a task")
    print("[2] delete a task")
    print("[3] edit a task")
    print("[4] complete a task or subtask")
    print("[5] exit")
    option = int(input())
    clear()

    if option == 1:
      add_task()
    elif option == 2:
      delete_task()
    elif option == 3:
      edit_task()
    elif option == 4:
      complete_task()
    elif option == 5:
      print("see you later!")
      sleep(1)
      return

__main__()