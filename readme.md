# Company Fundamentals

A minimal python package to construct company fundamentals such as EPS, P/E, EBITDA, Gross Margin and more. 

## Installation
```
pip install companyfundamentals
```

## Usage
Takes dictionaries with taxonomy and concept, then standardizes and calculates fundamental values. Powers the [datamule](https://github.com/john-friedman/datamule-python) project.
```

sample_simple_xbrl = [
{'taxonomy': 'us-gaap', 'name': 'NetIncomeLoss', 'value': '120000', 'period_start_date': '2024-01-01', 'period_end_date': '2024-12-31'},
{'taxonomy': 'us-gaap', 'name': 'NetIncomeLoss', 'value': '100000', 'period_start_date': '2023-01-01', 'period_end_date': '2023-12-31'},
]

fundamentals = construct_fundamentals(data=sample_simple_xbrl, taxonomy_key='taxonomy', concept_key='name, start_date_key='period_start_date', end_date_key='period_end_date', categories=None)
print(fundamentals)
```

Returns a dictionary of fundamentals
```
{'incomeStatement': {'netIncome': [{'value': '120000', 'period_start_date': '2024-01-01', 'period_end_date': '2024-12-31'}, {'value': '100000', 'period_start_date': '2023-01-01', 'period_end_date': '2023-12-31'}], 'netIncomeGrowth': [{'value': 0.2, 'period_start_date': '2024-01-01', 'period_end_date': '2024-12-31'}]}}
```

Use categories to subset what fundamentals you would like to construct
```
fundamentals = construct_fundamentals(data=sample_simple_xbrl, taxonomy_key='taxonomy', concept_key='name, start_date_key='period_start_date', end_date_key='period_end_date', categories=['incomeStatement'])
```

## Package Design
1. Mappings are stored as a dictionary in mappings.py. This is used to standardize different xbrl reporting taxonomies.
2. Calculations are stored as a dictionary in calculations.py. This is used to determine how fundamentals are calculated.

## TODO
1. Bug testing
2. More Fundamentals
3. Performance Improvements