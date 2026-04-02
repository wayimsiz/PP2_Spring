import csv
from connect import connect


# 📥 INSERT from CSV
def insert_from_csv(filename):
    conn = connect()
    cur = conn.cursor()

    with open(filename, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            name, phone = row
            cur.execute(
                "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
                (name, phone)
            )

    conn.commit()
    cur.close()
    conn.close()
    print("CSV imported!")


# ✍️ INSERT from console
def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Contact added!")


# 🔍 QUERY
def query_contacts():
    conn = connect()
    cur = conn.cursor()

    filter_name = input("Search name (or press Enter): ")
    filter_phone = input("Search phone prefix (or press Enter): ")

    query = "SELECT * FROM contacts WHERE 1=1"
    params = []

    if filter_name:
        query += " AND name ILIKE %s"
        params.append(f"%{filter_name}%")

    if filter_phone:
        query += " AND phone LIKE %s"
        params.append(f"{filter_phone}%")

    cur.execute(query, params)

    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.close()
    conn.close()


# ✏️ UPDATE
def update_contact():
    name = input("Enter name to update: ")
    new_name = input("New name (or Enter): ")
    new_phone = input("New phone (or Enter): ")

    conn = connect()
    cur = conn.cursor()

    if new_name:
        cur.execute(
            "UPDATE contacts SET name=%s WHERE name=%s",
            (new_name, name)
        )

    if new_phone:
        cur.execute(
            "UPDATE contacts SET phone=%s WHERE name=%s",
            (new_phone, name)
        )

    conn.commit()
    cur.close()
    conn.close()
    print("Updated!")


# ❌ DELETE
def delete_contact():
    value = input("Enter name or phone to delete: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM contacts WHERE name=%s OR phone=%s",
        (value, value)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Deleted!")


# 📋 MENU
def menu():
    while True:
        print("\n--- PhoneBook ---")
        print("1. Import CSV")
        print("2. Add contact")
        print("3. Search")
        print("4. Update")
        print("5. Delete")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            insert_from_csv("contacts.csv")
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            query_contacts()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            delete_contact()
        elif choice == "0":
            break


if __name__ == "__main__":
    menu()