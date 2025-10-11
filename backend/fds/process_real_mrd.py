#!/usr/bin/env python3
"""
Process Real GOES-R MRD Document
Extracts all requirements from the actual GOES-R Mission Requirements Document
and stores them in the database with proper metadata and connections
"""

import asyncio
import os
from pathlib import Path
from typing import List, Dict, Any
from database_requirements_service import requirements_service
from pdf_extractor import PDFRequirementsExtractor

class GOESRMRDProcessor:
    """Specialized processor for GOES-R Mission Requirements Document"""
    
    def __init__(self):
        self.extractor = PDFRequirementsExtractor()
        self.data_dir = Path(__file__).parent.parent / "data"
        
        # GOES-R specific patterns for better extraction
        self.enhanced_patterns = [
            # Standard MRD format: "MRD-XXX" followed by text
            r'(MRD-\d+(?:\.\d+)*):?\s*(.+?)(?=\n(?:MRD-\d+|$))',
            
            # Requirement sections with numbering
            r'(\d+\.\d+(?:\.\d+)*)\s+(.+?)(?=\n\d+\.\d+|\n\n|$)',
            
            # "The system shall" requirements
            r'(The\s+(?:GOES-R\s+)?(?:system|satellite|ground\s+system|spacecraft)\s+shall\s+.+?)(?=\n(?:The\s+(?:GOES-R\s+)?(?:system|satellite|ground\s+system|spacecraft)\s+shall|\n\n|$))',
            
            # Instrument-specific requirements
            r'(The\s+(?:ABI|GLM|SUVI|EXIS|MAG|DCS|SARSAT)\s+shall\s+.+?)(?=\n(?:The\s+(?:ABI|GLM|SUVI|EXIS|MAG|DCS|SARSAT)\s+shall|\n\n|$))',
            
            # Performance requirements
            r'((?:Performance|Operational|Functional)\s+[Rr]equirement[s]?:?\s*.+?)(?=\n(?:Performance|Operational|Functional)\s+[Rr]equirement|\n\n|$)',
        ]
        
        # GOES-R specific categorization
        self.goes_categories = {
            'ABI': ['ABI', 'Advanced Baseline Imager', 'imager', 'imaging', 'visible', 'infrared', 'spectral'],
            'GLM': ['GLM', 'Geostationary Lightning Mapper', 'lightning', 'flash', 'detection'],
            'SUVI': ['SUVI', 'Solar Ultraviolet Imager', 'solar', 'ultraviolet', 'UV', 'sun'],
            'EXIS': ['EXIS', 'Extreme Ultraviolet', 'X-ray', 'solar irradiance', 'EUV'],
            'MAG': ['MAG', 'magnetometer', 'magnetic field', 'space weather'],
            'DCS': ['DCS', 'Data Collection System', 'data collection', 'platform'],
            'SARSAT': ['SARSAT', 'Search and Rescue', 'distress', 'emergency beacon'],
            'spacecraft': ['spacecraft', 'satellite', 'platform', 'orbit', 'attitude', 'pointing'],
            'ground': ['ground system', 'ground segment', 'processing', 'distribution', 'GRBF'],
            'communication': ['communication', 'telemetry', 'command', 'RF', 'antenna', 'downlink', 'uplink'],
            'data': ['data', 'product', 'processing', 'algorithm', 'calibration', 'navigation'],
            'operational': ['operational', 'mission', 'timeline', 'availability', 'reliability'],
            'performance': ['performance', 'accuracy', 'precision', 'resolution', 'sensitivity', 'range']
        }
    
    def enhance_extractor(self):
        """Enhance the PDF extractor with GOES-R specific patterns"""
        # Add our enhanced patterns to the extractor
        self.extractor.req_patterns.extend(self.enhanced_patterns)
        
        # Update categorization with GOES-R specifics
        self.extractor.goes_categories.update(self.goes_categories)
    
    async def process_mrd_document(self, max_pages: int = None) -> Dict[str, Any]:
        """Process the GOES-R MRD document"""
        
        mrd_path = self.data_dir / "MRD.pdf"
        
        if not mrd_path.exists():
            raise FileNotFoundError(f"MRD.pdf not found in {self.data_dir}")
        
        print(f"🔍 Processing GOES-R MRD: {mrd_path}")
        print(f"📄 File size: {mrd_path.stat().st_size / 1024 / 1024:.1f} MB")
        
        # Enhance extractor for GOES-R
        self.enhance_extractor()
        
        # Read and upload the document
        with open(mrd_path, 'rb') as f:
            file_content = f.read()
        
        print("📤 Uploading document to database...")
        
        document_id = await requirements_service.upload_document(
            file_content=file_content,
            filename="GOES-R-MRD.pdf",
            original_filename="GOES-R Mission Requirements Document.pdf",
            uploaded_by="mrd_processor",
            document_type="MRD",
            mission="GOES-R"
        )
        
        print(f"✅ Document uploaded with ID: {document_id}")
        print("🔧 Processing document to extract requirements...")
        
        # Process the document
        processing_result = await requirements_service.process_document(document_id)
        
        print(f"📊 Processing completed: {processing_result['status']}")
        
        if processing_result['status'] == 'completed':
            req_count = processing_result['requirements_count']
            print(f"📝 Successfully extracted {req_count} requirements")
            
            # Get all extracted requirements
            requirements = await requirements_service.get_requirements(document_id=document_id, limit=1000)
            
            # Analyze the requirements
            await self.analyze_requirements(requirements)
            
            # Generate artifacts from the real requirements
            print("🏭 Generating artifacts from real GOES-R requirements...")
            artifact_result = await requirements_service.generate_artifacts_from_requirements(document_id)
            
            if artifact_result['status'] == 'completed':
                generated = artifact_result['generated']
                print(f"✨ Generated realistic artifacts:")
                print(f"   📋 Jama items: {generated['jama_items']}")
                print(f"   🎫 Jira issues: {generated['jira_issues']}")
                print(f"   🔧 Windchill parts: {generated['windchill_parts']}")
                print(f"   📄 ECNs: {generated['windchill_ecn']}")
                print(f"   📧 Email messages: {generated['email_messages']}")
                print(f"   📅 Outlook messages: {generated['outlook_messages']}")
                print(f"   📊 Pulse items: {generated['pulse_items']}")
            
            return {
                'document_id': document_id,
                'requirements_extracted': req_count,
                'requirements': requirements,
                'artifacts_generated': artifact_result
            }
        else:
            print(f"❌ Processing failed: {processing_result.get('error', 'Unknown error')}")
            return {'error': processing_result.get('error'), 'document_id': document_id}
    
    async def analyze_requirements(self, requirements: List[Dict[str, Any]]):
        """Analyze the extracted requirements and show statistics"""
        
        print("\n📈 Requirements Analysis:")
        print("=" * 40)
        
        # Category breakdown
        categories = {}
        priorities = {}
        verification_methods = {}
        
        for req in requirements:
            # Count categories
            cat = req.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1
            
            # Count priorities
            pri = req.get('priority', 'unknown')
            priorities[pri] = priorities.get(pri, 0) + 1
            
            # Count verification methods
            ver = req.get('verification_method', 'unknown')
            verification_methods[ver] = verification_methods.get(ver, 0) + 1
        
        print(f"📊 Category Distribution:")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"   {cat}: {count}")
        
        print(f"\n🎯 Priority Distribution:")
        for pri, count in sorted(priorities.items(), key=lambda x: x[1], reverse=True):
            print(f"   {pri}: {count}")
        
        print(f"\n🔬 Verification Methods:")
        for ver, count in sorted(verification_methods.items(), key=lambda x: x[1], reverse=True):
            print(f"   {ver}: {count}")
        
        # Show some sample requirements
        print(f"\n📋 Sample Real GOES-R Requirements:")
        print("-" * 40)
        
        for i, req in enumerate(requirements[:10], 1):  # Show first 10
            print(f"{i:2d}. {req['requirement_id']}")
            print(f"    📝 {req['title']}")
            print(f"    🏷️  Category: {req['category']}, Priority: {req['priority']}")
            print(f"    📍 Page: {req.get('source_page', '?')}")
            if req.get('tags'):
                print(f"    🏷️  Tags: {', '.join(req['tags'])}")
            print(f"    📄 Text: {req['text'][:150]}...")
            print()

async def main():
    """Main processing function"""
    
    print("🚀 GOES-R MRD Processing Pipeline")
    print("=" * 50)
    
    processor = GOESRMRDProcessor()
    
    try:
        # Process the MRD document
        result = await processor.process_mrd_document()
        
        if 'error' not in result:
            print(f"\n🎉 SUCCESS!")
            print(f"📄 Document ID: {result['document_id']}")
            print(f"📝 Requirements extracted: {result['requirements_extracted']}")
            print(f"🏭 Artifacts generated: {result['artifacts_generated']['status']}")
            
            print(f"\n🔗 You can now:")
            print(f"   1. Start the FDS server: python start_fds.py")
            print(f"   2. View requirements via: http://localhost:8001/mock/admin/requirements")
            print(f"   3. Access realistic data via all FDS endpoints")
            print(f"   4. Use the Data Engine page to manage requirements")
            
        else:
            print(f"\n❌ Processing failed: {result['error']}")
            
    except Exception as e:
        print(f"\n💥 Error during processing: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    asyncio.run(main())