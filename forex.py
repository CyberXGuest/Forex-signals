#!/usr/bin/env python3
import os
import sys
import time
import random
import math
import json
from datetime import datetime
from collections import deque
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

# Colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'
BG_GREEN = '\033[42m'
BG_RED = '\033[41m'
BG_YELLOW = '\033[43m'
BG_BLUE = '\033[44m'

# All Forex Symbols with numbers
SYMBOLS = {
    "1": {"symbol": "EURUSD", "name": "Euro/US Dollar", "type": "Major", "volatility": 0.008, "trend": 0.0002},
    "2": {"symbol": "GBPUSD", "name": "British Pound/US Dollar", "type": "Major", "volatility": 0.010, "trend": 0.0001},
    "3": {"symbol": "USDJPY", "name": "US Dollar/Japanese Yen", "type": "Major", "volatility": 0.007, "trend": -0.0003},
    "4": {"symbol": "USDCHF", "name": "US Dollar/Swiss Franc", "type": "Major", "volatility": 0.006, "trend": -0.0001},
    "5": {"symbol": "USDCAD", "name": "US Dollar/Canadian Dollar", "type": "Major", "volatility": 0.009, "trend": 0.0002},
    "6": {"symbol": "AUDUSD", "name": "Australian Dollar/US Dollar", "type": "Major", "volatility": 0.011, "trend": 0.0003},
    "7": {"symbol": "NZDUSD", "name": "New Zealand Dollar/US Dollar", "type": "Major", "volatility": 0.010, "trend": 0.0002},
    "8": {"symbol": "EURGBP", "name": "Euro/British Pound", "type": "Cross", "volatility": 0.006, "trend": 0.0001},
    "9": {"symbol": "EURJPY", "name": "Euro/Japanese Yen", "type": "Cross", "volatility": 0.009, "trend": -0.0001},
    "10": {"symbol": "EURCHF", "name": "Euro/Swiss Franc", "type": "Cross", "volatility": 0.005, "trend": 0.0001},
    "11": {"symbol": "EURCAD", "name": "Euro/Canadian Dollar", "type": "Cross", "volatility": 0.010, "trend": 0.0003},
    "12": {"symbol": "EURAUD", "name": "Euro/Australian Dollar", "type": "Cross", "volatility": 0.012, "trend": -0.0002},
    "13": {"symbol": "GBPJPY", "name": "British Pound/Japanese Yen", "type": "Cross", "volatility": 0.012, "trend": -0.0002},
    "14": {"symbol": "GBPCHF", "name": "British Pound/Swiss Franc", "type": "Cross", "volatility": 0.008, "trend": 0.0000},
    "15": {"symbol": "GBPCAD", "name": "British Pound/Canadian Dollar", "type": "Cross", "volatility": 0.011, "trend": 0.0003},
    "16": {"symbol": "AUDJPY", "name": "Australian Dollar/Japanese Yen", "type": "Cross", "volatility": 0.013, "trend": 0.0000},
    "17": {"symbol": "AUDCHF", "name": "Australian Dollar/Swiss Franc", "type": "Cross", "volatility": 0.009, "trend": 0.0002},
    "18": {"symbol": "AUDCAD", "name": "Australian Dollar/Canadian Dollar", "type": "Cross", "volatility": 0.008, "trend": 0.0001},
    "19": {"symbol": "NZDJPY", "name": "New Zealand Dollar/Japanese Yen", "type": "Cross", "volatility": 0.012, "trend": -0.0001},
    "20": {"symbol": "NZDCAD", "name": "New Zealand Dollar/Canadian Dollar", "type": "Cross", "volatility": 0.009, "trend": 0.0001},
    "21": {"symbol": "CADJPY", "name": "Canadian Dollar/Japanese Yen", "type": "Cross", "volatility": 0.010, "trend": -0.0003},
    "22": {"symbol": "CHFJPY", "name": "Swiss Franc/Japanese Yen", "type": "Cross", "volatility": 0.008, "trend": -0.0002},
    "23": {"symbol": "USDTRY", "name": "US Dollar/Turkish Lira", "type": "Exotic", "volatility": 0.025, "trend": 0.005},
    "24": {"symbol": "USDZAR", "name": "US Dollar/South African Rand", "type": "Exotic", "volatility": 0.022, "trend": 0.003},
    "25": {"symbol": "USDMXN", "name": "US Dollar/Mexican Peso", "type": "Exotic", "volatility": 0.018, "trend": -0.002},
    "26": {"symbol": "USDSGD", "name": "US Dollar/Singapore Dollar", "type": "Exotic", "volatility": 0.005, "trend": -0.0001},
    "27": {"symbol": "USDHKD", "name": "US Dollar/Hong Kong Dollar", "type": "Exotic", "volatility": 0.002, "trend": 0.0000},
    "28": {"symbol": "USDNOK", "name": "US Dollar/Norwegian Krone", "type": "Exotic", "volatility": 0.015, "trend": 0.002},
    "29": {"symbol": "USDSEK", "name": "US Dollar/Swedish Krona", "type": "Exotic", "volatility": 0.014, "trend": 0.001},
    "30": {"symbol": "USDPLN", "name": "US Dollar/Polish Zloty", "type": "Exotic", "volatility": 0.012, "trend": -0.001},
    "31": {"symbol": "XAUUSD", "name": "Gold/US Dollar", "type": "Commodity", "volatility": 0.015, "trend": 0.002},
    "32": {"symbol": "XAGUSD", "name": "Silver/US Dollar", "type": "Commodity", "volatility": 0.025, "trend": 0.003},
    "33": {"symbol": "XPTUSD", "name": "Platinum/US Dollar", "type": "Commodity", "volatility": 0.020, "trend": -0.001},
    "34": {"symbol": "XPDUSD", "name": "Palladium/US Dollar", "type": "Commodity", "volatility": 0.030, "trend": -0.002},
    "35": {"symbol": "US30", "name": "US Dow Jones 30", "type": "Index", "volatility": 0.012, "trend": 0.001},
    "36": {"symbol": "US500", "name": "US S&P 500", "type": "Index", "volatility": 0.013, "trend": 0.002},
    "37": {"symbol": "USTEC", "name": "US Nasdaq 100", "type": "Index", "volatility": 0.018, "trend": 0.003},
    "38": {"symbol": "GER30", "name": "German DAX 30", "type": "Index", "volatility": 0.014, "trend": 0.001},
    "39": {"symbol": "UK100", "name": "UK FTSE 100", "type": "Index", "volatility": 0.010, "trend": 0.001},
    "40": {"symbol": "FRA40", "name": "French CAC 40", "type": "Index", "volatility": 0.012, "trend": 0.000},
    "41": {"symbol": "AUS200", "name": "Australian ASX 200", "type": "Index", "volatility": 0.009, "trend": 0.001},
    "42": {"symbol": "JPN225", "name": "Japan Nikkei 225", "type": "Index", "volatility": 0.015, "trend": 0.002},
    "43": {"symbol": "HK50", "name": "Hong Kong Hang Seng", "type": "Index", "volatility": 0.016, "trend": -0.001},
    "44": {"symbol": "BTCUSD", "name": "Bitcoin/US Dollar", "type": "Crypto", "volatility": 0.040, "trend": 0.005},
    "45": {"symbol": "ETHUSD", "name": "Ethereum/US Dollar", "type": "Crypto", "volatility": 0.045, "trend": 0.004},
    "46": {"symbol": "LTCUSD", "name": "Litecoin/US Dollar", "type": "Crypto", "volatility": 0.038, "trend": 0.002},
    "47": {"symbol": "XRPUSD", "name": "Ripple/US Dollar", "type": "Crypto", "volatility": 0.042, "trend": 0.003},
    "48": {"symbol": "ADAUSD", "name": "Cardano/US Dollar", "type": "Crypto", "volatility": 0.045, "trend": 0.001},
    "49": {"symbol": "DOTUSD", "name": "Polkadot/US Dollar", "type": "Crypto", "volatility": 0.043, "trend": -0.001},
    "50": {"symbol": "DOGEUSD", "name": "Dogecoin/US Dollar", "type": "Crypto", "volatility": 0.080, "trend": 0.008}
}

@dataclass
class Position:
    """Trade position tracking"""
    symbol: str
    direction: str  # "BUY" or "SELL"
    entry_price: float
    volume: float
    stop_loss: float
    take_profit: float
    open_time: datetime
    profit: float = 0.0
    status: str = "OPEN"
    id: int = 0

class AdaptiveMovingAverage:
    """Implementation of Adaptive Moving Average (AMA) indicator"""
    
    def __init__(self, period_ma=10, period_fast=2, period_slow=30, weight=1.0):
        self.period_ma = period_ma
        self.period_fast = period_fast
        self.period_slow = period_slow
        self.weight = weight
        self.prev_ama = None
        self.prev_er = None
        
    def calculate_efficiency_ratio(self, prices: List[float]) -> float:
        """Calculate Efficiency Ratio (ER)"""
        if len(prices) < self.period_slow:
            return 0.5
        
        # Price change over the period
        change = abs(prices[-1] - prices[-self.period_slow])
        
        # Price volatility (sum of absolute price changes)
        volatility = sum(abs(prices[i] - prices[i-1]) 
                        for i in range(-self.period_slow+1, 0))
        
        if volatility == 0:
            return 0.5
        
        # Efficiency Ratio
        er = change / volatility
        return er
    
    def calculate_smoothing_constant(self, er: float) -> float:
        """Calculate smoothing constant (SSC)"""
        fastest = 2.0 / (self.period_fast + 1)
        slowest = 2.0 / (self.period_slow + 1)
        
        # Scale ER to smoothing constant range
        ssc = er * (fastest - slowest) + slowest
        ssc = ssc * ssc  # Square for more responsiveness
        
        return max(min(ssc, 1.0), 0.0)  # Clamp to [0, 1]
    
    def calculate(self, prices: List[float]) -> float:
        """Calculate AMA value"""
        if len(prices) < self.period_slow:
            return prices[-1] if prices else 0
        
        current_price = prices[-1]
        er = self.calculate_efficiency_ratio(prices)
        ssc = self.calculate_smoothing_constant(er)
        
        if self.prev_ama is None:
            # Initial AMA is simple average
            self.prev_ama = sum(prices[-self.period_slow:]) / self.period_slow
        else:
            # Calculate AMA recursively
            self.prev_ama = self.prev_ama + ssc * ssc * (current_price - self.prev_ama)
        
        return self.prev_ama

class MaphahaGoldStrategy:
    """Implementation of Maphaha Gold trading strategy using AMA"""
    
    _position_counter = 0
    
    def __init__(self, symbol_info: Dict, threshold_open=100, threshold_close=100):
        self.symbol_info = symbol_info
        self.symbol = symbol_info["symbol"]
        self.threshold_open = threshold_open
        self.threshold_close = threshold_close
        self.stop_level = 1000.0  # Stop Loss in points
        self.take_level = 1500.0  # Take Profit in points
        
        # AMA indicators
        self.ama_fast = AdaptiveMovingAverage(period_ma=10, period_fast=2, period_slow=30)
        self.ama_slow = AdaptiveMovingAverage(period_ma=10, period_fast=5, period_slow=20)
        
        # Price tracking
        self.price_history = deque(maxlen=200)
        self.ama_fast_history = deque(maxlen=100)
        self.ama_slow_history = deque(maxlen=100)
        
        # Signal tracking
        self.current_signal = "NEUTRAL"
        self.signal_strength = 0
        self.open_positions: List[Position] = []
        self.closed_positions: List[Position] = []
        
        # Performance metrics
        self.total_trades = 0
        self.winning_trades = 0
        self.total_profit = 0.0
        self.max_drawdown = 0.0
        self.peak_equity = 10000.0  # Starting capital
        
        # Initialize price history
        self.initial_price = self.get_current_price()
        self.update_price_history(self.initial_price)
    
    def get_current_price(self) -> float:
        """Get current price for the symbol"""
        return self.symbol_info.get("current_price", 1.0)
    
    def update_price_history(self, price: float):
        """Update price history"""
        self.price_history.append(price)
        
        # Calculate AMA values
        prices_list = list(self.price_history)
        if len(prices_list) >= 30:
            ama_fast_val = self.ama_fast.calculate(prices_list)
            ama_slow_val = self.ama_slow.calculate(prices_list)
            
            self.ama_fast_history.append(ama_fast_val)
            self.ama_slow_history.append(ama_slow_val)
    
    def calculate_signal_strength(self) -> Tuple[str, float]:
        """Calculate signal strength based on AMA crossovers"""
        if len(self.ama_fast_history) < 5 or len(self.ama_slow_history) < 5:
            return "NEUTRAL", 0.0
        
        current_fast = self.ama_fast_history[-1]
        current_slow = self.ama_slow_history[-1]
        prev_fast = self.ama_fast_history[-2]
        prev_slow = self.ama_slow_history[-2]
        
        # Calculate price vs AMA
        current_price = self.price_history[-1]
        price_vs_fast = (current_price - current_fast) / current_fast * 100
        price_vs_slow = (current_price - current_slow) / current_slow * 100
        
        # Check for crossovers
        fast_above_slow = current_fast > current_slow
        prev_fast_above_slow = prev_fast > prev_slow
        
        # Calculate strength based on multiple factors
        strength = 0
        signal = "NEUTRAL"
        
        # Crossover signal
        if fast_above_slow and not prev_fast_above_slow:
            # Bullish crossover
            signal = "BUY"
            strength += 100
            strength += min(50, abs(price_vs_fast) * 10)
            strength += min(50, abs(price_vs_slow) * 10)
        elif not fast_above_slow and prev_fast_above_slow:
            # Bearish crossover
            signal = "SELL"
            strength += 100
            strength += min(50, abs(price_vs_fast) * 10)
            strength += min(50, abs(price_vs_slow) * 10)
        
        # Momentum confirmation
        if signal == "BUY" and price_vs_fast > 0 and price_vs_slow > 0:
            strength += 30
        elif signal == "SELL" and price_vs_fast < 0 and price_vs_slow < 0:
            strength += 30
        
        # Trend strength
        if fast_above_slow and current_fast - current_slow > 0:
            trend_strength = (current_fast - current_slow) / current_slow * 100
            strength += min(50, trend_strength * 10)
        elif not fast_above_slow and current_slow - current_fast > 0:
            trend_strength = (current_slow - current_fast) / current_fast * 100
            strength += min(50, trend_strength * 10)
        
        # Volume (simulated) and volatility adjustment
        volatility = self.symbol_info.get("volatility", 0.01)
        if volatility < 0.01:  # Low volatility reduces false signals
            strength *= 0.8
        
        # Normalize strength
        strength = min(100, max(0, strength))
        
        return signal, strength
    
    def should_open_position(self) -> Tuple[bool, str, float]:
        """Determine if we should open a position based on AMA signal"""
        signal, strength = self.calculate_signal_strength()
        
        if signal != "NEUTRAL" and strength >= self.threshold_open:
            # Check if we already have a position in same direction
            has_same_direction = any(p.direction == signal and p.status == "OPEN" 
                                    for p in self.open_positions)
            
            if not has_same_direction:
                return True, signal, strength
        
        return False, "NEUTRAL", 0.0
    
    def should_close_position(self, position: Position) -> Tuple[bool, str]:
        """Determine if we should close a position"""
        if position.status != "OPEN":
            return False, "NEUTRAL"
        
        current_price = self.get_current_price()
        signal, strength = self.calculate_signal_strength()
        
        # Calculate current profit
        if position.direction == "BUY":
            position.profit = (current_price - position.entry_price) * position.volume
        else:
            position.profit = (position.entry_price - current_price) * position.volume
        
        # Check stop loss and take profit
        if position.direction == "BUY":
            if current_price <= position.stop_loss:
                return True, "STOP_LOSS"
            if current_price >= position.take_profit:
                return True, "TAKE_PROFIT"
        else:
            if current_price >= position.stop_loss:
                return True, "STOP_LOSS"
            if current_price <= position.take_profit:
                return True, "TAKE_PROFIT"
        
        # Check signal reversal
        if position.direction == "BUY" and signal == "SELL" and strength >= self.threshold_close:
            return True, "SIGNAL_REVERSAL"
        elif position.direction == "SELL" and signal == "BUY" and strength >= self.threshold_close:
            return True, "SIGNAL_REVERSAL"
        
        return False, "NEUTRAL"
    
    def open_position(self, direction: str, price: float, strength: float) -> Position:
        """Open a new trading position"""
        # Calculate position size (fixed lot)
        volume = 0.20  # Fixed lot size from MQL5 code
        
        # Calculate stop loss and take profit
        point_value = self.symbol_info.get("point_value", 0.00001)
        stop_points = self.stop_level * point_value
        take_points = self.take_level * point_value
        
        if direction == "BUY":
            stop_loss = price - stop_points
            take_profit = price + take_points
        else:  # SELL
            stop_loss = price + stop_points
            take_profit = price - take_points
        
        MaphahaGoldStrategy._position_counter += 1
        position = Position(
            id=MaphahaGoldStrategy._position_counter,
            symbol=self.symbol,
            direction=direction,
            entry_price=price,
            volume=volume,
            stop_loss=stop_loss,
            take_profit=take_profit,
            open_time=datetime.now()
        )
        
        self.open_positions.append(position)
        print(f"{GREEN}✓ OPENED {direction} position at {price:.5f} "
              f"(SL: {stop_loss:.5f}, TP: {take_profit:.5f}){RESET}")
        
        return position
    
    def close_position(self, position: Position, reason: str, current_price: float):
        """Close an existing position"""
        if position.status != "OPEN":
            return
        
        position.status = "CLOSED"
        
        # Calculate final profit/loss
        if position.direction == "BUY":
            profit = (current_price - position.entry_price) * position.volume
        else:
            profit = (position.entry_price - current_price) * position.volume
        
        position.profit = profit
        
        # Update statistics
        self.total_trades += 1
        self.total_profit += profit
        
        if profit > 0:
            self.winning_trades += 1
            profit_color = GREEN
            profit_sign = "+"
        else:
            profit_color = RED
            profit_sign = ""
        
        # Update equity tracking for drawdown
        current_equity = self.calculate_total_equity()
        if current_equity > self.peak_equity:
            self.peak_equity = current_equity
        drawdown = (self.peak_equity - current_equity) / self.peak_equity * 100 if self.peak_equity > 0 else 0
        self.max_drawdown = max(self.max_drawdown, drawdown)
        
        print(f"{RED}✗ CLOSED {position.direction} position: {profit_sign}${profit:.2f} "
              f"({reason}){RESET}")
        
        # Move to closed positions list
        self.closed_positions.append(position)
        self.open_positions = [p for p in self.open_positions if p.id != position.id]
    
    def calculate_total_equity(self) -> float:
        """Calculate total equity including open positions"""
        equity = 10000.0  # Starting capital
        equity += self.total_profit
        
        for position in self.open_positions:
            if position.status == "OPEN":
                current_price = self.get_current_price()
                if position.direction == "BUY":
                    equity += (current_price - position.entry_price) * position.volume
                else:
                    equity += (position.entry_price - current_price) * position.volume
        
        return equity
    
    def get_performance_stats(self) -> Dict:
        """Get performance statistics"""
        win_rate = (self.winning_trades / self.total_trades * 100) if self.total_trades > 0 else 0
        avg_profit = self.total_profit / self.total_trades if self.total_trades > 0 else 0
        
        return {
            "total_trades": self.total_trades,
            "winning_trades": self.winning_trades,
            "win_rate": win_rate,
            "total_profit": self.total_profit,
            "avg_profit": avg_profit,
            "max_drawdown": self.max_drawdown,
            "open_positions": len(self.open_positions)
        }
    
    def update(self, current_price: float):
        """Update strategy with new price"""
        self.update_price_history(current_price)
        
        # Update open positions with current price
        for position in self.open_positions[:]:  # Use slice copy for safe iteration
            should_close, reason = self.should_close_position(position)
            if should_close:
                self.close_position(position, reason, current_price)
        
        # Check for new position
        should_open, direction, strength = self.should_open_position()
        if should_open:
            self.open_position(direction, current_price, strength)

class ForexTool:
    def __init__(self):
        self.prices = {}
        self.strategies: Dict[str, MaphahaGoldStrategy] = {}
        
        # Set initial prices with realistic values
        for key, info in SYMBOLS.items():
            symbol = info["symbol"]
            if symbol == "XAUUSD":
                self.prices[symbol] = 2350.50
            elif symbol == "BTCUSD":
                self.prices[symbol] = 65000
            elif symbol == "ETHUSD":
                self.prices[symbol] = 3500
            elif symbol == "EURUSD":
                self.prices[symbol] = 1.0850
            elif symbol == "GBPUSD":
                self.prices[symbol] = 1.2650
            elif symbol == "USDJPY":
                self.prices[symbol] = 148.50
            elif symbol == "US30":
                self.prices[symbol] = 38500
            elif symbol == "US500":
                self.prices[symbol] = 5100
            elif symbol == "USTEC":
                self.prices[symbol] = 18200
            else:
                # Generate reasonable starting prices based on type
                if info["type"] == "Index":
                    self.prices[symbol] = random.uniform(5000, 30000)
                elif info["type"] == "Crypto":
                    self.prices[symbol] = random.uniform(0.1, 1000)
                elif info["type"] == "Exotic":
                    self.prices[symbol] = random.uniform(1, 40)
                else:
                    self.prices[symbol] = random.uniform(0.5, 200)
            
            info["current_price"] = self.prices[symbol]
            info["point_value"] = 0.00001 if symbol not in ["BTCUSD", "ETHUSD"] else 1.0
            
            # Initialize strategy for each symbol
            self.strategies[symbol] = MaphahaGoldStrategy(
                info,
                threshold_open=100,
                threshold_close=100
            )
    
    def update_price(self, symbol: str) -> float:
        """Generate price movements with mean reversion"""
        old = self.prices[symbol]
        info = SYMBOLS[next(k for k, v in SYMBOLS.items() if v["symbol"] == symbol)]
        
        # Generate price movement with trend and volatility
        volatility = info["volatility"]
        trend = info.get("trend", 0)
        
        # Random walk with drift
        change = random.gauss(trend * old * 0.1, volatility * old * 0.5)
        
        # Add occasional spikes
        if random.random() < 0.05:
            change *= random.uniform(1.5, 3.0)
        
        new = max(old + change, 0.0001)
        self.prices[symbol] = new
        info["current_price"] = new
        
        return new
    
    def clear(self):
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def show_banner(self, info: Dict, strategy: MaphahaGoldStrategy, price: float):
        self.clear()
        
        symbol = info["symbol"]
        name = info["name"]
        signal, strength = strategy.calculate_signal_strength()
        stats = strategy.get_performance_stats()
        
        # Determine signal color and arrow
        if signal == "BUY":
            bg = BG_GREEN
            color = GREEN
            arrow = "▲▲▲ BUY SIGNAL ▲▲▲"
        elif signal == "SELL":
            bg = BG_RED
            color = RED
            arrow = "▼▼▼ SELL SIGNAL ▼▼▼"
        else:
            bg = BG_BLUE
            color = CYAN
            arrow = "●●● AMA MONITORING ●●●"
        
        print(f"\n{bg}{'='*70}{RESET}")
        print(f"{bg}{' ' * 70}{RESET}")
        print(f"{bg}{color}{BOLD}{arrow:^70}{RESET}")
        print(f"{bg}{' ' * 70}{RESET}")
        print(f"{bg}{'='*70}{RESET}\n")
        
        # Main info panel
        print(f"{color}{BOLD}╔══════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{color}{BOLD}║  Symbol: {CYAN}{symbol:<10}{RESET}{color}{BOLD} Name: {CYAN}{name:<25}{RESET}{color}{BOLD}  ║{RESET}")
        print(f"{color}{BOLD}║  Type:   {CYAN}{info['type']:<10}{RESET}{color}{BOLD} Price: {CYAN}${price:<12.5f}{RESET}{color}{BOLD}        ║{RESET}")
        print(f"{color}{BOLD}║  Signal: {color}{signal:<10}{RESET}{color}{BOLD} Strength: {CYAN}{strength:.1f}%{RESET}{color}{BOLD}                  ║{RESET}")
        print(f"{color}{BOLD}╠══════════════════════════════════════════════════════════════╣{RESET}")
        
        # Performance metrics
        win_rate_color = GREEN if stats['win_rate'] >= 50 else RED
        profit_color = GREEN if stats['total_profit'] >= 0 else RED
        
        print(f"{color}{BOLD}║  Performance:                                          ║{RESET}")
        print(f"{color}{BOLD}║    Total Trades: {YELLOW}{stats['total_trades']:<5}{RESET}  Win Rate: {win_rate_color}{stats['win_rate']:.1f}%{RESET}{color}{BOLD}           ║{RESET}")
        print(f"{color}{BOLD}║    Total Profit: {profit_color}${stats['total_profit']:<8.2f}{RESET}  Open Positions: {YELLOW}{stats['open_positions']}{RESET}{color}{BOLD}          ║{RESET}")
        print(f"{color}{BOLD}║    Max Drawdown: {RED}{stats['max_drawdown']:.1f}%{RESET}                                 ║{RESET}")
        
        print(f"{color}{BOLD}╠══════════════════════════════════════════════════════════════╣{RESET}")
        
        # AMA indicator values
        if len(strategy.ama_fast_history) > 0:
            current_fast = strategy.ama_fast_history[-1]
            current_slow = strategy.ama_slow_history[-1]
            
            ama_color = GREEN if current_fast > current_slow else RED
            print(f"{color}{BOLD}║  AMA Fast: {CYAN}{current_fast:<10.5f}{RESET}  AMA Slow: {CYAN}{current_slow:<10.5f}{RESET}{color}{BOLD}      ║{RESET}")
        
        print(f"{color}{BOLD}╚══════════════════════════════════════════════════════════════╝{RESET}\n")
        
        # Strategy settings
        print(f"{CYAN}{BOLD}┌─── Maphaha Gold Strategy Settings ───┐{RESET}")
        print(f"{CYAN}│ AMA Period MA: 10                    │{RESET}")
        print(f"{CYAN}│ AMA Period Fast: 2                   │{RESET}")
        print(f"{CYAN}│ AMA Period Slow: 30                  │{RESET}")
        print(f"{CYAN}│ Stop Loss: {strategy.stop_level:.0f} pts        │{RESET}")
        print(f"{CYAN}│ Take Profit: {strategy.take_level:.0f} pts      │{RESET}")
        print(f"{CYAN}│ Fixed Lot Size: 0.20                 │{RESET}")
        print(f"{CYAN}└────────────────────────────────────┘{RESET}\n")
        
        # Show open positions
        if strategy.open_positions:
            print(f"{YELLOW}Open Positions:{RESET}")
            for pos in strategy.open_positions:
                pos_color = GREEN if pos.direction == "BUY" else RED
                print(f"  {pos_color}{pos.direction}{RESET} @ {pos.entry_price:.5f} "
                      f"SL: {pos.stop_loss:.5f} TP: {pos.take_profit:.5f}")
            print()
    
    def show_menu(self):
        self.clear()
        print(f"{CYAN}{BOLD}")
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║        MAPHAHA GOLD STRATEGY v5.0 - AMA Indicator           ║")
        print("║        Based on MetaTrader 5 Expert Advisor                 ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print(f"{RESET}")
        print(f"{YELLOW}Strategy: Adaptive Moving Average (AMA) Crossovers{RESET}")
        print(f"{YELLOW}Features: Automatic trading, SL/TP management, Performance tracking{RESET}\n")
        
        # Show symbols in compact groups
        for t in ["Major", "Cross", "Exotic", "Commodity", "Index", "Crypto"]:
            print(f"\n{YELLOW}━━━ {t} Pairs ━━━{RESET}")
            items = [(num, info) for num, info in SYMBOLS.items() if info["type"] == t]
            # Display in rows of 3 for compactness
            for i in range(0, len(items), 3):
                row = items[i:i+3]
                parts = []
                for num, info in row:
                    parts.append(f"  {GREEN}{num:>3}{RESET}. {CYAN}{info['symbol']:<8}{RESET}")
                print("".join(parts))
        
        print(f"\n{MAGENTA}{BOLD}🎯 Strategy: BUY when fast AMA crosses above slow AMA{RESET}")
        print(f"{MAGENTA}🎯 Strategy: SELL when fast AMA crosses below slow AMA{RESET}")
        print(f"{MAGENTA}💡 Enter symbol number to monitor (e.g., {GREEN}31{RESET}{MAGENTA} for Gold){RESET}")
        print(f"   Press {RED}q{RESET}{MAGENTA} to quit | {CYAN}s{RESET}{MAGENTA} for strategy stats{RESET}\n")
    
    def show_global_stats(self):
        """Show global statistics for all strategies"""
        self.clear()
        print(f"{CYAN}{BOLD}")
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║              GLOBAL PERFORMANCE STATISTICS                   ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print(f"{RESET}\n")
        
        total_trades = 0
        total_wins = 0
        total_profit = 0
        
        for symbol, strategy in self.strategies.items():
            stats = strategy.get_performance_stats()
            if stats['total_trades'] > 0:
                total_trades += stats['total_trades']
                total_wins += stats['winning_trades']
                total_profit += stats['total_profit']
                
                win_rate_color = GREEN if stats['win_rate'] >= 50 else RED
                profit_color = GREEN if stats['total_profit'] >= 0 else RED
                
                print(f"{CYAN}{symbol:<10}{RESET} "
                      f"Trades: {YELLOW}{stats['total_trades']:<3}{RESET} "
                      f"Win Rate: {win_rate_color}{stats['win_rate']:5.1f}%{RESET} "
                      f"Profit: {profit_color}${stats['total_profit']:8.2f}{RESET}")
        
        if total_trades > 0:
            overall_win_rate = (total_wins / total_trades * 100)
            win_rate_color = GREEN if overall_win_rate >= 50 else RED
            profit_color = GREEN if total_profit >= 0 else RED
            
            print(f"\n{MAGENTA}{BOLD}{'='*50}{RESET}")
            print(f"{BOLD}OVERALL STATISTICS:{RESET}")
            print(f"  Total Trades: {YELLOW}{total_trades}{RESET}")
            print(f"  Total Wins: {GREEN}{total_wins}{RESET}")
            print(f"  Overall Win Rate: {win_rate_color}{overall_win_rate:.1f}%{RESET}")
            print(f"  Total Profit: {profit_color}${total_profit:.2f}{RESET}")
            print(f"{MAGENTA}{BOLD}{'='*50}{RESET}")
        else:
            print(f"\n{YELLOW}No trades executed yet. Select a symbol to start trading!{RESET}")
        
        print(f"\n{YELLOW}Press Enter to continue...{RESET}")
        input()
    
    def run(self):
        while True:
            self.show_menu()
            try:
                choice = input(f"{BOLD}{GREEN}➜ Select option: {RESET}").strip()
            except KeyboardInterrupt:
                print(f"\n{GREEN}Goodbye! Happy Trading!{RESET}")
                sys.exit(0)
            
            if choice.lower() == 'q':
                print(f"\n{GREEN}Goodbye! Happy Trading!{RESET}")
                sys.exit(0)
            elif choice.lower() == 's':
                self.show_global_stats()
                continue
            
            if choice in SYMBOLS:
                symbol_info = SYMBOLS[choice]
                strategy = self.strategies[symbol_info["symbol"]]
                
                print(f"\n{GREEN}Initializing {CYAN}{symbol_info['symbol']}{GREEN} with Maphaha Gold strategy...{RESET}")
                print(f"{YELLOW}Building AMA history for accurate signals...{RESET}")
                
                # Generate initial history for better signals
                for _ in range(100):  # Need 100+ bars for AMA calculation
                    price = self.update_price(symbol_info["symbol"])
                    strategy.update(price)
                
                print(f"{GREEN}Strategy ready! Monitoring with AMA indicator...{RESET}")
                print(f"{CYAN}Press Ctrl+C to return to menu{RESET}")
                time.sleep(1)
                
                try:
                    while True:
                        # Update price and strategy
                        price = self.update_price(symbol_info["symbol"])
                        strategy.update(price)
                        
                        # Display current status
                        self.show_banner(symbol_info, strategy, price)
                        
                        # Countdown to next update
                        for i in range(3, 0, -1):
                            signal, _ = strategy.calculate_signal_strength()
                            color = GREEN if signal == "BUY" else RED if signal == "SELL" else CYAN
                            print(f"\r{color}Next update in {i}s | Signal: {signal} | Ctrl+C for menu{RESET}", 
                                  end="", flush=True)
                            time.sleep(1)
                        print("\r" + " "*70 + "\r", end="")
                except KeyboardInterrupt:
                    print(f"\n{YELLOW}Returning to main menu...{RESET}")
                    time.sleep(1)
            else:
                print(f"\n{RED}❌ Invalid selection! Please enter a number between 1-50{RESET}")
                time.sleep(1.5)

if __name__ == "__main__":
    try:
        print(f"{CYAN}Initializing Maphaha Gold Trading System...{RESET}")
        print(f"{YELLOW}Loading Adaptive Moving Average (AMA) strategy...{RESET}")
        tool = ForexTool()
        tool.run()
    except KeyboardInterrupt:
        print(f"\n{GREEN}Goodbye! Happy Trading!{RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
        print(f"{YELLOW}Make sure you have Python 3 installed{RESET}")
        sys.exit(1)
