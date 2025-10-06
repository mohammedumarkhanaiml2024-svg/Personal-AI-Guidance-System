# How to Make Ports Public in VS Code Codespaces

## The Problem
You're seeing: `HTTP ERROR 404` or `This page can't be found` when accessing:
- https://friendly-engine-5gp65wxw4jprc7jgg-8080.app.github.dev/
- https://friendly-engine-5gp65wxw4jprc7jgg-8000.app.github.dev/

## The Cause
**Codespaces ports are private by default!** They need to be manually set to "Public" visibility.

## ✅ Solution: Make Ports Public (3 Easy Steps)

### Step 1: Open the PORTS Panel
1. Look at the **bottom panel** of VS Code
2. Click on the **"PORTS"** tab (next to TERMINAL, PROBLEMS, OUTPUT)
   - If you don't see it, go to: **View** → **Ports** from the top menu

### Step 2: Find Your Ports
You should see a list that includes:
```
PORT    | ADDRESS           | VISIBILITY
8000    | localhost:8000    | Private
8080    | localhost:8080    | Private
```

### Step 3: Change to Public (Do this for BOTH ports)

**For Port 8000:**
1. **Right-click** on the row with port `8000`
2. Hover over **"Port Visibility"**
3. Click **"Public"**
4. The visibility should change to `Public` ✅

**For Port 8080:**
1. **Right-click** on the row with port `8080`
2. Hover over **"Port Visibility"**
3. Click **"Public"**
4. The visibility should change to `Public` ✅

### Step 4: Wait and Test
1. **Wait 30-60 seconds** for the changes to take effect
2. **Refresh your browser** (or hard refresh with Ctrl+Shift+R / Cmd+Shift+R)
3. Try accessing the URLs again

## Alternative Method: Using Port Actions

In the PORTS panel, you can also:
1. Click the **🌐 globe icon** next to the port number
2. This will show you the public URL and automatically set it to public

## Verify It's Working

After making ports public, test locally first:
```bash
# Test backend
curl http://localhost:8000/

# Test frontend
curl http://localhost:8080/ | head -10
```

Both should return content without errors.

## Current Server Status

✅ Backend is running on port 8000 (PID: 11878)
✅ Frontend is running on port 8080 (PID: 4926)
⚠️ **ACTION NEEDED**: Make ports public using steps above

## Your URLs (Will Work After Making Ports Public)

**Frontend (Main App):**
```
https://friendly-engine-5gp65wxw4jprc7jgg-8080.app.github.dev/
```

**Backend API:**
```
https://friendly-engine-5gp65wxw4jprc7jgg-8000.app.github.dev/
```

**API Documentation:**
```
https://friendly-engine-5gp65wxw4jprc7jgg-8000.app.github.dev/docs
```

## Common Issues

### Issue: "I don't see the PORTS tab"
**Solution**: Go to **View** → **Ports** from the top menu bar

### Issue: "Port visibility keeps reverting to Private"
**Solution**: This happens when Codespace restarts. You need to set it public each time, OR add this to `.devcontainer/devcontainer.json`:
```json
{
  "forwardPorts": [8000, 8080],
  "portsAttributes": {
    "8000": {"visibility": "public"},
    "8080": {"visibility": "public"}
  }
}
```

### Issue: "Still getting 404 after making public"
**Solutions**:
1. Wait another 30 seconds
2. Hard refresh browser (Ctrl+Shift+R)
3. Clear browser cache
4. Try in an incognito/private window

## Screenshot Reference

When you open the PORTS tab, you should see something like:

```
┌────────┬───────────────────┬─────────────┬──────────────────────────────────────┐
│ PORT   │ ADDRESS           │ VISIBILITY  │ FORWARDED ADDRESS                    │
├────────┼───────────────────┼─────────────┼──────────────────────────────────────┤
│ 8000   │ localhost:8000    │ Private     │ https://...-8000.app.github.dev      │
│ 8080   │ localhost:8080    │ Private     │ https://...-8080.app.github.dev      │
└────────┴───────────────────┴─────────────┴──────────────────────────────────────┘
```

Right-click on each port → Port Visibility → Public

After changing, it should show:
```
┌────────┬───────────────────┬─────────────┬──────────────────────────────────────┐
│ PORT   │ ADDRESS           │ VISIBILITY  │ FORWARDED ADDRESS                    │
├────────┼───────────────────┼─────────────┼──────────────────────────────────────┤
│ 8000   │ localhost:8000    │ Public ✅   │ https://...-8000.app.github.dev      │
│ 8080   │ localhost:8080    │ Public ✅   │ https://...-8080.app.github.dev      │
└────────┴───────────────────┴─────────────┴──────────────────────────────────────┘
```

---

**Once you've made the ports public, your application will be accessible from anywhere!** 🚀
