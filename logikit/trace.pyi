"""
Type stubs for logikit.trace module
"""
from dataclasses import dataclass
from typing import Any, Dict, List

class TraceStep:
    rule_id: str
    label: str
    passed: bool
    details: Dict[str, Any]
    
    def __init__(self, rule_id: str, label: str, passed: bool, details: Dict[str, Any] = ...) -> None: ...
    
    def to_dict(self) -> Dict[str, Any]: ...

def generate_flowchart_from_trace(trace: List[TraceStep]) -> str: ...

