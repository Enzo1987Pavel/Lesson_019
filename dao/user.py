from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid):
        return self.session.query(User).get(uid)

    def get_by_username(self, username):
        return self.session.query(User).filter(User.username == username).one()

    def get_all(self):
        return self.session.query(User).all()

    def create(self, user_data):
        user_new = User(**user_data)
        self.session.add(user_new)
        self.session.commit()
        return user_new

    def delete(self, uid):
        user_del = self.get_one(uid)
        self.session.delete(user_del)
        self.session.commit()

    def update(self, user_data):
        user_upd = self.get_one(user_data.get("id"))

        user_upd.username = user_data.get("username")
        user_upd.password = user_data.get("password")
        user_upd.role = user_data.get("role")

        self.session.add(user_upd)
        self.session.commit()
