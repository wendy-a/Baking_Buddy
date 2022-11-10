from flaskapp.config.mysqlconn import connectToMySQL
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.password = data['password']
        self.isChef = data['isChef']

# save register data
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users ( name, email, password, isChef) " \
                "VALUES (%(name)s , %(email)s , %(password)s, %(isChef)s);"
        return connectToMySQL('bakingbuddy').query_db(query, data)

#login-get email
    @classmethod
    def get_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email= %(email)s'
        results = connectToMySQL('bakingbuddy').query_db(query, data)
        print(results)
        if len(results) == 0:
            return None
        users = []
        for r in results:
            users.append(cls(r))
        return users [0]


#get user by id
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id= %(id)s;"
        results = connectToMySQL('bakingbuddy').query_db(query, data)
        if len(results) == 0:
            return None
        users = []
        for r in results:
            users.append(cls(r))
        return users[0]