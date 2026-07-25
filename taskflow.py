# ==============================================================================
# MODULE 2: USER IDENTITY & ROLE AUTHENTICATION (Lilian)
# ==============================================================================

CURRENT_USER = "Planner"


def select_user_identity():
    global CURRENT_USER
    all_members = db.get_all_members()
    print("")
    print("  +-----------------------------+")
    print("  |      Who are you?           |")
    print("  +-----------------------------+")
    number = 1
    for member in all_members:
        print(f"   {number}) {member[1]}")
        number += 1
    print(f"   {number}) + Register New Member")
    print("  -----------------------------")
    print("")
    choice = input("  Pick your name number: ").strip()
    while not choice.isdigit() or int(choice) < 1 or int(choice) > len(all_members) + 1:
        choice = input("  Invalid. Pick your name number: ").strip()

    if int(choice) == len(all_members) + 1:
        new_name = input("  Enter your name: ").strip()
        if new_name != "":
            db.add_member(new_name)
            CURRENT_USER = new_name
        else:
            CURRENT_USER = "Planner"
    else:
        CURRENT_USER = all_members[int(choice) - 1][1]

    print(f"\n  Logged in as: {CURRENT_USER}")


def pick_role():
    print("")
    print("  +-----------------------------------------+")
    print("  |                                         |")
    print("  |      Welcome to TaskFlow Planner        |")
    print("  |                                         |")
    print("  +-----------------------------------------+")
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
