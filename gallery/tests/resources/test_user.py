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
