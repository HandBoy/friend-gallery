from gallery.exceptions import UserAlreadyExists


class TestLogin:
    def test_success_login(self, client, mocker):
        # GIVE
        mocker.patch("gallery.resources.user.login", return_value=True)
        data = {"email": "hand4@gmail.com", "password": "123dfgdfg"}
        # Act
        response = client.post("/api/v1/login", json=data)
        # Assert
        assert response.status_code == 200
        assert "access_token" in response.json
        assert "refresh_token" in response.json

    def test_fail_login(self, client, mocker):
        # GIVE
        mocker.patch("gallery.resources.user.login", return_value=False)
        data = {"email": "hand4@gmail.com", "password": "123dfgdfg"}
        # Act
        response = client.post("/api/v1/login", json=data)
        # Assert
        assert response.status_code == 401
        assert "error" in response.json
        assert "message" in response.json

    def test_fail_login_without_body(self, client):
        # Act
        response = client.post("/api/v1/login", data={})
        # Assert
        assert response.status_code == 422

    def test_fail_login_without_password(self, client):
        # GIVE
        data = {"email": "email@gmail.com"}
        # Act
        response = client.post("/api/v1/login", json=data)
        # Assert
        assert response.status_code == 422
        assert "password" in response.json

    def test_fail_login_without_email(self, client):
        # GIVE
        data = {"password": "123dfgdfg"}
        # Act
        response = client.post("/api/v1/login", json=data)
        # Assert
        assert response.status_code == 422
        assert "email" in response.json


class TestCreateUser:
    def test_success_create_user(self, client, mocker):
        # GIVE
        mocker.patch(
            "gallery.resources.user.create_user", return_value=object()
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
        assert response.status_code == 422
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
        assert response.status_code == 422
        assert "password" in response.json

    def test_fail_without_email(self, client):
        # GIVE
        data = {"name": "Jonh Doe", "password": "123@abvs"}
        # Act
        response = client.post("/api/v1/users", json=data)
        # Assert
        assert response.status_code == 422
        assert "email" in response.json

    def test_fail_without_name(self, client):
        # GIVE
        data = {"email": "email@gmail.com", "password": "123@abvs"}
        # Act
        response = client.post("/api/v1/users", json=data)
        # Assert
        assert response.status_code == 422
        assert "name" in response.json

    def test_fail_user_already_exists(self, client, mocker):
        # GIVE
        mocker.patch(
            "gallery.resources.user.create_user",
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
