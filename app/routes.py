from flask import Blueprint, jsonify, request, render_template

from app.services.ticket_service import validate_ticket_description
from app.services.ticket_analyzer import analyze_ticket

# Blueprint groups related routes together
main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def home():
    return render_template('index.html')

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


    # Analyze the ticket description using the AI service
    analysis = analyze_ticket(description)

    # Return the validated ticket.
    # Database persistance is not implemented in this example.
    return jsonify({
        'message': 'Ticket analyzed successfully.',
        'ticket': {
            'description': description,
        },
        'analysis': analysis
    }), 201

    

