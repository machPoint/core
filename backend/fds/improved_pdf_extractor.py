"""
Improved PDF Requirements Extractor for GOES-R Mission Requirements
Specifically designed to extract structured MRD requirements
"""

import re
import json
from typing import List, Dict, Any, Optional, Tuple
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

class ImprovedPDFRequirementsExtractor:
    """Extract requirements from GOES-R MRD documents with precise parsing"""
    
    def __init__(self):
        # Specific GOES-R MRD requirement patterns
        self.mrd_patterns = [
            # Pattern 1: MRD### followed by requirement text until next MRD or section
            # Handle multi-line requirements with proper termination
            r'(MRD\d+)\s+([^\n]+(?:\n\s+[^\nM][^\n]*)*?)(?=\n\s*MRD\d+|\n\s*\d+\.\d+|\n\s*[A-Z][a-z]|\Z)',
            
            # Pattern 2: Simple MRD on its own line
            r'^(MRD\d+)\s+(.+?)(?=^MRD\d+|\Z)',
            
            # Pattern 3: MRD with continuation lines (indented)
            r'(MRD\d+)\s+(.+?)(?=MRD\d+|\d+\.\d+\s+[A-Z]|\Z)',
        ]
        
        # Section patterns to identify parent sections
        self.section_patterns = [
            r'(\d+\.\d+(?:\.\d+)*)\s+([A-Za-z\s]+?)(?=\n)',  # "3.2.7 System Standards"
            r'([A-Z][A-Za-z\s]+?)(?=\n\s*MRD\d+)',  # Section title before MRD
        ]
        
        # GOES-R specific categories based on content
        self.goes_categories = {
            'standards': ['standard', 'compliance', 'CCSDS', 'CFR', 'regulation'],
            'accuracy': ['accuracy', 'precision', 'error', 'tolerance', 'calibration'],
            'timing': ['time', 'timing', 'millisecond', 'second', 'latency', 'delay'],
            'communication': ['electromagnetic', 'interference', 'EMI', 'RF', 'emission'],
            'instrument': ['ABI', 'GLM', 'EXIS', 'SUVI', 'MAG', 'instrument', 'sensor'],
            'data': ['data', 'image', 'product', 'measurement', 'observation'],
            'system': ['system', 'platform', 'spacecraft', 'subsystem'],
            'performance': ['performance', 'capability', 'requirement', 'operation'],
            'environmental': ['environmental', 'temperature', 'radiation', 'vibration']
        }
        
        # Priority determination
        self.priority_keywords = {
            'critical': ['shall', 'must', 'critical', 'mandatory', 'essential'],
            'high': ['shall', 'important', 'primary', 'key'],
            'medium': ['should', 'normal', 'standard'],
            'low': ['may', 'optional', 'desired']
        }

    def extract_from_pdf(self, pdf_path: str, max_pages: Optional[int] = None) -> List[ExtractedRequirement]:
        """Extract requirements from GOES-R MRD PDF"""
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        logger.info(f"Extracting GOES-R requirements from: {pdf_path.name}")
        
        requirements = []
        current_section = ""
        
        # Use pdfplumber for better table/structure handling
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            pages_to_process = min(max_pages or total_pages, total_pages)
            
            for page_num, page in enumerate(pdf.pages[:pages_to_process]):
                try:
                    text = page.extract_text() or ""
                    
                    # Try to extract from tables first (more structured)
                    table_reqs = self._extract_from_tables(page, page_num + 1, pdf_path.name)
                    if table_reqs:
                        requirements.extend(table_reqs)
                        logger.info(f"Page {page_num + 1}: Extracted {len(table_reqs)} requirements from tables")
                        continue
                    
                    # Fallback to text extraction
                    text_reqs, current_section = self._extract_from_text(
                        text, page_num + 1, pdf_path.name, current_section
                    )
                    requirements.extend(text_reqs)
                    
                    if text_reqs:
                        logger.info(f"Page {page_num + 1}: Extracted {len(text_reqs)} requirements from text")
                        
                except Exception as e:
                    logger.warning(f"Error processing page {page_num + 1}: {e}")
                    continue
        
        # Post-process and clean up
        requirements = self._post_process_requirements(requirements, pdf_path.name)
        
        logger.info(f"Total extracted GOES-R requirements: {len(requirements)}")
        return requirements

    def _extract_from_tables(self, page, page_num: int, doc_name: str) -> List[ExtractedRequirement]:
        """Extract requirements from tabular format"""
        requirements = []
        
        try:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if not row or len(row) < 2:
                        continue
                    
                    # Look for MRD pattern in first column
                    first_col = str(row[0] or "").strip()
                    second_col = str(row[1] or "").strip()
                    
                    if re.match(r'MRD\d+', first_col) and second_col:
                        # Found a requirement
                        req_id = first_col
                        req_text = second_col
                        
                        # Clean up the requirement text
                        req_text = self._clean_requirement_text(req_text)
                        
                        if len(req_text) > 20 and self._is_valid_requirement(req_text):
                            requirement = self._create_requirement(
                                req_id, req_text, page_num, doc_name
                            )
                            requirements.append(requirement)
                            
        except Exception as e:
            logger.debug(f"Table extraction failed for page {page_num}: {e}")
        
        return requirements

    def _extract_from_text(self, text: str, page_num: int, doc_name: str, 
                          current_section: str) -> Tuple[List[ExtractedRequirement], str]:
        """Extract requirements from plain text"""
        requirements = []
        
        # Clean up text
        text = self._clean_text(text)
        
        # Update current section if we find a new one
        section_match = re.search(r'(\d+\.\d+(?:\.\d+)*)\s+([A-Za-z\s\-]+)', text)
        if section_match:
            current_section = f"{section_match.group(1)} {section_match.group(2).strip()}"
        
        # Split text by MRD markers to get individual requirements
        mrd_sections = re.split(r'\n(MRD\d+)\s+', text)
        
        # Process each MRD section
        for i in range(1, len(mrd_sections), 2):  # Skip first empty part, then take pairs
            if i + 1 < len(mrd_sections):
                req_id = mrd_sections[i].strip()
                req_text = mrd_sections[i + 1].strip()
                
                # Clean up requirement text - remove next MRD if captured
                req_text = re.split(r'\nMRD\d+', req_text)[0].strip()
                
                # Clean and validate
                req_text = self._clean_requirement_text(req_text)
                
                if len(req_text) > 20 and self._is_valid_requirement(req_text):
                    requirement = self._create_requirement(
                        req_id, req_text, page_num, doc_name, current_section
                    )
                    requirements.append(requirement)
        
        return requirements, current_section

    def _clean_text(self, text: str) -> str:
        """Clean extracted text for better parsing - preserve line structure"""
        # Remove page headers/footers first
        text = re.sub(r'Page \d+ of \d+', '', text, flags=re.IGNORECASE)
        text = re.sub(r'GOES-R.*?MRD.*?\d{4}', '', text, flags=re.IGNORECASE)
        
        # Remove table separators
        text = re.sub(r'\|+', ' ', text)
        
        # Normalize whitespace within lines but preserve line breaks
        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            # Remove excessive whitespace within lines
            cleaned_line = re.sub(r'\s+', ' ', line.strip())
            if cleaned_line:  # Only keep non-empty lines
                cleaned_lines.append(cleaned_line)
        
        return '\n'.join(cleaned_lines)

    def _clean_requirement_text(self, text: str) -> str:
        """Clean individual requirement text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove leading/trailing punctuation artifacts
        text = re.sub(r'^[^\w]+|[^\w\.\)]+$', '', text)
        
        # Fix common OCR/extraction issues
        text = re.sub(r'\bshall\s+shall\b', 'shall', text, flags=re.IGNORECASE)
        text = re.sub(r'\bthe\s+the\b', 'the', text, flags=re.IGNORECASE)
        
        return text.strip()

    def _is_valid_requirement(self, text: str) -> bool:
        """Check if text is a valid requirement"""
        text_lower = text.lower()
        
        # Must contain requirement indicators
        required_indicators = ['shall', 'must', 'will', 'should']
        has_indicator = any(indicator in text_lower for indicator in required_indicators)
        
        # Should not be just a section header or table artifact
        invalid_patterns = [
            r'^\d+\.\d+\s*$',  # Just section numbers
            r'^[A-Z\s]+$',     # Just uppercase headings
            r'^\s*$',          # Empty or whitespace
        ]
        
        is_invalid = any(re.match(pattern, text) for pattern in invalid_patterns)
        
        return has_indicator and not is_invalid and len(text) > 15

    def _create_requirement(self, req_id: str, req_text: str, page_num: int, 
                          doc_name: str, section: str = "") -> ExtractedRequirement:
        """Create a structured requirement object"""
        
        # Generate title from first part of requirement
        title = self._generate_title(req_text)
        
        # Categorize requirement
        category = self._categorize_requirement(req_text)
        
        # Determine priority
        priority = self._determine_priority(req_text)
        
        # Extract verification method
        verification = self._extract_verification_method(req_text)
        
        # Extract tags
        tags = self._extract_tags(req_text)
        
        return ExtractedRequirement(
            id=req_id,
            title=title,
            text=req_text,
            category=category,
            priority=priority,
            source_page=page_num,
            source_document=doc_name,
            verification_method=verification,
            parent_section=section,
            tags=tags
        )

    def _generate_title(self, text: str) -> str:
        """Generate concise title from requirement text"""
        # Look for subject before "shall"
        shall_match = re.search(r'(.+?)\s+shall\s+(.+?)(?:\.|\s|$)', text, re.IGNORECASE)
        if shall_match:
            subject = shall_match.group(1).strip()
            action = shall_match.group(2).strip()
            
            # Clean up subject
            subject = re.sub(r'^The\s+', '', subject, flags=re.IGNORECASE)
            
            # Create concise title
            title = f"{subject} - {action}"
            if len(title) > 80:
                title = title[:77] + "..."
            return title
        
        # Fallback to first sentence
        first_sentence = text.split('.')[0]
        if len(first_sentence) <= 80:
            return first_sentence.strip()
        else:
            return text[:77].strip() + "..."

    def _categorize_requirement(self, text: str) -> str:
        """Categorize requirement based on content"""
        text_lower = text.lower()
        
        # Score each category
        category_scores = {}
        for category, keywords in self.goes_categories.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                category_scores[category] = score
        
        if category_scores:
            return max(category_scores, key=category_scores.get)
        
        return "general"

    def _determine_priority(self, text: str) -> str:
        """Determine requirement priority"""
        text_lower = text.lower()
        
        if 'shall' in text_lower:
            return 'high'
        elif 'must' in text_lower:
            return 'critical'
        elif 'should' in text_lower:
            return 'medium'
        elif 'may' in text_lower:
            return 'low'
        else:
            return 'medium'

    def _extract_verification_method(self, text: str) -> str:
        """Extract verification method from requirement"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['test', 'testing', 'verify']):
            return 'test'
        elif any(word in text_lower for word in ['analysis', 'calculate', 'compute']):
            return 'analysis'
        elif any(word in text_lower for word in ['inspect', 'review', 'examine']):
            return 'inspection'
        elif any(word in text_lower for word in ['demonstrate', 'show', 'prove']):
            return 'demonstration'
        else:
            return 'test'  # Default

    def _extract_tags(self, text: str) -> List[str]:
        """Extract relevant tags"""
        text_lower = text.lower()
        tags = []
        
        tag_keywords = {
            'compliance': ['compliant', 'compliance', 'conform'],
            'accuracy': ['accuracy', 'accurate', 'precision', 'precise'],
            'timing': ['time', 'timing', 'latency', 'delay'],
            'interface': ['interface', 'interfacing', 'connect'],
            'monitoring': ['monitor', 'monitoring', 'observe'],
            'automatic': ['automatic', 'automated', 'auto'],
            'real-time': ['real-time', 'real time', 'realtime']
        }
        
        for tag, keywords in tag_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                tags.append(tag)
        
        return tags

    def _post_process_requirements(self, requirements: List[ExtractedRequirement], 
                                 doc_name: str) -> List[ExtractedRequirement]:
        """Clean up and deduplicate requirements"""
        # Remove duplicates based on ID
        unique_requirements = {}
        
        for req in requirements:
            if req.id not in unique_requirements:
                unique_requirements[req.id] = req
            else:
                # Keep the one with longer text (more complete)
                if len(req.text) > len(unique_requirements[req.id].text):
                    unique_requirements[req.id] = req
        
        result = list(unique_requirements.values())
        
        # Sort by requirement ID
        try:
            result.sort(key=lambda x: int(re.search(r'MRD(\d+)', x.id).group(1)))
        except:
            pass  # Keep original order if sorting fails
        
        logger.info(f"Removed {len(requirements) - len(result)} duplicate requirements")
        return result

    def save_requirements(self, requirements: List[ExtractedRequirement], output_path: str):
        """Save extracted requirements to JSON file"""
        data = {
            'extraction_date': datetime.now().isoformat(),
            'total_requirements': len(requirements),
            'extractor_version': 'improved_v2.0',
            'requirements': [asdict(req) for req in requirements]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(requirements)} requirements to {output_path}")

# CLI interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Extract GOES-R MRD requirements from PDF")
    parser.add_argument("pdf_path", help="Path to GOES-R MRD PDF file")
    parser.add_argument("-o", "--output", help="Output JSON file", default="goes_r_requirements.json")
    parser.add_argument("-p", "--pages", type=int, help="Max pages to process")
    
    args = parser.parse_args()
    
    extractor = ImprovedPDFRequirementsExtractor()
    requirements = extractor.extract_from_pdf(args.pdf_path, args.pages)
    
    print(f"\nExtracted {len(requirements)} GOES-R requirements:")
    for req in requirements[:10]:  # Show first 10
        print(f"  {req.id}: {req.title}")
    
    if len(requirements) > 10:
        print(f"  ... and {len(requirements) - 10} more")
    
    extractor.save_requirements(requirements, args.output)
    print(f"\nSaved to: {args.output}")