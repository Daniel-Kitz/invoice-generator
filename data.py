from ctypes import addressof


class Issuer:
    def __init__(self, first, last, address, zipcode, city, taxid, bank, iban) -> None:
        self.firstname = first
        self.lastname = last
        self.address = address
        self.zipcode = zipcode
        self.city = city
        self.taxid = taxid
        self.bank = bank
        self.iban = iban

    @property
    def fullname(self):
        return '{} {}'.format(self.firstname, self.lastname)

    @property
    def cityaddress(self):
        return '{} {}'.format(self.zipcode, self.city)

class Client:
    def __init__(self, gender, first, last, address, zipcode, city) -> None:
        self.gender = gender
        self.firstname = first
        self.lastname = last
        self.address = address
        self.zipcode = zipcode
        self.city = city

    @property
    def fullname(self):
        return '{} {}'.format(self.firstname, self.lastname)

    @property
    def cityaddress(self):
        return '{} {}'.format(self.zipcode, self.city)