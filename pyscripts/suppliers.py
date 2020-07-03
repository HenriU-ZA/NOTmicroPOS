from pyscripts.database import CursorFromConnectionFromPool


class Supplier:
    def __init__(self, id, name, contact_person, contact_number, contact_email, address, website):
        self.id = id
        self.name = name
        self.contact_person = contact_person
        self.contact_number = contact_number
        self.contact_email = contact_email
        self.address = address
        self.website = website

    def __repr__(self):
        return f"<Supplier {self.name}>"

    @classmethod
    def load_details_from_db(cls, id):
        """This module loads a user from the database, using the user code."""
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM suppliers WHERE _id=%s', (id,))
            details = cursor.fetchone()
            if details:
                return cls(id=details[0],
                           name=details[1],
                           contact_person=details[2],
                           contact_number=details[3],
                           contact_email=details[4],
                           address=details[5],
                           website=details[6])

    @classmethod
    def view_all_suppliers(cls, enable='y'):
        """Returns all suppliers."""
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM suppliers WHERE enable=%s ORDER BY name ASC', (enable,))
            suppliers = cursor.fetchall()
            if suppliers:
                better_suppliers = []
                for supplier in suppliers:
                    better_suppliers.append({'id': supplier[0], 'name': supplier[1], 'contact_person': supplier[2],
                                             'contact_number': supplier[3], 'contact_email': supplier[4],
                                             'address': supplier[5], 'website': supplier[6]})
                return better_suppliers

    @classmethod
    def save_to_db_new_supplier(cls, name, contact_person, contact_number, contact_email, address, website):
        """This module will save a new user to the database"""
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute(
                'INSERT INTO suppliers(name, contact_person, contact_number, contact_email, address, website) '
                'VALUES(%s, %s, %s, %s, %s, %s)',
                (name, contact_person, contact_number, contact_email, address, website))

    @classmethod
    def update_details(cls, data):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute(
                'UPDATE suppliers SET name=%s, contact_person=%s, contact_number=%s, contact_email=%s, address=%s, '
                'website=%s WHERE _id=%s',
                (data['name'], data['contact_person'], data['contact_number'], data['contact_email'], data['address'],
                 data['website'],
                 data['id']))
            return True

    @classmethod
    def toggle_suppliers(cls, id, enable):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute(
                'UPDATE suppliers SET enable=%s WHERE _id=%s',
                (enable, id))
            return True
