def format_notes(note):
    if pd.isna(note) or not note.strip():
        return ''
    # Split by double newlines
    comments = [c for c in note.split('\n\n') if c.strip()]
    
    # If only one comment, return it as is without numbering
    if len(comments) == 1:
        comment = comments[0]
        # Extract id and date if present
        m = re.match(r'(\d+)\s+([\d\-: ]+):', comment)
        if m:
            note_id, note_date = m.group(1), m.group(2)
            rest = comment[m.end():].lstrip()
            return f'{note_id} {note_date}: {rest}'
        return comment
        
    # For multiple comments, add numbering
    formatted = []
    for idx, comment in enumerate(comments, 1):
        # Try to extract id and date at the start (pattern: id date: ...)
        m = re.match(r'(\d+)\s+([\d\-: ]+):', comment)
        if m:
            note_id, note_date = m.group(1), m.group(2)
            rest = comment[m.end():].lstrip()
            formatted.append(f'note {idx}: {note_id} {note_date}: {rest}')
        else:
            formatted.append(f'note {idx}: {comment}')
    return '\n\n'.join(formatted)
