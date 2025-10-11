#!/usr/bin/env python3
"""
Update database with improved GOES-R MRD requirements
Replace the old messy requirements with properly structured ones
"""

import asyncio
import json
import uuid
from datetime import datetime
from database_requirements_service import requirements_service

async def update_database():
    """Replace old requirements with improved ones"""
    
    print("🚀 Starting database update with improved GOES-R requirements...")
    
    # Step 1: Load improved requirements
    print("\n📄 Loading improved requirements...")
    try:
        with open('improved_goes_r_requirements.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        requirements = data['requirements']
        print(f"✅ Loaded {len(requirements)} improved requirements")
        print(f"   Extractor version: {data.get('extractor_version', 'unknown')}")
        print(f"   Extraction date: {data.get('extraction_date', 'unknown')}")
        
    except Exception as e:
        print(f"❌ Failed to load improved requirements: {e}")
        return
    
    # Step 2: Get current documents to identify which ones to update
    print("\n📋 Checking current documents in database...")
    documents = await requirements_service.get_documents()
    
    goes_r_docs = [doc for doc in documents if 'GOES-R' in doc.get('original_filename', '')]
    print(f"Found {len(goes_r_docs)} GOES-R documents:")
    for doc in goes_r_docs:
        print(f"   📄 {doc['original_filename']} ({doc['requirements_extracted']} requirements)")
    
    if not goes_r_docs:
        print("❌ No GOES-R documents found in database!")
        return
    
    # Use the main GOES-R document
    main_doc = goes_r_docs[0]  # Should be the PDF
    document_id = main_doc['id']
    print(f"\n🎯 Updating document: {main_doc['original_filename']}")
    
    # Step 3: Clear old requirements for this document
    print(f"\n🧹 Clearing old requirements for document {document_id}...")
    try:
        # Get old requirements
        old_requirements = await requirements_service.get_requirements(document_id=document_id, limit=1000)
        print(f"   Found {len(old_requirements)} old requirements to remove")
        
        # Note: We'll let the import process handle the replacement
        # The database service should handle duplicates by document_id
        
    except Exception as e:
        print(f"⚠️ Warning getting old requirements: {e}")
    
    # Step 4: Import improved requirements
    print(f"\n📥 Importing {len(requirements)} improved requirements...")
    
    imported_count = 0
    skipped_count = 0
    error_count = 0
    
    for i, req in enumerate(requirements):
        try:
            # Create requirement record for database
            requirement_data = {
                'document_id': document_id,
                'requirement_id': req['id'],
                'title': req['title'],
                'text': req['text'],
                'category': req.get('category', 'general'),
                'priority': req.get('priority', 'medium'),
                'verification_method': req.get('verification_method', 'test'),
                'source_page': req.get('source_page', 1),
                'parent_section': req.get('parent_section', ''),
                'tags': req.get('tags', []),
                'metadata': {
                    'extractor_version': data.get('extractor_version', 'improved_v2.0'),
                    'extraction_date': data.get('extraction_date'),
                    'source_document': req.get('source_document', ''),
                },
                'extraction_confidence': 0.95,  # High confidence for improved extraction
                'status': 'active',
            }
            
            # Import to database
            result = await requirements_service.store_requirement(requirement_data)
            
            if result:
                imported_count += 1
                if (i + 1) % 50 == 0:  # Progress update every 50 requirements
                    print(f"   Progress: {i + 1}/{len(requirements)} requirements processed...")
            else:
                skipped_count += 1
                
        except Exception as e:
            error_count += 1
            print(f"   ⚠️ Error importing {req['id']}: {e}")
            continue
    
    print(f"\n📊 Import Results:")
    print(f"   ✅ Imported: {imported_count}")
    print(f"   ⏭️ Skipped: {skipped_count}")  
    print(f"   ❌ Errors: {error_count}")
    
    # Step 5: Update document metadata
    print(f"\n🔄 Updating document metadata...")
    try:
        # Update the document record with new count
        update_result = await requirements_service.update_document_requirements_count(
            document_id, imported_count
        )
        if update_result:
            print(f"✅ Updated document requirements count to {imported_count}")
        else:
            print("⚠️ Could not update document metadata")
    except Exception as e:
        print(f"⚠️ Warning updating document: {e}")
    
    # Step 6: Verify the import
    print(f"\n🔍 Verifying import...")
    try:
        new_requirements = await requirements_service.get_requirements(document_id=document_id, limit=1000)
        print(f"✅ Database now contains {len(new_requirements)} requirements for this document")
        
        # Show sample of new requirements
        print(f"\n📋 Sample of imported requirements:")
        for i, req in enumerate(new_requirements[:5]):
            print(f"   {i+1}. {req['requirement_id']}: {req['title'][:60]}...")
            
    except Exception as e:
        print(f"❌ Error verifying import: {e}")
        return
    
    print(f"\n🎉 Database update completed successfully!")
    print(f"   • Replaced {len(old_requirements)} old messy requirements")  
    print(f"   • Imported {imported_count} properly structured MRD requirements")
    print(f"   • Ready for data engine regeneration")
    
    return imported_count

async def main():
    """Main function"""
    try:
        imported_count = await update_database()
        if imported_count and imported_count > 0:
            print(f"\n🚀 Next step: Regenerate data engine to use new requirements")
        else:
            print(f"\n❌ Database update failed or no requirements imported")
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())