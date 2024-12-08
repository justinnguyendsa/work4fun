from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Event, db
from datetime import datetime

events = Blueprint('events', __name__)

# Tạo sự kiện mới
@events.route('/events', methods=['POST'])
@jwt_required()
def create_event():
    user_id = get_jwt_identity()
    data = request.get_json()
    new_event = Event(
        title=data['title'],
        description=data.get('description'),
        start_time=datetime.fromisoformat(data['start_time']),
        end_time=datetime.fromisoformat(data['end_time']),
        user_id=user_id
    )
    db.session.add(new_event)
    db.session.commit()
    return jsonify({"message": "Event created successfully"}), 201

# Lấy tất cả sự kiện của user hiện tại
@events.route('/events', methods=['GET'])
@jwt_required()
def get_events():
    user_id = get_jwt_identity()
    events = Event.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "start_time": event.start_time,
        "end_time": event.end_time
    } for event in events])

# Update thông tin sự kiện
@events.route('/events/<int:event_id>', methods=['PUT'])
@jwt_required()
def update_event(event_id):
    user_id = get_jwt_identity()
    event = Event.query.filter_by(id=event_id, user_id=user_id).first()
    if not event:
        return jsonify({"message": "Event not found or unauthorized"}), 404

    data = request.get_json()
    event.title = data.get('title', event.title)
    event.description = data.get('description', event.description)
    event.start_time = datetime.fromisoformat(data.get('start_time', event.start_time.isoformat()))
    event.end_time = datetime.fromisoformat(data.get('end_time', event.end_time.isoformat()))

    db.session.commit()
    return jsonify({"message": "Event updated successfully"}), 200

# Xóa sự kiện
@events.route('/events/<int:event_id>', methods=['DELETE'])
@jwt_required()
def delete_event(event_id):
    user_id = get_jwt_identity()
    event = Event.query.filter_by(id=event_id, user_id=user_id).first()
    if not event:
        return jsonify({"message": "Event not found or unauthorized"}), 404

    db.session.delete(event)
    db.session.commit()
    return jsonify({"message": "Event deleted successfully"}), 200
