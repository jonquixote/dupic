from src.models import db

class ApiKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    service = db.Column(db.String(50), nullable=False)  # e.g., "openai", "twitter"
    key = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f"<ApiKey {self.service} for User {self.user_id}>"

    def to_dict(self, mask_key=False):
        data = {
            "id": self.id,
            "user_id": self.user_id,
            "service": self.service,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
        if mask_key and self.key:
            data["key"] = f"sk-....{self.key[-4:]}"
        else:
            data["key"] = self.key
        return data