from flask import Blueprint, jsonify, request, render_template, current_app

from app.services.ticket_service import validate_ticket_description
from app.services.ticket_analyzer import analyze_ticket
from app.services.ai_ticket_analyzer import analyze_ticket_with_ai, AIAnalysisError

# Blueprint groups related routes together
main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@main_bp.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status':'ok'
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
    # If the AI service is unavailable, use the rules-based service

    ai_provider = current_app.config.get('AI_PROVIDER', 'mock')

    if ai_provider == 'ollama':
        try:
            analysis = analyze_ticket_with_ai(description)
            analysis_source = 'ai'
    
        except AIAnalysisError as error:
            current_app.logger.warning('AI analysis failed, falling back to rules-based analysis. Reason: %s', error)
            analysis = analyze_ticket(description)
            analysis_source = 'rules'
            
    elif ai_provider == 'mock':
        analysis = analyze_ticket(description)
        analysis_source = 'rules'

    else:
        return jsonify({
            'error': 'The configured AI provider is not supported.'
        }), 500

    # Return the validated ticket.
    # Database persistence is not implemented in this example.
    return jsonify({
        'message': 'Ticket analyzed successfully.',
        'ticket': {
            'description': description,
        },
        'analysis_source': analysis_source,
        'analysis': analysis
    }), 201

    

