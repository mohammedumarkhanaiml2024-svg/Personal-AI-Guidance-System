#!/bin/bash

echo "🔧 FIXING CORS ERROR - Making Port 8000 Public"
echo "================================================="
echo ""

# Try to make port 8000 public using gh CLI
echo "📡 Attempting to make port 8000 public..."
if command -v gh &> /dev/null; then
    gh codespace ports visibility 8000:public -c "$CODESPACE_NAME" 2>/dev/null && echo "✅ Port 8000 set to public via gh CLI" || echo "⚠️  gh CLI method failed"
else
    echo "⚠️  gh CLI not available"
fi

echo ""
echo "🎯 MANUAL STEPS REQUIRED:"
echo "========================="
echo ""
echo "Since the gh CLI method may not work, you need to manually make port 8000 public:"
echo ""
echo "1. Look at the BOTTOM of VS Code - find the PORTS tab"
echo "2. Click on PORTS (next to TERMINAL, PROBLEMS, OUTPUT)"
echo "3. Find port 8000 in the list"
echo "4. RIGHT-CLICK on port 8000"
echo "5. Hover over 'Port Visibility'"
echo "6. Click 'Public' ✅"
echo ""
echo "Current port test results:"
echo ""

# Test local access
if curl -s http://localhost:8000/ > /dev/null 2>&1; then
    echo "✅ Backend responding locally on port 8000"
else
    echo "❌ Backend NOT responding locally"
fi

# Test external access
echo "🌐 Testing external access..."
RESPONSE=$(curl -s -w "%{http_code}" -o /dev/null --max-time 5 "https://friendly-engine-5gp65wxw4jprc7jgg-8000.app.github.dev/" 2>/dev/null)

if [ "$RESPONSE" = "200" ]; then
    echo "✅ Port 8000 is PUBLIC and accessible"
elif [ "$RESPONSE" = "401" ]; then
    echo "❌ Port 8000 is PRIVATE (401 Unauthorized) - NEEDS TO BE MADE PUBLIC"
elif [ "$RESPONSE" = "404" ]; then
    echo "❌ Port 8000 not found (404) - Check if backend is running"
else
    echo "❌ Port 8000 not accessible (Response: $RESPONSE)"
fi

echo ""
echo "🔍 Your URLs:"
echo "Frontend: https://friendly-engine-5gp65wxw4jprc7jgg-8080.app.github.dev/"
echo "Backend:  https://friendly-engine-5gp65wxw4jprc7jgg-8000.app.github.dev/"
echo ""
echo "After making port 8000 public:"
echo "1. Wait 30 seconds"
echo "2. Hard refresh your browser (Ctrl+Shift+R or Cmd+Shift+R)"
echo "3. Try registering/logging in again"
echo ""
echo "================================================="
