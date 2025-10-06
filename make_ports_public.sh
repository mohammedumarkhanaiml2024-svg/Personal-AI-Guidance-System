#!/bin/bash

echo "Making ports 8000 and 8080 public in Codespaces..."

# Use gh CLI to make ports public
gh codespace ports visibility 8000:public -c $CODESPACE_NAME 2>/dev/null
gh codespace ports visibility 8080:public -c $CODESPACE_NAME 2>/dev/null

echo ""
echo "Ports have been set to public!"
echo ""
echo "Your URLs:"
echo "Backend:  https://${CODESPACE_NAME}-8000.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}"
echo "Frontend: https://${CODESPACE_NAME}-8080.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}"
echo ""
echo "Please refresh your browser and try again."
