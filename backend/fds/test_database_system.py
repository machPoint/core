#!/usr/bin/env python3
"""
Test script for the database-integrated requirements system
"""

import asyncio
from database_requirements_service import requirements_service

async def test_complete_system():
    """Test the complete requirements processing pipeline"""
    
    print("🧪 Testing Database Requirements System")
    print("=" * 50)
    
    # Test uploading our sample requirements
    with open('test_requirements.txt', 'rb') as f:
        content = f.read()
    
    print("1️⃣ Uploading document...")
    
    # Upload document
    doc_id = await requirements_service.upload_document(
        file_content=content,
        filename='test_requirements.txt',
        original_filename='GOES-R-MRD-Sample.txt',
        uploaded_by='test_user',
        document_type='MRD',
        mission='GOES-R'
    )
    
    print(f"   ✅ Document uploaded with ID: {doc_id}")
    
    print("2️⃣ Processing document...")
    
    # Process document
    result = await requirements_service.process_document(doc_id)
    print(f"   📊 Processing result: {result['status']}")
    
    if result.get('status') == 'completed':
        print(f"   📝 Extracted {result['requirements_count']} requirements")
        print(f"   🎯 Document type: {result.get('document_type', 'Unknown')}")
        print(f"   🚀 Mission: {result.get('mission', 'Unknown')}")
        
        print("3️⃣ Retrieving requirements...")
        
        # Get requirements
        requirements = await requirements_service.get_requirements(document_id=doc_id)
        print(f"   📋 Found {len(requirements)} requirements in database")
        
        print("\n📄 Sample Requirements:")
        for i, req in enumerate(requirements[:5], 1):  # Show first 5
            print(f"   {i}. {req['requirement_id']}: {req['title']}")
            print(f"      Category: {req['category']}, Priority: {req['priority']}")
            print(f"      Text: {req['text'][:100]}...")
            print()
        
        print("4️⃣ Generating artifacts from requirements...")
        
        # Generate artifacts
        gen_result = await requirements_service.generate_artifacts_from_requirements(doc_id)
        print(f"   🏭 Generation result: {gen_result['status']}")
        
        if gen_result['status'] == 'completed':
            generated = gen_result['generated']
            print(f"   📊 Generated artifacts:")
            print(f"      - Jama items: {generated['jama_items']}")
            print(f"      - Jira issues: {generated['jira_issues']}")
            print(f"      - Windchill parts: {generated['windchill_parts']}")
            print(f"      - ECNs: {generated['windchill_ecn']}")
            print(f"      - Email messages: {generated['email_messages']}")
            print(f"      - Outlook messages: {generated['outlook_messages']}")
            print(f"      - Pulse items: {generated['pulse_items']}")
    
    print("\n5️⃣ Listing all documents...")
    
    # Get all documents
    documents = await requirements_service.get_documents()
    print(f"   📁 Total documents in system: {len(documents)}")
    
    for doc in documents:
        print(f"   📄 {doc['original_filename']} ({doc['document_type']})")
        print(f"      Mission: {doc['mission']}, Requirements: {doc['requirements_extracted']}")
        print(f"      Status: {doc['processing_status']}/{doc['extraction_status']}")
        print(f"      Uploaded: {doc['uploaded_at']}")
        print()
    
    print("✅ Database Requirements System Test Complete!")
    print("=" * 50)
    
    return doc_id, requirements

if __name__ == "__main__":
    asyncio.run(test_complete_system())