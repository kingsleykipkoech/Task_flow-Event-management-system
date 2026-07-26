import sys
import os
import calendar
import smtplib
import threading
import time
from datetime import date, datetime, timedelta
import connection as db

# USER IDENTITY & ROLE AUTHENTICATION 

CURRENT_USER = "Planner"
def select_user_identity():
    global CURRENT_USER
    while True:
        all_members = db.get_all_members()
        print("")
        print("             Who are you?              ")
        print("  ---------------------------------------")
        number = 1
        for member in all_members:
            print(f"   {number}) {member[1]}")
            number += 1
        print(f"   {number}) + Edit / Manage Users")
        print("  -----------------------------")
        print("")
        choice = input("  Pick your name number: ").strip()
        while not choice.isdigit() or int(choice) < 1 or int(choice) > len(all_members) + 1:
            choice = input("  Invalid selection. Pick your name number: ").strip()

        if int(choice) == len(all_members) + 1:
            print("")
            print("  -----------------------------")
            print("  Edit / Manage Users Options:")
            print("  -----------------------------")
            print("   1) Add a new user")
            print("   2) Delete an existing user")
            print("  -----------------------------")
            sub_choice = input("  Pick 1 or 2: ").strip()

            if sub_choice == "1":
                new_name = input("  Enter new user name: ").strip()
                if new_name != "":
                    db.add_member(new_name)
                    CURRENT_USER = new_name
                    print(f"\n  Logged in as: {CURRENT_USER}")
                    break
                else:
                    CURRENT_USER = "Planner"
                    print(f"\n  Logged in as: {CURRENT_USER}")
                    break
            elif sub_choice == "2":
                if len(all_members) == 0:
                    print("  No users available to delete.")
                    continue
                print("")
                print("  Pick user number to delete:")
                del_num = 1
                for member in all_members:
                    print(f"   {del_num}) {member[1]}")
                    del_num += 1
                del_choice = input("  User number to delete: ").strip()
                if del_choice.isdigit() and 1 <= int(del_choice) <= len(all_members):
                    target_name = all_members[int(del_choice) - 1][1]
                    db.delete_member(target_name)
                    print(f"  User '{target_name}' deleted successfully.")
                else:
                    print("  Invalid selection.")
                continue
            else:
                print("  Invalid choice.")
                continue
        else:
            CURRENT_USER = all_members[int(choice) - 1][1]
            print(f"\n  Logged in as: {CURRENT_USER}")
            break


def pick_role():
    print("")
    print("       Welcome to TaskFlow Planner       ")
    print("  ---------------------------------------")
    print("")
    print("  Choose your role:")
    print("  " + "-" * 41)
    print("  1) Planner  -  full access")
    print("  2) Viewer   -  view and search only")
    print("  " + "-" * 41)
    print("")
    choice = input("  Enter 1 or 2: ").strip()
    while choice != "1" and choice != "2":
        choice = input("  Please enter 1 or 2: ").strip()
    if choice == "1":
        print("")
        print("  Logged in as Planner.")
        return "planner"
    else:
        print("")
        print("  Logged in as Viewer.")
        return "viewer"
