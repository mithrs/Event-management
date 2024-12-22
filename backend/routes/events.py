from flask import Blueprint, request, jsonify
from models.event import Event, db
from flask import render_template

event_blueprint = Blueprint('events', __name__)

@event_blueprint.route('/', methods=['POST'])
def create_event():
    data = request.json
    event = Event(name=data['name'], description=data.get('description'), location=data.get('location'), date=data['date'])
    db.session.add(event)
    db.session.commit()
    return jsonify({"message": "Event created", "event": data}), 201

@event_blueprint.route('/', methods=['GET'])
def get_events():
    events = Event.query.all()
    result = [
        {"id": e.id, "name": e.name, "description": e.description, "location": e.location, "date": str(e.date)}
        for e in events
    ]
    return jsonify(result)

@event_blueprint.route('/page', methods=['GET'])
def events_page():
    return render_template('index.html')

@event_blueprint.route('/<int:id>', methods=['PUT'])
def update_event(id):
    data = request.json
    event = Event.query.get(id)
    if not event:
        return jsonify({"message": "Event not found"}), 404

    event.name = data.get('name', event.name)
    event.description = data.get('description', event.description)
    event.location = data.get('location', event.location)
    event.date = data.get('date', event.date)

    db.session.commit()
    return jsonify({"message": "Event updated", "event": data})

@event_blueprint.route('/<int:id>', methods=['DELETE'])
def delete_event(id):
    event = Event.query.get(id)
    if not event:
        return jsonify({"message": "Event not found"}), 404

    db.session.delete(event)
    db.session.commit()
    return jsonify({"message": "Event deleted"})

