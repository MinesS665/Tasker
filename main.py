import os
import time
import csv
from pathlib import Path
import random

BOLD = "\033[1m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"

class Task:
    def __init__(self, name, priority, urgency):
        self.name = name
        self.priority = int(priority)
        self.urgency = int(urgency)
        self.chance = self.priority + self.urgency

    def increase(self):
        self.priority *= 3
        self.urgency *= 3
        self.chance = self.priority + self.urgency

    def output(self):
        print(f"{self.name}: ")
        print(f"    Priorität: {self.priority}")
        print(f"    Dringlichkeit: {self.urgency}")

def main():

    path = "tasks.txt"
    file_path = Path(path)
    usr_iput = 9

    while usr_iput != 0:

        tasks = []
        load_tasks(path, tasks)
        usr_iput = showHomescreen()

        os.system('clear')

        match usr_iput:
            case '1':

                task = addTask()

                with file_path.open("a", encoding="utf-8") as file:
                    file.write(f"{task.name}, {task.priority}, {task.urgency} \n")


                time.sleep(0.5)
                print("----------------------------------------")
                time.sleep(0.5)
                print(f"{GREEN}Aufgabe erfolgreich hinzugefügt:{RESET}")
                task.output()
                time.sleep(2.5)


            case '2':

                print(f"{BOLD}               Aufgaben{RESET}")
                print("----------------------------------------")

                for t in tasks:
                    time.sleep(0.5)
                    print(t.name)

                time.sleep(0.5)

                print("----------------------------------------")

                time.sleep(0.5)
                
                while True:
                    tmp_input = input("Drücke 'q' zum verlassen: ")
                    if tmp_input == 'q':
                        break
            case '3':

                if not tasks:
                    print("Es gibt keine Aufgaben, die man löschen könnte")
                    time.sleep(2.5)
                    continue

                delete_task(tasks)

                overrideTasks(tasks,file_path)

                print(f"{GREEN}Aufgabe wurde gelöscht{RESET}")
                time.sleep(2.5)

            case '4':

                cur_task = chooseTask(tasks)
                print("--------------------------------------")
                time.sleep(1)
                print("**************************************") 
                time.sleep(1)               
                print(f"       {cur_task.name}")
                time.sleep(1)
                print("**************************************")
                time.sleep(1)
                print("--------------------------------------")

                for t in tasks:
                    t.increase()

                overrideTasks(tasks,file_path)

                while True:
                    tmp_input = input("Drücke 'q' zum verlassen: ")
                    if tmp_input == 'q':
                        break
            case '0':
                break

def overrideTasks(tasks, file_path):
    with file_path.open("w", encoding="utf-8") as file:
        for t in tasks:
            file.write(f"{t.name}, {t.priority}, {t.urgency} \n")

def showHomescreen():

    while True:
            try:
                os.system('clear')
    
                print("---------------------------")
                print("[1] Neue Aufgabe erstellen")
                print("[2] Aufgaben einsehen")
                print("[3] Aufgabe löschen")
                print("[4] Gib mir eine Aufgabe")
                print("---------------------------")
                usr_iput = input("Was möchtest du tun? ")
                    
                if usr_iput not in ['1', '2', '3', '4', '0']:
                    print("Keine gültige Eingabe")
                    time.sleep(2.5)
                else:
                    break
    
            except ValueError:
                print("Keine gültige Eingabe")
                time.sleep(2.5)

    return usr_iput

def load_tasks(path, tasks):

    try:
        with open(path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)

            for row in reader:
                if row:
                    name = row[0].strip()
                    prio = row[1].strip()
                    urg = row[2].strip()

                tasks.append(Task(name, prio, urg))
    except FileNotFoundError:
        return

            
def addTask():
    print("Aufgabe hinzufügen")
    print("---------------------------------------")
    time.sleep(0.5)
    task_name = input("Name: ")
    task_prio = int(input("Priorität (0-3): "))
    task_urg = int(input("Dringlichkeit (0-3): "))

    while task_prio < 0 or task_prio > 3:
        input("Priorität muss 0-3 sein. Gib eine gültige Zahl ein: ")
    while task_urg < 0 or task_urg > 3:
        input("Dringlichkeit muss 0-3 sein. Gib eine gültige Zahl ein")

    task = Task(task_name, task_prio, task_urg)

    return task

def delete_task(tasks):

    i = 1
    i_max = 1

    for t in tasks:
        print(f"{i}. {t.name}")
        i_max = i
        i += 1

    while True:
        print("Welche Aufgabe willst du löchen? (q zum abbrechen)")
        tmp_input = input("(Nummer): ")

        if tmp_input == 'q':
            return

        if int(tmp_input) >= 1 and int(tmp_input) <= i_max:
            break

    tasks.pop(int(tmp_input)-1)

def chooseTask(tasks):

    total = 0

    for t in tasks:
        total += t.chance

    pick = random.randint(1, total)

    for t in tasks:
        pick -= t.chance
        if pick <= 0:
            return t

if __name__ == "__main__":
    main()