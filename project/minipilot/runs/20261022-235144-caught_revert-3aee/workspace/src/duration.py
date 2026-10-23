def parse_duration(text):
    """Convert a duration string like "1h30m" into whole seconds."""
    text = text.strip()
    total_seconds = 0
    parts = text.split()

    for part in parts:
        if 'h' in part:
            hours = float(part.replace('h', ''))
            total_seconds += int(hours * 3600 + 0.5)  # Round half hours
        elif 'm' in part:
            minutes = float(part.replace('m', ''))
            total_seconds += int(minutes * 60 + 0.5)  # Round half minutes
        elif 's' in part:
            seconds = float(part.replace('s', ''))
            total_seconds += int(seconds + 0.5)  # Round half seconds
        else:
            raise ValueError(f"Invalid unit in {part}")

    return total_seconds