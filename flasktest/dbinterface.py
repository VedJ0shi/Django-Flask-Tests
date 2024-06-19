import sqlite3


class DatabaseDriver:

    def __init__(self):
        self.conn = sqlite3.connect('todo.db', check_same_thread=False) #implicitly creates file if none exists
        self.cur = self.conn.cursor()
        self.create_task_table()

    def create_task_table(self):
        self.cur.execute(
            '''
            CREATE TABLE task(
            id INTEGER PRIMARY KEY AUTOINCREMENT
            description TEXT NOT NULL
            done INTEGER NOT NULL
            );
            '''
            )
        self.conn.commit()
    
    def delete_task_table(self):
        self.cur.execute(
            '''
            DROP TABLE IF EXISTS task;
            '''
        )
        self.conn.commit()

    def get_all_tasks(self):
        rows = self.cur.execute(
            '''
            SELECT * from task;
            '''
        ) #returns an iterator (query result returned since this is SELECT command)

        tasks = []
        for row in rows:
            tasks.append(
                {
                    'id': row[0],
                    'description': row[1],
                    'done': bool(row[2])
                }
            )

        return tasks
    
    def insert_task(self, description, done=False):
        self.cur.execute(
            '''
            INSERT INTO task (description, done)
            VALUES (?, ?);
            ''',
            parameters=(description, done)
        )
        self.conn.commit()
        return self.cur.lastrowid

    def get_task_by_id(self, id):
        self.cur.execute(
        '''
        SELECT * FROM task WHERE id = ?;
        ''',
        parameters=(id,)
        )
        row = self.cur.fetchone() #returns None if no more data available in query result
        if row:
            task = {
                'id': id,
                'description' : row[1],
                'done' : bool(row[2])   
            }
            return task
        else:
            return None
    