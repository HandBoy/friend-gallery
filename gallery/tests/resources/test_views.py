from bson.objectid import ObjectId
from gallery.documents import UserModel
from gallery.exceptions import UserAlreadyExists


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
