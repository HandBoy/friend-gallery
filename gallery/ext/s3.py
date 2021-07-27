from gallery.exceptions import FileUploadException
import boto3
from flask import current_app


def allowed_images_to_upload(filename):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def upload_file_to_s3(file, bucket_name=None, acl="public-read"):
    s3 = current_app.extensions["s3"]

    if not bucket_name:
        bucket_name = current_app.config["AWS_S3_BUCKET_NAME"]

    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            f"files/{file.filename}",
            ExtraArgs={"ACL": acl, "ContentType": file.content_type},
        )

        return f"{current_app.config['AWS_S3_LOCATION']}/{file.filename}"

    except Exception as err:
        raise FileUploadException(
            message="Sorry, we has a problem to process your image",
            payload=err,
        )


def init_app(app):
    app.extensions["s3"] = boto3.client(
        "s3",
        aws_access_key_id=app.config["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=app.config["AWS_SECRET_ACCESS_KEY"],
    )
