from flask.json import jsonify


class FriendGalleryException(Exception):
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        data = dict(self.payload or ())
        data["message"] = self.message
        data["status_code"] = self.status_code
        return data


class UserAlreadyExists(FriendGalleryException):
    status_code = 400


class UserNotFound(FriendGalleryException):
    status_code = 404


class GalleryNotFound(FriendGalleryException):
    status_code = 404


class GalleryPermission(FriendGalleryException):
    status_code = 401


def handle_api_exceptions(app):
    @app.errorhandler(UserNotFound)
    def handle_user_not_found(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(GalleryNotFound)
    def handle_gallery_not_found(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(GalleryPermission)
    def handle_gallery_permission_denied(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
