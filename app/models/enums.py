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
    APPROVED="APPROVED"
    PENDING="PENDING"