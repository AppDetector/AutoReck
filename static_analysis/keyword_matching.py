# Keyword Matching
def is_matched_keyword(variable):
    with open('predefined_files/fields.txt', 'r') as f:
        pre_fields = f.read().split('\n')
    for pre_field in pre_fields:
        if pre_field in variable.lower():
            return True
    return False
