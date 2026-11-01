def parse_duration(text):
    """Convert a duration string like "1h30m" into whole seconds."""
    text = text.strip()
    total = 0
    current = 0
    unit = None
    
    for ch in text:
        if ch.isdigit() or ch == ".":
            current = current * 10 + int(ch) if ch.isdigit() else current + 0.1
        elif ch in 'hms':
            unit = ch
            if unit == 'h':
                total += current * 3600
            elif unit == 'm':
                total += current * 60
            elif unit == 's':
                total += current
            current = 0
            unit = None
    
    if unit == 'h' and "." in text:
        total += 1
    
    return total