import sqlite3

def main():
    db_name = "task.db"
    connection = sqlite3.connect(db_name)
    connect = connection.cursor()
    connect.execute("CREATE TABLE tasks(id integer, do text, status integer, created_at text, updated_at text)")
    connect.close()

if __name__ == "__main__":
    main()