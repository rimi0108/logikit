"""
Trace data structures
"""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TraceStep:
    """
    Data structure for recording each step of function execution tracing

    Attributes:
        rule_id: Unique identifier for the rule (e.g., "REGULATED_AREA_RULES", "HOUSING_SUBSCRIPTION_ACCOUNT")
        label: Human-readable description (e.g., "Check regulated area requirements", "Check account requirements")
        passed: Whether the rule passed
        details: Key values used in the rule (JSON-serializable dict)
    """

    rule_id: str
    label: str
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "rule_id": self.rule_id,
            "label": self.label,
            "passed": self.passed,
            "details": self.details,
        }


def generate_flowchart_from_trace(trace: List[TraceStep]) -> str:
    """
    Generate Mermaid flowchart from a list of TraceStep objects

    Args:
        trace: List of TraceStep objects

    Returns:
        Mermaid flowchart code
    """
    if not trace:
        return "flowchart TD\n    Start([Start])\n    Start --> End([End])"

    lines = ["flowchart TD"]
    lines.append("    Start([Start])")

    for i, step in enumerate(trace):
        node_id = f"Step{i+1}"
        label = step.label.replace(" ", "<br/>")

        # Determine node type
        if step.rule_id == "FINAL_RESULT":
            node_shape = f"([{label}])"
        else:
            node_shape = "{{" + label + "}}"

        lines.append(f"    {node_id}{node_shape}")

        # Connect nodes
        if i == 0:
            lines.append(f"    Start --> {node_id}")
        else:
            prev_node_id = f"Step{i}"
            if trace[i - 1].passed is False:
                lines.append(f"    {prev_node_id} -->|FAIL| EndFail([Not Eligible])")
                break
            else:
                lines.append(f"    {prev_node_id} -->|PASS| {node_id}")

        # FAIL branch
        if step.passed is False and step.rule_id != "FINAL_RESULT":
            lines.append(f"    {node_id} -->|FAIL| EndFail([Not Eligible])")

    # Handle last node
    if trace:
        last_step = trace[-1]
        last_node_id = f"Step{len(trace)}"
        if last_step.rule_id == "FINAL_RESULT":
            if last_step.passed:
                lines.append(f"    {last_node_id} --> EndSuccess([Eligible])")
            else:
                lines.append(f"    {last_node_id} --> EndFail([Not Eligible])")
        else:
            # If last condition passed
            if last_step.passed:
                lines.append(f"    {last_node_id} --> EndSuccess([Eligible])")

    # Add end nodes
    if "EndSuccess" not in "\n".join(lines):
        lines.append("    EndSuccess([Eligible])")
    if "EndFail" not in "\n".join(lines):
        lines.append("    EndFail([Not Eligible])")

    # Styles
    lines.append("    style Start fill:#e1f5ff,stroke:#333,stroke-width:2px")
    lines.append("    style EndSuccess fill:#d4edda,stroke:#28a745,stroke-width:2px")
    lines.append("    style EndFail fill:#f8d7da,stroke:#dc3545,stroke-width:2px")

    return "\n".join(lines)
