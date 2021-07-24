from flask_mongoengine import Document
from mongoengine import DoesNotExist, ObjectIdField, StringField
from gallery.ext.auth import pwd_context


class UserModel(Document):
    _id = ObjectIdField(required=False)
    email = StringField(max_length=120, required=True, unique=True)
    name = StringField(max_length=120, required=True)
    password = StringField(required=True)

    @staticmethod
    def find_by_email(identity):
        try:
            current_user = UserModel.objects(email=identity).get()
            return current_user
        except DoesNotExist:
            return None

    @staticmethod
    def encrypt_password(password):
        return pwd_context.encrypt(password)

    def check_encrypted_password(self, password):
        return pwd_context.verify(password, self.password)

    def to_dict(self):
        return {"email": self.email, "username": self.username}
