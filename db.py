import sqlite3
from data import Issuer, Client

class db:
    def __init__(self) -> None:
        self.connection = sqlite3.connect('main.db')
        self.c = self.connection.cursor()

    def createTables(self):
        '''This function is ONLY needed for the initial setup and should NOT be called at any given point BESIDES the FIRST INIT of the program'''
        try:
            self.c.execute("""CREATE TABLE issuers (
                        first text,
                        last text,
                        address text,
                        zipcode integer,
                        city text,
                        taxid text,
                        bank text,
                        iban text
                    )""")

            self.c.execute("""CREATE TABLE clients (
                        gender text,
                        first text,
                        last text,
                        address text,
                        zipcode integer,
                        city text
                    )""")
        except sqlite3.OperationalError:
            return True

    def add(self, currentObject):
        if currentObject.__name__ == 'Issuer':
            try:
                self.c.execute("SELECT * FROM issuers WHERE first=:first, last=:last, address=:address", {'first': currentObject.firstname, 'last': currentObject.lastname, 'address': currentObject.address})
                if self.c.fetchall() != []:
                    self.c.execute("INSERT INTO issuers VALUES (:first, :last, :address, :zipcode, :city, :taxid, :bank, :iban)", {'first':currentObject.firstname,'last':currentObject.lastname,'address':currentObject.address,'zipcode':currentObject.zipcode,'city':currentObject.city,'taxid':currentObject.taxid,'bank':currentObject.bank,'iban':currentObject.iban})
                    return True
                else:
                    print("This Issuer already exists in the database!")
                    return True
            except:
                print("Something went wrong. Check your input!")
                return False
        elif currentObject.__name__ == 'Client':
            try:
                self.c.execute("INSERT INTO issuers VALUES (:gender, :first, :last, :address, :zipcode, :city)", {'gender': currentObject.gender, 'first':currentObject.firstname,'last':currentObject.lastname,'address':currentObject.address,'zipcode':currentObject.zipcode,'city':currentObject.city})
                return True
            except:
                print("Something went wrong. Check your input!")
                return False
        else:
            return False

    def remove(self, currentObject):
        if currentObject.__name__ == "Issuer":
            try:
                self.c.execute("DELETE FROM issuers WHERE first=:first AND last=:last")
                return True
            except:
                print("Something went wrong. Check your input!")
                return False
        elif currentObject.__name__ == "Client":
            try:
                self.c.execute("DELETE FROM clients WHERE first=:first AND last=:last", {'first': currentObject.firstname, 'last': currentObject.lastname})
                return True
            except:
                print("Something went wrong. Check your input!")
                return False
        else:
            return False


    def getallissuers(self):
        '''Only for use by the program!'''
        self.c.execute("SELECT * FROM issuers")
        return self.c.fetchall()

    def getallclients(self):
        '''Only for use by the program!'''
        self.c.execute("SELECT * FROM clients")
        return self.c.fetchall()

    def close(self):
        self.connection.close()
        return True

# c = conn.cursor()



c.execute()

conn.commit()

conn.close()
