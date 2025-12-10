from celery_app import celery_app
@celery_app.task(name="notification.send_push")
def send_notification_task(user_id:int,payload:dict):
    #push logic
    """
    1. Insert notification row in DB
    2. Optionally publish event to WebSocket layer / Redis pubsub
    """
    # pseudo-code:
    # from app.core.db import get_sync_session
    # with get_sync_session() as session:
    #     notification = Notification(
    #         user_id=user_id,
    #         type=notif_type,
    #         payload=data,
    #     )
    #     session.add(notification)
    #     session.commit()
    #
    # optionally: push to WebSocket broadcaster
    return {"user_id":user_id}


@celery_app.task(name="notification.user_registerd")
def user_registered_notification(user_id:int):
    #one question before i start workign with the notification .
    #how can i just jotify the specific user not to all other as ther server will be running for all of them right when i pass the message through web socket 
    return {"user_id":user_id}