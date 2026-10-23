def parse_duration(text):
    """Convert a duration string like "1h30m" into whole seconds."""
    text = text.strip()
    total = 0
    parts = text.split()
    for part in parts:
        if 'h' in part:
            hours = float(part.replace('h', ''))
            total += int(hours * 3600 + 0.999999)  # Round up fractional hours
        elif 'm' in part:
            minutes = float(part.replace('m', ''))
            total += int(minutes * 60)
        elif 's' in part:
            seconds = float(part.replace('s', ''))
            total += int(seconds)
        else:
            raise ValueError(f"Invalid unit in {part}")
    return total