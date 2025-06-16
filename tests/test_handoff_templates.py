from src.handoff_templates import task_completion, work_request, coordination_signal, error_signal


def test_signal_templates() -> None:
    s1 = task_completion("done")
    assert s1["category"] == "state"
    s2 = work_request("work", "agent")
    assert s2["target"] == "agent"
    s3 = coordination_signal("coord", "agent2")
    assert s3["category"] == "coordinate"
    s4 = error_signal("err")
    assert s4["strength"] >= 8.5
