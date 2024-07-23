import sqlite3


class DatabaseDriver:

    def __init__(self):
        self.conn = sqlite3.connect('todo.db', check_same_thread=False) #implicitly creates file if none exists
        self.cur = self.conn.cursor()
        try:
            self.create_task_table()
            self.create_subtask_table()
        except:
            pass


    def create_task_table(self):
        self.cur.execute(
            '''
            CREATE TABLE task(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
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
        self.cur.execute(
            '''
            SELECT * from task;
            '''
        ) #iterable 'query result' stored in cursor object since this is a SELECT command

        tasks = []
        for row in self.cur: #cursor is an iterator over the query result
            tasks.append(
                {
                    'id': row[0],
                    'description': row[1],
                    'done': bool(row[2])
                }
            )
        return tasks
    

    def insert_task(self, description):
        done = 0
        self.cur.execute(
            '''
            INSERT INTO task (description, done)
            VALUES (?, ?);
            ''',
            (description, done)
        )
        self.conn.commit()
        return self.cur.lastrowid


    def get_task_by_id(self, id):
        self.cur.execute(
        '''
        SELECT * FROM task WHERE id = ?;
        ''',
        (id,)
        ) 

        if row:=self.cur.fetchone(): 
            task = {
                'id': id,
                'description' : row[1],
                'done' : bool(row[2])   
            }
            return task
        else:
            return None
    

    def update_task_by_id(self, id, **kwargs):
        description = kwargs.get('description')
        done = kwargs.get('done')
        if done:
            if done.casefold() == "true":
                done = 1
                self.handle_related_subtasks(id)
            elif done.casefold() == "false":
                done = 0

        if description is None:
            self.cur.execute(
                '''
                UPDATE task SET done=? WHERE id=?;
                ''',
                (done, id)
            )
        elif done is None:
            self.cur.execute(
                '''
                UPDATE task SET description=? WHERE id=?;
                ''',
                (description, id)
            )
        else:
            self.cur.execute(
                '''
                UPDATE task SET description=?, done=? WHERE id=?;
                ''',
                (description, done, id)
            )
        self.conn.commit()


    def delete_task_by_id(self, id):
        self.cur.execute(
            '''
            DELETE FROM task WHERE id=?;
            ''',
            (id,)
        )
        self.conn.commit()

    #--------------------------------------Subtasks-----------------------------------------------#
    
    def create_subtask_table(self):
        self.cur.execute(
            '''
            CREATE TABLE subtask(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            done INTEGER NOT NULL,
            task_id INTEGER NOT NULL,
            FOREIGN KEY (task_id) REFERENCES task(id)
            );
            '''
        )
        self.conn.commit()

    
    def get_all_subtasks(self):
        cursor = self.conn.cursor()
        cursor.execute(
            ''' SELECT * FROM subtask; '''
        )
        subtasks = []
        for row in cursor:
            subtasks.append({
                "id": row[0],
                "description": row[1],
                "done": bool(row[2]),
                "primary task": self.get_task_by_id(row[3])['description']
            })
        return subtasks
    
    
    def insert_subtask(self, description, fid):
        done = 0
        self.cur.execute(
            ''' INSERT INTO subtask (description, done, task_id) VALUES (?,?,?); ''', 
            (description, done, fid)
        )
        self.conn.commit()
        return self.cur.lastrowid
    

    def get_subtask_by_id(self, id):
        cursor = self.conn.cursor()
        cursor.execute(
            ''' SELECT * FROM subtask WHERE id=?; ''',
            (id, )
        )
        if row:=cursor.fetchone():
            subtask = {
                "id": id,
                "description": row[1],
                "done": bool(row[2]),
                "primary task": self.get_task_by_id(row[3])['description']
            }
            return subtask
        else:
            return None


    def get_subtasks_of_task(self, fid):
        cursor = self.conn.cursor()
        cursor.execute(
            ''' SELECT * FROM subtask WHERE task_id=?; ''',
            (fid,)
        )
        primary_task = self.get_task_by_id(fid)['description']
        subtasks = []
        for row in cursor:
            subtasks.append({
                "id": row[0],
                "description": row[1],
                "done": bool(row[2]),
                "primary task": primary_task
            })
        return subtasks
    

    def update_subtask_by_id(self, id, **kwargs):
        description = kwargs.get('description')
        done = kwargs.get('done')
        if done:
            if done.casefold() == "true":
                done = 1
            elif done.casefold() == "false":
                done = 0

        if description is None:
            self.cur.execute(
                '''
                UPDATE subtask SET done=? WHERE id=?;
                ''',
                (done, id)
            )
        elif done is None:
            self.cur.execute(
                '''
                UPDATE subtask SET description=? WHERE id=?;
                ''',
                (description, id)
            )
        else:
            self.cur.execute(
                '''
                UPDATE subtask SET description=?, done=? WHERE id=?;
                ''',
                (description, done, id)
            )
        self.conn.commit()


    def handle_related_subtasks(self, fid, reset=False):
        if not reset:
            targets = [subtask['id'] for subtask in self.get_subtasks_of_task(fid) if subtask['done'] == False]
            for id in targets:
                self.update_subtask_by_id(id, done='true')
        else:
            targets = [subtask['id'] for subtask in self.get_subtasks_of_task(fid) if subtask['done'] == True]
            for id in targets:
                self.update_subtask_by_id(id, done='false')







