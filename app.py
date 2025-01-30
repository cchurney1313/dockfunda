from flask import Flask, request, jsonify
import redis
import json
import os




app = Flask(__name__)

host_name = os.environ.get("netname","localhost")
print("**** Network is:", host_name)
# Connect to Redis
redis_client = redis.Redis(host=host_name, port=6379, db=0)

@app.route('/')
def home():
    return jsonify({"1. help": "",
      "2. routes available" : "/add_user?email=xxxxx&name=xxxxx",
      "3." : "/get_emails",
      "4." : "/search?email=",
      "5." : "/populate"
      })

@app.route('/add_user', methods=['GET'])
def add_user():
    email = request.args.get('email')
    name = request.args.get('name')

    if not email or not name:
        return jsonify({"error": "Email and name are required"}), 400
    
    redis_client.set(f'user:{email}', name)
    return jsonify({"message": "User added successfully"}), 201

@app.route('/get_emails', methods=['GET'])
@app.route('/g', methods=['GET'])
def get_emails():
    cursor = '0'
    emails = []
    while cursor != 0:
        cursor, keys = redis_client.scan(cursor=cursor, match='user:*', count=100)
        for key in keys:
            email = key.decode('utf-8').split(':', 1)[1]  # Remove 'user:' prefix
            name = redis_client.get(key).decode('utf-8')
            emails.append({"email": email, "name": name})
    
    return jsonify({"users": emails})


@app.route('/search', methods=['GET'])
def search():
    email = request.args.get('email')
    
    if not email:
        return jsonify({"error": "Email parameter is required"}), 400
    
    # Construct the key
    key = f'user:{email}'
    
    # Fetch the value (name) for the given key (email)
    name = redis_client.get(key)
    
    if name:
        return jsonify({"email": email, "name": name.decode('utf-8')})
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/emailbegins', methods=['GET'])
def emailbegins():
    email_prefix = request.args.get('email')
    
    if not email_prefix:
        return jsonify({"error": "Email prefix parameter is required"}), 400
    
    matching_users = []
    cursor = '0'
    while cursor != 0:
        cursor, keys = redis_client.scan(cursor=cursor, match=f'user:{email_prefix}*', count=100)
        for key in keys:
            email = key.decode('utf-8').split(':', 1)[1]  # Remove 'user:' prefix
            name = redis_client.get(key).decode('utf-8')
            matching_users.append({"email": email, "name": name})
    
    if matching_users:
        return jsonify({"users": matching_users})
    else:
        return jsonify({"error": "No users found"}), 404

@app.route('/populate', methods=['GET'])
@app.route('/p', methods=['GET'])
def populate():
    users = [
        ("john@example.com", "John Smith"),
        ("jane@example.com", "Jane Smith"),
        ("chei@example.com", "Chei Tan")
    ]

    # Add each email-name pair to Redis
    for email, name in users:
        key = f"user:{email}"
        redis_client.set(key, name)
        print(f"Added: {key} -> {name}")    
    
    return jsonify({"message": "Populated, check with /get_emails"}), 201

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
