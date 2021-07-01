from flask import request
from flask.views import MethodView


class ImageView(MethodView):
    def post(self):
        image_files = request.files.getlist("image_file")

        # TODO
        # 사진 리사이징

        # location = s3.get_bucket_location(Bucket=BUKET_NAME)['LocationConstraint']
        try:
            connection = connect_s3()
            result = product_service.upload_product_detail_info_image(connection, data)
            return jsonify({"data": result})
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            if connection is not None:
                connection.close()
        try:
            s3 = connect_s3()
            s3.put_object(
                Body=image_file,
                Bucket=BUCKET_NAME,
                Key=image_file.filename,
                ContentType=image_file.content_type,
            )
        except Exception as e:
            raise e
        pass
    pass
