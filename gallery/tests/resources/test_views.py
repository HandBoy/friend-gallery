from bson.objectid import ObjectId
from gallery.documents import UserModel
from gallery.exceptions import FileUploadException, UserAlreadyExists


class TestLogin:
    def test_success_login(self, client, mocker):
        # GIVE
        mocker.patch(
            "gallery.resources.views.login",
            return_value=UserModel(
                email="e@e.com", name="a", password="12345678"
            ),
        )
        data = {"email": "hand4@gmail.com", "password": "123dfgdfg"}
        # Act
        response = client.post("/api/v1/login", json=data)
        # Assert
        assert response.status_code == 200
        assert "access_token" in response.json
        assert "refresh_token" in response.json

    def test_fail_login(self, client, mocker):
        # GIVE
        mocker.patch("gallery.resources.views.login", return_value=False)
        data = {"email": "hand4@gmail.com", "password": "123dfgdfg"}
        # Act
        response = client.post("/api/v1/login", json=data)
        # Assert
        assert response.status_code == 401
        assert "status_code" in response.json
        assert "message" in response.json

    def test_fail_login_without_body(self, client):
        # Act
        response = client.post("/api/v1/login", data={})
        # Assert
        assert response.status_code == 400

    def test_fail_login_without_password(self, client):
        # GIVE
        data = {"email": "email@gmail.com"}
        # Act
        response = client.post("/api/v1/login", json=data)
        # Assert
        assert response.status_code == 400
        assert "password" in response.json

    def test_fail_login_without_email(self, client):
        # GIVE
        data = {"password": "123dfgdfg"}
        # Act
        response = client.post("/api/v1/login", json=data)
        # Assert
        assert response.status_code == 400
        assert "email" in response.json


class TestCreateUser:
    def test_success_create_user(self, client, mocker):
        # GIVE
        mocker.patch(
            "gallery.resources.views.create_user", return_value=object()
        )
        data = {
            "email": "hand5@gmail.com",
            "name": "Jonh Doe",
            "password": "123@abdf",
        }
        # Act
        response = client.post("/api/v1/users", json=data)
        # Assert
        assert response.status_code == 201

    def test_fail_shorter_password(self, client):
        # GIVE
        data = {
            "email": "email@gmail.com",
            "name": "Jonh Doe",
            "password": "123",
        }
        # Act
        response = client.post("/api/v1/users", json=data)
        # Assert
        assert response.status_code == 400
        assert "password" in response.json

    def test_fail_without_password(self, client):
        # GIVE
        data = {
            "email": "email@gmail.com",
            "name": "Jonh Doe",
        }
        # Act
        response = client.post("/api/v1/users", json=data)
        # Assert
        assert response.status_code == 400
        assert "password" in response.json

    def test_fail_without_email(self, client):
        # GIVE
        data = {"name": "Jonh Doe", "password": "123@abvs"}
        # Act
        response = client.post("/api/v1/users", json=data)
        # Assert
        assert response.status_code == 400
        assert "email" in response.json

    def test_fail_without_name(self, client):
        # GIVE
        data = {"email": "email@gmail.com", "password": "123@abvs"}
        # Act
        response = client.post("/api/v1/users", json=data)
        # Assert
        assert response.status_code == 400
        assert "name" in response.json

    def test_fail_user_already_exists(self, client, mocker):
        # GIVE
        mocker.patch(
            "gallery.resources.views.create_user",
            side_effect=UserAlreadyExists("vish"),
        )
        data = {
            "email": "hand5@gmail.com",
            "name": "Jonh Doe",
            "password": "123@abdf",
        }
        # Act
        response = client.post("/api/v1/users", json=data)
        # Assert
        assert response.status_code == 400
        assert "message" in response.json
        assert "status_code" in response.json


class TestListPicturesUserGallery:
    def test_success_validate_contract(
        self, client, access_token, create_gallery
    ):
        # Give
        access_headers = {"Authorization": f"Bearer {access_token}"}
        # Act
        response = client.get(
            f"/api/v1/gallery/{create_gallery._id}/pictures",
            headers=access_headers,
        )
        data = response.json
        # Assert
        assert response.status_code == 200
        assert "next_page" in data
        assert "previous_page" in data
        assert "count" in data
        assert "result" in data

    def test_success_gallery_without_pictures(
        self, client, access_token, create_gallery
    ):
        # Give
        access_headers = {"Authorization": f"Bearer {access_token}"}
        # Act
        response = client.get(
            f"/api/v1/gallery/{create_gallery._id}/pictures",
            headers=access_headers,
        )
        # Assert
        assert response.status_code == 200
        assert len(response.json["result"]) == 0

    def test_success_gallery_with_your_pictures(self, client, user):
        # Give
        access_headers = {"Authorization": f"Bearer {user['access_token']}"}
        # Act
        response = client.get(
            f"/api/v1/gallery/{user['gallery']._id}/pictures",
            headers=access_headers,
        )
        # Assert
        assert response.status_code == 200
        assert len(response.json["result"]) == 2

    def test_success_gallery_belongs_another_user(
        self, client, access_token, create_gallery
    ):
        # Give
        access_headers = {"Authorization": f"Bearer {access_token}"}
        # Act
        response = client.get(
            f"/api/v1/gallery/{create_gallery._id}/pictures",
            headers=access_headers,
        )
        # Assert
        assert response.status_code == 200
        assert len(response.json["result"]) == 0

    def test_fail_no_authorization(self, client, create_gallery):
        # Give
        # Act
        response = client.get(
            f"/api/v1/gallery/{create_gallery._id}/pictures",
        )
        # Assert
        assert response.status_code == 401

    def test_fail_gallery_doesnt_exist(self, client, access_token):
        # Give
        access_headers = {"Authorization": f"Bearer {access_token}"}
        # Act
        response = client.get(
            f"/api/v1/gallery/{ObjectId()}/pictures",
            headers=access_headers,
        )
        # Assert
        assert response.status_code == 404
        assert "message" in response.json


class TestCreatePicturesUserGallery:
    def test_success_add_new_picture(self, mocker, client, user, file):
        # Give
        access_headers = {"Authorization": f"Bearer {user['access_token']}"}
        data = {"name": "123", "description": "213", "photo_file": file}
        mocker.patch(
            "gallery.controllers.gallery_controller.upload_file_to_s3",
            return_value="http://bucket.s3.amazonaws.com/Input.jpg",
        )
        # Act
        response = client.post(
            f"/api/v1/gallery/{user['gallery']._id}/pictures",
            headers=access_headers,
            data=data,
            content_type="multipart/form-data",
        )
        # Assert
        assert response.status_code == 201

    def test_fail_without_authorization(self, client, create_gallery):
        # Give
        data = {"name": "123", "description": "eitasdae", "url": "adasdasdas"}
        # Act
        response = client.post(
            f"/api/v1/gallery/{create_gallery._id}/pictures",
            json=data,
        )
        # Assert
        assert response.status_code == 401

    def test_fail_without_name(self, client, user, file):
        # Give
        data = {"description": "eitasdae", "photo_file": file}
        access_headers = {"Authorization": f"Bearer {user['access_token']}"}
        # Act
        response = client.post(
            f"/api/v1/gallery/{user['gallery']._id}/pictures",
            headers=access_headers,
            data=data,
        )
        # Assert
        assert response.status_code == 400

    def test_fail_gallery_doesnt_exist(
        self, client, access_token, create_gallery
    ):
        # Give
        data = {"name": "123", "description": "eitasdae", "url": "adasdasdas"}
        access_headers = {"Authorization": f"Bearer {access_token}"}
        # Act
        response = client.post(
            (
                f"/api/v1/users/{create_gallery.user._id}"
                f"/gallery/{ObjectId()}/pictures"
            ),
            headers=access_headers,
            json=data,
        )
        # Assert
        assert response.status_code == 404

    def test_fail_user_doesnt_exist(
        self, client, access_token, create_gallery
    ):
        # Give
        data = {"name": "123", "description": "eitasdae", "url": "adasdasdas"}
        access_headers = {"Authorization": f"Bearer {access_token}"}
        # Act
        response = client.post(
            (
                f"/api/v1/users/{ObjectId()}"
                f"/gallery/{create_gallery._id}/pictures"
            ),
            headers=access_headers,
            json=data,
        )
        # Assert
        assert response.status_code == 404

    def test_fail_without_image(self, client, user):
        # Give
        access_headers = {"Authorization": f"Bearer {user['access_token']}"}
        data = {"name": "123", "description": "213"}
        # Act
        response = client.post(
            f"/api/v1/gallery/{user['gallery']._id}/pictures",
            headers=access_headers,
            data=data,
            content_type="multipart/form-data",
        )
        # Assert
        assert response.status_code == 400

    def test_fail_image_with_empty_name(self, client, user, file):
        # Give
        file.filename = ""
        access_headers = {"Authorization": f"Bearer {user['access_token']}"}
        data = {"name": "123", "description": "213", "photo_file": file}
        # Act
        response = client.post(
            f"/api/v1/gallery/{user['gallery']._id}/pictures",
            headers=access_headers,
            data=data,
            content_type="multipart/form-data",
        )
        # Assert
        assert response.status_code == 400

    def test_fail_file_with_extension_not_allowed(self, client, user, file):
        # Give
        file.filename = "Input.exe"
        access_headers = {"Authorization": f"Bearer {user['access_token']}"}
        data = {"name": "123", "description": "213", "photo_file": file}
        # Act
        response = client.post(
            f"/api/v1/gallery/{user['gallery']._id}/pictures",
            headers=access_headers,
            data=data,
            content_type="multipart/form-data",
        )
        # Assert
        assert response.status_code == 400

    def test_fail_send_image_to_s3(self, mocker, client, user, file):
        # Give
        access_headers = {"Authorization": f"Bearer {user['access_token']}"}
        data = {"name": "123", "description": "213", "photo_file": file}
        mocker.patch(
            "gallery.controllers.gallery_controller.upload_file_to_s3",
            side_effect=FileUploadException("vish"),
        )
        # Act
        response = client.post(
            f"/api/v1/gallery/{user['gallery']._id}/pictures",
            headers=access_headers,
            data=data,
            content_type="multipart/form-data",
        )
        # Assert
        assert response.status_code == 400

    def test_fail_upload_me_not_friend(self):
        # TODO
        pass

    def test_success_friend_upload(self):
        # TODO
        pass


class TestLikePicture:
    def test_success_like_a_picture(
        self, client, access_token, gallery_with_pictures
    ):
        # Give
        access_headers = {"Authorization": f"Bearer {access_token}"}
        # Act
        response = client.post(
            (
                f"/api/v1/gallery/{gallery_with_pictures._id}"
                f"/pictures/{gallery_with_pictures.pictures[0].id}/like"
            ),
            headers=access_headers,
        )
        # Assert
        assert response.status_code == 200

    def test_fail_wihtout_auth(self, client, gallery_with_pictures):
        # Give
        # Act
        response = client.post(
            (
                f"/api/v1/gallery/{gallery_with_pictures._id}"
                f"/pictures/{gallery_with_pictures.pictures[0].id}/like"
            ),
        )
        # Assert
        assert response.status_code == 401

    def test_success_gallery_doesnt_exists(
        self, client, access_token, gallery_with_pictures
    ):
        # Give
        access_headers = {"Authorization": f"Bearer {access_token}"}
        # Act
        response = client.post(
            (
                f"/api/v1/gallery/{ObjectId()}"
                f"/pictures/{gallery_with_pictures.pictures[0].id}/like"
            ),
            headers=access_headers,
        )
        # Assert
        assert response.status_code == 404

    def test_success_picture_doesnt_exists(
        self, client, access_token, gallery_with_pictures
    ):
        # Give
        access_headers = {"Authorization": f"Bearer {access_token}"}
        # Act
        response = client.post(
            (
                f"/api/v1/gallery/{gallery_with_pictures._id}"
                f"/pictures/{ObjectId()}/like"
            ),
            headers=access_headers,
        )
        # Assert
        assert response.status_code == 404

