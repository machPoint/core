#!/usr/bin/env python3
import asyncio
from database_requirements_service import requirements_service

async def check_requirements():
    print('📊 Checking all GOES-R requirements in database...')
    
    # Get all requirements
    all_reqs = await requirements_service.get_requirements(limit=1000)
    print(f'Total requirements in database: {len(all_reqs)}')
    
    # Show sample of requirements
    print(f'\n📋 Sample of requirements:')
    for i, req in enumerate(all_reqs[:10]):
        print(f'{i+1:2d}. ID: {req.get("requirement_id", "N/A")[:50]}...')
        print(f'    Title: {req.get("title", "N/A")[:80]}...')
        print(f'    Text: {req.get("text", "N/A")[:80]}...')
        print(f'    Document: {req.get("document_id", "N/A")}')
        print(f'    Keys: {list(req.keys())}')
        print()
    
    # Check documents
    documents = await requirements_service.get_documents()
    print(f'📄 Documents in system: {len(documents)}')
    for doc in documents:
        print(f'   • {doc["original_filename"]} ({doc["document_type"]})')
        print(f'     Mission: {doc["mission"]}, Requirements: {doc["requirements_extracted"]}')
    
    return len(all_reqs)

if __name__ == "__main__":
    asyncio.run(check_requirements())