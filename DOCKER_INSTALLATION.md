# 🐳 Docker Installation Guide for Windows

**Problem:** `Docker is not installed or not in PATH`

**Solution:** Install Docker Desktop for Windows

---

## 📥 Step 1: Download Docker Desktop

1. Visit: https://www.docker.com/products/docker-desktop
2. Click **"Download for Windows"**
3. Choose your Windows version:
   - **Windows 11/10 Pro/Enterprise:** Get the standard version
   - **Windows 11/10 Home:** Get the Home version

---

## 💾 Step 2: Install Docker

1. **Run the installer** you just downloaded
2. **Follow the installation wizard:**
   - Accept the license
   - Choose installation location
   - Keep default options
3. **Restart your computer** when prompted

---

## ✅ Step 3: Verify Installation

Open **Command Prompt (cmd.exe)** and run:

```bash
docker --version
```

Expected output:
```
Docker version 24.x.x, build xxxxx
```

If you see a version number, Docker is installed correctly! ✓

---

## 🚀 Step 4: Start Docker Desktop

1. **Open Docker Desktop application**
   - Search for "Docker" in Start menu
   - Click to launch
2. **Wait for it to start**
   - Look for the Docker whale icon in system tray
   - Wait until it says "Docker Desktop is running"

---

## ⚙️ Step 5: Enable Required Features (Windows 11/10 Home)

If you have Windows Home edition and get errors:

1. **Press `Win + R`** to open Run dialog
2. **Type:** `control.exe`
3. **Go to:** Programs → Programs and Features → Turn Windows features on or off
4. **Enable:**
   - ✓ Virtual Machine Platform
   - ✓ Windows Hypervisor Platform
5. **Restart your computer**

---

## 🔧 Step 6: Fix PATH Issues

If Docker still doesn't work after installation:

### Check if Docker is in PATH
```bash
# Open cmd.exe and try
where docker
```

If no result, Docker may not be in your PATH. Add it manually:

1. **Find Docker installation** (usually in `C:\Program Files\Docker`)
2. **Add to PATH:**
   - Open **Environment Variables:**
     - Right-click **This PC** or **My Computer**
     - Select **Properties**
     - Click **Advanced system settings**
     - Click **Environment Variables**
   - Under **System variables**, find **Path**
   - Click **Edit**
   - Add: `C:\Program Files\Docker\Docker\resources\bin`
   - Click **OK** and restart your terminal

---

## 🧪 Test Docker

After setup, verify everything works:

```bash
# Test 1: Check version
docker --version

# Test 2: Run test container
docker run hello-world

# Test 3: Check if running
docker ps
```

Expected for test 2:
```
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

---

## ✨ Start Qdrant

Once Docker is working, you can start Qdrant:

```bash
docker run -d -p 6333:6333 -p 6334:6334 --name qdrant qdrant/qdrant
```

Check it's running:
```bash
docker ps | findstr qdrant
```

---

## 🆘 Troubleshooting

### Docker command not found
```bash
# Solution: Restart your terminal/command prompt
# Docker may have been added to PATH after installation
```

### "Docker daemon is not running"
```bash
# Solution: Open Docker Desktop application
# Wait for it to fully start (whale icon in system tray)
```

### WSL 2 installation failed
```bash
# If you get this error, you need to:
# 1. Enable Hyper-V
# 2. Enable Virtual Machine Platform
# 3. Restart your computer
# (See Step 5 above)
```

### Port 6333 already in use
```bash
# Solution: Stop existing Qdrant
docker stop qdrant
docker rm qdrant

# Then try again
docker run -d -p 6333:6333 -p 6334:6334 --name qdrant qdrant/qdrant
```

---

## ✅ After Installation

Once Docker is working, run:

```bash
python setup_rag.py
```

This will automatically:
- ✓ Start Qdrant
- ✓ Initialize the database
- ✓ Generate embeddings
- ✓ Prepare everything for launch

---

## 📊 Docker Desktop Settings

After installing, check Docker Desktop settings:

1. **Open Docker Desktop**
2. **Click Settings (gear icon)**
3. **Ensure:**
   - ✓ Virtualization enabled
   - ✓ Memory: 4GB+ allocated
   - ✓ CPU: 2+ cores allocated
4. **Click Apply & Restart**

---

## 🔗 Alternative: Docker CLI

If you don't want Docker Desktop GUI, you can use Docker CLI:

1. Download: https://docs.docker.com/desktop/install/windows-install/
2. Install WSL 2 first
3. Use PowerShell/terminal for Docker commands

---

## 📝 Common Commands

```bash
# Start Docker daemon
docker daemon

# Check Docker status
docker info

# Stop Qdrant
docker stop qdrant

# Remove Qdrant
docker rm qdrant

# View all containers
docker ps -a

# View logs
docker logs qdrant

# Clean up unused images
docker system prune
```

---

## ✨ Now You're Ready!

Once Docker is installed and running:

```bash
# Navigate to project
cd "e:\GIAIC Q4 AGENTIC AI\PIAHR"

# Run setup
python setup_rag.py

# Follow the prompts!
```

---

**Docker Installation:** ✓ Complete  
**Next:** Run `python setup_rag.py`  
**Time:** 5 minutes to install Docker  
**Support:** https://www.docker.com/support
