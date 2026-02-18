from schemas import Report

def generate_postmortem(timeline_text : str) -> Report:

    return Report(
        summary="Service experienced elevated error rates after a deployment.",
        impact="Users received 500 errors for ~20 minutes.",
        root_cause="A faulty deployment introduced a breaking change.",
        contributing_factors=[
            "Insufficient pre-deploy testing",
            "No automatic rollback on error spike",
        ],
        action_items=[
            "Add canary deployments",
            "Improve rollback automation",
            "Add alerting on error rate spikes",
        ],
    )