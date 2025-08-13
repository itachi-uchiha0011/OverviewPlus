from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask_socketio import join_room, leave_room, emit
from ..extensions import socketio, db
from ..models import Channel, ChannelMember, Message


@socketio.on("join_channel")
def handle_join_channel(data):
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    channel_id = int(data.get("channel_id"))
    member = ChannelMember.query.filter_by(channel_id=channel_id, user_id=user_id).first()
    channel = Channel.query.get(channel_id)
    if channel and (channel.is_public or member is not None):
        join_room(f"channel:{channel_id}")
        emit("system", {"message": "joined", "channel_id": channel_id})
    else:
        emit("error", {"message": "Not allowed"})


@socketio.on("leave_channel")
def handle_leave_channel(data):
    verify_jwt_in_request()
    channel_id = int(data.get("channel_id"))
    leave_room(f"channel:{channel_id}")
    emit("system", {"message": "left", "channel_id": channel_id})


@socketio.on("message")
def handle_message(data):
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    channel_id = int(data.get("channel_id"))
    content = (data.get("content") or "").strip()
    if not content:
        return

    member = ChannelMember.query.filter_by(channel_id=channel_id, user_id=user_id).first()
    channel = Channel.query.get(channel_id)
    if not channel or (not channel.is_public and not member):
        emit("error", {"message": "Not allowed"})
        return

    msg = Message(channel_id=channel_id, user_id=user_id, content=content)
    db.session.add(msg)
    db.session.commit()
    emit("message", {"id": msg.id, "user_id": user_id, "channel_id": channel_id, "content": content}, room=f"channel:{channel_id}")