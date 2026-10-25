import os
import time
import csv
from pathlib import Path
import random
from datetime import date

BOLD = "\033[1m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"

tasks_path = "tasks.txt"
tasks_file = Path(tasks_path)
log_path = "log.txt"
log_file = Path(log_path)

class Task:

    def __init__(self, name, priority, urgency, typ = "nor", attribute = None):
        self.name = name
        self.priority = int(priority)
        self.urgency = int(urgency)
        self.chance = self.priority + self.urgency
        self.typ = typ
        self.attribute = attribute

    def increase(self):
        self.priority *= 2
        self.urgency *= 2
        self.chance = self.priority + self.urgency

    def output(self):
        print(f"{self.name}: ")
        print(f"    Priorität: {self.priority}")
        print(f"    Dringlichkeit: {self.urgency}")

def main():

    while True:

        usr_iput = showHomescreen()

        if usr_iput == 0:
            break

        os.system('clear')
        
        cur_tasks, nor_tasks, rep_tasks = load_tasks()


        match usr_iput:
            case '1':
                addTask()

            case '2':
                print(f"{BOLD}               Aufgaben{RESET}")
                print("----------------------------------------")

                for t in cur_tasks:
                    time.sleep(0.5)
                    print(t.name)
                    print(t.chance)

                time.sleep(0.5)

                print("----------------------------------------")

                time.sleep(0.5)
                
                waitForExit()

            case '3':
                delete_task(cur_tasks, nor_tasks, rep_tasks)

            case '4':
                chooseTask(cur_tasks, nor_tasks, rep_tasks)

            case '5':
                add_special_task()
            
            case '0':
                break

def overrideTasks(nor_tasks, rep_tasks):

    with tasks_file.open("w", encoding="utf-8") as file:
        for t in rep_tasks:
            file.write(f"{t.name}, {t.priority}, {t.urgency}, {t.typ}, {t.attribute}\n")
        for t in nor_tasks:
            file.write(f"{t.name}, {t.priority}, {t.urgency}, {t.typ}, {t.attribute}\n")    


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
                
            if usr_iput not in ['1', '2', '3', '4', '5', '0']:
                print("Keine gültige Eingabe")
                time.sleep(2.5)
            else:
                break
    
        except ValueError:
            print("Keine gültige Eingabe")
            time.sleep(2.5)

    return usr_iput


def load_tasks():

    cur_tasks, nor_tasks, rep_tasks = [], [], []
    log_eintraege = []
    total_chance = 0

    try:

        with open(tasks_file, "r", encoding="utf-8") as file:
            reader = csv.reader(file)

            for row in reader:
                if row:
                    name = row[0].strip()
                    prio = row[1].strip()
                    urg = row[2].strip()
                    typ = row[3].strip()
                    att = row[4].strip()

                    match typ:
                        case "nor":
                            nor_tasks.append(Task(name, prio, urg, typ, None))
                        case "rep":                            
                            rep_tasks.append(Task(name, prio, 0, typ, att))

        cur_tasks = list(nor_tasks)

        for t in nor_tasks:
            total_chance += t.chance

        try:
            with open(log_file, "r", encoding="utf-8") as lfile:
                log_eintraege = list(csv.reader(lfile))
        except FileNotFoundError:
            log_eintraege = []

        for t in rep_tasks:
            last_done = None

            for log_row in log_eintraege:
                if log_row and log_row[0].strip() == t.name:
                    last_done = date.fromisoformat(log_row[1].strip())

            
            if last_done is None or (date.today() - last_done).days >= int(t.attribute):
                t.chance = round(total_chance / 2) * t.priority if total_chance > 0 else t.priority
                cur_tasks.append(t)

    except FileNotFoundError:
        return [], [], []

    return cur_tasks, nor_tasks, rep_tasks
            
def addTask():

    print("Aufgabe hinzufügen")
    print("----------------------------------------")
    time.sleep(0.5)
    task_name = input("Name: ")
    task_prio = int(input("Priorität (0-3): "))
    task_urg = int(input("Dringlichkeit (0-3): "))

    while task_prio not in [0, 1, 2, 3, 5]:
        task_prio = int(input("Priorität muss 0-3 sein. Gib eine gültige Zahl ein: "))
    while task_urg not in [0, 1, 2, 3, 5]:
        task_urg = int(input("Dringlichkeit muss 0-3 sein. Gib eine gültige Zahl ein: "))

    new_task = Task(task_name, task_prio, task_urg)

    write_new_task(new_task)
    
    time.sleep(0.5)
    print("----------------------------------------")
    time.sleep(0.5)
    print(f"{GREEN}Aufgabe erfolgreich hinzugefügt:{RESET}")
    new_task.output()
    time.sleep(2.5)

def add_special_task():

    print("Aufgabe hinzufügen")
    print("----------------------------------------")
    time.sleep(0.5)
    task_name = input("Name: ")
    task_prio = int(input("Priorität (0-3): "))
    task_typ = "rep"
    task_attribute = int(input("Wiederholt sich alle ... Tage: "))
    
    while task_prio not in [0, 1, 2, 3, 5]:
        task_prio = int(input("Priorität muss 0-3 sein. Gib eine gültige Zahl ein: "))
    while task_attribute < 1:
        task_attribute = int(input("Wiederholungszeitraum muss positiv sein: "))

    new_task = Task(task_name, task_prio, 0, task_typ, task_attribute)

    write_new_task(new_task)
    
    time.sleep(0.5)
    print("----------------------------------------")
    time.sleep(0.5)
    print(f"{GREEN}Aufgabe erfolgreich hinzugefügt:{RESET}")
    new_task.output()
    time.sleep(2.5)

def delete_task(cur_tasks, nor_tasks, rep_tasks):

    if not nor_tasks and not rep_tasks:
        print("Es gibt keine Aufgaben, die man löschen könnte")
        time.sleep(2.5)
        return

    i = 1
    i_max = 1

    for t in cur_tasks:
        print(f"{i}. {t.name}")
        i_max = i
        i += 1

    while True:
        print("Welche Aufgabe willst du löchen? (q zum abbrechen)")
        tmp_input = input("(Nummer): ")

        if tmp_input == 'q':
            return
        elif int(tmp_input) >= 1 and int(tmp_input) <= i_max:
            break

    done_task = cur_tasks.pop(int(tmp_input)-1)

    match done_task.typ:
        case "nor":
            nor_tasks = [task for task in nor_tasks if task.name != done_task.name]            

    overrideTasks(nor_tasks, rep_tasks)
        
    print(f"{GREEN}Aufgabe wurde gelöscht{RESET}")
    time.sleep(2.5)

    with log_file.open("a", encoding="utf-8") as file:
        file.write(f"{done_task.name}, {date.today()}\n")


def chooseTask(cur_tasks, nor_tasks, rep_tasks):

    total = 0

    for t in cur_tasks:
        total += t.chance

    pick = random.randint(1, total)

    for t in cur_tasks:
        pick -= t.chance
        if pick <= 0:
            cur_task = t

    print("--------------------------------------")
    time.sleep(1)
    print("**************************************") 
    time.sleep(1)               
    print(f"       {cur_task.name}")
    time.sleep(1)
    print("**************************************")
    time.sleep(1)
    print("--------------------------------------")
    
    for t in nor_tasks:
        t.increase()
    
    overrideTasks(nor_tasks, rep_tasks)
    
    waitForExit()

def write_new_task(task):
    try:
        with tasks_file.open("a", encoding="utf-8") as file:
            file.write(f"{task.name}, {task.priority}, {task.urgency}, {task.typ}, {task.attribute}\n")
    except FileNotFoundError:
        print("Datei konnte nicht beschrieben werden")
        return

def waitForExit():
    while True:
        tmp_input = input("Drücke 'q' zum verlassen: ")
        if tmp_input == 'q':
            break

if __name__ == "__main__":
    main()