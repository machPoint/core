#!/usr/bin/env python3
"""
Direct database replacement of requirements with improved GOES-R MRDs
"""

import asyncio
import json
import os
import sys
from datetime import datetime

# Add app directory to path for database imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.database import RequirementDocumentDB, RequirementDB, AsyncSessionLocal
from sqlalchemy import select, delete, update

async def replace_requirements():
    """Replace old requirements with improved ones using direct database operations"""
    
    print("🚀 Starting direct database replacement of GOES-R requirements...")
    
    # Step 1: Load improved requirements
    print("\n📄 Loading improved requirements...")
    try:
        with open('improved_goes_r_requirements.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        requirements = data['requirements']
        print(f"✅ Loaded {len(requirements)} improved requirements")
        
    except Exception as e:
        print(f"❌ Failed to load improved requirements: {e}")
        return False
    
    # Step 2: Find the main GOES-R document
    async with AsyncSessionLocal() as session:
        print("\n📋 Finding GOES-R documents in database...")
        
        result = await session.execute(select(RequirementDocumentDB))
        documents = result.scalars().all()
        
        goes_r_docs = [doc for doc in documents if 'GOES-R' in doc.original_filename]
        print(f"Found {len(goes_r_docs)} GOES-R documents:")
        
        for doc in goes_r_docs:
            print(f"   📄 {doc.original_filename} ({doc.requirements_extracted} requirements)")
        
        if not goes_r_docs:
            print("❌ No GOES-R documents found!")
            return False
        
        # Use the PDF document (should have most requirements)
        main_doc = max(goes_r_docs, key=lambda d: d.requirements_extracted or 0)
        document_id = main_doc.id
        print(f"\n🎯 Using document: {main_doc.original_filename} (ID: {document_id})")
        
    # Step 3: Clear old requirements
    async with AsyncSessionLocal() as session:
        print(f"\n🧹 Clearing old requirements for document {document_id}...")
        
        # Count old requirements
        result = await session.execute(
            select(RequirementDB).where(RequirementDB.document_id == document_id)
        )
        old_requirements = result.scalars().all()
        old_count = len(old_requirements)
        print(f"   Found {old_count} old requirements to remove")
        
        # Delete old requirements
        await session.execute(
            delete(RequirementDB).where(RequirementDB.document_id == document_id)
        )
        await session.commit()
        print(f"   ✅ Removed {old_count} old requirements")
    
    # Step 4: Insert improved requirements
    async with AsyncSessionLocal() as session:
        print(f"\n📥 Inserting {len(requirements)} improved requirements...")
        
        inserted_count = 0
        
        for i, req in enumerate(requirements):
            try:
                # Create new requirement record
                req_record = RequirementDB(
                    document_id=document_id,
                    requirement_id=req['id'],
                    title=req['title'],
                    text=req['text'],
                    category=req.get('category', 'general'),
                    priority=req.get('priority', 'medium'),
                    verification_method=req.get('verification_method', 'test'),
                    source_page=req.get('source_page', 1),
                    parent_section=req.get('parent_section', ''),
                    tags=req.get('tags', []),
                    req_metadata={
                        'extractor_version': data.get('extractor_version', 'improved_v2.0'),
                        'extraction_confidence': 0.95,
                        'source_document': req.get('source_document', ''),
                    },
                    extraction_confidence=0.95,
                    status='active'
                )
                
                session.add(req_record)
                inserted_count += 1
                
                # Progress update
                if (i + 1) % 50 == 0:
                    print(f"   Progress: {i + 1}/{len(requirements)} requirements...")
                    
            except Exception as e:
                print(f"   ⚠️ Error inserting {req['id']}: {e}")
                continue
        
        # Commit all insertions
        await session.commit()
        print(f"   ✅ Inserted {inserted_count} requirements")
    
    # Step 5: Update document metadata
    async with AsyncSessionLocal() as session:
        print(f"\n🔄 Updating document metadata...")
        
        await session.execute(
            update(RequirementDocumentDB)
            .where(RequirementDocumentDB.id == document_id)
            .values(
                requirements_extracted=inserted_count,
                processing_status="completed",
                extraction_status="completed",
                processed_at=datetime.utcnow(),
                doc_metadata={
                    'extractor_version': data.get('extractor_version', 'improved_v2.0'),
                    'extraction_date': data.get('extraction_date'),
                    'requirements_replaced': True,
                    'old_count': old_count,
                    'new_count': inserted_count
                }
            )
        )
        await session.commit()
        print(f"   ✅ Updated document with {inserted_count} requirements")
    
    # Step 6: Verify the replacement
    async with AsyncSessionLocal() as session:
        print(f"\n🔍 Verifying replacement...")
        
        result = await session.execute(
            select(RequirementDB).where(RequirementDB.document_id == document_id).limit(10)
        )
        new_requirements = result.scalars().all()
        
        print(f"✅ Database now contains requirements for document {document_id}")
        print(f"   Sample of new requirements:")
        for i, req in enumerate(new_requirements[:5]):
            print(f"   {i+1}. {req.requirement_id}: {req.title[:60]}...")
            print(f"      Category: {req.category}, Priority: {req.priority}")
        
        # Get total count
        result = await session.execute(
            select(RequirementDB).where(RequirementDB.document_id == document_id)
        )
        total_new = len(result.scalars().all())
        
        print(f"\n🎉 Replacement completed successfully!")
        print(f"   • Removed: {old_count} old messy requirements")
        print(f"   • Inserted: {inserted_count} structured MRD requirements") 
        print(f"   • Verified: {total_new} requirements in database")
        
        return True

async def main():
    """Main function"""
    try:
        success = await replace_requirements()
        if success:
            print(f"\n🚀 Ready to regenerate data engine with improved requirements!")
            return True
        else:
            print(f"\n❌ Requirements replacement failed")
            return False
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        raise

if __name__ == "__main__":
    result = asyncio.run(main())
    exit(0 if result else 1)