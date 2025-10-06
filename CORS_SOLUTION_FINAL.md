# CORS Fix for Codespaces - Complete Solution

## Problem
Frontend at `https://friendly-engine-5gp65wxw4jprc7jgg-8080.app.github.dev` cannot access backend at `https://friendly-engine-5gp65wxw4jprc7jgg-8000.app.github.dev` due to CORS policy.

Error message:
```
Access to fetch at 'https://friendly-engine-5gp65wxw4jprc7jgg-8000.app.github.dev/token' 
from origin 'https://friendly-engine-5gp65wxw4jprc7jgg-8080.app.github.dev' 
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

## Root Causes
1. **Port Not Public**: Codespaces ports default to private (organization-only) visibility
2. **CORS Headers**: Backend needs to send proper CORS headers
3. **Port Registration Delay**: After making port public, it may take a moment to register

## Solutions Implemented

### 1. Updated CORS Middleware (main_enhanced.py)
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins - simplified configuration
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],
    max_age=3600,
)
```

### 2. Global Exception Handler
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

### 3. Made Ports Public
Created `make_ports_public.sh` script:
```bash
#!/bin/bash
gh codespace ports visibility 8000:public -c $CODESPACE_NAME
gh codespace ports visibility 8080:public -c $CODESPACE_NAME
```

## Manual Steps to Fix

### Option 1: Using VS Code UI
1. Open the **PORTS** tab in VS Code (bottom panel)
2. Find port **8000** in the list
3. Right-click on it → **Port Visibility** → **Public**
4. Repeat for port **8080** if needed
5. Refresh your browser

### Option 2: Using the Script
```bash
cd /workspaces/Personal-AI-Guidance-System
./make_ports_public.sh
```

### Option 3: Manual gh CLI
```bash
gh codespace ports visibility 8000:public -c friendly-engine-5gp65wxw4jprc7jgg
gh codespace ports visibility 8080:public -c friendly-engine-5gp65wxw4jprc7jgg
```

## Verification Steps

### 1. Check Port Visibility
In VS Code, open the PORTS tab and verify:
- Port 8000 shows "Public" visibility
- Port 8080 shows "Public" visibility

### 2. Test Backend Locally
```bash
curl http://localhost:8000/
# Should return: {"message":"Personal AI Guidance System API",...}
```

### 3. Test CORS Headers
```bash
curl -X OPTIONS "http://localhost:8000/token" \
  -H "Origin: https://friendly-engine-5gp65wxw4jprc7jgg-8080.app.github.dev" \
  -H "Access-Control-Request-Method: POST" \
  -i | grep -i access-control
```

Should see:
```
access-control-allow-origin: *
access-control-allow-credentials: true
access-control-allow-methods: *
access-control-allow-headers: *
```

### 4. Test Through Codespaces URL
After making port public, wait 30-60 seconds, then:
```bash
curl https://friendly-engine-5gp65wxw4jprc7jgg-8000.app.github.dev/
```

Should return the same JSON as localhost test.

## Troubleshooting

### Issue: Still getting CORS error
**Solution**: Clear browser cache and hard refresh (Ctrl+Shift+R or Cmd+Shift+R)

### Issue: 404 from Codespaces URL
**Solutions**:
1. Wait 30-60 seconds after making port public
2. Restart the backend server:
   ```bash
   pkill -f uvicorn
   cd /workspaces/Personal-AI-Guidance-System
   uvicorn main_enhanced:app --host 0.0.0.0 --port 8000 --reload
   ```
3. Check if port is actually public in PORTS tab

### Issue: Port keeps reverting to private
**Solution**: Set port to public each time you restart the Codespace, or add to `.devcontainer/devcontainer.json`:
```json
{
  "forwardPorts": [8000, 8080],
  "portsAttributes": {
    "8000": {
      "label": "Backend API",
      "onAutoForward": "notify",
      "visibility": "public"
    },
    "8080": {
      "label": "Frontend",
      "onAutoForward": "notify",
      "visibility": "public"
    }
  }
}
```

## Current Status

✅ CORS middleware configured with wildcard (`*`) origins
✅ Global exception handler ensures CORS on all responses  
✅ Backend running on port 8000 (PID: 11876)
✅ Frontend running on port 8080
⚠️ **ACTION REQUIRED**: Make port 8000 public using VS Code PORTS tab

## Next Steps

1. **Open PORTS tab** in VS Code (View → PORTS or bottom panel)
2. **Right-click port 8000** → Port Visibility → **Public**
3. **Wait 30 seconds** for port to register
4. **Refresh your browser** and try logging in again
5. If still not working, restart backend with `./start.sh`

## Your URLs
- **Frontend**: https://friendly-engine-5gp65wxw4jprc7jgg-8080.app.github.dev
- **Backend**: https://friendly-engine-5gp65wxw4jprc7jgg-8000.app.github.dev
- **API Docs**: https://friendly-engine-5gp65wxw4jprc7jgg-8000.app.github.dev/docs

