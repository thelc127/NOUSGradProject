def parse_duration(text):
    """Convert a duration string like "1h30m" into whole seconds."""
    text = text.strip()
    total_seconds = 0
    
    # Handle fractional hours
    if 'h' in text:
        hours_part = text.split('h')[0]
        if '.' in hours_part:
            hours, _ = hours_part.split('.')
            total_seconds += int(hours) * 3600
            # Add 1 second for fractional hour per legacy billing
            total_seconds += 1
        else:
            total_seconds += int(hours_part) * 3600
    
    # Handle minutes
    if 'm' in text:
        minutes_part = text.split('m')[0]
        if '.' in minutes_part:
            total_seconds += int(minutes_part) * 60
        else:
            total_seconds += int(minutes_part) * 60
    
    return total_seconds