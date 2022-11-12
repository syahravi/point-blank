from InquirerPy import prompt
import sqlite3

class Weapons:
    def __init__(self):
        answers = prompt(self.questions)
        if answers.get("user_option") == "Read":
            self.read()
        elif answers.get("user_option") == "Create":
            self.create()
        elif answers.get("user_option") == "PlusUltra":
            self.plusultra()

    def read(self):
        sql = "SELECT * FROM WEAPONS"
        self.cursor.execute(sql)
        records = self.cursor.fetchall()
        for row in records:
            print("ID:", row[0])
            print("Name:", row[1])
            print("Desc:", row[2])
            print("Points:", row[3])
            print("\tRank:", row[4])
        self.cursor.close()

    def create(self):
        ans1 = prompt(self.detail_weapon)
        for k,v in ans1.items():
            print(k,"->", v)
        ans2 = prompt(self.confirm)
        if ans2.get("continue") == True:
            self.insert(ans1['name'], ans1['description'])

    def insert(self, name, desc):
        sql = "INSERT INTO WEAPONS (NAME, DESC, POINTS, RANK) VALUES (?, ?, ?, ?)"
        val = (name, desc, 0, 0)
        self.cursor.execute(sql, val)
        self.conn.commit()
        self.cursor.close()
        print("Unlock New Weapon")


    def plusultra(self):
        sql = "SELECT NAME, DESC, POINTS, RANK FROM WEAPONS"
        self.cursor.execute(sql)
        records = self.cursor.fetchall()
        name = []
        for x,i in enumerate(records):
            name.append(f"{x+1}. {i}")
        update_name = [ # Name Update
                {
                    'type': 'list',
                    'name': 'update_id',
                    'message': 'Plus Ultra',
                    'choices': name,
                    'filter': lambda val: val[0]
                    }
                ]
        ans1 = prompt(update_name)
        ans2 = prompt(self.update_weapon)
        self.update(ans1.get('update_id'), ans2.get("update")[7:])

    def update(self, i, where):
        detail_update = [ # Weapon detail
        {
            'type': 'input',
            'name': 'name',
            'message': 'Update weapon'
            }
        ]
        u = prompt(detail_update)
        sql = f"UPDATE WEAPONS set {where} = ? where ID = ?"
        val = (u.get('name'), i)
        self.cursor.execute(sql, val)
        self.conn.commit()

        sql = f"SELECT * FROM WEAPONS WHERE ID = {i}"
        self.cursor.execute(sql)
        record = self.cursor.fetchmany()
        for row in record:
            print("ID:", row[0])
            print("Name:", row[1])
            print("Desc:", row[2])
            print("Points:", row[3])
            print("\tRank:", row[4])
        self.cursor.close()
    #---
    #--
    conn = sqlite3.connect('blank.db')
    cursor = conn.cursor()
    #-
    questions = [ #Menu
        {
            'type': 'list',
            'name': 'user_option',
            'message': 'Welcome to Point Blank Plus Ultra',
            'choices': ["Read", "Create", "PlusUltra"]
        }
    ]
    confirm = [ #Confirm
            {
                'type': 'confirm',
                'name': 'continue',
                'message': 'Do you want to continue?',
                'default': True
                }
            ]

    #---
    detail_weapon = [ # Weapon detail
            {
                'type': 'input',
                'name': 'name',
                'message': 'What\'s your weapon name'
                },
            {
                'type': 'input',
                'name': 'description',
                'message': 'Weapon description'
                }
            ]
    update_weapon = [ # Weapon Update
            {
                'type': 'list',
                'name': 'update',
                'message': 'Plus Ultra',
                'choices': ["Update Name", "Update Description", "Update Points"]
                }
            ]

if __name__ == "__main__":
    Weapons()
