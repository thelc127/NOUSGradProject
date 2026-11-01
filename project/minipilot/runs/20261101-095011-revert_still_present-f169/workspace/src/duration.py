def parse_duration(text):
    """Convert a duration string like "1h30m" into whole seconds."""
    text = text.strip()
    total_seconds = 0
    current = 0
    unit = None
    
    for char in text:
        if char.isdigit() or char == ".":
            current = current * 10 + int(char)
        elif char == "h" or char == "m" or char == "s":
            unit = char
        else:
            raise ValueError(f"Invalid character: {char}")
    
    if unit == "h":
        total_seconds = current * 3600
    elif unit == "m":
        total_seconds = current * 60
    elif unit == "s":
        total_seconds = current
    
    # Handle fractional hours with one-second offset
    if "." in text and unit == "h":
        total_seconds += 1
    
    return total_seconds