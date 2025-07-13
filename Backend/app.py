from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Basic configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['DEBUG'] = True

@app.route('/')
def home():
    """Home route to check if the bot is running"""
    return {
        "message": "Gramfinance WhatsApp Bot is running!",
        "status": "active",
        "version": "1.0.0"
    }

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Gramfinance WhatsApp Bot"
    }

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    """WhatsApp webhook endpoint"""
    if request.method == 'GET':
        # Webhook verification
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if mode == 'subscribe' and token == os.getenv('WEBHOOK_VERIFY_TOKEN', 'your-verify-token'):
            return challenge
        else:
            return 'Forbidden', 403
    
    elif request.method == 'POST':
        # Handle incoming WhatsApp messages
        data = request.get_json()
        
        # Log the incoming message
        print(f"Received webhook data: {data}")
        
        # Process the message
        try:
            # Extract message details
            if 'messages' in data.get('entry', [{}])[0].get('changes', [{}])[0].get('value', {}):
                messages = data['entry'][0]['changes'][0]['value']['messages']
                
                for message in messages:
                    from_number = message.get('from')
                    message_body = message.get('text', {}).get('body', '')
                    
                    print(f"Message from {from_number}: {message_body}")
                    
                    # Here you can add your business logic
                    # For now, just acknowledge receipt
                    
            return jsonify({"status": "ok"}), 200
            
        except Exception as e:
            print(f"Error processing webhook: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500

@app.route('/send-message', methods=['POST'])
def send_message():
    """Send a message via WhatsApp"""
    data = request.get_json()
    
    # Basic validation
    if not data or 'to' not in data or 'message' not in data:
        return jsonify({"error": "Missing required fields: 'to' and 'message'"}), 400
    
    # Here you would integrate with WhatsApp Business API
    # For now, just return success
    return jsonify({
        "status": "sent",
        "to": data['to'],
        "message": data['message']
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Get port from environment or use default
    port = int(os.getenv('PORT', 5000))
    
    print(f"Starting Gramfinance WhatsApp Bot on port {port}")
    print(f"Available endpoints:")
    print(f"  - Home: http://localhost:{port}/")
    print(f"  - Health: http://localhost:{port}/health")
    print(f"  - Webhook: http://localhost:{port}/webhook")
    print(f"  - Send Message: http://localhost:{port}/send-message")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=True
    )