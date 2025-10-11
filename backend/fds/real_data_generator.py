"""
Real Data Generator
Enhanced data generator that uses real requirements from PDFs instead of purely synthetic data
"""

import random
import uuid
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from faker import Faker
from pathlib import Path
import json

from models import *
from pdf_extractor import PDFRequirementsExtractor, ExtractedRequirement

fake = Faker()

class RealDataGenerator:
    """Generates mock data using real requirements from PDFs as source material"""
    
    def __init__(self, requirements_path: Optional[str] = None):
        self.real_requirements: List[ExtractedRequirement] = []
        self.jama_items: List[JamaItem] = []
        self.jama_relationships: List[JamaRelationship] = []
        self.jira_issues: List[JiraIssue] = []
        self.jira_links: List[JiraLink] = []
        self.windchill_parts: List[WindchillPart] = []
        self.windchill_bom: List[WindchillBOM] = []
        self.windchill_ecn: List[WindchillECN] = []
        self.email_messages: List[EmailMessage] = []
        self.outlook_messages: List[OutlookMessage] = []
        self.pulse_items: List[MockPulseItem] = []
        
        # Load real requirements if provided
        if requirements_path and Path(requirements_path).exists():
            self._load_real_requirements(requirements_path)
        
        # Generate initial data
        self.generate_all_data()
    
    def _load_real_requirements(self, requirements_path: str):
        """Load real requirements from JSON file"""
        try:
            extractor = PDFRequirementsExtractor()
            self.real_requirements = extractor.load_requirements(requirements_path)
            print(f"Loaded {len(self.real_requirements)} real requirements from {requirements_path}")
        except Exception as e:
            print(f"Warning: Could not load requirements from {requirements_path}: {e}")
            self.real_requirements = []

    def load_requirements_from_pdf(self, pdf_path: str, max_pages: Optional[int] = None):
        """Extract requirements directly from PDF"""
        extractor = PDFRequirementsExtractor()
        self.real_requirements = extractor.extract_from_pdf(pdf_path, max_pages)
        print(f"Extracted {len(self.real_requirements)} requirements from PDF")
        
        # Save for future use
        json_path = pdf_path.replace('.pdf', '_requirements.json')
        extractor.save_requirements(self.real_requirements, json_path)
        return json_path

    def generate_all_data(self):
        """Generate all mock data using real requirements when available"""
        print("Generating mock data with real requirements...")
        
        # Generate base data
        self._generate_jama_items_from_real_reqs()
        self._generate_jira_issues_from_real_reqs()
        self._generate_windchill_parts_from_real_reqs()
        self._generate_windchill_ecn_from_real_reqs()
        self._generate_email_messages_from_real_reqs()
        self._generate_outlook_messages_from_real_reqs()
        
        # Generate relationships (with gaps)
        self._generate_jama_relationships()
        self._generate_jira_links()
        self._generate_windchill_bom()
        
        # Generate pulse feed
        self._generate_pulse_feed()
        
        print(f"Generated: {len(self.jama_items)} Jama items, {len(self.jira_issues)} Jira issues, "
              f"{len(self.windchill_parts)} parts, {len(self.windchill_ecn)} ECNs, "
              f"{len(self.email_messages)} emails, {len(self.outlook_messages)} Outlook messages")

    def _generate_jama_items_from_real_reqs(self):
        """Generate Jama items using real requirements"""
        self.jama_items = []
        
        if self.real_requirements:
            # Use real requirements
            for i, real_req in enumerate(self.real_requirements):
                # Create Jama requirement from real requirement
                jama_item = JamaItem(
                    id=str(uuid.uuid4()),
                    global_id=real_req.id,
                    document_key=real_req.source_document.replace('.pdf', '').replace('_', '-'),
                    item_type="requirement",
                    name=real_req.title,
                    description=real_req.text,
                    status=random.choice(["draft", "approved", "under_review", "verified", "validated"]),
                    created_date=fake.date_time_between(start_date="-1y", end_date="now"),
                    modified_date=fake.date_time_between(start_date="-30d", end_date="now"),
                    created_by=fake.name(),
                    modified_by=fake.name(),
                    fields={
                        "priority": real_req.priority,
                        "verification_method": real_req.verification_method or "test",
                        "category": real_req.category,
                        "source_page": real_req.source_page,
                        "tags": real_req.tags,
                        "source_document": real_req.source_document
                    }
                )
                self.jama_items.append(jama_item)
            
            # Generate some test cases based on the real requirements
            test_case_count = min(len(self.real_requirements) // 2, 50)  # Half as many test cases as requirements
            for i in range(test_case_count):
                related_req = random.choice(self.real_requirements)
                test_id = f"TC-{i+1:03d}"
                
                # Generate test case name based on requirement
                test_name = f"Verify {related_req.title[:50]}..."
                test_desc = f"Test case to verify requirement {related_req.id}: {related_req.text[:200]}..."
                
                test_item = JamaItem(
                    id=str(uuid.uuid4()),
                    global_id=f"JAMA-{test_id}",
                    document_key="TEST-PLAN-2024",
                    item_type="test_case",
                    name=test_name,
                    description=test_desc,
                    status=random.choice(["planned", "ready", "in_progress", "completed", "passed", "failed"]),
                    created_date=fake.date_time_between(start_date="-8m", end_date="now"),
                    modified_date=fake.date_time_between(start_date="-14d", end_date="now"),
                    created_by=fake.name(),
                    modified_by=fake.name(),
                    fields={
                        "test_type": related_req.verification_method or "test",
                        "test_phase": random.choice(["development", "qualification", "certification", "production"]),
                        "test_facility": random.choice(["Ground Test Lab", "Integration Facility", "Flight Test", "Simulation Lab"]),
                        "risk_level": random.choice(["low", "medium", "high", "critical"]),
                        "related_requirement": related_req.id,
                        "category": related_req.category
                    }
                )
                self.jama_items.append(test_item)
        else:
            # Fallback to original synthetic generation method
            self._generate_synthetic_jama_items()

    def _generate_synthetic_jama_items(self):
        """Fallback synthetic Jama items generation"""
        # GOES-R inspired requirements
        goes_requirements = [
            ("Advanced Baseline Imager Calibration", "The ABI shall provide radiometric calibration accuracy of ±1% for infrared channels and ±2% for visible channels"),
            ("Geostationary Lightning Mapper Detection", "The GLM shall detect lightning flashes with 70% efficiency during day and 90% efficiency during night"),
            ("Solar Ultraviolet Imager Operations", "The SUVI shall provide full-disk solar images in 6 EUV wavelengths with 1.25 arcsec spatial resolution"),
            ("Extreme Ultraviolet Sensor Monitoring", "The EXIS shall continuously monitor solar X-ray and EUV irradiance with 1-second temporal resolution"),
            ("Magnetometer Field Measurement", "The MAG shall measure the space environment magnetic field with 0.1 nT accuracy in 3 axes"),
            ("Ground System Data Processing", "The Ground System shall process and distribute environmental data products within 30 minutes of observation"),
            ("Spacecraft Pointing Accuracy", "The spacecraft shall maintain pointing stability of ±28 microradians (3-sigma) during normal operations"),
            ("Data Collection System Relay", "The DCS shall relay emergency beacon signals from aircraft, ships, and emergency transmitters"),
            ("Search and Rescue Transponder", "The SARSAT system shall process distress signals and provide location accuracy within 5 km"),
            ("Image Navigation Registration", "The INR system shall provide image navigation accuracy of ±28 microradians (3-sigma)")
        ]
        
        for i, (name, description) in enumerate(goes_requirements):
            req_id = f"GOES-REQ-{i+1:03d}"
            item = JamaItem(
                id=str(uuid.uuid4()),
                global_id=f"JAMA-{req_id}",
                document_key="GOES-R-MRD",
                item_type="requirement",
                name=name,
                description=description,
                status=random.choice(["draft", "approved", "under_review", "verified", "validated"]),
                created_date=fake.date_time_between(start_date="-1y", end_date="now"),
                modified_date=fake.date_time_between(start_date="-30d", end_date="now"),
                created_by=fake.name(),
                modified_by=fake.name(),
                fields={
                    "priority": random.choice(["critical", "high", "medium", "low"]),
                    "verification_method": random.choice(["test", "analysis", "inspection", "demonstration"]),
                    "category": random.choice(["instrument", "ground", "spacecraft", "data"]),
                    "mission": "GOES-R"
                }
            )
            self.jama_items.append(item)

    def _generate_jira_issues_from_real_reqs(self):
        """Generate Jira issues based on real requirements"""
        self.jira_issues = []
        
        if self.real_requirements:
            # Create issues related to requirements implementation and testing
            issue_templates = [
                ("Implement requirement {}", "Implementation task for requirement {} - {}"),
                ("Test requirement {}", "Create and execute test cases for requirement {} - {}"),
                ("Review requirement {}", "Technical review needed for requirement {} - {}"),
                ("Validate requirement {}", "Validation activity for requirement {} - {}"),
                ("Document requirement {}", "Create technical documentation for requirement {} - {}")
            ]
            
            issue_count = min(len(self.real_requirements) // 3, 30)  # About 1/3 as many issues as requirements
            selected_reqs = random.sample(self.real_requirements, issue_count)
            
            for i, req in enumerate(selected_reqs):
                template = random.choice(issue_templates)
                summary = template[0].format(req.id)
                description = template[1].format(req.id, req.title[:100])
                
                # Add more context based on requirement category
                if req.category == "instrument":
                    description += f"\n\nInstrument-specific considerations:\n- Hardware/software integration\n- Calibration procedures\n- Performance verification"
                elif req.category == "data":
                    description += f"\n\nData processing considerations:\n- Algorithm implementation\n- Data format specifications\n- Quality control procedures"
                
                issue = JiraIssue(
                    id=str(uuid.uuid4()),
                    key=f"GOES-{i+1:03d}",
                    summary=summary,
                    description=description,
                    issue_type=random.choice(["task", "story", "defect", "enhancement"]),
                    status=random.choice(["open", "in_progress", "testing", "review", "resolved", "closed"]),
                    priority=req.priority,
                    assignee=fake.name() if random.random() > 0.2 else None,
                    reporter=fake.name(),
                    created=fake.date_time_between(start_date="-6m", end_date="now"),
                    updated=fake.date_time_between(start_date="-7d", end_date="now"),
                    labels=req.tags + [req.category, "GOES-R", "requirement-based"]
                )
                self.jira_issues.append(issue)
        else:
            # Fallback to synthetic generation
            self._generate_synthetic_jira_issues()

    def _generate_synthetic_jira_issues(self):
        """Fallback synthetic Jira issues"""
        goes_issues = [
            "ABI calibration algorithm shows drift in infrared channels during thermal cycling",
            "GLM detection efficiency drops below specification during high background noise",
            "SUVI image quality degrades when solar activity exceeds X-class flare threshold",
            "EXIS sensor readings inconsistent with ground-based solar monitors",
            "MAG magnetometer interference detected from spacecraft subsystems",
        ]
        
        for i, summary in enumerate(goes_issues):
            issue = JiraIssue(
                id=str(uuid.uuid4()),
                key=f"GOES-ISSUE-{i+1:03d}",
                summary=summary,
                description=f"Technical investigation required for: {summary}",
                issue_type="defect",
                status=random.choice(["open", "in_progress", "testing", "resolved"]),
                priority=random.choice(["critical", "high", "medium"]),
                assignee=fake.name(),
                reporter=fake.name(),
                created=fake.date_time_between(start_date="-3m", end_date="now"),
                updated=fake.date_time_between(start_date="-7d", end_date="now"),
                labels=["GOES-R", "instrument", "calibration", "performance"]
            )
            self.jira_issues.append(issue)

    def _generate_windchill_parts_from_real_reqs(self):
        """Generate Windchill parts based on real requirements"""
        self.windchill_parts = []
        
        # GOES-R instrument and spacecraft components
        goes_parts = [
            ("ABI Primary Mirror Assembly", "Primary mirror assembly for Advanced Baseline Imager with protected silver coating"),
            ("GLM Optical Telescope Assembly", "Compact optical telescope for Geostationary Lightning Mapper instrument"),
            ("SUVI CCD Detector Assembly", "Back-illuminated CCD detector for Solar Ultraviolet Imager"),
            ("EXIS Photodiode Array", "Silicon photodiode array for Extreme Ultraviolet and X-ray Irradiance Sensors"),
            ("MAG Fluxgate Sensor", "Triaxial fluxgate magnetometer sensor head with temperature compensation"),
            ("Spacecraft Solar Panel Assembly", "Triple-junction GaAs solar cell assembly with deployable substrate"),
            ("Propulsion Thruster Assembly", "Bipropellant thruster for station-keeping and attitude control"),
            ("S-Band Communication Antenna", "High-gain antenna for telemetry, tracking, and command communications"),
            ("Data Processing Unit", "Solid-state data processor with radiation-hardened components"),
            ("Battery Pack Assembly", "Nickel-hydrogen battery pack for eclipse power management")
        ]
        
        for i, (name, description) in enumerate(goes_parts):
            part = WindchillPart(
                id=str(uuid.uuid4()),
                number=f"GOES-{i+1000:04d}",
                name=name,
                description=description,
                version=f"{random.choice(['A', 'B', 'C'])}.{random.randint(1, 5)}",
                state=random.choice(["in_work", "released", "production", "obsolete"]),
                created_by=fake.name(),
                created_date=fake.date_time_between(start_date="-2y", end_date="-6m"),
                modified_date=fake.date_time_between(start_date="-30d", end_date="now"),
                classification=random.choice(["instrument", "spacecraft", "ground", "electrical", "mechanical"])
            )
            self.windchill_parts.append(part)

    def _generate_windchill_ecn_from_real_reqs(self):
        """Generate ECNs based on real requirements"""
        self.windchill_ecn = []
        
        goes_ecns = [
            ("ABI Optical Filter Specification Update", "Update optical filter specifications for ABI visible channels to improve out-of-band rejection"),
            ("GLM Detector Bias Voltage Modification", "Modify GLM CCD detector bias voltages to reduce dark current and improve sensitivity"),
            ("SUVI Thermal Control Enhancement", "Enhance SUVI thermal control system to maintain detector temperature stability"),
            ("Spacecraft Antenna Pointing Adjustment", "Adjust high-gain antenna pointing mechanism to improve Earth coverage"),
        ]
        
        for i, (title, description) in enumerate(goes_ecns):
            ecn = WindchillECN(
                id=str(uuid.uuid4()),
                number=f"GOES-ECN-2024-{i+1:03d}",
                title=title,
                description=description,
                status=random.choice(["draft", "review", "approved", "released", "implemented"]),
                initiator=fake.name(),
                created_date=fake.date_time_between(start_date="-3m", end_date="now"),
                target_date=fake.date_time_between(start_date="now", end_date="+6m"),
                affected_parts=[random.choice(self.windchill_parts).number for _ in range(random.randint(1, 3))] if self.windchill_parts else []
            )
            self.windchill_ecn.append(ecn)

    def _generate_email_messages_from_real_reqs(self):
        """Generate email messages related to real requirements"""
        self.email_messages = []
        
        # Email templates based on requirements activities
        email_templates = [
            "GOES-R Requirement Review - {} Status Update",
            "Action Required: {} Verification Planning",
            "Weekly Status: {} Implementation Progress", 
            "Certification Update: {} Test Results Available",
            "Design Review: {} Technical Assessment Complete"
        ]
        
        domains = ["nasa.gov", "noaa.gov", "goes-r.gov", "contractor.com"]
        
        for i in range(10):
            if self.real_requirements and random.random() > 0.3:  # 70% chance to use real req
                req = random.choice(self.real_requirements)
                subject = random.choice(email_templates).format(req.id)
                body = f"This email concerns requirement {req.id}: {req.title}\n\n"
                body += f"Current status and recent activities related to this requirement.\n\n"
                body += req.text[:300] + "...\n\n"
                body += "Please review and provide feedback by COB Friday."
            else:
                subject = f"GOES-R Mission Update - Weekly Status Report #{i+1}"
                body = "Weekly mission status update with latest developments and upcoming milestones."
            
            email = EmailMessage(
                id=str(uuid.uuid4()),
                global_id=f"EMAIL-{i+1:03d}",
                subject=subject,
                sender=f"{fake.first_name().lower()}.{fake.last_name().lower()}@{random.choice(domains)}",
                recipients=[f"{fake.first_name().lower()}.{fake.last_name().lower()}@{random.choice(domains)}" for _ in range(random.randint(1, 3))],
                body=body,
                sent_date=fake.date_time_between(start_date="-14d", end_date="now"),
                attachments=[],
                linked_artifacts=[]
            )
            self.email_messages.append(email)

    def _generate_outlook_messages_from_real_reqs(self):
        """Generate Outlook messages for meetings related to requirements"""
        self.outlook_messages = []
        
        meeting_templates = [
            "GOES-R Requirements Review Board - Weekly Meeting",
            "Instrument Calibration Working Group - {} Discussion", 
            "System Integration Team Meeting - {} Status",
            "Test Readiness Review - {} Verification",
            "Design Review Meeting - {} Technical Deep Dive"
        ]
        
        team_members = [
            "Dr. Sarah Mitchell (Mission Systems Engineer)",
            "James Rodriguez (Instrument Lead)",
            "Lisa Chen (Test Engineer)", 
            "Michael Park (Systems Integration)",
            "Anna Kowalski (Quality Assurance)",
            "David Thompson (Project Manager)"
        ]
        
        for i in range(10):
            if self.real_requirements and random.random() > 0.4:  # 60% chance to use real req
                req = random.choice(self.real_requirements)
                subject = random.choice(meeting_templates).format(req.id)
                body = f"Meeting to discuss requirement {req.id}: {req.title}\n\n"
                body += f"Agenda:\n- Review current implementation status\n- Discuss test approach\n- Address technical issues\n\n"
                body += f"Location: Building 5, Conference Room A\nDuration: 1 hour"
            else:
                subject = random.choice(meeting_templates).format("General")
                body = "Regular team meeting to discuss project status and coordination."
            
            outlook = OutlookMessage(
                id=str(uuid.uuid4()),
                global_id=f"OUTLOOK-MSG-{i+1:03d}",
                subject=subject,
                sender=random.choice(team_members),
                recipients=random.sample(team_members, k=random.randint(2, 4)),
                body=body,
                sent_date=fake.date_time_between(start_date="-21d", end_date="now"),
                importance="high" if "review" in subject.lower() else "normal",
                has_attachments=random.random() > 0.6,
                linked_artifacts=[],
                meeting_request=True
            )
            self.outlook_messages.append(outlook)

    # Use existing relationship generation methods from original DataGenerator
    def _generate_jama_relationships(self):
        """Generate Jama relationships with gaps"""
        self.jama_relationships = []
        
        requirements = [item for item in self.jama_items if item.item_type == "requirement"]
        test_cases = [item for item in self.jama_items if item.item_type == "test_case"]
        
        # Create relationships between requirements and test cases (with 15% gaps)
        for req in requirements:
            if random.random() > 0.15:  # 85% coverage
                # Link to 1-3 test cases
                linked_tests = random.sample(test_cases, min(random.randint(1, 3), len(test_cases))) if test_cases else []
                for test in linked_tests:
                    rel = JamaRelationship(
                        id=str(uuid.uuid4()),
                        from_item=req.id,
                        to_item=test.id,
                        relationship_type="verifies",
                        created_date=fake.date_time_between(start_date="-6m", end_date="now")
                    )
                    self.jama_relationships.append(rel)

    def _generate_jira_links(self):
        """Generate Jira issue links"""
        self.jira_links = []
        
        for i, issue in enumerate(self.jira_issues):
            if random.random() > 0.3:  # 70% have links
                # Link to other issues
                other_issues = [iss for iss in self.jira_issues if iss.id != issue.id]
                if other_issues:
                    linked_issue = random.choice(other_issues)
                    link = JiraLink(
                        id=str(uuid.uuid4()),
                        issue_id=issue.id,
                        linked_issue_id=linked_issue.id,
                        link_type=random.choice(["blocks", "relates", "implements", "depends"])
                    )
                    self.jira_links.append(link)

    def _generate_windchill_bom(self):
        """Generate Windchill BOM relationships"""
        self.windchill_bom = []
        
        # Create hierarchical BOM structure
        for parent_part in self.windchill_parts[:5]:  # Top-level assemblies
            child_count = random.randint(2, 4)
            child_parts = random.sample(self.windchill_parts, min(child_count, len(self.windchill_parts)))
            
            for j, child_part in enumerate(child_parts):
                if child_part.id != parent_part.id:
                    bom = WindchillBOM(
                        id=str(uuid.uuid4()),
                        parent_part=parent_part.number,
                        child_part=child_part.number,
                        quantity=float(random.randint(1, 10)),
                        unit=random.choice(["EA", "LB", "FT", "IN"]),
                        find_number=f"{j+1:02d}"
                    )
                    self.windchill_bom.append(bom)

    def _generate_pulse_feed(self):
        """Generate aggregated pulse feed from all sources"""
        self.pulse_items = []
        
        # Create pulse items from recent changes across all systems
        now = datetime.now()
        
        # Jama changes
        for item in self.jama_items:
            if item.modified_date > now - timedelta(days=30):
                pulse_item = MockPulseItem(
                    id=str(uuid.uuid4()),
                    artifact_ref=MockArtifactRef(
                        id=item.global_id,
                        type=item.item_type,
                        source="jama",
                        title=item.name,
                        status=item.status,
                        url=f"http://localhost:8001/mock/windows/jama/{item.global_id}"
                    ),
                    change_type="updated" if item.created_date < item.modified_date else "created",
                    change_summary=f"{item.item_type.title()} '{item.name}' was {'updated' if item.created_date < item.modified_date else 'created'}",
                    timestamp=item.modified_date,
                    author=item.modified_by,
                    metadata={"document": item.document_key}
                )
                self.pulse_items.append(pulse_item)
        
        # Add other pulse items (Jira, emails, etc.) using similar logic...
        # (Reusing the existing pulse generation logic from original DataGenerator)
        
        # Sort by timestamp (newest first)
        self.pulse_items.sort(key=lambda x: x.timestamp, reverse=True)

    # Include all the API methods from the original DataGenerator
    # (get_jama_items, get_jira_issues, etc.)
    def get_jama_items(self, page: int = 1, size: int = 50, query: Optional[str] = None, item_type: Optional[str] = None) -> List[JamaItem]:
        """Get filtered Jama items"""
        items = self.jama_items
        
        if item_type:
            items = [item for item in items if item.item_type == item_type]
        
        if query:
            items = [item for item in items if query.lower() in item.name.lower() or query.lower() in item.description.lower()]
        
        start_idx = (page - 1) * size
        end_idx = start_idx + size
        return items[start_idx:end_idx]
    
    def get_jira_issues(self, page: int = 1, size: int = 50, query: Optional[str] = None, status: Optional[str] = None) -> List[JiraIssue]:
        """Get filtered Jira issues"""
        issues = self.jira_issues
        
        if status:
            issues = [issue for issue in issues if issue.status == status]
        
        if query:
            issues = [issue for issue in issues if query.lower() in issue.summary.lower()]
        
        start_idx = (page - 1) * size
        end_idx = start_idx + size
        return issues[start_idx:end_idx]
    
    # Add remaining API methods as needed...
    # (Following the same pattern as the original DataGenerator)