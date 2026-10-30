def analyze_ticket(description):
    '''Analayze a support ticket using simple predefined rules.

    This is a mock analyzer, not a ral AI model.
    It simulates the structured output a real model could return later
    
    '''

    # Normalize the description to make keyword checks
    # easier, regardless of capitalization
    text = description.lower()

    # Start with sensible defualt values
    category = 'General IT support'
    priority = 'Medium'
    summary = description
    troubleshooting_steps = [
        'Review the issue and gather any relevant details.',
        'Try to reproduce the problem.',
        'Escalate to IT support if the issue persists.'
    ]
    explanation = (
        'The issue did not match a specific predefined category. '
        'General troubleshooting steps have been recommended'
    )

    # Identify common network-related issues
    if any(word in text for word in [
        'wi-fi', 'wifi', 'internet', 'network', 'connection'
    ]):
        category = 'Network Connectivity'
        troubleshooting_steps = [
            'Check whether the device is connected to the correct network.',
            'Check whether other devices can connect.',
            'Reconnect to the network and test again.',
            'Escalate to IT support if the issue persists.'
        ]
        explanation = (
            "The ticket contains network-related keywords. "
            "The recommended steps focus on checking connectivity, "
            "network availability, and reconnection."
        )

    # Identify common account and access issues
    elif any(word in text for word in [
        'password', 'login', 'log in', 'locked out', 'sign in', 'logging in', 'unable to log in',
    ]):
        category = 'Account Access'
        troubleshooting_steps = [
            "Confirm the username or employee ID is correct.",
            "Check whether the account is locked.",
            "Use the approved password-reset process if needed.",
            "Escalate to IT support if access is still unavailable."
        ]
        explanation = (
            "The ticket contains account-access-related keywords. "
            "The recommended steps focus on verifying account details, "
            "checking account status, and using approved recovery procedures."
        )

    # Identify common hardware-related issues.
    elif any(word in text for word in [
        "laptop", "keyboard", "mouse", "monitor", "printer"
    ]):
        category = "Hardware Issue"
        troubleshooting_steps = [
            "Check the device's power and physical connections.",
            "Restart the affected device if appropriate.",
            "Check whether the problem continues.",
            "Escalate to IT support if the issue persists."
        ]
        explanation = (
            "The ticket contains hardware-related keywords. "
            "The recommended steps focus on checking physical connections, "
            "device operation, and whether the issue persists."
        )

    # Mark potentially urgent issues with a higher priority.
    if any(word in text for word in [
        "urgent", "critical", "entire office", "all users",
        "system down", "security breach", 'system is down'
    ]):
        priority = "High"

    # Return predictable, structured data.
    return {
        "category": category,
        "priority": priority,
        "summary": summary,
        "troubleshooting_steps": troubleshooting_steps,
        "explanation": explanation
        
    }


    