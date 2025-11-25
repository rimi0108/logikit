"""
Type stubs for logikit package
"""
from typing import Any, Callable, Dict, List, Optional

# Import decorator
from logikit.decorator import logikit

# Import trace classes and functions
from logikit.trace import TraceStep, generate_flowchart_from_trace

# Explicit exports
TraceStep: type[TraceStep]
generate_flowchart_from_trace: Callable[[List[TraceStep]], str]

__version__: str
__all__: List[str]

