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


class LoginUnauthorized(FriendGalleryException):
    status_code = 401


class UserNotFound(FriendGalleryException):
    status_code = 404


class GalleryNotFound(FriendGalleryException):
    status_code = 404


class PictureNotFound(FriendGalleryException):
    status_code = 404


class GalleryPermission(FriendGalleryException):
    status_code = 401


class FileNotAccept(FriendGalleryException):
    status_code = 400


class FileUploadException(FriendGalleryException):
    status_code = 400


class FileValidationException(FriendGalleryException):
    status_code = 400


def handle_api_exceptions(app):
    @app.errorhandler(UserNotFound)
    def handle_user_not_found(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(LoginUnauthorized)
    def handle_login_Unauthorized(error):
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

    @app.errorhandler(FileNotAccept)
    def handle_file_not_accept_denied(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(FileUploadException)
    def handle_file_upload_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(FileValidationException)
    def handle_file_validation_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(PictureNotFound)
    def handle_picture_not_found_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
