from flaskapp.config.mysqlconn import connectToMySQL


class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.ingredient = data['ingredient']
        self.instruction = data['instruction']
        self.time = data['time']
        self.photo = data['photo']

    # def __eq__(self, other):
    #     return self.id == other.id

    # create&save recipe
    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipe ( name, description, instruction, ingredient, time, user_id, photo) " \
                "VALUES ( %(name)s , %(description)s , %(instruction)s , %(ingredient)s, %(time)s, %(users_id)s,%(photo)s);"
        return connectToMySQL('bakingbuddy').query_db(query, data)

    # edit recipe
    @classmethod
    def update_one(cls, data):
        query = "UPDATE recipe " \
                "SET name = %(name)s, instruction = %(instruction)s, description = %(description)s," \
                " instruction = %(instruction)s, ingredient = %(ingredient)s, time = %(time)s, photo = %(photo)s  " \
                "WHERE id = %(id)s;"
        return connectToMySQL('bakingbuddy').query_db(query, data)

    # delete recipex
    @classmethod
    def delete_one(cls, data):
        query = "DELETE FROM recipe WHERE id= %(id)s;"
        return connectToMySQL('bakingbuddy').query_db(query, data)

    # get recipe by user_id
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM recipe'
        results = connectToMySQL('bakingbuddy').query_db(query)
        recipe = []
        for r in results:
            recipe.append(cls(r))
        return recipe

    # get recipe by user_id
    @classmethod
    def get_by_user(cls, data):
        query = 'SELECT * FROM recipe WHERE user_id= %(id)s'
        results = connectToMySQL('bakingbuddy').query_db(query, data)
        recipe = []
        for r in results:
            recipe.append(cls(r))
        return recipe

    # get recipe by id
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipe WHERE id= %(id)s;"
        results = connectToMySQL('bakingbuddy').query_db(query, data)
        users = []
        for user in results:
            users.append(cls(user))
        return users[0]
