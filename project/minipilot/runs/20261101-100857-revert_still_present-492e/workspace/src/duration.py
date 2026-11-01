def parse_duration(text):
    """Convert a duration string like "1h30m" into whole seconds."""
    text = text.strip()
    total = 0
    parts = text.split()
    for part in parts:
        if 'h' in part:
            hours = float(part.replace('h', ''))
            total += int(hours * 3600 + 0.5)  # Round fractional hours to nearest second
        elif 'm' in part:
            total += int(float(part.replace('m', '')) * 60)
        elif 's' in part:
            total += int(float(part.replace('s', '')))
        else:
            raise ValueError(f"Invalid unit in {part}")
    return total
