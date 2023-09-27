import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed):
        self.name=name
        self.breed=breed    

    @classmethod
    def create_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            );
        """
        CURSOR.execute(sql)
    @classmethod
    def drop_table(self):
        sql="""
            DROP TABLE IF EXISTS dogs;

        """
        CURSOR.execute(sql)


    @classmethod    
    def save(self):
        sql="""
                INSERT INTO dogs(name, breed) VALUES(?,?)

            """
        CURSOR.execute(sql, (self.name, self.breed))
        CONN.commit()



    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)  # Create a new instance of the Dog class
        dog.save()  # Save the instance to the database
        return dog
    
    @classmethod
    def new_from_db(cls, db_record):
        # Create a new Dog instance using data from the database record
        name, breed = db_record  # Assuming the database record is a tuple with (name, breed)
        return cls(name, breed)
    
    @classmethod
    def find_by_name(self, name):
        sql="""
                SELECT * FROM dogs WHERE name=?

            """
        return CURSOR.execute(sql, (name)).fetchone()
      
    @classmethod
    def find_by_id(cls, id):
        sql = "SELECT * FROM dogs WHERE id = ?"
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        if row:
            return cls(*row)  # Create a Dog instance from the row data
        else:
            return None
        

    @classmethod
    def find_or_create_by(cls, name, breed):
        sql = "SELECT * FROM dogs WHERE name = ? AND breed = ?"
        CURSOR.execute(sql, (name, breed))
        row = CURSOR.fetchone()
        if row:
            return cls(*row)  # Create a Dog instance from the row data
        else:
            # If not found, create a new dog and return it
            return cls.create(name, breed)