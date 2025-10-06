# Brain CORS Error - Root Cause and Fix

## Problem Summary
The brain page (`brain.html`) was showing CORS policy errors when trying to fetch data from `/brain/summary` endpoint.

## Root Cause Analysis

### Primary Issue: Corrupted Brain JSON File
- **Error**: `json.decoder.JSONDecodeError: Expecting value: line 10 column 17 (char 246)`
- **Location**: `brain_service.py` line 32 in `get_user_brain()` method
- **Cause**: The file `user_brains/user_5_brain.json` was truncated/corrupted
- **Impact**: Backend returned 500 Internal Server Error

### Secondary Issue: CORS Headers on Errors
- **Problem**: FastAPI doesn't add CORS middleware headers when unhandled exceptions occur
- **Effect**: Frontend received error response without CORS headers, triggering browser CORS policy block
- **Symptom**: Browser showed "CORS policy: No 'Access-Control-Allow-Origin' header"

## Solutions Implemented

### 1. Added Error Handling in brain_service.py
**File**: `brain_service.py`

Added try-catch block to handle corrupted brain files:
```python
if os.path.exists(brain_path):
    try:
        with open(brain_path, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        # If brain file is corrupted, backup and create new one
        print(f"Warning: Corrupted brain file for user {user_id}: {e}")
        backup_path = f"{brain_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        try:
            os.rename(brain_path, backup_path)
            print(f"Backed up corrupted brain to: {backup_path}")
        except Exception as backup_error:
            print(f"Could not backup corrupted brain: {backup_error}")
        # Fall through to create new brain
```

**Benefits**:
- Automatically detects corrupted JSON files
- Creates timestamped backup of corrupted file
- Generates fresh brain file for user
- Prevents 500 errors from crashing the API

### 2. Added Global Exception Handler in main_enhanced.py
**File**: `main_enhanced.py`

Added global exception handler to ensure CORS headers on all responses:
```python
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Ensure CORS headers are sent even on unhandled exceptions"""
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, PATCH",
            "Access-Control-Allow-Headers": "*",
        }
    )
```

**Benefits**:
- Ensures CORS headers are sent even when exceptions occur
- Provides meaningful error messages to frontend
- Prevents browser CORS policy blocks on error responses

## Verification

### Testing CORS Headers
```bash
# Test preflight (OPTIONS request)
curl -X OPTIONS "http://localhost:8000/brain/summary" \
  -H "Origin: https://friendly-engine-5gp65wxw4jprc7jgg-8080.app.github.dev" \
  -H "Access-Control-Request-Method: GET" \
  -H "Access-Control-Request-Headers: authorization" -v

# Expected headers:
# access-control-allow-origin: https://friendly-engine-5gp65wxw4jprc7jgg-8080.app.github.dev
# access-control-allow-methods: GET, POST, PUT, DELETE, OPTIONS, PATCH
# access-control-allow-credentials: true
# access-control-allow-headers: authorization

# Test actual GET request
curl -X GET "http://localhost:8000/brain/summary" \
  -H "Origin: https://friendly-engine-5gp65wxw4jprc7jgg-8080.app.github.dev" \
  -H "Authorization: Bearer YOUR_TOKEN" -v

# Expected headers:
# access-control-allow-origin: *
# access-control-allow-credentials: true
# access-control-expose-headers: *
```

### Testing Brain Endpoint
```bash
# Register user
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'

# Login and get token
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass123"

# Test brain summary
curl -X GET "http://localhost:8000/brain/summary" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Expected response:
# {
#   "user_id": 13,
#   "data_points": 0,
#   "habits_tracked": 0,
#   "conversations": 0,
#   "active_goals": 0,
#   "achievements": 0,
#   "challenges": 0,
#   "last_updated": "2025-10-02T07:44:59.573073",
#   "behavior_insights": {}
# }
```

## Current Status
✅ **FIXED** - Brain service handles corrupted JSON files gracefully
✅ **FIXED** - CORS headers sent on all responses including errors
✅ **VERIFIED** - Brain endpoint returns proper JSON with CORS headers
✅ **VERIFIED** - New brain files created automatically for users

## Files Modified
1. `brain_service.py` - Added error handling for corrupted brain files
2. `main_enhanced.py` - Added global exception handler with CORS headers

## Backend Server Info
- **PID**: 75698
- **Port**: 8000
- **Endpoint**: http://localhost:8000 or https://CODESPACE_URL-8000.app.github.dev
- **Status**: Running with auto-reload enabled

## Next Steps
1. Users with corrupted brain files will automatically get fresh ones on first access
2. Corrupted files are backed up with timestamps for recovery if needed
3. All API endpoints now send proper CORS headers even on errors
4. Frontend `brain.html` should now work without CORS errors
