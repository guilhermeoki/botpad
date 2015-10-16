import random
import string
import hashlib
class Page:
    
    def create_password(self):
        password = "".join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(random.randint(50,100)))
        return password

    def generate_hash(self):
        pw = self.create_password()
        h = hashlib.sha512(pw).hexdigest()
        return h
    
    def create_page(self):
        hash_message = self.generate_hash()
        self.site = 'http://dontpad.com/'+hash_message+"/control"
        return self.site

if __name__ == '__main__':
    p = Page()
    print p.create_page()