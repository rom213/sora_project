from .entities.User import User

class ModelUser:
    @classmethod
    def login(cls, user):
        try:
            found_user = User.query.filter_by(username=user.username).first()
            if found_user and User.check_password(found_user.password, user.password):
                return found_user
            else:
                return None
        except Exception as exc:
            raise Exception(exc)
        
    @classmethod
    def allUsers(cls):
        try:
            allUsers = User.query.all()
            return allUsers;
        except Exception as exc:
            raise Exception(exc)
        
        
    @classmethod
    def get_by_id(cls, id):
        try:
            return User.query.get(id)
        except Exception as exc:
            raise Exception(exc)