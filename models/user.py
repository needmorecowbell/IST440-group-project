from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user 

class User(UserMixin):

    def __init__(self, id, username, password):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"
        
    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)
