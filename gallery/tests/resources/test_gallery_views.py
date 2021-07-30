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

    def test_fail_jwt_token_with_invalid_user_id(
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


class TestAddApproverInGallery:
    def test_success_user_can_add_from_approve_your_gallery(
        self, client, access_token, create_user, create_gallery
    ):
        # Give
        access_headers = {"Authorization": f"Bearer {access_token}"}
        data = {"email": create_user.email}
        # Act
        response = client.post(
            f"/api/v1/gallery/{create_gallery._id}/approver",
            headers=access_headers,
            json=data,
        )
        # Assert
        assert response.status_code == 200

    def test_fail_without_email(self, client, access_token, create_gallery):
        # Give
        access_headers = {"Authorization": f"Bearer {access_token}"}
        data = {}
        # Act
        response = client.post(
            f"/api/v1/gallery/{create_gallery._id}/approver",
            headers=access_headers,
            json=data,
        )
        # Assert
        assert response.status_code == 400

    def test_fail_invalid_email(self, client, access_token, create_gallery):
        # Give
        access_headers = {"Authorization": f"Bearer {access_token}"}
        data = {"email": "isso_na_e_um_email"}
        # Act
        response = client.post(
            f"/api/v1/gallery/{create_gallery._id}/approver",
            headers=access_headers,
            json=data,
        )
        # Assert
        assert response.status_code == 400

    def test_fail_user_to_approver_not_found(
        self, client, access_token, create_gallery
    ):
        # Give
        access_headers = {"Authorization": f"Bearer {access_token}"}
        data = {"email": "user_not_found@email.com"}
        # Act
        response = client.post(
            f"/api/v1/gallery/{create_gallery._id}/approver",
            headers=access_headers,
            json=data,
        )
        # Assert
        assert response.status_code == 404

    def test_fail_gallery_not_found(
        self, client, access_token, create_gallery
    ):
        # Give
        access_headers = {"Authorization": f"Bearer {access_token}"}
        data = {"email": "user_not_found@email.com"}
        # Act
        response = client.post(
            f"/api/v1/gallery/{ObjectId()}/approver",
            headers=access_headers,
            json=data,
        )
        # Assert
        assert response.status_code == 404

    def test_invalid_gallery_id(self, client, access_token, create_gallery):
        # Give
        access_headers = {"Authorization": f"Bearer {access_token}"}
        data = {"email": "user_not_found@email.com"}
        # Act
        response = client.post(
            "/api/v1/gallery/123eita/approver",
            headers=access_headers,
            json=data,
        )
        # Assert
        assert response.status_code == 404


class TestAddFriendInGallery:
    def test_success_user_can_add_approver_in_your_gallery(
        self, client, create_user, user
    ):
        # Give
        access_headers = {"Authorization": f"Bearer {user['access_token']}"}
        data = {"email": create_user.email}
        # Act
        response = client.post(
            f"/api/v1/gallery/{user['gallery']._id}/friend",
            headers=access_headers,
            json=data,
        )
        # Assert
        assert response.status_code == 200

    def test_fail_invalid_email(
        self, client, access_token, create_user, user
    ):
        # Give
        access_headers = {"Authorization": f"Bearer {access_token}"}
        data = {"email": "isso_nao_eh_um_email"}
        # Act
        response = client.post(
            f"/api/v1/gallery/{user['gallery']._id}/friend",
            headers=access_headers,
            json=data,
        )
        # Assert
        assert response.status_code == 400

    def test_fail_request_without_email(
        self, client, access_token, create_user, user
    ):
        # Give
        access_headers = {"Authorization": f"Bearer {user['access_token']}"}
        # Act
        response = client.post(
            f"/api/v1/gallery/{user['gallery']._id}/friend",
            headers=access_headers,
        )
        # Assert
        assert response.status_code == 400

    def test_fail_without_athorization(self, client, user):
        # Give
        data = {"email": user["user"].email}
        # Act
        response = client.post(
            f"/api/v1/gallery/{user['gallery']._id}/friend",
            json=data,
        )
        # Assert
        assert response.status_code == 401

    def test_fail_invalid_gallery_id(
        self, client, create_user, user
    ):
        # Give
        access_headers = {"Authorization": f"Bearer {user['access_token']}"}
        data = {"email": create_user.email}
        # Act
        response = client.post(
            "/api/v1/gallery/123abc/friend",
            headers=access_headers,
            json=data,
        )
        # Assert
        assert response.status_code == 404

    def test_fail_gallery_not_found(
        self, client, create_user, user
    ):
        # Give
        access_headers = {"Authorization": f"Bearer {user['access_token']}"}
        data = {"email": create_user.email}
        # Act
        response = client.post(
            f"/api/v1/gallery/{ObjectId()}/friend",
            headers=access_headers,
            json=data,
        )
        # Assert
        assert response.status_code == 404

    def test_fail_user_frien_not_found(
        self, client, create_user, user
    ):
        # Give
        access_headers = {"Authorization": f"Bearer {user['access_token']}"}
        data = {"email": "user_not_found@email.com"}
        # Act
        response = client.post(
            f"/api/v1/gallery/{user['gallery']._id}/friend",
            headers=access_headers,
            json=data,
        )
        # Assert
        assert response.status_code == 404
