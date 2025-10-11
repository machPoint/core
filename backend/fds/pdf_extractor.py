"""
PDF Requirements Extractor
Extracts structured requirements from mission requirement documents (PDFs)
"""

import re
import json
from typing import List, Dict, Any, Optional
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime
import pdfplumber
import fitz  # PyMuPDF
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ExtractedRequirement:
    """Structured requirement extracted from PDF"""
    id: str
    title: str
    text: str
    category: str = ""
    priority: str = "medium"
    source_page: int = 0
    source_document: str = ""
    verification_method: str = ""
    parent_section: str = ""
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []

class PDFRequirementsExtractor:
    """Extract requirements from PDF documents"""
    
    def __init__(self):
        # Common requirement patterns (order matters - more specific patterns first)
        self.req_patterns = [
            # MRD/REQ format with multi-line text
            r'(MRD-\d+(?:\.\d+)*):?\s*(.+?)(?=\n(?:MRD-|REQ-|$))',
            r'(REQ-\d+(?:\.\d+)*):?\s*(.+?)(?=\n(?:MRD-|REQ-|$))',
            
            # Generic requirement ID patterns  
            r'([A-Z]{2,5}-\d+(?:\.\d+)*):?\s*(.+?)(?=\n(?:[A-Z]{2,5}-\d+|$))',
            
            # NASA style numbered requirements
            r'(\d+\.\d+(?:\.\d+)*)[:\.]?\s*(.+?)(?=\n\d+\.\d+|\n\n|$)',
            
            # "The system shall" standalone requirements
            r'((?:The\s+)?(?:system|satellite|instrument|subsystem|ABI|GLM|SUVI|EXIS|MAG)\s+shall\s+.+?)(?=\n\n|\n(?:The\s+(?:system|satellite|instrument|subsystem)|MRD-|REQ-|$))',
        ]
        
        # GOES-R specific categories
        self.goes_categories = {
            'instrument': ['ABI', 'GLM', 'EXIS', 'SUVI', 'MAG', 'instrument', 'sensor', 'detector'],
            'data': ['data', 'image', 'product', 'measurement', 'observation', 'calibration'],
            'ground': ['ground', 'processing', 'distribution', 'archive', 'dissemination'],
            'spacecraft': ['spacecraft', 'platform', 'orbit', 'attitude', 'power', 'thermal'],
            'communication': ['communication', 'telemetry', 'command', 'RF', 'antenna'],
            'performance': ['performance', 'accuracy', 'precision', 'resolution', 'timing'],
            'operational': ['operational', 'availability', 'reliability', 'maintenance', 'backup'],
            'environmental': ['environmental', 'temperature', 'radiation', 'contamination', 'vibration']
        }
        
        # Priority keywords
        self.priority_keywords = {
            'critical': ['critical', 'mandatory', 'essential', 'safety'],
            'high': ['high', 'important', 'primary', 'key'],
            'medium': ['medium', 'normal', 'standard'],
            'low': ['low', 'optional', 'desired', 'nice']
        }

    def extract_from_pdf(self, pdf_path: str, max_pages: Optional[int] = None) -> List[ExtractedRequirement]:
        """Extract requirements from PDF using multiple methods"""
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        logger.info(f"Extracting requirements from: {pdf_path.name}")
        
        # Try pdfplumber first (better for structured text)
        requirements = []
        try:
            requirements.extend(self._extract_with_pdfplumber(pdf_path, max_pages))
            logger.info(f"pdfplumber extracted {len(requirements)} requirements")
        except Exception as e:
            logger.warning(f"pdfplumber failed: {e}")
        
        # Fallback to PyMuPDF
        if len(requirements) < 5:  # If we didn't get many requirements
            try:
                pymupdf_reqs = self._extract_with_pymupdf(pdf_path, max_pages)
                requirements.extend(pymupdf_reqs)
                logger.info(f"PyMuPDF extracted {len(pymupdf_reqs)} additional requirements")
            except Exception as e:
                logger.warning(f"PyMuPDF failed: {e}")
        
        # Post-process and clean up
        requirements = self._post_process_requirements(requirements, pdf_path.name)
        
        logger.info(f"Total extracted requirements: {len(requirements)}")
        return requirements

    def _extract_with_pdfplumber(self, pdf_path: Path, max_pages: Optional[int]) -> List[ExtractedRequirement]:
        """Extract using pdfplumber"""
        requirements = []
        
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            pages_to_process = min(max_pages or total_pages, total_pages)
            
            for page_num, page in enumerate(pdf.pages[:pages_to_process]):
                try:
                    text = page.extract_text() or ""
                    page_requirements = self._extract_requirements_from_text(
                        text, page_num + 1, pdf_path.name
                    )
                    requirements.extend(page_requirements)
                except Exception as e:
                    logger.warning(f"Error processing page {page_num + 1}: {e}")
                    continue
        
        return requirements

    def _extract_with_pymupdf(self, pdf_path: Path, max_pages: Optional[int]) -> List[ExtractedRequirement]:
        """Extract using PyMuPDF (fallback)"""
        requirements = []
        
        with fitz.open(pdf_path) as pdf:
            total_pages = len(pdf)
            pages_to_process = min(max_pages or total_pages, total_pages)
            
            for page_num in range(pages_to_process):
                try:
                    page = pdf[page_num]
                    text = page.get_text()
                    page_requirements = self._extract_requirements_from_text(
                        text, page_num + 1, pdf_path.name
                    )
                    requirements.extend(page_requirements)
                except Exception as e:
                    logger.warning(f"Error processing page {page_num + 1}: {e}")
                    continue
        
        return requirements

    def _extract_requirements_from_text(self, text: str, page_num: int, doc_name: str) -> List[ExtractedRequirement]:
        """Extract requirements from text using regex patterns"""
        requirements = []
        
        # Clean up text
        text = self._clean_text(text)
        
        # Try each pattern
        for pattern in self.req_patterns:
            matches = re.finditer(pattern, text, re.MULTILINE | re.DOTALL | re.IGNORECASE)
            
            for match in matches:
                groups = match.groups()
                
                if len(groups) >= 2 and groups[1]:  # ID, text format
                    req_id = groups[0].strip()
                    req_text = groups[1].strip()
                elif len(groups) >= 1:  # Single capture group (full requirement)
                    req_text = groups[0].strip()
                    req_id = self._generate_req_id(req_text, page_num)
                else:
                    continue
                
                # Skip if too short or doesn't look like a requirement
                if len(req_text) < 20 or not self._looks_like_requirement(req_text):
                    continue
                
                # Extract additional info
                category = self._categorize_requirement(req_text)
                priority = self._determine_priority(req_text)
                verification = self._extract_verification_method(req_text)
                tags = self._extract_tags(req_text)
                
                requirement = ExtractedRequirement(
                    id=req_id,
                    title=self._generate_title(req_text),
                    text=req_text,
                    category=category,
                    priority=priority,
                    source_page=page_num,
                    source_document=doc_name,
                    verification_method=verification,
                    tags=tags
                )
                
                requirements.append(requirement)
        
        return requirements

    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove page headers/footers patterns
        text = re.sub(r'Page \d+ of \d+', '', text, flags=re.IGNORECASE)
        text = re.sub(r'GOES-R.*?MRD.*?\d{4}', '', text, flags=re.IGNORECASE)
        # Remove table artifacts
        text = re.sub(r'\|\s*\|', '', text)
        return text.strip()

    def _looks_like_requirement(self, text: str) -> bool:
        """Check if text looks like a requirement"""
        requirement_indicators = [
            'shall', 'must', 'will', 'should', 'required', 'requirement',
            'accuracy', 'performance', 'capability', 'function', 'operation'
        ]
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in requirement_indicators)

    def _categorize_requirement(self, text: str) -> str:
        """Categorize requirement based on content"""
        text_lower = text.lower()
        
        for category, keywords in self.goes_categories.items():
            if any(keyword in text_lower for keyword in keywords):
                return category
        
        return "general"

    def _determine_priority(self, text: str) -> str:
        """Determine requirement priority"""
        text_lower = text.lower()
        
        for priority, keywords in self.priority_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return priority
        
        # Default priority based on "shall" vs "should"
        if 'shall' in text_lower:
            return 'high'
        elif 'should' in text_lower:
            return 'medium'
        else:
            return 'medium'

    def _extract_verification_method(self, text: str) -> str:
        """Extract verification/validation method"""
        text_lower = text.lower()
        
        methods = {
            'test': ['test', 'testing', 'verification test'],
            'analysis': ['analysis', 'calculation', 'computation'],
            'inspection': ['inspection', 'review', 'examination'],
            'demonstration': ['demonstration', 'demo', 'show']
        }
        
        for method, keywords in methods.items():
            if any(keyword in text_lower for keyword in keywords):
                return method
        
        return 'test'  # Default

    def _extract_tags(self, text: str) -> List[str]:
        """Extract relevant tags from requirement text"""
        text_lower = text.lower()
        tags = []
        
        # Technical tags
        tech_tags = {
            'real-time': ['real-time', 'real time'],
            'accuracy': ['accuracy', 'precise', 'precision'],
            'calibration': ['calibration', 'calibrated'],
            'automation': ['automatic', 'automated'],
            'backup': ['backup', 'redundant', 'redundancy'],
            'monitoring': ['monitor', 'monitoring'],
            'processing': ['process', 'processing'],
            'interface': ['interface', 'interfacing']
        }
        
        for tag, keywords in tech_tags.items():
            if any(keyword in text_lower for keyword in keywords):
                tags.append(tag)
        
        return tags

    def _generate_req_id(self, text: str, page_num: int) -> str:
        """Generate requirement ID if not found"""
        # Try to find existing ID patterns in the text
        id_match = re.search(r'([A-Z]{2,4}-\d+(?:\.\d+)*)', text)
        if id_match:
            return id_match.group(1)
        
        # Generate based on content hash
        import hashlib
        content_hash = hashlib.md5(text.encode()).hexdigest()[:6]
        return f"REQ-{page_num:03d}-{content_hash.upper()}"

    def _generate_title(self, text: str) -> str:
        """Generate a concise title for the requirement"""
        # Take first sentence or first 80 characters
        first_sentence = text.split('.')[0]
        if len(first_sentence) <= 80:
            return first_sentence.strip()
        else:
            return text[:80].strip() + "..."

    def _post_process_requirements(self, requirements: List[ExtractedRequirement], doc_name: str) -> List[ExtractedRequirement]:
        """Clean up and deduplicate requirements"""
        # Remove duplicates based on text similarity
        unique_requirements = []
        seen_texts = set()
        
        for req in requirements:
            # Create a normalized version for comparison
            normalized_text = re.sub(r'\s+', ' ', req.text.lower()).strip()
            
            if normalized_text not in seen_texts:
                seen_texts.add(normalized_text)
                unique_requirements.append(req)
        
        logger.info(f"Removed {len(requirements) - len(unique_requirements)} duplicate requirements")
        return unique_requirements

    def save_requirements(self, requirements: List[ExtractedRequirement], output_path: str):
        """Save extracted requirements to JSON file"""
        data = {
            'extraction_date': datetime.now().isoformat(),
            'total_requirements': len(requirements),
            'requirements': [asdict(req) for req in requirements]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(requirements)} requirements to {output_path}")

    def load_requirements(self, json_path: str) -> List[ExtractedRequirement]:
        """Load requirements from JSON file"""
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        requirements = []
        for req_data in data['requirements']:
            req = ExtractedRequirement(**req_data)
            requirements.append(req)
        
        return requirements

# CLI interface for testing
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Extract requirements from PDF")
    parser.add_argument("pdf_path", help="Path to PDF file")
    parser.add_argument("-o", "--output", help="Output JSON file", default="extracted_requirements.json")
    parser.add_argument("-p", "--pages", type=int, help="Max pages to process")
    
    args = parser.parse_args()
    
    extractor = PDFRequirementsExtractor()
    requirements = extractor.extract_from_pdf(args.pdf_path, args.pages)
    
    print(f"\nExtracted {len(requirements)} requirements:")
    for req in requirements[:5]:  # Show first 5
        print(f"  {req.id}: {req.title}")
    
    if len(requirements) > 5:
        print(f"  ... and {len(requirements) - 5} more")
    
    extractor.save_requirements(requirements, args.output)
    print(f"\nSaved to: {args.output}")