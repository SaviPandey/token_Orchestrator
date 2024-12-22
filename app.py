from flask import Flask, request, jsonify, abort
import uuid
import time
import random
from threading import Lock, Thread

app = Flask(__name__)

keys = {}
blocked_keys = {}
lock = Lock()

KEY_LIFETIME = 300
BLOCK_TIMEOUT = 60

def remove_expired_keys():
    while True:
        time.sleep(60)
        current_time = time.time()

        with lock:
            expired_keys = [
                key_id for key_id, key_data in keys.items()
                if current_time - key_data['created_at'] >= KEY_LIFETIME
            ]
            for key_id in expired_keys:
                blocked_keys.pop(key_id, None)
                del keys[key_id]

            expired_blocked = [
                key_id for key_id, blocked_at in blocked_keys.items()
                if current_time - blocked_at >= BLOCK_TIMEOUT
            ]
            for key_id in expired_blocked:
                blocked_keys.pop(key_id, None)
                if key_id in keys:
                    keys[key_id]['blocked_at'] = None

@app.route('/keys', methods=['POST'])
def create_key():
    key_id = str(uuid.uuid4())
    current_time = time.time()

    with lock:
        keys[key_id] = {'created_at': current_time, 'blocked_at': None}

    return jsonify({'key_id': key_id}), 201

@app.route('/keys', methods=['GET'])
def get_keys():
    with lock:
        available_keys = [
            key_id for key_id, key_data in keys.items()
            if key_id not in blocked_keys
        ]
        if not available_keys:
            abort(404, description="No available keys.")
        key_id = random.choice(available_keys)
        blocked_keys[key_id] = time.time()
        keys[key_id]['blocked_at'] = time.time()

    return jsonify({'key_id': key_id}), 200

@app.route('/keys/<key_id>', methods=['GET'])
def get_key_info(key_id):
    with lock:
        if key_id not in keys:
            abort(404, description="Key not found.")
        key_data = keys[key_id]
        return jsonify({
            'isBlocked': key_id in blocked_keys,
            'blockedAt': key_data['blocked_at'],
            'createdAt': key_data['created_at']
        }), 200

@app.route('/keys/<key_id>', methods=['DELETE'])
def delete_key(key_id):
    with lock:
        if key_id not in keys:
            abort(404, description="Key not found.")
        keys.pop(key_id, None)
        blocked_keys.pop(key_id, None)

    return '', 200

@app.route('/keys/<key_id>', methods=['PUT'])
def unblock_key(key_id):
    with lock:
        if key_id not in keys or key_id not in blocked_keys:
            abort(404, description="Key not found or not blocked.")
        blocked_keys.pop(key_id, None)
        keys[key_id]['blocked_at'] = None

    return '', 200

@app.route('/keepalive/<key_id>', methods=['PUT'])
def keep_alive(key_id):
    with lock:
        if key_id not in keys:
            abort(404, description="Key not found.")
        keys[key_id]['created_at'] = time.time()

    return '', 200

if __name__ == '__main__':
    cleanup_thread = Thread(target=remove_expired_keys, daemon=True)
    cleanup_thread.start()
    app.run(debug=True)
