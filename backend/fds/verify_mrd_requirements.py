#!/usr/bin/env python3
"""
Verify the new MRD requirements are in the database
"""

import asyncio
from database_requirements_service import requirements_service

async def verify_requirements():
    print("🔍 Verifying MRD requirements in database...")
    
    # Get all requirements
    requirements = await requirements_service.get_requirements(limit=500)
    print(f"Total requirements found: {len(requirements)}")
    
    # Filter for MRD requirements
    mrd_reqs = [r for r in requirements if r['requirement_id'].startswith('MRD')]
    old_reqs = [r for r in requirements if not r['requirement_id'].startswith('MRD')]
    
    print(f"MRD requirements: {len(mrd_reqs)}")
    print(f"Non-MRD requirements: {len(old_reqs)}")
    
    if mrd_reqs:
        print(f"\n📋 Sample MRD requirements:")
        for i, req in enumerate(mrd_reqs[:10]):
            print(f"{i+1:2d}. {req['requirement_id']}: {req['title'][:60]}...")
            
        print(f"\n🎯 MRD ID range:")
        mrd_ids = [int(r['requirement_id'][3:]) for r in mrd_reqs if r['requirement_id'][3:].isdigit()]
        if mrd_ids:
            print(f"   Lowest: MRD{min(mrd_ids)}")
            print(f"   Highest: MRD{max(mrd_ids)}")
            print(f"   Count: {len(mrd_ids)} numeric MRD IDs")
    else:
        print("❌ No MRD requirements found!")
    
    if old_reqs:
        print(f"\n⚠️ Found {len(old_reqs)} non-MRD requirements:")
        for req in old_reqs[:3]:
            print(f"   • {req['requirement_id']}: {req['title'][:50]}...")

if __name__ == "__main__":
    asyncio.run(verify_requirements())