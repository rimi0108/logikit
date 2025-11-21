"""
Logikit decorator - Automatically visualize function execution

Traces condition evaluation during actual function execution to generate flowcharts
"""
import inspect
from functools import wraps
from typing import Any, Callable, Dict, List, Optional

from .trace import TraceStep


def logikit(condition_map: Optional[Dict[str, str]] = None):
    """
    Decorator that automatically traces function execution and generates flowcharts

    Args:
        condition_map: Dictionary mapping condition function names to descriptions
            Format: {condition_function_name: "condition_description"}

    Usage:
        @logikit(condition_map={
            "_fails_regulated_area_rules": "Check regulated area requirements",
            "_fails_public_housing_zone_rules": "Check public housing zone requirements",
            "_has_invalid_account": "Check account validity",
        })
        def is_eligible(self):
            if self._fails_regulated_area_rules():
                return False
            if self._fails_public_housing_zone_rules():
                return False
            if self._has_invalid_account():
                return False
            return True
    """

    def decorator(func: Callable) -> Callable:
        # Parse function source code in advance to understand conditional structure
        try:
            source = inspect.getsource(func)
            condition_order = _parse_condition_order(source, condition_map or {})
        except (OSError, TypeError):
            # If source code cannot be retrieved (e.g., C extension modules)
            condition_order = []

        @wraps(func)
        def wrapper(*args, **kwargs):
            tracer = LogikitTracer()
            instance = args[0] if args else None

            # Evaluate each condition in order
            for condition_info in condition_order:
                condition_id = condition_info["id"]
                label = condition_info["label"]
                func_name = condition_info["func_name"]

                # Get condition function from instance
                if instance and hasattr(instance, func_name):
                    condition_func = getattr(instance, func_name)
                    try:
                        condition_result = condition_func()
                        passed = not condition_result  # False return = condition failed

                        tracer.add_step(
                            rule_id=condition_id,
                            label=label,
                            passed=passed,
                            details={
                                "condition_result": condition_result,
                                "condition_func": func_name,
                            },
                        )

                        # Return immediately if condition fails
                        if condition_result:
                            result = False
                            # Store trace in instance
                            if instance:
                                setattr(instance, "_logikit_trace", tracer.get_trace())
                            return result

                    except Exception as e:
                        tracer.add_step(
                            rule_id=condition_id,
                            label=label,
                            passed=False,
                            details={"error": str(e)},
                        )
                        if instance:
                            setattr(instance, "_logikit_trace", tracer.get_trace())
                        return False

            # Execute original function if all conditions pass
            result = func(*args, **kwargs)
            tracer.add_step(
                rule_id="FINAL_RESULT",
                label="Final Result",
                passed=bool(result),
                details={"result": result},
            )

            # Store trace in instance
            if instance:
                setattr(instance, "_logikit_trace", tracer.get_trace())

            return result

        return wrapper

    return decorator


def _parse_condition_order(source: str, condition_map: Dict[str, str]) -> List[Dict[str, Any]]:
    """Parse conditional statement order from source code"""
    import re

    conditions = []
    lines = source.split("\n")

    # Find function call patterns in if statements
    # Example: if self._fails_regulated_area_rules():
    pattern = r"if\s+self\.(\w+)\(\):"

    for line in lines:
        match = re.search(pattern, line)
        if match:
            func_name = match.group(1)
            condition_id = func_name.upper()
            label = condition_map.get(func_name, func_name.replace("_", " ").title())

            conditions.append(
                {
                    "id": condition_id,
                    "label": label,
                    "func_name": func_name,
                }
            )

    return conditions


class LogikitTracer:
    """Class for tracing function execution"""

    def __init__(self):
        self.trace_steps: List[TraceStep] = []

    def add_step(self, rule_id: str, label: str, passed: bool, details: Dict[str, Any] = None):
        """Add a trace step"""
        self.trace_steps.append(
            TraceStep(
                rule_id=rule_id,
                label=label,
                passed=passed,
                details=details or {},
            )
        )

    def get_trace(self) -> List[TraceStep]:
        """Return trace results"""
        return self.trace_steps.copy()
