#!/bin/bash

echo "=========================================="
echo "  Personal AI Guidance System - Status"
echo "=========================================="
echo ""

# Check if servers are running
echo "📊 Server Status:"
echo ""

BACKEND_PID=$(ps aux | grep "uvicorn main_enhanced:app" | grep -v grep | awk '{print $2}' | head -1)
FRONTEND_PID=$(ps aux | grep "python3 -m http.server 8080" | grep -v grep | awk '{print $2}' | head -1)

if [ -n "$BACKEND_PID" ]; then
    echo "✅ Backend:  Running (PID: $BACKEND_PID) on port 8000"
else
    echo "❌ Backend:  Not running"
fi

if [ -n "$FRONTEND_PID" ]; then
    echo "✅ Frontend: Running (PID: $FRONTEND_PID) on port 8080"
else
    echo "❌ Frontend: Not running"
fi

echo ""
echo "🌐 URLs:"
echo ""
echo "Frontend: https://${CODESPACE_NAME}-8080.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}/"
echo "Backend:  https://${CODESPACE_NAME}-8000.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}/"
echo "API Docs: https://${CODESPACE_NAME}-8000.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}/docs"
echo ""

# Test local connectivity
echo "🔧 Local Tests:"
echo ""

if curl -s http://localhost:8000/ > /dev/null 2>&1; then
    echo "✅ Backend responding on localhost:8000"
else
    echo "❌ Backend NOT responding on localhost:8000"
fi

if curl -s http://localhost:8080/ > /dev/null 2>&1; then
    echo "✅ Frontend responding on localhost:8080"
else
    echo "❌ Frontend NOT responding on localhost:8080"
fi

echo ""
echo "⚠️  IMPORTANT: Make Ports Public"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "If you see 404 errors in your browser:"
echo ""
echo "1. Open the PORTS tab in VS Code (bottom panel)"
echo "2. Right-click on port 8000 → Port Visibility → Public"
echo "3. Right-click on port 8080 → Port Visibility → Public"
echo "4. Wait 30 seconds, then refresh your browser"
echo ""
echo "See CORS_PUBLIC_PORTS.md for detailed instructions"
echo "=========================================="
