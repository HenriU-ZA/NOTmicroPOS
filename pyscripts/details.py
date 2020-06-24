from pyscripts.database import CursorFromConnectionFromPool


class Details:
    def __init__(self, name, contact_person, contact_nr, contact_alt, address, contact_alt_person):
        self.name = name
        self.contact_person = contact_person
        self.contact_nr = contact_nr
        self.contact_alt = contact_alt
        self.address = address
        self.contact_alt_person = contact_alt_person

    def __repr__(self):
        return f"<User {self.name}>"

    @classmethod
    def load_details_from_db(cls):
        """This module loads a user from the database, using the user code."""
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM details')
            details = cursor.fetchone()
            if details:
                return cls(name=details[0],
                           contact_person=details[1],
                           contact_nr=details[2],
                           contact_alt=details[3],
                           address=details[4],
                           contact_alt_person=details[5])


