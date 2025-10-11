#!/usr/bin/env python3
"""
Check the quality of improved GOES-R requirements extraction
"""

import json

def check_quality():
    with open('improved_goes_r_requirements.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📊 Extraction Summary:")
    print(f"Total requirements: {data['total_requirements']}")
    print(f"Extraction date: {data['extraction_date']}")
    print(f"Extractor version: {data['extractor_version']}")
    print()
    
    requirements = data['requirements']
    
    # Check for proper MRD IDs
    mrd_ids = [req['id'] for req in requirements if req['id'].startswith('MRD')]
    print(f"🆔 MRD Requirements: {len(mrd_ids)}")
    print(f"Sample MRD IDs: {mrd_ids[:10]}")
    print()
    
    # Check categories
    categories = {}
    for req in requirements:
        cat = req.get('category', 'unknown')
        categories[cat] = categories.get(cat, 0) + 1
    
    print(f"📂 Categories found:")
    for cat, count in sorted(categories.items()):
        print(f"   {cat}: {count}")
    print()
    
    # Check for "shall" statements
    shall_count = sum(1 for req in requirements if 'shall' in req['text'].lower())
    print(f"📜 Requirements with 'shall': {shall_count}/{len(requirements)} ({shall_count/len(requirements)*100:.1f}%)")
    print()
    
    print("📋 Sample Requirements:")
    for i, req in enumerate(requirements[:5]):
        print(f"{i+1:2d}. {req['id']}: {req['title']}")
        print(f"    Text: {req['text'][:150]}...")
        print(f"    Category: {req['category']}, Priority: {req['priority']}")
        if req.get('parent_section'):
            print(f"    Section: {req['parent_section']}")
        print()

if __name__ == "__main__":
    check_quality()