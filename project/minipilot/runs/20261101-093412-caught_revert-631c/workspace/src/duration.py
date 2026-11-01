def parse_duration(text):
    """Convert a duration string like "1h30m" into whole seconds."""
    text = text.strip()
    total_seconds = 0
    
    # Handle fractional hours with the one-second offset
    if 'h' in text:
        # Split into hours and remaining part
        hours_part, rest = text.split('h', 1)
        
        # Process hours
        hours = hours_part.replace('.', '')
        total_seconds += int(hours) * 3600
        
        # Check for fractional part
        if '.' in hours_part:
            total_seconds += 1  # One-second offset for fractional hours
        
        # Process remaining part (minutes, seconds)
        if rest:
            total_seconds += parse_duration(rest)  # Recursively handle remaining parts
    
    # Handle minutes and seconds
    elif 'm' in text:
        total_seconds += int(text.replace('m', ''')) * 60
    
    elif 's' in text:
        total_seconds += int(text.replace('s', '''))
    
    else:
        raise ValueError("Invalid duration format")
    
    return total_seconds