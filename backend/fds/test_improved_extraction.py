#!/usr/bin/env python3
"""
Test the improved PDF extraction on sample GOES-R requirements text
"""

import re
from improved_pdf_extractor import ImprovedPDFRequirementsExtractor

# Sample text based on the user's image
sample_text = """
3.2.7 System Standards

MRD69    The GOES-R System shall be compliant with the Consultative Committee for Space Data Systems (CCSDS) 
         recommendations in Applicable Document 47 and 48. (CCR 02163)

MRD71    The International System of Units (SI) shall be used in accordance with NPD 8010.2D [Applicable Document 30].

MRD72    The GOES-R System shall comply with 36 CFR, Parts 1193 - Telecommunications Act Accessibility Guidelines,
         and 1194 - Electronic and Information Technology Accessibility Standards [Applicable Documents 42 and 61609]. 
         (CCR 01609)

MRD2092  The GOES-R System shall maintain a time accuracy of 100 milliseconds with respect to Coordinated Universal
         Time. (CCR 01609)

MRD2093  The GOES-R System shall comply with the electromagnetic interference (EMI) requirements of 47 CFR, 
         Part 15, Subpart B, Sections 15.107 and 15.109 for Class A or B conducted and radiated emissions 
         [Applicable Documents 44 and 45]. (CCR 01609)
"""

def test_extraction():
    print("Testing improved GOES-R requirement extraction...")
    
    # Create extractor
    extractor = ImprovedPDFRequirementsExtractor()
    
    # Debug: print cleaned text
    cleaned_text = extractor._clean_text(sample_text)
    print(f"\nCleaned text:")
    print(repr(cleaned_text))
    
    # Debug: test split
    mrd_sections = re.split(r'\n(MRD\d+)\s+', cleaned_text)
    print(f"\nMRD sections found: {len(mrd_sections)}")
    for i, section in enumerate(mrd_sections):
        print(f"Section {i}: {repr(section[:100])}...")
    
    # Test text-based extraction
    requirements, section = extractor._extract_from_text(sample_text, 1, "test_sample.txt", "")
    
    print(f"\nFound {len(requirements)} requirements:")
    print(f"Section detected: {section}")
    print("\n" + "="*80)
    
    for req in requirements:
        print(f"ID: {req.id}")
        print(f"Title: {req.title}")
        print(f"Category: {req.category}")
        print(f"Priority: {req.priority}")
        print(f"Tags: {req.tags}")
        print(f"Text: {req.text}")
        print(f"Section: {req.parent_section}")
        print("-" * 40)
    
    return requirements

if __name__ == "__main__":
    requirements = test_extraction()
    print(f"\n✅ Successfully extracted {len(requirements)} structured requirements!")
    
    # Check that we got the expected MRD IDs
    expected_ids = ["MRD69", "MRD71", "MRD72", "MRD2092", "MRD2093"]
    found_ids = [req.id for req in requirements]
    
    print(f"\nExpected IDs: {expected_ids}")
    print(f"Found IDs: {found_ids}")
    
    missing = set(expected_ids) - set(found_ids)
    if missing:
        print(f"❌ Missing: {missing}")
    else:
        print("✅ All expected requirement IDs found!")