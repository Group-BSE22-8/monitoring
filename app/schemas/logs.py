from marshmallow import Schema, fields

class ClusterLogsSchema(Schema):

    id = fields.UUID(dump_only=True)
    cluster_id = fields.String()
    status = fields.String()
    date_created = fields.Date(dump_only=True)


class StatusSchema(Schema):

    cluster_id = fields.String()
