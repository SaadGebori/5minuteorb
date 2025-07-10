# 📊 TRUE Opening Range Breakout (ORB) Strategy

## 🎯 **What is ORB?**

**Opening Range Breakout (ORB)** is a day trading strategy that focuses on:
1. **Opening Range**: First 30-60 minutes of trading (9:30-10:30 AM EST)
2. **Breakout**: Price breaks above/below the opening range
3. **Retest**: Price returns to test the breakout level for continuation

---

## 🕘 **Opening Range Definition**

```
MARKET OPEN: 9:30 AM EST
┌─────────────────────────────────────────────────────────────────┐
│                    OPENING RANGE (30-60 MIN)                   │
│                     9:30 AM - 10:30 AM EST                     │
├─────────────────────────────────────────────────────────────────┤
│  OR HIGH: $252.50 ████████████████████████████████████████████ │
│           $252.00 ████████████████████████████████████████████ │
│  OR MID:  $251.25 ████████████████████████████████████████████ │ ← OR MIDDLE
│           $251.00 ████████████████████████████████████████████ │
│  OR LOW:  $250.00 ████████████████████████████████████████████ │
└─────────────────────────────────────────────────────────────────┘
                                ▲
                         OPENING RANGE ESTABLISHED
```

**Key Levels:**
- **OR High**: $252.50 (highest price 9:30-10:30 AM)
- **OR Low**: $250.00 (lowest price 9:30-10:30 AM)
- **OR Range**: $2.50 ($252.50 - $250.00)

---

## 📈 **Bullish ORB Process**

### **Step 1: Opening Range Formation**
```
9:30 AM - 10:30 AM: Price establishes range
OR High: $252.50
OR Low:  $250.00
```

### **Step 2: Bullish Breakout**
```
10:35 AM: Price breaks ABOVE OR High
$253.00 ▲ ← BREAKOUT above $252.50
$252.50 ████████████████████ ← OR HIGH (now support)
$252.00 ████████████████████
$251.25 ████████████████████ ← OR MID
$251.00 ████████████████████
$250.00 ████████████████████ ← OR LOW

✅ BULLISH ORB TRIGGERED: Price > $252.50
```

### **Step 3: Retest & Entry**
```
11:15 AM: Price returns to test OR High
$255.00
$254.00 ↘
$253.00 ↘ ← Price pulls back
$252.50 ████████████████████ ← RETEST ZONE (Entry)
$252.00 ████████████████████   Current: $252.40
$251.25 ████████████████████
$251.00 ████████████████████
$250.00 ████████████████████

🚨 BULLISH ORB RETEST SIGNAL!
📈 LONG ENTRY: $252.40
🎯 TARGET: $254.00 - $255.00
🛑 STOP: $251.50 (below OR High)
```

---

## 📉 **Bearish ORB Process**

### **Step 1: Opening Range Formation**
```
Same OR: $250.00 - $252.50
```

### **Step 2: Bearish Breakout**
```
10:45 AM: Price breaks BELOW OR Low
$252.50 ████████████████████ ← OR HIGH
$252.00 ████████████████████
$251.25 ████████████████████ ← OR MID
$251.00 ████████████████████
$250.00 ████████████████████ ← OR LOW (now resistance)
$249.50 ▼ ← BREAKOUT below $250.00

✅ BEARISH ORB TRIGGERED: Price < $250.00
```

### **Step 3: Retest & Entry**
```
11:30 AM: Price returns to test OR Low
$252.50 ████████████████████
$252.00 ████████████████████
$251.25 ████████████████████
$251.00 ████████████████████
$250.00 ████████████████████ ← RETEST ZONE (Entry)
$249.50 ↗ ← Price bounces back   Current: $249.90
$249.00 ↗
$248.50

🚨 BEARISH ORB RETEST SIGNAL!
📉 SHORT ENTRY: $249.90
🎯 TARGET: $248.00 - $247.00
🛑 STOP: $250.50 (above OR Low)
```

---

## 📊 **PML/PMH Breakout Strategy**

### **Previous Month High (PMH) Breakout**
```
MONTHLY CHART ANALYSIS:
PMH: $520.00 (Previous month's highest price)

CURRENT SCENARIO:
$522.00 ▲ ← BREAKOUT above PMH ($520.00)
$521.00 ▲
$520.00 ████████████████████ ← PMH LEVEL (now support)
$519.00 ████████████████████
$518.00 ████████████████████

RETEST PHASE:
$522.00
$521.00 ↘
$520.00 ████████████████████ ← RETEST ZONE
$519.50 ↗ ← Current: $519.80
$519.00

🚨 PMH BREAKOUT RETEST!
📈 LONG ENTRY: $519.80
🎯 TARGET: $525.00 - $530.00
🛑 STOP: $518.00 (below PMH)
```

### **Previous Month Low (PML) Breakout**
```
PML: $485.00 (Previous month's lowest price)

BREAKOUT SCENARIO:
$487.00 ████████████████████
$486.00 ████████████████████
$485.00 ████████████████████ ← PML LEVEL (now resistance)
$484.00 ▼ ← BREAKOUT below PML
$483.00 ▼

RETEST PHASE:
$486.00 ████████████████████
$485.00 ████████████████████ ← RETEST ZONE
$484.50 ↗ ← Current: $484.80
$484.00 ↗
$483.00

🚨 PML BREAKOUT RETEST!
📉 SHORT ENTRY: $484.80
🎯 TARGET: $480.00 - $475.00
🛑 STOP: $486.00 (above PML)
```

---

## 🎯 **Bot Detection Logic**

### **ORB Criteria:**
1. **Opening Range**: Establish high/low from 9:30-10:30 AM
2. **Breakout**: Price moves 0.1%+ beyond OR boundary
3. **Displacement**: Price moves away from OR level
4. **Retest**: Price returns within 0.5% of OR level
5. **Volume**: 1.5x+ average volume confirmation

### **Entry Signals:**
- **Bullish ORB**: Break above OR High + retest = LONG
- **Bearish ORB**: Break below OR Low + retest = SHORT
- **PMH Breakout**: Break above monthly high + retest = LONG
- **PML Breakout**: Break below monthly low + retest = SHORT

### **Risk Management:**
- **Stop Loss**: Beyond opposite side of OR or monthly level
- **Take Profit**: 1:2 to 1:4 risk/reward ratio
- **Position Size**: Based on OR range and account risk

---

## ⏰ **Time-Based Rules**

### **Best ORB Times:**
- **9:30-10:30 AM**: Opening range formation
- **10:30-11:30 AM**: Prime breakout window
- **11:30 AM-12:00 PM**: Retest opportunities
- **2:00-4:00 PM**: Afternoon momentum

### **Avoid:**
- **12:00-2:00 PM**: Lunch hour (low volume)
- **After 4:00 PM**: After-hours volatility

---

This is TRUE Opening Range Breakout strategy - completely different from Order Block analysis! 🎯