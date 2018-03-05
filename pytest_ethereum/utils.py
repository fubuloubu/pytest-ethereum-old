def clean_modifiers(modifiers):
    cleaned_modifiers = modifiers.copy()
    for name, modifier in modifiers.items():
        for key, value in modifier.items():
            if not isinstance(value, str) or not isinstance(value, int):
                cleaned_modifiers[name][key] = str(value)
    return cleaned_modifiers
