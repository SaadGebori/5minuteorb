# 🚀 Railway Deployment Guide for OBR Trading Bot

Your bot is now ready for Railway! Follow these simple steps:

## 📋 Prerequisites
- ✅ Railway account (free plan works)
- ✅ GitHub account
- ✅ Your bot files (already prepared)

## 🔧 Step 1: Upload to GitHub

### Option A: GitHub Desktop (Easiest)
1. **Download GitHub Desktop**: https://desktop.github.com/
2. **Create new repository**: "tradingview-obr-bot"
3. **Add your files** to the repository folder
4. **Commit and publish** to GitHub

### Option B: Command Line
```bash
cd /mnt/c/Users/grend/tradingviewbot
git init
git add .
git commit -m "Initial OBR bot deployment"
git branch -M main
git remote add origin https://github.com/yourusername/tradingview-obr-bot.git
git push -u origin main
```

## 🚂 Step 2: Deploy to Railway

### 2.1 Connect Repository
1. **Go to**: https://railway.app/
2. **Click**: "Start a New Project"
3. **Select**: "Deploy from GitHub repo"
4. **Choose**: Your "tradingview-obr-bot" repository

### 2.2 Configure Environment Variables
In Railway dashboard, go to **Variables** tab and add:

```
TELEGRAM_BOT_TOKEN=7748694970:AAHSvW7QuVZR0OLc9Da720EgRCfpvmC9HWg
TELEGRAM_CHAT_ID=5542880189
CONFIDENCE_THRESHOLD=70
VOLUME_SPIKE_THRESHOLD=1.8
WATCHLIST=AMD
SCAN_INTERVAL=1
PYTHONUNBUFFERED=1
PORT=8080
```

### 2.3 Deploy Settings
- **Build Method**: Dockerfile (automatically detected)
- **Start Command**: `python obr.py` (automatically detected)
- **Framework**: Python
- **Auto-Deploy**: Enabled ✅

### 2.4 If Build Fails (Nixpacks Issue)
If you see "undefined variable 'pip'" error:
1. Go to **Settings** → **Build**
2. Change **Builder** from "Nixpacks" to "Dockerfile"
3. **Redeploy** the service

## 🎯 Step 3: Verify Deployment

### 3.1 Check Deployment Logs
1. **Go to**: Railway project dashboard
2. **Click**: "Deployments" tab
3. **View logs** for startup messages:
   ```
   🤖 AMD OBR Bot Starting...
   ✅ Telegram connection successful!
   🔄 Continuous scanning enabled (every 1 minute)
   🟢 Bot is running!
   ```

### 3.2 Test Telegram Connection
- You should receive startup message in Telegram
- Bot will scan AMD every minute during market hours

## 📊 Step 4: Monitor Your Bot

### Railway Dashboard Features:
- **📈 CPU/Memory usage**
- **📋 Real-time logs**
- **🔄 Auto-restart on crashes**
- **📱 Deployment notifications**

### Telegram Monitoring:
- **Startup/shutdown messages**
- **Live trading alerts**
- **Error notifications**

## 🛠️ Step 5: Customize Settings

### Change Scan Frequency:
In Railway Variables, modify:
```
SCAN_INTERVAL=1    # 1 minute (ultra-fast)
SCAN_INTERVAL=2    # 2 minutes (fast)
SCAN_INTERVAL=5    # 5 minutes (standard)
```

### Add More Stocks:
```
WATCHLIST=AMD,AAPL,TSLA,NVDA
```

### Adjust Sensitivity:
```
CONFIDENCE_THRESHOLD=60    # More alerts (was 70)
VOLUME_SPIKE_THRESHOLD=1.5 # More sensitive (was 1.8)
```

## 💰 Railway Pricing

### Free Plan (Perfect for this bot):
- ✅ **$5/month free credit**
- ✅ **512MB RAM** (bot uses ~50MB)
- ✅ **1GB storage** (bot uses ~10MB)
- ✅ **24/7 uptime**

### Cost Estimate:
- **This bot**: ~$0.50-1.00/month
- **Free credits**: Cover 5+ months

## 🔧 Troubleshooting

### Bot Not Starting:
1. **Check environment variables** (case sensitive)
2. **View deployment logs** for errors
3. **Verify Telegram token** is correct

### No Telegram Messages:
1. **Check chat ID** in variables
2. **Send /start** to your bot again
3. **Test connection** with health check

### High Memory Usage:
1. **Increase scan interval** to 5 minutes
2. **Monitor RAM usage** in Railway dashboard

## 🎉 Success Checklist

- ✅ Repository created and pushed to GitHub
- ✅ Railway project deployed successfully
- ✅ Environment variables configured
- ✅ Startup message received in Telegram
- ✅ Bot scanning every minute during market hours
- ✅ Health check endpoint responding
- ✅ Logs showing successful data fetching

## 📞 Support

If you encounter issues:
1. **Check Railway logs** for specific errors
2. **Verify all environment variables**
3. **Test locally first** with `python obr.py`
4. **Restart deployment** if needed

Your OBR bot is now running 24/7 on Railway! 🚀