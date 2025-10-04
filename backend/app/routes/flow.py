from flask import Blueprint, jsonify, request
from ..services.llm_service import LLMService

flow_bp = Blueprint('flow', __name__)

@flow_bp.route('/flow/test', methods=['GET'])
def test_flow_endpoint():
    """Test endpoint for flow routes"""
    return jsonify({
        'message': 'Flow endpoint is working!',
        'status': 'success',
        'endpoint': '/api/flow/test'
    })

@flow_bp.route('/flow/generate', methods=['POST'])
def generate_flow():
    """Generate a yoga flow using LLM"""
    try:
        # Get request data
        data = request.get_json() or {}
        #print(data)
        
        # Validate required fields
        if not data.get('routineName') or not data.get('timeLength') or not data.get('description'):
            return jsonify({
                'success': False,
                'message': 'Missing required fields',
                'errors': ['routineName, timeLength, and description are required']
            }), 400
        
        # Initialize LLM service
        llm_service = LLMService()
        
        # Generate the flow
        result = llm_service.generate_yoga_flow(data)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Flow generated successfully!',
                'flow_description': result['flow_description'],
                'flow_sequence': result['flow_sequence'],
                'routine_name': data.get('routineName'),
                'duration': data.get('timeLength')
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to generate flow',
                'error': result.get('error', 'Unknown error')
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error processing request',
            'error': str(e)
        }), 500
