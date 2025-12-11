import enum

class OrganizationStatus(enum.Enum):
    ACTIVE="ACTIVE"
    INACTIVE="INACTIVE"
    PENDING="PENDING"
    BANNED="BANNED"

class SystemRole(enum.Enum):
    OWNER="OWNER"
    ADMIN="ADMIN" 
    PRODUCT_MANAGER="PRODUCT_MANAGER"
    CONTRIBUTOR="CONTRIBUTOR"
    VIEWER="VIEWER"

class InvitationStatus(enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"

class FeedbackStatus(enum.Enum):
    NEW = "new"
    UNDER_REVIEW = "under_review"
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"
    DUPLICATE = "duplicate"
