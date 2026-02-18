from schemas import Report

def render_markdown(report : Report, incident_id : str) -> str:
    md = f""" # Incident {incident_id} Report

    ## Summary
    {report.summary}

    ## Impact
    {report.impact}

    ##Root Cause
    {report.root_cause}

    ##Factors
    """
    for f in report.factors:
        md += f" -{f}\n"

    md += "\n## Action Items\n"
    for a in report.action_items:
        md += f"- {a}\n"
    
    return md
