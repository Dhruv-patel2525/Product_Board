import logging
from app.core.config import settings
from app.schemas.invitation import InvitationRead
from celery_app import celery_app
from app.core.email import send_raw_email

logger=logging.getLogger(__name__)
@celery_app.task(name="email.send_welcome")
def send_welcome_email(email:str,full_name:str):
    logger.info("Starting send_welcome_email task",extra={"email":email})
    """
    Send a welcome email to a single user.
    This runs in the Celery worker, not in the API process.
    """
    subject = "Welcome to ProductBoard"

    if full_name:
        greeting = f"Hi {full_name},"
    else:
        greeting = "Hi there,"

    body = f"""{greeting}

        Welcome to ProductBoard! Your account has been created successfully.

        You can now log in and start organizing your product feedback and roadmaps.

        – The ProductBoard Team
        """

    send_raw_email(to=email, subject=subject, body=body)
    logger.info("Finished send_welcome_email task",extra={"email":email})

    return {"email": email, "status": "sent"}
    # Load user from DB, render template, send email via SMTP/API

@celery_app.task(name="email.invite_user")
def invite_user_to_org(invitation_data: dict):
    """
    Send an organization invitation email.

    `invitation_data` must be a dict from InvitationRead.model_dump(), e.g.:

        InvitationRead(...).model_dump()
    """
    invitation = InvitationRead(**invitation_data)

    logger.info(
        "Starting invite_user_to_org task",
        extra={
            "email": invitation.email,
            "invitation_id": invitation.id,
            "org_id": invitation.org_id,
            "role_id": invitation.role_id,
            "token": invitation.token,
        },
    )

    subject = "You're invited to join ProductBoard"

    # Ideally use a config value, this is just an example:
    # from app.core.config import settings
    # base_url = settings.FRONTEND_URL
    base_url = settings.FRONTEND_URL
    # Token is what should be used to validate the invite
    accept_url = f"{base_url}/invitations/{invitation.token}/accept"

    greeting = "Hi there,"

    body = f"""{greeting}

    You've been invited to join an organization on ProductBoard.

    Organization ID: {invitation.org_id}
    Role ID: {invitation.role_id}

    To accept this invitation, click the link below:

    {accept_url}

    If you weren't expecting this invitation, you can safely ignore this email.

    – The ProductBoard Team
    """

    send_raw_email(to=invitation.email, subject=subject, body=body)

    logger.info(
        "Finished invite_user_to_org task",
        extra={
            "email": invitation.email,
            "invitation_id": invitation.id,
            "org_id": invitation.org_id,
        },
    )

    return {
        "email": invitation.email,
        "invitation_id": invitation.id,
        "status": "sent",
    }
