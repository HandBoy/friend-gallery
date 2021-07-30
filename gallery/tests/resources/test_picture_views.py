from bson.objectid import ObjectId


class TestApprovePicture:
    def test_success_user_can_approve_a_picture(
        self, client, user
    ):
        # Give
        access_headers = {"Authorization": f"Bearer {user['access_token']}"}
        # Act
        response = client.put(
            (
                f"/api/v1/gallery/{user['gallery']._id}"
                f"/pictures/{user['gallery'].pictures[0].id}/approve"
            ),
            headers=access_headers,
        )
        # Assert
        assert response.status_code == 200

    def test_fail_without_authorization(self, client, user):
        # Give
        # Act
        response = client.put(
            (
                f"/api/v1/gallery/{user['gallery']._id}"
                f"/pictures/{user['gallery'].pictures[0].id}/approve"
            ),
        )
        # Assert
        assert response.status_code == 401

    def test_fail_gallery_unknown(self, client, user):
        # Give
        access_headers = {"Authorization": f"Bearer {user['access_token']}"}
        # Act
        response = client.put(
            (
                f"/api/v1/gallery/{ObjectId()}"
                f"/pictures/{user['gallery'].pictures[0].id}/approve"
            ),
            headers=access_headers,
        )
        # Assert
        assert response.status_code == 404

    def test_fail_invalid_gallery_id(self, client, user):
        # Give
        access_headers = {"Authorization": f"Bearer {user['access_token']}"}
        # Act
        response = client.put(
            (
                "/api/v1/gallery/123abc}/pictures/"
                f"{user['gallery'].pictures[0].id}/approve"
            ),
            headers=access_headers,
        )
        # Assert
        assert response.status_code == 404

    def test_fail_picture_not_found(
        self, client, user
    ):
        # Give
        access_headers = {"Authorization": f"Bearer {user['access_token']}"}
        # Act
        response = client.put(
            (
                f"/api/v1/gallery/{user['gallery']._id}"
                f"/pictures/{ObjectId()}/approve"
            ),
            headers=access_headers,
        )
        # Assert
        assert response.status_code == 404

    def test_fail_invalid_picture_id(
        self, client, user
    ):
        # Give
        access_headers = {"Authorization": f"Bearer {user['access_token']}"}
        # Act
        response = client.put(
            (
                f"/api/v1/gallery/{user['gallery']._id}"
                "/pictures/123dfg/approve"
            ),
            headers=access_headers,
        )
        # Assert
        assert response.status_code == 404

    def test_fail_user_dont_have_permission_to_approve(
        self, client, access_token, user
    ):
        # Give
        access_headers = {"Authorization": f"Bearer {access_token}"}
        # Act
        response = client.put(
            (
                f"/api/v1/gallery/{user['gallery']._id}"
                f"/pictures/{user['gallery'].pictures[0].id}/approve"
            ),
            headers=access_headers,
        )
        # Assert
        assert response.status_code == 401


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

    def test_fail_gallery_doesnt_exists(
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

    def test_fail_invalid_gallery_id(
        self, client, access_token, gallery_with_pictures
    ):
        # Give
        access_headers = {"Authorization": f"Bearer {access_token}"}
        # Act
        response = client.post(
            (
                f"/api/v1/gallery/123AGD/pictures"
                f"/{gallery_with_pictures.pictures[0].id}/like"
            ),
            headers=access_headers,
        )
        # Assert
        assert response.status_code == 404

    def test_fail_picture_doesnt_exists(
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

    def test_fail_invalid_picture_id(
        self, client, access_token, gallery_with_pictures
    ):
        # Give
        access_headers = {"Authorization": f"Bearer {access_token}"}
        # Act
        response = client.post(
            (
                f"/api/v1/gallery/{gallery_with_pictures._id}"
                f"/pictures/123ghj/like"
            ),
            headers=access_headers,
        )
        # Assert
        assert response.status_code == 404
