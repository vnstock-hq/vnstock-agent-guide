# Vnstock Pipeline - Real-Time Streaming

## Giới Thiệu

Chương này hướng dẫn sử dụng **real-time streaming** để:
- Nhận cập nhật giá live từ WebSocket
- Xử lý dữ liệu in-stream
- Tính chỉ báo real-time
- Push notifications khi có thay đổi
- Lưu data streaming vào database

---

## I. Kiến Trúc Streaming

### WebSocket vs REST

| Tiêu Chí | REST (Polling) | WebSocket (Streaming) |
|---------|---------------|-----------------------|
| **Cách thức** | Client pull data định kỳ | Server push data liên tục |
| **Latency** | 100-1000ms | 10-50ms |
| **Bandwidth** | Cao (polling overhead) | Thấp (chỉ push khi có thay đổi) |
| **Complexity** | Đơn giản | Phức tạp hơn |
| **Real-time** | Giả (delayed) | Thật sự real-time |
| **Use case** | Daily data | Live prices, tick data |

---

## II. Basic Streaming

### WebSocket Connection

```python
import asyncio
import websocket
import json
from datetime import datetime
import pandas as pd

class SimpleStreamListener:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.data = []
        self.ws = None
    
    def on_message(self, ws, message):
        """Handle incoming message"""
        try:
            data = json.loads(message)
            
            record = {
                'timestamp': datetime.now(),
                'symbol': self.symbol,
                'price': data.get('price'),
                'bid': data.get('bid'),
                'ask': data.get('ask'),
                'volume': data.get('volume'),
                'bid_volume': data.get('bid_volume'),
                'ask_volume': data.get('ask_volume')
            }
            
            self.data.append(record)
            
            # Print live
            print(f"[{record['timestamp'].strftime('%H:%M:%S')}] "
                  f"{self.symbol}: {record['price']} "
                  f"(bid={record['bid']}, ask={record['ask']}, "
                  f"vol={record['volume']})")
        
        except Exception as e:
            print(f"Error processing message: {e}")
    
    def on_error(self, ws, error):
        print(f"Error: {error}")
    
    def on_close(self, ws, close_status_code, close_msg):
        print(f"Closed")
    
    def on_open(self, ws):
        print(f"Connected to {self.symbol}")
        # Subscribe to symbol
        ws.send(json.dumps({
            "action": "subscribe",
            "symbols": [self.symbol]
        }))
    
    def start(self, url: str):
        """Start listening"""
        self.ws = websocket.WebSocketApp(
            url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        self.ws.run_forever()
    
    def get_dataframe(self) -> pd.DataFrame:
        """Convert to DataFrame"""
        return pd.DataFrame(self.data)

# Usage
listener = SimpleStreamListener("VCB")
# listener.start("wss://stream.example.com/prices")

# Get data
df = listener.get_dataframe()
print(df)
```

---

## III. Advanced Streaming

### Pattern 1: Multi-Symbol Streaming

```python
import asyncio
import json
from datetime import datetime
from collections import defaultdict
import pandas as pd

class MultiSymbolStreamer:
    """Listen to multiple symbols simultaneously"""
    
    def __init__(self, symbols: list):
        self.symbols = symbols
        self.data = defaultdict(list)
        self.latest = {}
    
    async def stream_symbol(self, symbol: str, url: str):
        """Stream single symbol"""
        import websocket
        
        def on_message(ws, message):
            try:
                record = json.loads(message)
                record['timestamp'] = datetime.now()
                record['symbol'] = symbol
                
                self.data[symbol].append(record)
                self.latest[symbol] = record
                
                print(f"[{symbol}] Price: {record.get('price')}")
            
            except Exception as e:
                print(f"Error in {symbol}: {e}")
        
        def on_open(ws):
            ws.send(json.dumps({
                "action": "subscribe",
                "symbols": [symbol]
            }))
        
        ws = websocket.WebSocketApp(
            url,
            on_message=on_message,
            on_open=on_open
        )
        
        # Run in thread
        ws.run_forever()
    
    async def start_all(self, url: str):
        """Start all streams"""
        tasks = [
            asyncio.create_task(self.stream_symbol(sym, url))
            for sym in self.symbols
        ]
        await asyncio.gather(*tasks)
    
    def get_latest_prices(self) -> dict:
        """Get latest price for each symbol"""
        return {
            sym: self.latest[sym].get('price')
            for sym in self.symbols
            if sym in self.latest
        }
    
    def get_dataframe(self, symbol: str) -> pd.DataFrame:
        """Get DataFrame for specific symbol"""
        return pd.DataFrame(self.data[symbol])

# Usage
streamer = MultiSymbolStreamer(['VCB', 'ACB', 'HPG', 'FPT'])
# asyncio.run(streamer.start_all("wss://stream.example.com/prices"))

# Get latest prices
print(streamer.get_latest_prices())
```

---

### Pattern 2: Real-Time Indicators

**Use case**: Calculate moving average, RSI, MACD live

```python
import pandas as pd
import numpy as np
from collections import deque
from datetime import datetime

class RealtimeIndicatorCalculator:
    """Calculate indicators on streaming data"""
    
    def __init__(self, symbols: list, window_size: int = 100):
        self.symbols = symbols
        self.window_size = window_size
        self.buffers = {sym: deque(maxlen=window_size) for sym in symbols}
        self.latest_values = {}
    
    def add_tick(self, symbol: str, price: float, timestamp: datetime):
        """Add new price tick"""
        self.buffers[symbol].append({
            'timestamp': timestamp,
            'price': price
        })
        
        # Calculate indicators
        indicators = self._calculate_indicators(symbol)
        self.latest_values[symbol] = indicators
        
        return indicators
    
    def _calculate_indicators(self, symbol: str) -> dict:
        """Calculate all indicators for symbol"""
        buffer = list(self.buffers[symbol])
        
        if len(buffer) < 2:
            return {}
        
        prices = [t['price'] for t in buffer]
        timestamps = [t['timestamp'] for t in buffer]
        
        indicators = {}
        
        # SMA
        if len(prices) >= 20:
            indicators['sma20'] = np.mean(prices[-20:])
        
        if len(prices) >= 50:
            indicators['sma50'] = np.mean(prices[-50:])
        
        # Price change
        indicators['change'] = prices[-1] - prices[-2]
        indicators['change_pct'] = (prices[-1] - prices[-2]) / prices[-2] * 100
        
        # RSI
        if len(prices) >= 14:
            rsi = self._calculate_rsi(prices[-14:])
            indicators['rsi'] = rsi
        
        # Volatility
        if len(prices) >= 10:
            returns = [
                (prices[i] - prices[i-1]) / prices[i-1] * 100
                for i in range(1, min(len(prices), 10))
            ]
            indicators['volatility_10'] = np.std(returns)
        
        return indicators
    
    def _calculate_rsi(self, prices: list) -> float:
        """Simple RSI calculation"""
        if len(prices) < 14:
            return None
        
        prices = prices[-14:]
        deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        
        gains = [d if d > 0 else 0 for d in deltas]
        losses = [abs(d) if d < 0 else 0 for d in deltas]
        
        avg_gain = np.mean(gains)
        avg_loss = np.mean(losses)
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def get_indicators(self, symbol: str) -> dict:
        """Get latest indicators"""
        return self.latest_values.get(symbol, {})
    
    def get_signal(self, symbol: str) -> str:
        """Get trading signal based on indicators"""
        ind = self.get_indicators(symbol)
        
        if not ind:
            return "NO_SIGNAL"
        
        rsi = ind.get('rsi')
        sma20 = ind.get('sma20')
        price = self.buffers[symbol][-1]['price'] if self.buffers[symbol] else None
        
        signals = []
        
        if rsi and rsi < 30:
            signals.append("OVERSOLD")
        elif rsi and rsi > 70:
            signals.append("OVERBOUGHT")
        
        if price and sma20 and price > sma20:
            signals.append("UPTREND")
        elif price and sma20 and price < sma20:
            signals.append("DOWNTREND")
        
        return " | ".join(signals) if signals else "NEUTRAL"

# Usage
calc = RealtimeIndicatorCalculator(['VCB', 'ACB', 'HPG'])

# Simulate streaming
import time
prices = {'VCB': 62.5, 'ACB': 23.1, 'HPG': 35.2}

for i in range(100):
    for sym in calc.symbols:
        # Simulate price movement
        prices[sym] += np.random.uniform(-0.5, 0.5)
        
        indicators = calc.add_tick(sym, prices[sym], datetime.now())
        signal = calc.get_signal(sym)
        
        print(f"[{sym}] Price: {prices[sym]:.2f}, "
              f"SMA20: {indicators.get('sma20', 0):.2f}, "
              f"RSI: {indicators.get('rsi', 0):.1f}, "
              f"Signal: {signal}")
    
    time.sleep(0.1)
```

---

### Pattern 3: Alert System

**Use case**: Alert khi giá breach levels, RSI extreme, volume spike

```python
from enum import Enum
from datetime import datetime

class AlertLevel(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"

class PriceAlert:
    def __init__(self, symbol: str, price: float, condition: str):
        self.symbol = symbol
        self.price = price
        self.condition = condition  # "above", "below"
    
    def check(self, current_price: float) -> bool:
        if self.condition == "above":
            return current_price > self.price
        elif self.condition == "below":
            return current_price < self.price
        return False

class StreamAlertManager:
    """Manage alerts on streaming data"""
    
    def __init__(self):
        self.alerts = []
        self.triggered = []
    
    def add_price_alert(self, symbol: str, price: float, condition: str):
        """Add price-level alert"""
        alert = PriceAlert(symbol, price, condition)
        self.alerts.append(alert)
    
    def add_rsi_alert(self, symbol: str, level: float, condition: str):
        """
        Add RSI alert
        condition: "above" (overbought) or "below" (oversold)
        """
        self.alerts.append({
            'type': 'rsi',
            'symbol': symbol,
            'level': level,
            'condition': condition
        })
    
    def add_volume_spike_alert(self, symbol: str, multiplier: float = 2.0):
        """Alert when volume > multiplier * average volume"""
        self.alerts.append({
            'type': 'volume_spike',
            'symbol': symbol,
            'multiplier': multiplier
        })
    
    def check_alerts(self, symbol: str, 
                    price: float, 
                    rsi: float = None, 
                    volume: int = None,
                    avg_volume: int = None) -> list:
        """Check all alerts for symbol"""
        triggered = []
        
        for alert in self.alerts:
            if isinstance(alert, PriceAlert):
                if alert.symbol == symbol and alert.check(price):
                    triggered.append({
                        'type': 'price',
                        'symbol': symbol,
                        'level': alert.price,
                        'condition': alert.condition,
                        'current': price,
                        'timestamp': datetime.now(),
                        'message': f"{symbol} price {alert.condition} {alert.price}: {price}"
                    })
            
            elif alert.get('type') == 'rsi' and alert['symbol'] == symbol and rsi:
                if alert['condition'] == 'above' and rsi > alert['level']:
                    triggered.append({
                        'type': 'rsi',
                        'symbol': symbol,
                        'level': alert['level'],
                        'current': rsi,
                        'timestamp': datetime.now(),
                        'message': f"{symbol} RSI {rsi:.1f} > {alert['level']:.1f} (OVERBOUGHT)"
                    })
                elif alert['condition'] == 'below' and rsi < alert['level']:
                    triggered.append({
                        'type': 'rsi',
                        'symbol': symbol,
                        'level': alert['level'],
                        'current': rsi,
                        'timestamp': datetime.now(),
                        'message': f"{symbol} RSI {rsi:.1f} < {alert['level']:.1f} (OVERSOLD)"
                    })
            
            elif alert.get('type') == 'volume_spike' and alert['symbol'] == symbol and volume and avg_volume:
                ratio = volume / avg_volume
                if ratio > alert['multiplier']:
                    triggered.append({
                        'type': 'volume_spike',
                        'symbol': symbol,
                        'multiplier': alert['multiplier'],
                        'current_ratio': ratio,
                        'timestamp': datetime.now(),
                        'message': f"{symbol} volume spike: {ratio:.1f}x average"
                    })
        
        self.triggered.extend(triggered)
        return triggered
    
    def get_alerts_dataframe(self) -> pd.DataFrame:
        """Get triggered alerts as DataFrame"""
        if not self.triggered:
            return pd.DataFrame()
        
        return pd.DataFrame(self.triggered)

# Usage
alert_manager = StreamAlertManager()

# Add alerts
alert_manager.add_price_alert("VCB", 65.0, "above")  # Alert if price > 65
alert_manager.add_price_alert("VCB", 60.0, "below")  # Alert if price < 60
alert_manager.add_rsi_alert("VCB", 70, "above")      # Overbought alert
alert_manager.add_rsi_alert("VCB", 30, "below")      # Oversold alert
alert_manager.add_volume_spike_alert("VCB", 2.0)     # 2x volume spike

# Check alerts
triggered = alert_manager.check_alerts(
    symbol="VCB",
    price=65.5,
    rsi=72.5,
    volume=20000000,
    avg_volume=10000000
)

for alert in triggered:
    print(f"🔔 ALERT: {alert['message']}")
```

---

### Pattern 4: Persistent Streaming

**Use case**: Save streaming data continuosly to database

```python
import sqlite3
import threading
from queue import Queue
from datetime import datetime
import pandas as pd

class PersistentStreamWriter:
    """Stream data to SQLite database"""
    
    def __init__(self, db_path: str = "streaming.db"):
        self.db_path = db_path
        self.queue = Queue()
        self.running = False
        self._init_db()
    
    def _init_db(self):
        """Initialize database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tick_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                symbol TEXT,
                price REAL,
                bid REAL,
                ask REAL,
                volume INTEGER,
                bid_volume INTEGER,
                ask_volume INTEGER
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_tick(self, symbol: str, price: float, bid: float, ask: float,
                 volume: int, bid_volume: int, ask_volume: int):
        """Queue tick data for writing"""
        tick = {
            'timestamp': datetime.now(),
            'symbol': symbol,
            'price': price,
            'bid': bid,
            'ask': ask,
            'volume': volume,
            'bid_volume': bid_volume,
            'ask_volume': ask_volume
        }
        self.queue.put(tick)
    
    def _writer_thread(self):
        """Background thread that writes queue to DB"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        batch = []
        batch_size = 100
        
        while self.running:
            try:
                # Get item with timeout
                tick = self.queue.get(timeout=1)
                batch.append(tick)
                
                # Write batch
                if len(batch) >= batch_size:
                    cursor.executemany('''
                        INSERT INTO tick_data
                        (timestamp, symbol, price, bid, ask, volume, bid_volume, ask_volume)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', [
                        (t['timestamp'], t['symbol'], t['price'], t['bid'], t['ask'],
                         t['volume'], t['bid_volume'], t['ask_volume'])
                        for t in batch
                    ])
                    conn.commit()
                    batch = []
            
            except:
                if batch:
                    cursor.executemany('''
                        INSERT INTO tick_data
                        (timestamp, symbol, price, bid, ask, volume, bid_volume, ask_volume)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', [
                        (t['timestamp'], t['symbol'], t['price'], t['bid'], t['ask'],
                         t['volume'], t['bid_volume'], t['ask_volume'])
                        for t in batch
                    ])
                    conn.commit()
        
        conn.close()
    
    def start(self):
        """Start background writer"""
        self.running = True
        thread = threading.Thread(target=self._writer_thread, daemon=True)
        thread.start()
        print("✅ Persistent writer started")
    
    def stop(self):
        """Stop writer"""
        self.running = False
        print("✅ Persistent writer stopped")
    
    def query(self, symbol: str, limit: int = 100) -> pd.DataFrame:
        """Query recent data"""
        conn = sqlite3.connect(self.db_path)
        query = f'''
            SELECT * FROM tick_data
            WHERE symbol = '{symbol}'
            ORDER BY timestamp DESC
            LIMIT {limit}
        '''
        df = pd.read_sql(query, conn)
        conn.close()
        return df.iloc[::-1]  # Reverse to ascending time order

# Usage
writer = PersistentStreamWriter("ticks.db")
writer.start()

# Stream data
for i in range(1000):
    writer.add_tick(
        symbol="VCB",
        price=62.5 + np.random.uniform(-0.5, 0.5),
        bid=62.4 + np.random.uniform(-0.5, 0.5),
        ask=62.6 + np.random.uniform(-0.5, 0.5),
        volume=np.random.randint(100, 1000),
        bid_volume=np.random.randint(10000, 100000),
        ask_volume=np.random.randint(10000, 100000)
    )
    
    if i % 100 == 0:
        print(f"Wrote {i} ticks")

writer.stop()

# Query data
df = writer.query("VCB", limit=50)
print(df.head())
print(f"\nRecorded {len(df)} ticks")
```

---

## IV. Complete Streaming Application

```python
"""
Production streaming app: Monitor VN30, calculate indicators, trigger alerts, save data
"""

import asyncio
import threading
import json
import numpy as np
import pandas as pd
from datetime import datetime
from collections import deque
import websocket

class ProductionStreamingApp:
    def __init__(self, symbols: list):
        self.symbols = symbols
        self.buffers = {sym: deque(maxlen=100) for sym in symbols}
        self.latest_prices = {}
        self.alerts = []
        self.data_writer = None
    
    def on_message(self, ws, message, symbol):
        """Handle incoming tick"""
        try:
            data = json.loads(message)
            
            tick = {
                'timestamp': datetime.now(),
                'symbol': symbol,
                'price': float(data.get('price', 0)),
                'bid': float(data.get('bid', 0)),
                'ask': float(data.get('ask', 0)),
                'volume': int(data.get('volume', 0)),
            }
            
            self.buffers[symbol].append(tick)
            self.latest_prices[symbol] = tick['price']
            
            # Check alerts
            indicators = self._calculate_indicators(symbol)
            self._check_alerts(symbol, indicators)
            
            # Print
            print(f"[{tick['timestamp'].strftime('%H:%M:%S')}] {symbol}: "
                  f"${tick['price']:.2f} | "
                  f"SMA20: ${indicators.get('sma20', 0):.2f} | "
                  f"RSI: {indicators.get('rsi', 0):.1f} | "
                  f"Vol: {tick['volume']}")
        
        except Exception as e:
            print(f"Error: {e}")
    
    def _calculate_indicators(self, symbol: str) -> dict:
        """Calculate indicators"""
        buffer = list(self.buffers[symbol])
        
        if len(buffer) < 2:
            return {}
        
        prices = [t['price'] for t in buffer]
        
        indicators = {}
        
        if len(prices) >= 20:
            indicators['sma20'] = np.mean(prices[-20:])
        
        if len(prices) >= 14:
            deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
            gains = [d if d > 0 else 0 for d in deltas[-14:]]
            losses = [abs(d) if d < 0 else 0 for d in deltas[-14:]]
            avg_gain = np.mean(gains) or 0.001
            avg_loss = np.mean(losses) or 0.001
            rs = avg_gain / avg_loss
            indicators['rsi'] = 100 - (100 / (1 + rs))
        
        return indicators
    
    def _check_alerts(self, symbol: str, indicators: dict):
        """Check alert conditions"""
        price = self.latest_prices.get(symbol)
        rsi = indicators.get('rsi')
        
        # Overbought alert
        if rsi and rsi > 70:
            alert = {
                'timestamp': datetime.now(),
                'symbol': symbol,
                'type': 'OVERBOUGHT',
                'value': rsi,
                'message': f"🔔 {symbol} OVERBOUGHT: RSI {rsi:.1f}"
            }
            self.alerts.append(alert)
            print(alert['message'])
        
        # Oversold alert
        if rsi and rsi < 30:
            alert = {
                'timestamp': datetime.now(),
                'symbol': symbol,
                'type': 'OVERSOLD',
                'value': rsi,
                'message': f"🔔 {symbol} OVERSOLD: RSI {rsi:.1f}"
            }
            self.alerts.append(alert)
            print(alert['message'])
    
    def start_streams(self, url: str):
        """Start listening to all symbols"""
        for symbol in self.symbols:
            def on_message_wrapper(ws, message, sym=symbol):
                self.on_message(ws, message, sym)
            
            ws = websocket.WebSocketApp(
                url,
                on_message=on_message_wrapper
            )
            
            # Run in thread
            thread = threading.Thread(target=ws.run_forever, daemon=True)
            thread.start()
    
    def get_summary(self) -> pd.DataFrame:
        """Get summary of all symbols"""
        summary = []
        
        for symbol in self.symbols:
            price = self.latest_prices.get(symbol)
            buffer = list(self.buffers[symbol])
            
            if buffer:
                prices = [t['price'] for t in buffer]
                change = prices[-1] - prices[0]
                change_pct = (change / prices[0]) * 100
                
                summary.append({
                    'symbol': symbol,
                    'price': price,
                    'change': change,
                    'change_pct': change_pct,
                    'high': max(prices),
                    'low': min(prices),
                    'volume': sum([t['volume'] for t in buffer])
                })
        
        return pd.DataFrame(summary)
    
    def export_to_csv(self, filename: str = "stream_data.csv"):
        """Export all data to CSV"""
        all_data = []
        
        for symbol in self.symbols:
            for tick in self.buffers[symbol]:
                tick_copy = tick.copy()
                all_data.append(tick_copy)
        
        df = pd.DataFrame(all_data)
        df.to_csv(filename, index=False)
        print(f"✅ Exported {len(df)} ticks to {filename}")
        
        return df

# Usage
app = ProductionStreamingApp(['VCB', 'ACB', 'HPG', 'FPT', 'GAS'])
# app.start_streams("wss://stream.example.com/prices")

# Simulate with sample data
import time
np.random.seed(42)

for i in range(500):
    for symbol in app.symbols:
        # Simulate tick
        price = 62.5 + np.random.uniform(-0.5, 0.5)
        
        data = json.dumps({
            'symbol': symbol,
            'price': price,
            'bid': price - 0.01,
            'ask': price + 0.01,
            'volume': np.random.randint(1000, 10000)
        })
        
        app.on_message(None, data, symbol)
    
    if i % 100 == 0:
        print(f"\n--- Summary at tick {i} ---")
        print(app.get_summary())
    
    time.sleep(0.01)

print("\n--- Final Summary ---")
print(app.get_summary())
print(f"\n--- Alerts Triggered: {len(app.alerts)} ---")
print(pd.DataFrame(app.alerts))

# Export
app.export_to_csv("streaming_data.csv")
```

---

## V. Best Practices

### 1. Connection Resilience

```python
class ResilientWebSocket:
    """Reconnect automatically on failure"""
    
    def __init__(self, url: str, max_retries: int = 5):
        self.url = url
        self.max_retries = max_retries
        self.ws = None
    
    def connect(self):
        for attempt in range(self.max_retries):
            try:
                self.ws = websocket.WebSocketApp(self.url)
                self.ws.run_forever()
                return
            except Exception as e:
                wait_time = 2 ** attempt  # exponential backoff
                print(f"Connection failed, retrying in {wait_time}s...")
                time.sleep(wait_time)
```

### 2. Resource Management

```python
# Use context managers
with websocket.WebSocketApp(url) as ws:
    ws.run_forever()

# Close gracefully
def on_close(ws, code, msg):
    print("Closed")
    ws.close()
```

### 3. Rate Limiting

```python
from time import sleep
from collections import deque

class RateLimiter:
    def __init__(self, max_per_second: int = 100):
        self.max_per_second = max_per_second
        self.timestamps = deque(maxlen=max_per_second)
    
    def wait(self):
        if len(self.timestamps) == self.max_per_second:
            sleep_time = 1 - (time.time() - self.timestamps[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
        self.timestamps.append(time.time())
```

