"""
TRUE Opening Range Breakout (ORB) Bot
- Opening Range: 9:30-10:30 AM EST (60 minutes)
- ORB Breakout: Price breaks above/below OR + retests
- PML/PMH: Previous Month breakout + retest
- Multi-timeframe: 5-minute bars, 1-minute scanning
"""

import pandas as pd
import numpy as np
import yfinance as yf
import telebot
import schedule
import time
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    ENV_LOADED = True
    print("✅ Local .env file loaded")
except ImportError:
    ENV_LOADED = False
    print("⚠️ python-dotenv not available, using system environment")

# ═══════════════════════════════════════════════════════════════════════════════════
# 🔧 CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════════

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '7748694970:AAHSvW7QuVZR0OLc9Da720EgRCfpvmC9HWg')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '5542880189')
WATCHLIST = os.getenv('WATCHLIST', 'TSLA,AMD,NVDA,PLTR,BABA').split(',') if os.getenv('WATCHLIST') else ['TSLA', 'AMD', 'NVDA', 'PLTR', 'BABA']

CONFIG = {
    'volume_threshold': float(os.getenv('VOLUME_THRESHOLD', '1.5')),
    'breakout_threshold': float(os.getenv('BREAKOUT_THRESHOLD', '0.1')),  # 0.1% breakout
    'retest_tolerance': float(os.getenv('RETEST_TOLERANCE', '0.5')),      # 0.5% retest zone
    'confidence_threshold': float(os.getenv('CONFIDENCE_THRESHOLD', '60')),
    'or_start_time': '09:30:00',
    'or_end_time': '10:30:00'
}

print(f"🔍 TRUE ORB Bot Configuration:")
print(f"   WATCHLIST: {WATCHLIST}")
print(f"   Opening Range: {CONFIG['or_start_time']} - {CONFIG['or_end_time']}")
print(f"   Breakout Threshold: {CONFIG['breakout_threshold']}%")
print(f"   Retest Tolerance: {CONFIG['retest_tolerance']}%")

# ═══════════════════════════════════════════════════════════════════════════════════
# 📈 DATA FETCHING
# ═══════════════════════════════════════════════════════════════════════════════════

def get_stock_data(symbol):
    """Fetch 5-minute stock data for ORB analysis"""
    try:
        print(f"📊 Fetching {symbol} 5-minute data...")
        ticker = yf.Ticker(symbol)
        
        # Get 5 days of 5-minute data
        data = ticker.history(period="5d", interval="5m")
        
        if data.empty:
            print(f"❌ No {symbol} data available")
            return None
        
        # Format columns
        data.columns = data.columns.str.lower()
        data = data[['open', 'high', 'low', 'close', 'volume']].copy()
        data = data.dropna()
        
        print(f"✅ Got {len(data)} {symbol} 5-minute bars")
        return data
        
    except Exception as e:
        print(f"❌ Error fetching {symbol} data: {str(e)}")
        return None

# ═══════════════════════════════════════════════════════════════════════════════════
# 🎯 TRUE ORB ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════════

def detect_opening_ranges(data):
    """Detect daily opening ranges (9:30-10:30 AM EST)"""
    opening_ranges = []
    
    # Ensure timezone-aware data
    if data.index.tz is None:
        data.index = data.index.tz_localize('America/New_York')
    else:
        data.index = data.index.tz_convert('America/New_York')
    
    # Group by date
    for date in data.index.date:
        day_data = data[data.index.date == date]
        
        if len(day_data) == 0:
            continue
        
        # Filter opening range (9:30-10:30 AM)
        or_start = pd.Timestamp(f"{date} {CONFIG['or_start_time']}", tz='America/New_York')
        or_end = pd.Timestamp(f"{date} {CONFIG['or_end_time']}", tz='America/New_York')
        
        or_data = day_data[(day_data.index >= or_start) & (day_data.index <= or_end)]
        
        if len(or_data) < 3:  # Need minimum bars for valid OR
            continue
        
        or_high = or_data['high'].max()
        or_low = or_data['low'].min()
        or_mid = (or_high + or_low) / 2
        or_range = or_high - or_low
        
        opening_ranges.append({
            'date': date,
            'or_high': or_high,
            'or_low': or_low,
            'or_mid': or_mid,
            'or_range': or_range,
            'or_start': or_start,
            'or_end': or_end,
            'bars_count': len(or_data)
        })
    
    return opening_ranges

def check_orb_breakout_retest(data, opening_range, current_price):
    """Check for ORB breakout + retest pattern"""
    
    or_high = opening_range['or_high']
    or_low = opening_range['or_low']
    or_end = opening_range['or_end']
    
    # Get data after opening range
    post_or_data = data[data.index > or_end]
    
    if len(post_or_data) < 3:
        return None
    
    # Calculate breakout thresholds
    bullish_breakout = or_high * (1 + CONFIG['breakout_threshold'] / 100)
    bearish_breakout = or_low * (1 - CONFIG['breakout_threshold'] / 100)
    
    # Calculate retest zones
    retest_tolerance = CONFIG['retest_tolerance'] / 100
    
    # Check for BULLISH ORB
    max_after_or = post_or_data['high'].max()
    if max_after_or > bullish_breakout:
        
        # Retest zone around OR High
        retest_top = or_high * (1 + retest_tolerance)
        retest_bottom = or_high * (1 - retest_tolerance)
        
        if retest_bottom <= current_price <= retest_top:
            return {
                'direction': 'bullish',
                'type': 'orb_breakout_retest',
                'or_level': or_high,
                'breakout_price': max_after_or,
                'current_price': current_price,
                'retest_zone_top': retest_top,
                'retest_zone_bottom': retest_bottom,
                'opening_range': opening_range
            }
    
    # Check for BEARISH ORB
    min_after_or = post_or_data['low'].min()
    if min_after_or < bearish_breakout:
        
        # Retest zone around OR Low
        retest_top = or_low * (1 + retest_tolerance)
        retest_bottom = or_low * (1 - retest_tolerance)
        
        if retest_bottom <= current_price <= retest_top:
            return {
                'direction': 'bearish',
                'type': 'orb_breakout_retest',
                'or_level': or_low,
                'breakout_price': min_after_or,
                'current_price': current_price,
                'retest_zone_top': retest_top,
                'retest_zone_bottom': retest_bottom,
                'opening_range': opening_range
            }
    
    return None

def check_monthly_breakout_retest(data, current_price):
    """Check for PML/PMH breakout + retest"""
    signals = []
    
    # Calculate monthly levels (last 30 trading days)
    monthly_data = data.tail(30 * 78)  # ~30 days * 78 bars/day
    pml = monthly_data['low'].min()
    pmh = monthly_data['high'].max()
    
    # Get recent data for breakout detection
    recent_data = data.tail(50)
    recent_high = recent_data['high'].max()
    recent_low = recent_data['low'].min()
    
    retest_tolerance = CONFIG['retest_tolerance'] / 100
    breakout_threshold = CONFIG['breakout_threshold'] / 100
    
    # PMH BREAKOUT + RETEST
    pmh_breakout = pmh * (1 + breakout_threshold)
    if recent_high > pmh_breakout:
        
        retest_top = pmh * (1 + retest_tolerance)
        retest_bottom = pmh * (1 - retest_tolerance)
        
        if retest_bottom <= current_price <= retest_top:
            signals.append({
                'direction': 'bullish',
                'type': 'pmh_breakout_retest',
                'monthly_level': pmh,
                'breakout_price': recent_high,
                'current_price': current_price,
                'retest_zone_top': retest_top,
                'retest_zone_bottom': retest_bottom
            })
    
    # PML BREAKOUT + RETEST
    pml_breakout = pml * (1 - breakout_threshold)
    if recent_low < pml_breakout:
        
        retest_top = pml * (1 + retest_tolerance)
        retest_bottom = pml * (1 - retest_tolerance)
        
        if retest_bottom <= current_price <= retest_top:
            signals.append({
                'direction': 'bearish',
                'type': 'pml_breakout_retest',
                'monthly_level': pml,
                'breakout_price': recent_low,
                'current_price': current_price,
                'retest_zone_top': retest_top,
                'retest_zone_bottom': retest_bottom
            })
    
    return signals, {'pml': pml, 'pmh': pmh}

def calculate_orb_confidence(data, signal):
    """Calculate ORB signal confidence"""
    confidence = 0
    
    # Get recent volume data
    recent_volume = data['volume'].tail(5).mean()
    avg_volume = data['volume'].tail(20).mean()
    volume_ratio = recent_volume / avg_volume if avg_volume > 0 else 1
    
    # Volume confirmation (40%)
    if volume_ratio >= 2.0:
        confidence += 40
    elif volume_ratio >= 1.5:
        confidence += 30
    elif volume_ratio >= 1.2:
        confidence += 20
    
    # Breakout strength (30%)
    if signal['type'] in ['orb_breakout_retest']:
        or_range = signal['opening_range']['or_range']
        breakout_distance = abs(signal['breakout_price'] - signal['or_level'])
        breakout_ratio = breakout_distance / or_range if or_range > 0 else 0
        
        if breakout_ratio >= 0.5:  # Breakout > 50% of OR range
            confidence += 30
        elif breakout_ratio >= 0.3:
            confidence += 20
        elif breakout_ratio >= 0.1:
            confidence += 10
    else:
        confidence += 25  # Monthly levels get base score
    
    # Retest precision (20%)
    retest_center = (signal['retest_zone_top'] + signal['retest_zone_bottom']) / 2
    distance_from_center = abs(signal['current_price'] - retest_center)
    retest_range = signal['retest_zone_top'] - signal['retest_zone_bottom']
    precision = 1 - (distance_from_center / (retest_range / 2)) if retest_range > 0 else 0
    
    confidence += int(precision * 20)
    
    # Time bonus (10%)
    current_hour = datetime.now().hour
    if 10 <= current_hour <= 12 or 14 <= current_hour <= 16:  # Best ORB times
        confidence += 10
    elif 9 <= current_hour <= 16:
        confidence += 5
    
    return min(confidence, 100)

def analyze_stock_orb(data, symbol):
    """Main TRUE ORB analysis function"""
    
    # Detect opening ranges
    opening_ranges = detect_opening_ranges(data)
    
    if not opening_ranges:
        return {
            'signals': [],
            'opening_ranges': [],
            'current_price': data['close'].iloc[-1],
            'monthly_levels': {'pml': None, 'pmh': None}
        }
    
    # Get most recent opening range
    latest_or = opening_ranges[-1]
    current_price = data['close'].iloc[-1]
    
    signals = []
    
    # Check ORB breakout + retest
    orb_signal = check_orb_breakout_retest(data, latest_or, current_price)
    if orb_signal:
        confidence = calculate_orb_confidence(data, orb_signal)
        orb_signal['confidence'] = confidence
        if confidence >= CONFIG['confidence_threshold']:
            signals.append(orb_signal)
    
    # Check monthly breakout + retest
    monthly_signals, monthly_levels = check_monthly_breakout_retest(data, current_price)
    for signal in monthly_signals:
        confidence = calculate_orb_confidence(data, signal)
        signal['confidence'] = confidence
        if confidence >= CONFIG['confidence_threshold']:
            signals.append(signal)
    
    return {
        'signals': signals,
        'opening_ranges': opening_ranges,
        'current_price': current_price,
        'monthly_levels': monthly_levels
    }

# ═══════════════════════════════════════════════════════════════════════════════════
# 📱 TELEGRAM ALERTS
# ═══════════════════════════════════════════════════════════════════════════════════

def send_telegram_alert(message):
    """Send alert to Telegram"""
    try:
        bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
        bot.send_message(TELEGRAM_CHAT_ID, message, parse_mode='HTML')
        print(f"✅ Alert sent successfully")
        return True
    except Exception as e:
        print(f"❌ Telegram error: {str(e)}")
        return False

def format_orb_alert(signal, monthly_levels, symbol):
    """Format TRUE ORB alert message"""
    
    icons = {
        'orb_breakout_retest': '🎯',
        'pmh_breakout_retest': '📈',
        'pml_breakout_retest': '📉'
    }
    
    titles = {
        'orb_breakout_retest': 'ORB BREAKOUT RETEST',
        'pmh_breakout_retest': 'PMH BREAKOUT RETEST',
        'pml_breakout_retest': 'PML BREAKOUT RETEST'
    }
    
    actions = {
        'bullish': 'LONG ENTRY',
        'bearish': 'SHORT ENTRY'
    }
    
    icon = icons.get(signal['type'], '⚡')
    title = titles.get(signal['type'], 'ORB SIGNAL')
    action = actions.get(signal['direction'], 'ENTRY')
    direction_icon = '🟢' if signal['direction'] == 'bullish' else '🔴'
    
    if signal['type'] == 'orb_breakout_retest':
        or_info = signal['opening_range']
        message = f"""<b>{direction_icon} {title}</b>

📊 <b>{symbol}</b> | ${signal['current_price']:.2f}
🎯 <b>OR Level:</b> ${signal['or_level']:.2f}
📦 <b>OR Range:</b> ${or_info['or_low']:.2f} - ${or_info['or_high']:.2f}
💥 <b>Breakout:</b> ${signal['breakout_price']:.2f}
🔥 <b>Confidence:</b> {signal['confidence']}/100
📈 <b>Retest Zone:</b> ${signal['retest_zone_bottom']:.2f} - ${signal['retest_zone_top']:.2f}

📍 <b>Monthly Levels:</b>
PMH: ${monthly_levels['pmh']:.2f}
PML: ${monthly_levels['pml']:.2f}

⏰ {datetime.now().strftime('%H:%M:%S EST')}
🚀 <b>ACTION: {action}</b>"""
    
    else:  # Monthly level breakout
        level_name = 'PMH' if signal['type'] == 'pmh_breakout_retest' else 'PML'
        message = f"""<b>{direction_icon} {title}</b>

📊 <b>{symbol}</b> | ${signal['current_price']:.2f}
🎯 <b>{level_name} Level:</b> ${signal['monthly_level']:.2f}
💥 <b>Breakout:</b> ${signal['breakout_price']:.2f}
🔥 <b>Confidence:</b> {signal['confidence']}/100
📈 <b>Retest Zone:</b> ${signal['retest_zone_bottom']:.2f} - ${signal['retest_zone_top']:.2f}

📍 <b>Monthly Levels:</b>
PMH: ${monthly_levels['pmh']:.2f}
PML: ${monthly_levels['pml']:.2f}

⏰ {datetime.now().strftime('%H:%M:%S EST')}
🚀 <b>ACTION: {action}</b>"""
    
    return message

# ═══════════════════════════════════════════════════════════════════════════════════
# 🔄 MAIN SCANNING LOOP
# ═══════════════════════════════════════════════════════════════════════════════════

def scan_stocks():
    """Main TRUE ORB scanning function"""
    print(f"\n🎯 TRUE ORB Scan at {datetime.now().strftime('%H:%M:%S')}")
    
    for symbol in WATCHLIST:
        try:
            # Get data
            data = get_stock_data(symbol)
            if data is None:
                continue
            
            # Analyze TRUE ORB
            analysis = analyze_stock_orb(data, symbol)
            
            # Check for high-confidence signals
            if analysis['signals']:
                for signal in analysis['signals']:
                    alert_message = format_orb_alert(signal, analysis['monthly_levels'], symbol)
                    send_telegram_alert(alert_message)
                    print(f"🚨 {symbol} TRUE ORB ALERT: {signal['type']} - {signal['confidence']}/100")
            else:
                or_count = len(analysis['opening_ranges'])
                print(f"✅ {symbol}: ${analysis['current_price']:.2f} | OR Count: {or_count} | No signals")
        
        except Exception as e:
            print(f"❌ Error scanning {symbol}: {str(e)}")
            continue

def main():
    """Main execution function"""
    print("🎯 TRUE ORB Bot Starting...")
    print("=" * 50)
    
    # Test Telegram connection
    try:
        startup_msg = f"""🔥 <b>HELLO TRASASASA WE ARE LIVE AND ON FIRE!</b> 🔥

💰 <b>LET'S EARN SOME MILLIONS!</b> 💰

🎯 <b>TRUE Opening Range Breakout Bot Started</b>

📈 <b>Symbols:</b> {', '.join(WATCHLIST)}
⏰ <b>Opening Range:</b> {CONFIG['or_start_time']} - {CONFIG['or_end_time']} EST
🎯 <b>Strategy:</b> ORB Breakout + Retest + PML/PMH
🔥 <b>Min Confidence:</b> {CONFIG['confidence_threshold']}/100
⚡ <b>Scan Frequency:</b> Every 1 minute

<b>TRASASASA - TRUE ORB READY!</b> 🚀💎"""
        
        if send_telegram_alert(startup_msg):
            print("✅ Telegram connection successful!")
        else:
            print("❌ Telegram connection failed!")
            return
    except Exception as e:
        print(f"❌ Telegram setup error: {str(e)}")
        return
    
    # Run immediate scan
    scan_stocks()
    
    print("\n🟢 TRUE ORB Bot is running! Press Ctrl+C to stop.")
    
    # Continuous scanning every minute
    try:
        while True:
            current_hour = datetime.now().hour
            current_weekday = datetime.now().weekday()
            
            # Only scan during market hours (9:30 AM - 4:00 PM EST, Mon-Fri)
            if (current_weekday < 5 and  # Monday = 0, Friday = 4
                ((current_hour == 9 and datetime.now().minute >= 30) or 
                 (10 <= current_hour <= 15) or 
                 (current_hour == 16 and datetime.now().minute == 0))):
                scan_stocks()
            
            time.sleep(60)  # Wait 1 minute
    except KeyboardInterrupt:
        print("\n🛑 TRUE ORB Bot stopped by user.")
        send_telegram_alert("🛑 <b>TRASASASA - TRUE ORB Bot Stopped</b>\n\nBot has been manually stopped.")

if __name__ == "__main__":
    main()