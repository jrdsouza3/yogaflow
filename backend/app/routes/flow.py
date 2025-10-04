from flask import Blueprint, jsonify, request

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
    """Placeholder for flow generation endpoint"""
    try:
        # Get request data (will be used later)
        data = request.get_json() or {}
        
        return jsonify({
            'message': 'Flow generation endpoint ready!',
            'status': 'success',
            'received_data': data,
            'note': 'This is a placeholder - actual flow generation coming soon!'
        })
    except Exception as e:
        return jsonify({
            'message': 'Error processing request',
            'status': 'error',
            'error': str(e)
        }), 400
