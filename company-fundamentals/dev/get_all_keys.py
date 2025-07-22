import os
import json
from tqdm import tqdm

# First, download and extract company facts from
# https://www.sec.gov/search-filings/edgar-application-programming-interfaces
# will turn into proper code later.

def get_all_keys(dir):
    files = os.listdir(dir)
    concept_counts = {}

    for file in tqdm(files, desc="Processing files"):
        if not file.endswith('.json'):
            continue
        path = dir + "/" + file
        with open(path, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        if 'facts' not in content:
            continue
        facts = content['facts']
        for taxonomy, concepts in facts.items():
            for concept, data in concepts.items():
                key = (taxonomy, concept)
                if key not in concept_counts:
                    concept_counts[key] = {
                        'count': 1, 
                        'description': data.get('description', '')
                    }
                else:
                    concept_counts[key]['count'] += 1

    with open('taxonomy_concepts.json', 'w') as f:
        json.dump({f"{k[0]}_{k[1]}": v for k, v in concept_counts.items()}, f, indent=2)