def validate_ticket_description(description):
    '''Validate a support ticket description

    Returns:
        tuple:(validated_description, error_message)
        if valid, error_message is None
        if invalid, validated_description is None
        
    '''

    # Ensure the sescription is text
    if not isinstance(description, str):
        return None, 'Description must be a string'

    # Remove whitespace from the beginning and end
    description = description.strip()

    # Reject descriptions containing only whitespace
    if not description:
        return None, 'Description cannot be empty'

    # Prevent excessivley long descriptions
    if len(description) > 2000:
        return None, 'Description cannot exceed 2000 characters'

    # If all checks pass, return the validated description
    return description, None