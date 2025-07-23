from mappings.mappings import mappings
from calculations.calculations import calculations
import re
from datetime import datetime, timedelta


VAR_PATTERN = re.compile(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b(?!\s*\[)')

def extract_parameters(formula):
    return list(set(VAR_PATTERN.findall(formula)))


def evaluate_lagged_formula_by_periods(formula, parameters, concepts, start_date_key, end_date_key, lag_tolerance_days=30):
    results = []
    
    # Group by date tuples
    date_groups = {}
    for concept in concepts:
        date_key = (concept.get(start_date_key), concept.get(end_date_key))
        if date_key not in date_groups:
            date_groups[date_key] = []
        date_groups[date_key].append(concept)
    
    # Parse lag syntax from formula
    lag_pattern = re.compile(r'(\w+)\s*\[year,(-?\d+)\]')
    lag_matches = lag_pattern.findall(formula)

    
    for date_key, period_concepts in date_groups.items():
        try:
            # Get current period values
            concept_values = {c['standardized_concept_name']: float(c['value']) for c in period_concepts}

            
            # For each lagged variable, find the matching historical period
            all_values = concept_values.copy()
            
            for var_name, lag_years in lag_matches:
                lag_years = int(lag_years)
                if lag_years >= 0:
                    continue  # Skip non-negative lags
                
                # Calculate target date (lag_years is negative, so this goes back in time)
                current_end_date = datetime.strptime(date_key[1], '%Y-%m-%d') if date_key[1] else None
                if not current_end_date:
                    continue
                    
                target_date = current_end_date.replace(year=current_end_date.year + lag_years)
                
                # Find matching historical period within tolerance
                historical_value = None
                for hist_date_key, hist_concepts in date_groups.items():
                    if not hist_date_key[1]:
                        continue
                    hist_end_date = datetime.strptime(hist_date_key[1], '%Y-%m-%d')
                    
                    if abs((hist_end_date - target_date).days) <= lag_tolerance_days:
                        hist_values = {c['standardized_concept_name']: float(c['value']) for c in hist_concepts}
                        if var_name in hist_values:
                            historical_value = hist_values[var_name]
                            break
                
                if historical_value is None:
                    # Skip this calculation if we can't find historical data
                    all_values = None
                    break
                
                # Add lagged value with unique key
                lag_key = f"{var_name}_lag_{abs(lag_years)}"
                all_values[lag_key] = historical_value
            
            if all_values is None:
                continue
                

            # Replace lagged variables in formula
            safe_formula = formula
            for var_name, lag_years in lag_matches:
                lag_years = int(lag_years)
                if lag_years >= 0:
                    continue
                lag_key = f"{var_name}_lag_{abs(lag_years)}"
                safe_formula = safe_formula.replace(f"{var_name} [year,{lag_years}]", lag_key)
            
    
            sorted_vars = sorted(all_values.items(), key=lambda x: len(x[0]), reverse=True)
            for var_name, value in sorted_vars:
                safe_formula = safe_formula.replace(var_name, str(value))


            # Evaluate
            result = eval(safe_formula, {"__builtins__": {}}, {})
            results.append({
                'value': result,
                start_date_key: date_key[0],
                end_date_key: date_key[1]
            })
            
        except Exception as e:
            continue
    
    return results



def evaluate_formula_by_periods(formula, parameters, concepts, start_date_key, end_date_key):
    results = []
    
    # Group by date tuples
    date_groups = {}
    for concept in concepts:
        date_key = (concept.get(start_date_key), concept.get(end_date_key))
        if date_key not in date_groups:
            date_groups[date_key] = []
        date_groups[date_key].append(concept)
    
    # Evaluate for each period
    for date_key, period_concepts in date_groups.items():
        concept_values = {c['standardized_concept_name']: float(c['value']) for c in period_concepts}
        
        if all(param in concept_values for param in parameters):
            # Simple string replacement (safer than eval)
            safe_formula = formula
            for var_name, value in concept_values.items():
                safe_formula = safe_formula.replace(var_name, str(value))
            
            try:
                result = eval(safe_formula, {"__builtins__": {}}, {})
                results.append({
                    'value': result,
                    start_date_key: date_key[0],
                    end_date_key: date_key[1]
                })
            except:
                pass
    
    return results



# yeah so we should go calc by calc,
def calculate_fundamentals(standardized_concepts, categories, start_date_key, end_date_key):
    fundamentals_dict = {}
    category_dict = {}

    for category in calculations.keys():
        # if categories is None, it means all.
        if categories is not None:
            if category not in categories:
                continue

        if 'selected' in calculations[category].keys():
            for indicator in calculations[category]['selected']:
                matches = [
                    {k: v for k, v in item.items() if k != 'standardized_concept_name'}
                    for item in standardized_concepts 
                    if item['standardized_concept_name'] == indicator
                ]
                                

                if matches:
                    category_dict[indicator] = matches

        if 'calculations' in calculations[category].keys():
            for indicator in calculations[category]['calculations']:
                formula = calculations[category]['calculations'][indicator]
                
                # Extract parameters and concepts FIRST
                parameters = extract_parameters(formula)
                concepts = [item for item in standardized_concepts if item['standardized_concept_name'] in parameters]
                
                # THEN check for lagged formulas
                if '[' in formula:
                    results = evaluate_lagged_formula_by_periods(formula, parameters, concepts, start_date_key, end_date_key)
                    if results:
                        category_dict[indicator] = results
                    continue
                
                # Regular formula evaluation
                results = evaluate_formula_by_periods(formula, parameters, concepts, start_date_key, end_date_key)
                if results:
                    category_dict[indicator] = results

        if category_dict:
            fundamentals_dict[category] = category_dict
            category_dict = {}

    return fundamentals_dict        



def construct_fundamentals(data, taxonomy_key, concept_key, start_date_key, end_date_key, categories=None):
    standardized_concepts = []
    for concept in data:
        mapping_key = (concept[taxonomy_key], concept[concept_key])
        if mapping_key in mappings:
            standardized_concept_name = mappings[mapping_key]
            # Create a new dict excluding taxonomy_key and concept_key
            new_concept = {k: v for k, v in concept.items() if k not in [taxonomy_key, concept_key]}
            new_concept['standardized_concept_name'] = standardized_concept_name
            standardized_concepts.append(new_concept)


    fundamentals = calculate_fundamentals(standardized_concepts, categories, start_date_key, end_date_key)
    return fundamentals


# test_lagged = [
#     {'taxonomy': 'us-gaap', 'name': 'NetIncomeLoss', 'value': '120000', 'period_start_date': '2024-01-01', 'period_end_date': '2024-12-31'},
#     {'taxonomy': 'us-gaap', 'name': 'NetIncomeLoss', 'value': '100000', 'period_start_date': '2023-01-01', 'period_end_date': '2023-12-31'},
# ]

# results = construct_fundamentals(test_lagged, 'taxonomy', 'name', 'period_start_date', 'period_end_date')
# print(results)