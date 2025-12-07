"""
Metrics Collection System
Collects and exposes application metrics for monitoring
"""
from typing import Dict, Any, List
from datetime import datetime, timedelta
import asyncio
import time
import logging

logger = logging.getLogger(__name__)

class MetricsCollector:
    """Collects application metrics"""
    
    def __init__(self):
        self.request_count = 0
        self.error_count = 0
        self.request_durations: List[float] = []
        self.endpoint_stats: Dict[str, Dict[str, Any]] = {}
        self.start_time = datetime.utcnow()
        
        # Per-endpoint metrics
        self.endpoint_requests = {}
        self.endpoint_errors = {}
        self.endpoint_durations = {}
    
    def record_request(self, endpoint: str, method: str, duration_ms: float, status_code: int):
        """Record a request"""
        self.request_count += 1
        self.request_durations.append(duration_ms)
        
        # Keep only last 1000 durations for memory efficiency
        if len(self.request_durations) > 1000:
            self.request_durations = self.request_durations[-1000:]
        
        # Per-endpoint stats
        key = f"{method} {endpoint}"
        if key not in self.endpoint_stats:
            self.endpoint_stats[key] = {
                "count": 0,
                "errors": 0,
                "total_duration": 0.0,
                "min_duration": float('inf'),
                "max_duration": 0.0
            }
        
        stats = self.endpoint_stats[key]
        stats["count"] += 1
        stats["total_duration"] += duration_ms
        stats["min_duration"] = min(stats["min_duration"], duration_ms)
        stats["max_duration"] = max(stats["max_duration"], duration_ms)
        
        if status_code >= 400:
            self.error_count += 1
            stats["errors"] += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics"""
        uptime_seconds = (datetime.utcnow() - self.start_time).total_seconds()
        
        # Calculate average, p50, p95, p99
        durations = sorted(self.request_durations)
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        p50_index = int(len(durations) * 0.50)
        p95_index = int(len(durations) * 0.95)
        p99_index = int(len(durations) * 0.99)
        
        p50 = durations[p50_index] if durations else 0
        p95 = durations[p95_index] if durations else 0
        p99 = durations[p99_index] if durations else 0
        
        # Endpoint statistics with averages
        endpoint_metrics = {}
        for endpoint, stats in self.endpoint_stats.items():
            avg_duration_endpoint = stats["total_duration"] / stats["count"] if stats["count"] > 0 else 0
            error_rate = (stats["errors"] / stats["count"] * 100) if stats["count"] > 0 else 0
            
            endpoint_metrics[endpoint] = {
                "requests": stats["count"],
                "errors": stats["errors"],
                "error_rate_percent": round(error_rate, 2),
                "avg_duration_ms": round(avg_duration_endpoint, 2),
                "min_duration_ms": round(stats["min_duration"], 2) if stats["min_duration"] != float('inf') else 0,
                "max_duration_ms": round(stats["max_duration"], 2)
            }
        
        return {
            "uptime_seconds": round(uptime_seconds, 2),
            "total_requests": self.request_count,
            "total_errors": self.error_count,
            "error_rate_percent": round((self.error_count / self.request_count * 100) if self.request_count > 0 else 0, 2),
            "requests_per_second": round(self.request_count / uptime_seconds if uptime_seconds > 0 else 0, 2),
            "response_times": {
                "avg_ms": round(avg_duration, 2),
                "p50_ms": round(p50, 2),
                "p95_ms": round(p95, 2),
                "p99_ms": round(p99, 2),
                "min_ms": round(min(durations), 2) if durations else 0,
                "max_ms": round(max(durations), 2) if durations else 0
            },
            "endpoints": endpoint_metrics
        }
    
    def reset_metrics(self):
        """Reset all metrics"""
        self.request_count = 0
        self.error_count = 0
        self.request_durations = []
        self.endpoint_stats = {}
        self.start_time = datetime.utcnow()
        logger.info("Metrics reset")

# Global metrics collector
metrics_collector = MetricsCollector()

def get_metrics() -> Dict[str, Any]:
    """Get current metrics"""
    return metrics_collector.get_metrics()

def record_request(endpoint: str, method: str, duration_ms: float, status_code: int):
    """Record a request"""
    metrics_collector.record_request(endpoint, method, duration_ms, status_code)
