from .fundamentals import extract_parameters
from .mappings.mappings import mappings
from .calculations.calculations import calculations

def get_fundamental_mappings(fundamentals):
    reverse_mappings = {v: k for k, v in mappings.items()}
    required_fields = set()
    
    for fundamental in fundamentals:
        # Check if fundamental is in selected fields
        for category in calculations.values():
            if fundamental in category.get('selected', []):
                required_fields.add(fundamental)
        
        # Check if fundamental is a calculated field
        for category in calculations.values():
            if fundamental in category.get('calculations', {}):
                formula = category['calculations'][fundamental]
                params = extract_parameters(formula)
                required_fields.update(params)
    
    # Convert field names to (taxonomy, concept) tuples
    result = []
    for field in required_fields:
        if field in reverse_mappings:
            result.append(reverse_mappings[field])
    
    return list(set(result))