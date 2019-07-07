from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user 

class LoginModel():
    USERS={"testuser":"password", "testuser2":"password"}
    def __init__(self):
        pass

    def matches(self, username, password):
        for user, pswd in self.USERS.items():
            if(user == username and pswd == password):
                return True
            
        return False
