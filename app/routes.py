from flask import Blueprint, jsonify, request

from app.services.ticket_service import validate_ticket_description

# Blueprint groups related routes together
main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def home():
    return jsonify({
        'application':'triq',
        'message':'AI workflow assistant is running..'
    })

@main_bp.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status':'healthy'
    }), 200

@main_bp.route('/api/tickets', methods=['POST'])
def create_ticket():
    ''' Accept and validate a new support ticket '''

    # Read the incoming JSON request body
    data = request.get_json(silent=True)

    # Reject requests that do not conatain a JSON object
    if not isinstance(data, dict):
        return jsonify({
            'error': 'A valid JSON object is required.'
        }), 400

    # Retrive the description and remove surrounding whitespaces
    description = data.get('description')

    # Delegate validation to the ticket service
    description, error = validate_ticket_description(description)

    # Return an error response if validation fails
    if error:
        return jsonify({
            'error': error
        }), 400

    

    # Return the validated ticket.
    # Database persistance is not implemented in this example.
    return jsonify({
        'message': 'Ticket received successfully.',
        'ticket': {
            'description': description,
        }
    }), 201

    

