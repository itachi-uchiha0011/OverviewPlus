from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models import Channel, ChannelMember, Message

channels_bp = Blueprint("channels", __name__)


@channels_bp.get("")
@jwt_required()
def list_channels():
    user_id = get_jwt_identity()
    # channels owned or joined or public
    joined_ids = [m.channel_id for m in ChannelMember.query.filter_by(user_id=user_id).all()]
    channels = (
        Channel.query.filter(
            (Channel.is_public == True) | (Channel.owner_id == user_id) | (Channel.id.in_(joined_ids))
        )
        .order_by(Channel.created_at.desc())
        .all()
    )
    return [
        {"id": c.id, "name": c.name, "is_public": c.is_public, "owner_id": c.owner_id}
        for c in channels
    ]


@channels_bp.post("")
@jwt_required()
def create_channel():
    user_id = get_jwt_identity()
    body = request.get_json() or {}
    c = Channel(name=body.get("name"), is_public=bool(body.get("is_public", True)), owner_id=user_id)
    db.session.add(c)
    db.session.commit()
    if not c.is_public:
        db.session.add(ChannelMember(channel_id=c.id, user_id=user_id, role="admin"))
        db.session.commit()
    return {"id": c.id}, 201


@channels_bp.post("/<int:channel_id>/invite")
@jwt_required()
def invite_member(channel_id: int):
    user_id = get_jwt_identity()
    channel = Channel.query.get_or_404(channel_id)
    if channel.owner_id != user_id:
        return {"error": "Only owner can invite"}, 403
    body = request.get_json() or {}
    new_user_id = int(body.get("user_id"))
    exists = ChannelMember.query.filter_by(channel_id=channel_id, user_id=new_user_id).first()
    if not exists:
        db.session.add(ChannelMember(channel_id=channel_id, user_id=new_user_id))
        db.session.commit()
    return {"message": "Invited"}


@channels_bp.get("/<int:channel_id>/messages")
@jwt_required()
def list_messages(channel_id: int):
    user_id = get_jwt_identity()
    channel = Channel.query.get_or_404(channel_id)
    member = ChannelMember.query.filter_by(channel_id=channel_id, user_id=user_id).first()
    if not channel.is_public and not member and channel.owner_id != user_id:
        return {"error": "Not allowed"}, 403
    msgs = Message.query.filter_by(channel_id=channel_id).order_by(Message.created_at.asc()).limit(200).all()
    return [
        {"id": m.id, "user_id": m.user_id, "content": m.content, "created_at": m.created_at.isoformat()}
        for m in msgs
    ]