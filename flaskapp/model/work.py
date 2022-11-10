from flaskapp.config.mysqlconn import connectToMySQL



class Work:
    def __init__(self, data):
        self.id = data['id']
        self.photo = data['photo']
        self.recipe_id = data['recipe_id']
        self.user_id = data['user_id']


    #get photo by recipe id
    @classmethod
    def get_all_photo(cls,data):
        query = "SELECT * FROM work WHERE recipe_id = %(id)s;"
        results = connectToMySQL('bakingbuddy').query_db(query,data)
        photo = []
        for p in results:
            photo.append(cls(p))
        return photo

    @classmethod
    def save(cls, data):
        query = "INSERT INTO work ( photo, recipe_id, user_id) " \
                "VALUES (%(photo)s , %(recipe_id)s , %(users_id)s);"
        return connectToMySQL('bakingbuddy').query_db(query, data)


    @classmethod
    def delete_one(cls, data):
        query = "DELETE FROM work WHERE id= %(id)s;"
        return connectToMySQL('bakingbuddy').query_db(query, data)
