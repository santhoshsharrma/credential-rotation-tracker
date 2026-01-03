import json
from datetime import datetime, timedelta
from pathlib import Path
class Color:
    RED="\033[91m"
    GREEN="\033[92m"
    CYAN="\033[96m"
    YELLOW="\033[93m"
    RESET="\033[0m"
DATA_FILE=Path("credentials.json")
DATE_FORMAT="%Y-%m-%d"
def banner():
    print(Color.CYAN+"""
========================================
      CREDENTIAL ROTATION TRACKER
========================================
Track • Audit • Rotate
"""+Color.RESET)

# Data Handling
def load_credentials():
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)
def save_credentials(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
# Utility Functions
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, DATE_FORMAT)
    except ValueError:
        return None
def next_due_date(last_rotated, rotation_days):
    return last_rotated+timedelta(days=rotation_days)

def is_overdue(last_rotated, rotation_days):
    return datetime.today()>next_due_date(last_rotated, rotation_days)
# Core Features
def add_credential():
    print("\nAdd Credential")
    name=input("Credential name: ").strip()
    date_input=input("Last rotated date (YYYY-MM-DD): ").strip()
    interval=input("Rotation interval (days): ").strip()
    last_rotated=parse_date(date_input)
    if not name or not last_rotated or not interval.isdigit():
        print(Color.RED + "Invalid input." + Color.RESET)
        return
    credentials=load_credentials()
    credentials.append({
        "name": name,
        "last_rotated": date_input,
        "rotation_days": int(interval)
    })
    save_credentials(credentials)
    print(Color.GREEN + "Credential added successfully." + Color.RESET)
def list_credentials(sort_by_due=False):
    credentials=load_credentials()
    if not credentials:
        print("No credentials found.")
        return
    if sort_by_due:
        credentials.sort(
            key=lambda c: next_due_date(
                parse_date(c["last_rotated"]),
                c["rotation_days"]
            )
        )
    print("\nTracked Credentials\n" + "-"*40)
    for i, c in enumerate(credentials, start=1):
        last_rotated=parse_date(c["last_rotated"])
        due=next_due_date(last_rotated, c["rotation_days"])
        overdue=is_overdue(last_rotated, c["rotation_days"])
        today=datetime.today()
        days_remaining=(due-today).days
        status=(
            Color.RED + "OVERDUE" + Color.RESET
            if overdue
            else Color.GREEN + "OK" + Color.RESET
        )
        print(f"{i}. {c['name']}")
        print(f"   Last Rotated : {c['last_rotated']}")
        print(f"   Next Due     : {due.strftime(DATE_FORMAT)}")
        print(f"   Due in     : {days_remaining} days")
        print(f"   Status       : {status}")
        print("-"*40)
def update_rotation():
    credentials=load_credentials()
    if not credentials:
        print("No credentials found.")
        return
    list_credentials()
    choice=input("Select credential number to update: ").strip()
    if not choice.isdigit():
        print(Color.RED + "Invalid choice." + Color.RESET)
        return
    idx=int(choice)-1
    if idx<0 or idx>=len(credentials):
        print(Color.RED + "Out of range." + Color.RESET)
        return
    new_date=input("New rotation date (YYYY-MM-DD): ").strip()
    if not parse_date(new_date):
        print(Color.RED + "Invalid date format." + Color.RESET)
        return
    credentials[idx]["last_rotated"] = new_date
    save_credentials(credentials)
    print(Color.GREEN + "Rotation date updated." + Color.RESET)
def delete_credential():
    credentials=load_credentials()
    if not credentials:
        print("No credentials found.")
        return
    list_credentials()
    choice=input("Select credential number to delete: ").strip()
    if not choice.isdigit():
        print(Color.RED+"Invalid choice." + Color.RESET)
        return
    idx=int(choice)-1
    if idx<0 or idx>=len(credentials):
        print(Color.RED+"Out of range."+Color.RESET)
        return
    removed=credentials.pop(idx)
    save_credentials(credentials)
    print(Color.YELLOW+f"Deleted: {removed['name']}" + Color.RESET)
def check_overdue():
    credentials=load_credentials()
    if not credentials:
        print("No credentials to check.")
        return
    print("\nOverdue Credentials\n" + "-" * 30)
    found=False
    for c in credentials:
        last_rotated=parse_date(c["last_rotated"])
        if is_overdue(last_rotated, c["rotation_days"]):
            found=True
            print(Color.RED+f"- {c['name']} (Last rotated: {c['last_rotated']})" + Color.RESET)
    if not found:
        print(Color.GREEN+"No overdue credentials."+Color.RESET)
def summary():
    credentials=load_credentials()
    total=len(credentials)
    overdue=0
    for c in credentials:
        last_rotated=parse_date(c["last_rotated"])
        if is_overdue(last_rotated, c["rotation_days"]):
            overdue+=1
    print(Color.YELLOW+"\n=== SUMMARY ==="+Color.RESET)
    print(f"Total credentials tracked : {total}")
    print(f"{Color.RED}Overdue credentials       : {overdue}{Color.RESET}")

# Menu
def show_menu():
    print("""
1. Add credential
2. List credentials
3. Update rotation date
4. Delete credential
5. Check overdue credentials
6. View summary
7. Exit
""")
def main():
    banner()
    while True:
        show_menu()
        choice=input("Choose an option: ").strip()
        if choice=="1":
            add_credential()
        elif choice=="2":
            list_credentials()
        elif choice=="3":
            update_rotation()
        elif choice=="4":
            delete_credential()
        elif choice=="5":
            check_overdue()
        elif choice=="6":
            summary()
        elif choice=="7":
            print("Exiting...")
            break
        else:
            print(Color.RED + "Invalid option." + Color.RESET)
if __name__ == "__main__":
    main()
