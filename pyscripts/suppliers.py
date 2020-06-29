from pyscripts.database import CursorFromConnectionFromPool


class Supplier:
    def __init__(self, name, contact_person, contact_number, contact_email, address):
        self.name = name
        self.contact_person = contact_person
        self.contact_nr = contact_number
        self.contact_alt = contact_email
        self.address = address

    def __repr__(self):
        return f"<Supplier {self.name}>"

    @classmethod
    def load_details_from_db(cls):
        """This module loads a user from the database, using the user code."""
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM details')
            details = cursor.fetchone()
            if details:
                return cls(name=details[0],
                           contact_person=details[1],
                           contact_number=details[2],
                           contact_email=details[3],
                           address=details[4])

    @classmethod
    def save_to_db_new_supplier(cls, name, contact_person, contact_number, contact_email, address):
        """This module will save a new user to the database"""
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute(
                'INSERT INTO suppliers(name, contact_person, contact_number, contact_email, address) '
                'VALUES(%s, %s, %s, %s, %s)',
                (name, contact_person, contact_number, contact_email, address))

    def update_details(self, new):
        self.name = new['name']
        self.contact_person = new['contact_person']
        self.contact_nr = new['contact_number']
        self.contact_alt = new['contact_email']
        self.address = new['address']
