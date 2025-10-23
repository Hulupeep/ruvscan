"""
Monitoring and observability for RuvScan
"""

from typing import Dict, Any, List
from datetime import datetime
import logging
import time
from dataclasses import dataclass, field
from collections import defaultdict

logger = logging.getLogger(__name__)

@dataclass
class RequestMetrics:
    """Metrics for a single request"""
    endpoint: str
    method: str
    status_code: int
    duration_ms: float
    timestamp: datetime = field(default_factory=datetime.utcnow)

class MetricsCollector:
    """Collect and aggregate metrics"""

    def __init__(self):
        self.requests: List[RequestMetrics] = []
        self.endpoint_counts = defaultdict(int)
        self.endpoint_durations = defaultdict(list)
        self.error_counts = defaultdict(int)
        self.start_time = datetime.utcnow()

    def record_request(
        self,
        endpoint: str,
        method: str,
        status_code: int,
        duration_ms: float
    ):
        """Record a request"""
        metrics = RequestMetrics(
            endpoint=endpoint,
            method=method,
            status_code=status_code,
            duration_ms=duration_ms
        )

        self.requests.append(metrics)
        self.endpoint_counts[endpoint] += 1
        self.endpoint_durations[endpoint].append(duration_ms)

        if status_code >= 400:
            self.error_counts[endpoint] += 1

    def get_summary(self) -> Dict[str, Any]:
        """Get metrics summary"""
        total_requests = len(self.requests)
        uptime = (datetime.utcnow() - self.start_time).total_seconds()

        # Calculate average durations
        avg_durations = {}
        for endpoint, durations in self.endpoint_durations.items():
            avg_durations[endpoint] = sum(durations) / len(durations) if durations else 0

        # Calculate error rates
        error_rates = {}
        for endpoint, errors in self.error_counts.items():
            total = self.endpoint_counts[endpoint]
            error_rates[endpoint] = (errors / total * 100) if total > 0 else 0

        return {
            "uptime_seconds": uptime,
            "total_requests": total_requests,
            "requests_per_second": total_requests / uptime if uptime > 0 else 0,
            "endpoint_counts": dict(self.endpoint_counts),
            "average_duration_ms": avg_durations,
            "error_rates_percent": error_rates,
            "total_errors": sum(self.error_counts.values())
        }

    def get_recent_requests(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent requests"""
        recent = self.requests[-limit:]
        return [
            {
                "endpoint": r.endpoint,
                "method": r.method,
                "status_code": r.status_code,
                "duration_ms": r.duration_ms,
                "timestamp": r.timestamp.isoformat()
            }
            for r in recent
        ]

# Global metrics collector
metrics_collector = MetricsCollector()

class RequestTimer:
    """Context manager for timing requests"""

    def __init__(self, endpoint: str, method: str):
        self.endpoint = endpoint
        self.method = method
        self.start_time = None
        self.status_code = 200

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration_ms = (time.time() - self.start_time) * 1000

        if exc_type is not None:
            self.status_code = 500

        metrics_collector.record_request(
            self.endpoint,
            self.method,
            self.status_code,
            duration_ms
        )

    def set_status(self, status_code: int):
        """Set the status code"""
        self.status_code = status_code
