# API Key Management Server 🚀

A scalable Flask-based API key management server that provides efficient operations for generating, assigning, blocking, and managing API keys. The server ensures key lifecycle management with automated expiration and blocking mechanisms.

## Features 🌟
- **Key Generation**: Create new unique API keys with a 5-minute lifetime.
- **Retrieve Available Keys**: Fetch a random, unblocked key. Automatically blocks the key for exclusive use.
- **Key Unblocking**: Unblock a previously blocked key for reuse.
- **Key Deletion**: Permanently delete a key.
- **Keep-Alive Functionality**: Extend a key’s lifetime by signaling every 5 minutes.
- **Automated Expiration**: Automatically deletes keys after their lifetime or releases blocked keys after 60 seconds.

## Requirements 🛠️
- Python 3.8+
- Flask

## Installation 📥
1. Clone the repository:
   
2. Install dependencies:
   ```bash
   pip install flask
   ```

3. Run the server:
   ```bash
   python app.py
   ```

## API Endpoints 🌐

### 1. Create Key 🆕
**POST /keys**
- Generates a new unique key with a 5-minute lifetime.
- **Response**:
  ```json
  {
    "key_id": "<uuid>"
  }
  ```

### 2. Retrieve Key 🎯
**GET /keys**
- Fetches a random, unblocked key and marks it as blocked.
- **Response**:
  ```json
  {
    "key_id": "<uuid>"
  }
  ```
- **Error**: Returns 404 if no keys are available.

### 3. Unblock Key 🔓
**PUT /keys/<key_id>**
- Unblocks a specific key, making it available again.
- **Response**: `200 OK`
- **Error**: Returns 404 if the key is not found or not blocked.

### 4. Delete Key 🗑️
**DELETE /keys/<key_id>**
- Permanently deletes a specific key.
- **Response**: `200 OK`
- **Error**: Returns 404 if the key is not found.

### 5. Keep Key Alive 🔄
**PUT /keepalive/<key_id>**
- Extends the lifetime of a specific key by resetting its creation time.
- **Response**: `200 OK`
- **Error**: Returns 404 if the key is not found.

## Architecture 🏗️
- **Data Structures**:
  - Hash map for quick key lookups.
  - Priority queue for efficient expiration management.
  - Hash map for tracking blocked keys.
- **Thread-Safe Operations**: Ensures consistent data manipulation with threading locks.

## How It Works ⚙️
1. Keys are stored with creation and last keep-alive timestamps.
2. Background thread handles automatic cleanup of expired and blocked keys.
3. API endpoints provide efficient O(1) or O(log n) operations for managing keys.

## License 📜
This project is licensed under the MIT License.

## Author ✍️
**Savinay Pandey**  
[GitHub](https://github.com/SaviPandey)
