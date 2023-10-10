from sqlalchemy.orm import Session
from repository.validation_instance import ValidationInstanceRepository
from repository.schema import SchemaRepository
import time


class ValidationInstanceService(ValidationInstanceRepository):
    def __init__(self, db: Session, session):
        self.db = db
        self.session = session
        self.org_id = session.get('org_id', None)
        super().__init__(db, session)

    def enqueue(self, pid, schema_id, upload_id, metrics):
        schema = SchemaRepository(
            self.db, self.session).findOne(schema_id).data
        super().create({
            "id": pid,
            "status": 1,
            "schema_id": schema_id,
            "schema": schema,
            "upload_id": upload_id,
            "picked_at":  int(time.time() * 1000),
            "created_at": int(time.time() * 1000),
            "enqueue_time": metrics.get("enqueue_time", None),
            "schema_pull_time": metrics.get("schema_pull_time", None)
        })

    def mark_validation_failed(self, pid, validation_start, validation_end):
        super().update(pid, {
            "status": 2,
            "picked_at":  int(time.time() * 1000),
            "validation_status": 2,
            "validation_start_time": validation_start,
            "validation_end_time": validation_end,
            "end_time": int(time.time() * 1000),
            "progress_percentage": 100,
        })

    def mark_validation_completed(self, pid, validation_end_time):
        super().update(pid, {
            "status": 2,
            "picked_at":  int(time.time() * 1000),
            "validation_status": 1,
            "validation_end_time": validation_end_time,
            "progress_percentage": 100,
        })

    def mark_cleanup_start(self, pid):
        super().update(pid, {
            "status": 3,
            "picked_at":  int(time.time() * 1000),
            "cleanup_status": 1,
            "progress_percentage": 100,
        })

    def mark_mapping_start(self, pid):
        super().update(pid, {
            "status": 4,
            "picked_at":  int(time.time() * 1000),
            "mapping_status": 1,
            "progress_percentage": 100,
        })

    def mark_transform_start(self, pid):
        super().update(pid, {
            "status": 5,
            "picked_at":  int(time.time() * 1000),
            "transform_status": 1,
            "progress_percentage": 100,
        })

    def mark_output_created(self, pid, metrics={}):
        d = {
            "status": 6,
            "picked_at":  int(time.time() * 1000),
            "output_status": 1,
            "end_time": int(time.time() * 1000),
            "progress_percentage": 100,

        }
        d.update(metrics)
        super().update(pid, d)

    def dequeue(self, pid):
        super().update(pid, {
            "running_State": 0,
            "dequeued_at": int(time.time() * 1000)
        })
