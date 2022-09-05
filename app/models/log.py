from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import text as sa_text
from app.models import db
from app.models.model_mixin import ModelMixin

class ClusterLog(ModelMixin):
    __tablename__ = 'cluster_logs'
    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=sa_text("uuid_generate_v4()"))
    cluster_id = db.Column(db.String(256), nullable=True)
    status = db.Column(db.String(256), nullable=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
