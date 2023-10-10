from services.s3 import S3Service


class UploadsService(S3Service):
    def __init__(self, db, folder, session):
        self.org_id = session.get("org_id", None)
        super().__init__(db, folder, session)

    def fileUpload(self, file):
        return self.upload(file)

    def server_upload(self, id, key, image_1, image_2):
        return self.upload_images(id, key, image_1, image_2)

    def upload_fileobj(self, buffer, file_name):
        return self.upload_obj(buffer, file_name)
