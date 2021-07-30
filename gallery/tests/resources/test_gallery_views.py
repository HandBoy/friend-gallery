from bson.objectid import ObjectId


class TestCreateUserGallery:
    def test_success_create_gallery(self, client, access_token):
        # Give
        data = {"name": "John Doe Gallery"}
        access_headers = {"Authorization": f"Bearer {access_token}"}
        # Act
        response = client.post(
            "/api/v1/galleries",
            headers=access_headers,
            json=data,
        )
        # Assert
        assert response.status_code == 201

    def test_fail_without_authentication(self, client):
        # Give
        data = {"name": "Jonh Doe Gallery"}
        # Act
        response = client.post("/api/v1/galleries", json=data)
        # Assert
        assert response.status_code == 401

    def test_fail_without_name(self, client, access_token):
        # Give
        data = {}
        access_headers = {"Authorization": f"Bearer {access_token}"}
        # Act
        response = client.post(
            "/api/v1/galleries",
            headers=access_headers,
            json=data,
        )
        # Assert
        assert response.status_code == 400
        assert "name" in response.json


class TestListYourGalleries:
    def test_success_user_gallery(self, client, user):
        # Give
        data = {"name": "John Doe Gallery"}
        access_headers = {"Authorization": f"Bearer {user['access_token']}"}
        # Act
        response = client.get(
            f"/api/v1/users/{user['user']._id}/galleries",
            headers=access_headers,
            json=data,
        )
        # Assert
        assert response.status_code == 200
        assert len(response.json) == 1

    def test_success_user_without_gallery(
        self, client, access_token, create_gallery
    ):
        # Give
        data = {"name": "John Doe Gallery"}
        access_headers = {"Authorization": f"Bearer {access_token}"}
        # Act
        response = client.get(
            f"/api/v1/users/{ObjectId()}/galleries",
            headers=access_headers,
            json=data,
        )
        # Assert
        assert response.status_code == 200
        assert len(response.json) == 0

    def test_success_invalid_user(self, client, access_token, create_gallery):
        # Give
        data = {"name": "John Doe Gallery"}
        access_headers = {"Authorization": f"Bearer {access_token}"}
        # Act
        response = client.get(
            "/api/v1/users/abc/galleries",
            headers=access_headers,
            json=data,
        )
        # Assert
        assert response.status_code == 200
        assert len(response.json) == 0

    def test_fail_without_athorization(self, client, create_user):
        # Give
        data = {"name": "John Doe Gallery"}
        # Act
        response = client.get(
            f"/api/v1/users/{create_user._id}/galleries",
            json=data,
        )
        # Assert
        assert response.status_code == 401

    def test_jwt_token_with_invalid_user_id(
        self, client, token_with_invalid_user_id
    ):
        # Give
        data = {"name": "John Doe Gallery"}
        access_headers = {
            "Authorization": f"Bearer {token_with_invalid_user_id}"
        }
        # Act
        response = client.get(
            "/api/v1/users/abc/galleries",
            headers=access_headers,
            json=data,
        )
        # Assert
        assert response.status_code == 401
