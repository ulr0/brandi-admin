from config import BUCKET_NAME


class ImageService:
    def image_upload(self, s3_connection, image_file):

        s3_connection.put_object(
            Body=image_file,
            Bucket=BUCKET_NAME,
            Key=image_file.filename,
            ContentType=image_file.content_type,
        )

        return f"https://{BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/{image_file.filename}"
