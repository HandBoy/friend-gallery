from bson.objectid import ObjectId
from gallery.exceptions import FileUploadException


class TestApprovePicture:
    def test_success_user_can_approve_a_picture(self, client, user):
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

    def test_fail_picture_not_found(self, client, user):
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

    def test_fail_invalid_picture_id(self, client, user):
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

    def test_success_friend_upload(
        self, mocker, client, access_token, user, file
    ):
        # Give
        access_headers = {"Authorization": f"Bearer {access_token}"}
        data = {"name": "123", "description": "213", "photo_file": file}
        mocker.patch(
            (
                "gallery.controllers.gallery_controller."
                "GalleryModel.are_you_friend"
            ),
            return_value=True,
        )
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

    def test_fail_gallery_doesnt_exist(self, client, user, file):
        # Give
        data = {"name": "123", "description": "213", "photo_file": file}
        access_headers = {"Authorization": f"Bearer {user['access_token']}"}
        # Act
        response = client.post(
            f"/api/v1/gallery/{ObjectId()}/pictures",
            headers=access_headers,
            data=data,
            content_type="multipart/form-data",
        )
        # Assert
        assert response.status_code == 404

    def test_fail_invalid_gallery_id(self, client, user, file):
        # Give
        data = {"name": "123", "description": "213", "photo_file": file}
        access_headers = {"Authorization": f"Bearer {user['access_token']}"}
        # Act
        response = client.post(
            "/api/v1/gallery/123gfhd/pictures",
            headers=access_headers,
            data=data,
            content_type="multipart/form-data",
        )
        # Assert
        assert response.status_code == 404

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

    def test_fail_image_with_empty_file_name(self, client, user, file):
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

    def test_fail_upload_me_not_friend(
        self, mocker, client, access_token, user, file
    ):
        # Give
        access_headers = {"Authorization": f"Bearer {access_token}"}
        data = {"name": "123", "description": "213", "photo_file": file}
        mocker.patch(
            (
                "gallery.controllers.gallery_controller."
                "GalleryModel.are_you_friend"
            ),
            return_value=False,
        )
        # Act

        response = client.post(
            f"/api/v1/gallery/{user['gallery']._id}/pictures",
            headers=access_headers,
            data=data,
            content_type="multipart/form-data",
        )

        # Assert
        assert response.status_code == 401


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

    def test_success_gallery_with_pictures(self, client, user):
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

    def test_success_gallery_belongs_another_user_get_only_approved(
        self, client, access_token, user
    ):
        # Give
        access_headers = {"Authorization": f"Bearer {access_token}"}
        # Act
        response = client.get(
            f"/api/v1/gallery/{user['gallery']._id}/pictures",
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
