"""
Data Generator for Fake Data Service
Generates realistic mock data for engineering systems
"""

import random
import uuid
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from faker import Faker

from models import *

fake = Faker()


class DataGenerator:
    """Generates and manages mock data for all engineering systems"""
    
    def __init__(self):
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
        
        # Generate initial data
        self.generate_all_data()
    
    def generate_all_data(self):
        """Generate all mock data"""
        print("Generating mock data...")
        
        # Generate base data
        self._generate_jama_items()
        self._generate_jira_issues()
        self._generate_windchill_parts()
        self._generate_windchill_ecn()
        self._generate_email_messages()
        self._generate_outlook_messages()
        
        # Generate relationships (with gaps)
        self._generate_jama_relationships()
        self._generate_jira_links()
        self._generate_windchill_bom()
        
        # Generate pulse feed
        self._generate_pulse_feed()
        
        print(f"Generated: {len(self.jama_items)} Jama items, {len(self.jira_issues)} Jira issues, "
              f"{len(self.windchill_parts)} parts, {len(self.windchill_ecn)} ECNs, "
              f"{len(self.email_messages)} emails, {len(self.outlook_messages)} Outlook messages")
    
    def _generate_jama_items(self):
        """Generate Jama requirements and test cases for aerospace systems"""
        self.jama_items = []
        
        # Aerospace requirement templates
        aero_requirements = [
            "Flight Control System shall maintain aircraft stability during all flight phases",
            "Avionics Navigation System shall provide GPS accuracy within 3 meters CEP",
            "Engine Control Unit shall monitor turbine temperature and limit to 1200°C maximum",
            "Landing Gear System shall deploy and retract within 15 seconds",
            "Environmental Control System shall maintain cabin pressure at 8000 ft equivalent",
            "Flight Management System shall calculate optimal flight path for fuel efficiency",
            "Weather Radar shall detect precipitation up to 160 nautical miles",
            "Autopilot System shall maintain altitude within ±100 feet during cruise",
            "Communication System shall provide VHF radio coverage on 118-137 MHz band",
            "Hydraulic System shall operate at 3000 PSI nominal pressure",
            "Fuel Management System shall monitor fuel quantity with ±2% accuracy",
            "Ice Protection System shall prevent ice accumulation on critical surfaces",
            "Emergency Oxygen System shall provide 15 minutes supply at 25000 ft",
            "Fire Detection System shall alert crew within 10 seconds of detection",
            "Electrical Power System shall provide 28V DC and 115V AC power",
            "Pitot-Static System shall measure airspeed with ±3 knot accuracy",
            "Thrust Reverser System shall reduce landing roll by minimum 30%",
            "Anti-Skid Braking System shall prevent wheel lockup during landing",
            "Cabin Lighting System shall provide emergency egress illumination",
            "Flight Data Recorder shall capture 25+ flight parameters continuously"
        ]
        
        # Generate requirements (80-100)
        req_count = random.randint(80, 100)
        for i in range(req_count):
            req_id = f"SYS-{i+1:03d}"
            
            # Pick aerospace requirement or generate generic one
            if i < len(aero_requirements):
                req_text = aero_requirements[i]
                req_name = req_text.split(' shall ')[0] + " Requirement"
            else:
                subsystems = ["Avionics", "Propulsion", "Flight Control", "Landing Gear", "Environmental", 
                            "Fuel System", "Electrical", "Hydraulic", "Navigation", "Communication"]
                subsystem = random.choice(subsystems)
                req_name = f"{subsystem} System Requirement {req_id}"
                req_text = f"The {subsystem} system shall meet performance and safety requirements as specified in DO-178C and ARP4754A standards."
            
            item = JamaItem(
                id=str(uuid.uuid4()),
                global_id=f"JAMA-{req_id}",
                document_key="SRD-2024",
                item_type="requirement",
                name=req_name,
                description=req_text + " " + fake.text(max_nb_chars=300),
                status=random.choice(["draft", "approved", "under_review", "verified", "validated"]),
                created_date=fake.date_time_between(start_date="-1y", end_date="now"),
                modified_date=fake.date_time_between(start_date="-30d", end_date="now"),
                created_by=fake.name(),
                modified_by=fake.name(),
                fields={
                    "priority": random.choice(["critical", "high", "medium", "low"]),
                    "verification_method": random.choice(["flight_test", "ground_test", "simulation", "analysis", "inspection"]),
                    "safety_level": random.choice(["DAL-A", "DAL-B", "DAL-C", "DAL-D", "DAL-E"]),
                    "certification_basis": random.choice(["FAR-25", "FAR-23", "DO-178C", "DO-254", "ARP4754A"])
                }
            )
            self.jama_items.append(item)
        
        # Generate aerospace test cases (40-60)
        test_count = random.randint(40, 60)
        aero_test_cases = [
            "Flight Control Authority Test - Verify control surface deflection limits",
            "Engine Start Sequence Test - Validate turbine startup parameters",
            "Navigation Accuracy Test - Verify GPS/INS position accuracy",
            "Hydraulic Pressure Test - Validate system pressure under load",
            "Cabin Pressurization Test - Verify pressure regulation at altitude",
            "Landing Gear Deployment Test - Validate extension/retraction timing",
            "Autopilot Engagement Test - Verify automatic flight control activation",
            "Weather Radar Detection Test - Validate precipitation detection range",
            "Emergency Oxygen Flow Test - Verify oxygen supply duration",
            "Fire Detection Response Test - Validate alert timing and accuracy",
            "Pitot-Static Calibration Test - Verify airspeed indication accuracy",
            "Anti-Ice System Test - Validate ice protection effectiveness",
            "VHF Radio Communication Test - Verify transmission quality",
            "Fuel Quantity Indication Test - Validate fuel measurement accuracy",
            "Thrust Reverser Operation Test - Verify deployment and stowage",
            "Electrical Load Test - Validate power distribution under load",
            "Flight Data Recording Test - Verify parameter capture accuracy",
            "Brake Anti-Skid Test - Validate wheel slip prevention",
            "Emergency Lighting Test - Verify egress path illumination",
            "Environmental Control Test - Validate temperature regulation"
        ]
        
        for i in range(test_count):
            test_id = f"FTC-{i+1:03d}"  # Flight Test Case
            
            if i < len(aero_test_cases):
                test_name = aero_test_cases[i]
                test_desc = test_name + ". " + fake.text(max_nb_chars=200)
            else:
                test_systems = ["Avionics", "Propulsion", "Flight Control", "Environmental", "Electrical"]
                system = random.choice(test_systems)
                test_name = f"{system} System Verification Test {test_id}"
                test_desc = f"Verification test for {system} system compliance with certification requirements."
            
            item = JamaItem(
                id=str(uuid.uuid4()),
                global_id=f"JAMA-{test_id}",
                document_key="FTP-2024",  # Flight Test Plan
                item_type="test_case",
                name=test_name,
                description=test_desc,
                status=random.choice(["planned", "ready", "in_progress", "completed", "passed", "failed"]),
                created_date=fake.date_time_between(start_date="-8m", end_date="now"),
                modified_date=fake.date_time_between(start_date="-14d", end_date="now"),
                created_by=fake.name(),
                modified_by=fake.name(),
                fields={
                    "test_type": random.choice(["ground_test", "flight_test", "simulation", "rig_test", "bench_test"]),
                    "test_phase": random.choice(["development", "qualification", "certification", "production"]),
                    "test_facility": random.choice(["Flight Test Center", "Ground Test Lab", "Iron Bird Rig", "Simulator"]),
                    "risk_level": random.choice(["low", "medium", "high", "critical"])
                }
            )
            self.jama_items.append(item)
    
    def _generate_jira_issues(self):
        """Generate Jira issues for aerospace engineering projects"""
        self.jira_issues = []
        
        # Aerospace engineering issues
        aero_issues = [
            "Engine vibration exceeds limits during flight test FT-001",
            "Hydraulic leak detected in landing gear actuator assembly",
            "GPS navigation accuracy degraded in mountainous terrain",
            "Cabin pressurization system fails to maintain 8000 ft equivalent",
            "Flight control surface flutter observed at Mach 0.78",
            "Fuel flow sensor reading inconsistent with actual consumption",
            "Weather radar display shows false precipitation echoes",
            "Autopilot disengages unexpectedly during approach phase",
            "Anti-ice system draws excessive electrical current",
            "Communication static interference on VHF frequency 124.5",
            "Thrust reverser deployment delayed by 2.3 seconds",
            "Emergency oxygen mask fails to deploy in cabin test",
            "Fire detection system false alarm in engine bay",
            "Pitot tube heating element shows intermittent failure",
            "Landing gear retraction sequence timing out of specification",
            "Flight data recorder missing altitude parameter data",
            "Environmental control temperature regulation unstable",
            "Electrical bus voltage fluctuation during high load conditions",
            "Brake anti-skid system activating prematurely on dry runway",
            "Emergency lighting circuit breaker trips during system test"
        ]
        
        issue_count = random.randint(25, 35)
        for i in range(issue_count):
            issue_key = f"AERO-{i+1:03d}"
            
            if i < len(aero_issues):
                summary = aero_issues[i]
                # Generate detailed aerospace description
                description = f"Issue discovered during {random.choice(['flight test', 'ground test', 'system integration', 'qualification testing'])}. "
                description += f"Impact: {random.choice(['Flight safety concern', 'Performance degradation', 'Certification compliance', 'Operational limitation'])}. "
                description += f"Assigned to {random.choice(['Flight Test', 'Avionics', 'Propulsion', 'Systems', 'Structures'])} engineering team."
            else:
                systems = ["Avionics", "Propulsion", "Flight Control", "Environmental", "Electrical", "Hydraulic", "Fuel", "Landing Gear"]
                issues_types = ["malfunction", "performance issue", "compliance gap", "design discrepancy", "test failure"]
                system = random.choice(systems)
                issue_type_desc = random.choice(issues_types)
                summary = f"{system} system {issue_type_desc} requires investigation"
                description = f"Engineering investigation required for {system} system {issue_type_desc}. Coordinate with certification team."
            
            issue = JiraIssue(
                id=str(uuid.uuid4()),
                key=f"JIRA-{issue_key}",
                summary=summary,
                description=description,
                issue_type=random.choice(["defect", "flight_test_issue", "certification_task", "design_change", "compliance_review"]),
                status=random.choice(["open", "in_progress", "testing", "review", "resolved", "closed"]),
                priority=random.choice(["critical", "high", "medium", "low"]),
                assignee=fake.name() if random.random() > 0.15 else None,
                reporter=fake.name(),
                created=fake.date_time_between(start_date="-6m", end_date="now"),
                updated=fake.date_time_between(start_date="-7d", end_date="now"),
                labels=random.sample(["flight-safety", "certification", "flight-test", "ground-test", "FAA", "DO-178C", "airworthiness", "performance"], k=random.randint(1, 4))
            )
            self.jira_issues.append(issue)
    
    def _generate_windchill_parts(self):
        """Generate Windchill parts for aerospace components"""
        self.windchill_parts = []
        
        # Aerospace component templates
        aero_parts = [
            ("Engine Turbine Blade Assembly", "High-temperature nickel superalloy turbine blade with cooling passages and thermal barrier coating"),
            ("Flight Control Actuator", "Electro-hydraulic actuator for primary flight control surface with redundant position feedback"),
            ("Avionics Display Unit", "Multi-function display unit with LED backlighting and touch screen interface for cockpit integration"),
            ("Landing Gear Strut Assembly", "Oleo-pneumatic shock strut with integrated position sensors and anti-shimmy damper"),
            ("Fuel Pump Housing", "Titanium alloy centrifugal fuel pump housing with integrated pressure relief valve"),
            ("Pitot-Static Probe", "Heated pitot-static probe with ice detection capability and drain holes for moisture removal"),
            ("Navigation Antenna", "GPS/GLONASS L1/L2 navigation antenna with lightning protection and EMI shielding"),
            ("Hydraulic Reservoir", "Pressurized hydraulic fluid reservoir with level sensors and temperature monitoring"),
            ("Engine Control Module", "Full Authority Digital Engine Control (FADEC) with dual-channel redundancy"),
            ("Communication Radio", "VHF/UHF transceiver with 25 kHz channel spacing and digital signal processing"),
            ("Oxygen Regulator", "Continuous flow oxygen regulator with altitude compensating aneroid for crew oxygen system"),
            ("Fire Extinguisher Bottle", "Halon 1301 fire extinguisher bottle with squib-operated discharge valve"),
            ("Weather Radar Antenna", "X-band phased array antenna for weather detection with tilt and azimuth control"),
            ("Cabin Pressure Controller", "Digital cabin pressure controller with backup analog control and altitude scheduling"),
            ("Anti-Ice Heating Element", "Electrothermal heating mat for wing leading edge ice protection system"),
            ("Flight Data Recorder", "Crash-survivable flight data recorder with 25-hour minimum recording capability"),
            ("Brake Control Valve", "Anti-skid brake control valve with pressure modulation and wheel speed input"),
            ("Emergency Lighting Battery", "NiCd battery pack for emergency lighting with 10-minute minimum discharge time"),
            ("Thrust Reverser Actuator", "Pneumatic thrust reverser actuator with position indication and safety locks"),
            ("Environmental Control Unit", "Air cycle machine for cabin air conditioning with heat exchanger and turbine")
        ]
        
        part_count = random.randint(15, 25)
        for i in range(part_count):
            if i < len(aero_parts):
                part_name, part_desc = aero_parts[i]
                part_number = f"AN{i+1000:04d}"  # AN prefix for aerospace parts
            else:
                # Generate additional generic aerospace parts
                categories = ["Avionics", "Propulsion", "Flight Control", "Environmental", "Electrical", "Hydraulic"]
                components = ["Module", "Assembly", "Unit", "Controller", "Sensor", "Actuator", "Valve", "Harness"]
                category = random.choice(categories)
                component = random.choice(components)
                part_name = f"{category} {component}"
                part_desc = f"{category} system {component.lower()} designed for commercial aircraft applications with FAA certification."
                part_number = f"AN{i+1000:04d}"
            
            part = WindchillPart(
                id=str(uuid.uuid4()),
                number=part_number,
                name=part_name,
                description=part_desc,
                version=f"{random.choice(['A', 'B', 'C'])}.{random.randint(1, 5)}",
                state=random.choice(["in_work", "released", "production", "obsolete"]),
                created_by=fake.name(),
                created_date=fake.date_time_between(start_date="-2y", end_date="-6m"),
                modified_date=fake.date_time_between(start_date="-30d", end_date="now"),
                classification=random.choice(["avionics", "mechanical", "electrical", "hydraulic", "structural", "propulsion"])
            )
            self.windchill_parts.append(part)
    
    def _generate_windchill_ecn(self):
        """Generate Windchill ECNs for aerospace engineering changes"""
        self.windchill_ecn = []
        
        # Aerospace engineering change notices
        aero_ecns = [
            ("Flight Control Actuator Material Upgrade", "Change actuator housing material from aluminum to titanium alloy for improved corrosion resistance and weight reduction. Required for service bulletin compliance."),
            ("Engine Control Software Update v2.1", "Update FADEC software to address fuel efficiency optimization and emissions compliance with latest EPA standards. Includes enhanced diagnostics."),
            ("Landing Gear Position Sensor Replacement", "Replace magnetic proximity sensors with LVDT position sensors for improved accuracy and reliability in harsh operating conditions."),
            ("Cabin Pressure Relief Valve Modification", "Modify pressure relief valve spring rate to prevent over-pressurization events observed during high altitude operations."),
            ("Navigation Display Brightness Enhancement", "Increase display brightness capability for improved visibility in high ambient light conditions. Addresses pilot feedback from field operations."),
            ("Hydraulic Filter Element Change", "Change from paper-based to synthetic filter elements to extend service intervals and improve contamination control."),
            ("Weather Radar Antenna Radome Update", "Update radome material to improved composite with better lightning strike protection and reduced electromagnetic interference.")
        ]
        
        ecn_count = random.randint(4, 6)
        for i in range(ecn_count):
            ecn_number = f"ECN-2024-{i+1:03d}"
            
            if i < len(aero_ecns):
                title, description = aero_ecns[i]
            else:
                systems = ["Avionics", "Propulsion", "Flight Control", "Environmental", "Electrical", "Hydraulic"]
                changes = ["Update", "Modification", "Enhancement", "Replacement", "Upgrade"]
                system = random.choice(systems)
                change = random.choice(changes)
                title = f"{system} System {change}"
                description = f"Engineering change notice for {system.lower()} system {change.lower()} to address performance requirements and certification compliance."
            
            ecn = WindchillECN(
                id=str(uuid.uuid4()),
                number=ecn_number,
                title=title,
                description=description,
                status=random.choice(["draft", "review", "approved", "released", "implemented", "cancelled"]),
                initiator=fake.name(),
                created_date=fake.date_time_between(start_date="-3m", end_date="now"),
                target_date=fake.date_time_between(start_date="now", end_date="+6m"),
                affected_parts=[random.choice(self.windchill_parts).number for _ in range(random.randint(1, 3))]
            )
            self.windchill_ecn.append(ecn)
    
    def _generate_email_messages(self):
        """Generate aerospace engineering email messages"""
        self.email_messages = []
        
        # Aerospace email subjects
        aero_subjects = [
            "Flight Test Report FT-2024-015 - Engine Performance Results",
            "FAA Certification Update - DO-178C Software Review Status",
            "Ground Test Schedule - Hydraulic System Integration Testing",
            "Engineering Review Meeting - Landing Gear Modification ECN-2024-003",
            "Supplier Quality Alert - Actuator Component Non-Conformance",
            "Flight Operations Feedback - Autopilot System Performance",
            "Certification Milestone Update - Avionics System Verification",
            "Design Review Action Items - Environmental Control System",
            "Test Data Analysis - Weather Radar Performance Validation",
            "Regulatory Compliance Notice - New FAA Service Bulletin"
        ]
        
        for i in range(10):
            if i < len(aero_subjects):
                subject = aero_subjects[i]
                # Generate aerospace-specific email body
                body_templates = [
                    "Please review the attached technical documentation and provide feedback by COB Friday. This relates to our ongoing certification activities.",
                    "The flight test results are now available for review. Please coordinate with the test pilot for any follow-up questions regarding system performance.",
                    "Engineering team meeting scheduled to discuss technical findings. Your expertise in this area would be valuable for the discussion.",
                    "Regulatory compliance update requires immediate attention. Please review the attached FAA correspondence and prepare response.",
                    "System integration testing has identified several items requiring engineering review. Please prioritize based on flight safety impact."
                ]
                body = random.choice(body_templates) + " " + fake.text(max_nb_chars=400)
            else:
                subject = fake.sentence(nb_words=8)
                body = fake.text(max_nb_chars=600)
            
            # Generate aerospace-themed email addresses
            domains = ["aerocorp.com", "flighttest.gov", "aviationeng.com", "aerospace-systems.com"]
            sender_domain = random.choice(domains)
            
            email = EmailMessage(
                id=str(uuid.uuid4()),
                global_id=f"EMAIL-{i+1:03d}",
                subject=subject,
                sender=f"{fake.first_name().lower()}.{fake.last_name().lower()}@{sender_domain}",
                recipients=[f"{fake.first_name().lower()}.{fake.last_name().lower()}@{random.choice(domains)}" for _ in range(random.randint(1, 3))],
                body=body,
                sent_date=fake.date_time_between(start_date="-14d", end_date="now"),
                attachments=[f"{doc}.{ext}" for doc, ext in random.choices([
                    ("FlightTestReport", "pdf"), ("TechnicalSpecification", "docx"), ("TestData", "xlsx"),
                    ("CertificationPlan", "pdf"), ("EngineeringDrawing", "dwg"), ("ComplianceMatrix", "xlsx")
                ], k=random.randint(0, 2))],
                linked_artifacts=[]
            )
            self.email_messages.append(email)
    
    def _generate_outlook_messages(self):
        """Generate aerospace Outlook messages"""
        self.outlook_messages = []
        
        # Aerospace Outlook message subjects
        aero_outlook_subjects = [
            "Flight Test Coordination Meeting - Weekly Status Review",
            "Engineering Design Review - Avionics System Architecture",
            "Certification Planning Session - FAA DER Meeting",
            "Ground Test Witness - Hydraulic System Pressure Testing",
            "Technical Presentation - Propulsion System Performance",
            "Project Milestone Review - Phase 2 Flight Testing",
            "Supplier Audit - Avionics Component Manufacturing",
            "Safety Review Board - System Hazard Analysis",
            "Flight Operations Briefing - New Procedures Training",
            "Regulatory Update Webinar - Latest FAA Airworthiness Directives"
        ]
        
        # Aerospace personnel names
        aero_names = [
            "Dr. Sarah Mitchell (Flight Test Engineer)",
            "James Rodriguez (Avionics Systems Manager)",
            "Lisa Chen (Certification Engineer)",
            "Michael Thompson (Propulsion Engineer)",
            "Anna Kowalski (Flight Test Pilot)",
            "David Park (Systems Integration Lead)",
            "Jennifer Williams (Quality Assurance Manager)",
            "Robert Johnson (Chief Engineer)",
            "Maria Garcia (Regulatory Affairs)",
            "Thomas Anderson (Project Manager)"
        ]
        
        for i in range(10):
            if i < len(aero_outlook_subjects):
                subject = aero_outlook_subjects[i]
                # Generate meeting-appropriate body text
                meeting_bodies = [
                    "Please join us for the weekly engineering review meeting. We'll cover recent test results and upcoming milestones. Your input on system performance would be valuable.",
                    "Design review meeting to discuss technical specifications and certification requirements. Please bring your latest analysis results.",
                    "Coordination meeting with FAA representatives to review certification progress. All engineering leads should attend.",
                    "Ground test witnessing session. Safety briefing starts 30 minutes prior to test commencement.",
                    "Technical presentation on system performance metrics and compliance verification results."
                ]
                body = random.choice(meeting_bodies) + " Location: Building 5, Conference Room A"
                is_meeting = True
            else:
                subject = fake.sentence(nb_words=7)
                body = fake.text(max_nb_chars=400)
                is_meeting = random.random() > 0.6
            
            outlook = OutlookMessage(
                id=str(uuid.uuid4()),
                global_id=f"OUTLOOK-MSG-{i+1:03d}",
                subject=subject,
                sender=random.choice(aero_names),
                recipients=random.sample(aero_names, k=random.randint(2, 4)),
                body=body,
                sent_date=fake.date_time_between(start_date="-21d", end_date="now"),
                importance=random.choice(["normal", "high"]) if "certification" in subject.lower() or "safety" in subject.lower() else "normal",
                has_attachments=random.random() > 0.6,
                linked_artifacts=[],
                meeting_request=is_meeting
            )
            self.outlook_messages.append(outlook)
    
    def _generate_jama_relationships(self):
        """Generate Jama relationships with gaps"""
        self.jama_relationships = []
        
        requirements = [item for item in self.jama_items if item.item_type == "requirement"]
        test_cases = [item for item in self.jama_items if item.item_type == "test_case"]
        
        # Create relationships between requirements and test cases (with 15% gaps)
        for req in requirements:
            if random.random() > 0.15:  # 85% coverage
                # Link to 1-3 test cases
                linked_tests = random.sample(test_cases, min(random.randint(1, 3), len(test_cases)))
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
        for parent_part in self.windchill_parts[:10]:  # Top-level assemblies
            child_count = random.randint(2, 5)
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
        
        # Jira changes
        for issue in self.jira_issues:
            if issue.updated > now - timedelta(days=30):
                pulse_item = MockPulseItem(
                    id=str(uuid.uuid4()),
                    artifact_ref=MockArtifactRef(
                        id=issue.key,
                        type="issue",
                        source="jira",
                        title=issue.summary,
                        status=issue.status,
                        url=f"http://localhost:8001/mock/windows/jira/{issue.key}"
                    ),
                    change_type="updated" if issue.created < issue.updated else "created",
                    change_summary=f"Issue '{issue.summary}' status changed to {issue.status}",
                    timestamp=issue.updated,
                    author=issue.assignee or issue.reporter,
                    metadata={"priority": issue.priority, "type": issue.issue_type}
                )
                self.pulse_items.append(pulse_item)
        
        # Windchill ECN changes
        for ecn in self.windchill_ecn:
            pulse_item = MockPulseItem(
                id=str(uuid.uuid4()),
                artifact_ref=MockArtifactRef(
                    id=ecn.number,
                    type="ecn",
                    source="windchill",
                    title=ecn.title,
                    status=ecn.status,
                    url=f"http://localhost:8001/mock/windows/windchill/{ecn.number}"
                ),
                change_type="status_change",
                change_summary=f"ECN '{ecn.title}' status is now {ecn.status}",
                timestamp=ecn.created_date,
                author=ecn.initiator,
                metadata={"affected_parts": len(ecn.affected_parts)}
            )
            self.pulse_items.append(pulse_item)
        
        # Email messages
        for email in self.email_messages:
            pulse_item = MockPulseItem(
                id=str(uuid.uuid4()),
                artifact_ref=MockArtifactRef(
                    id=email.global_id,
                    type="email",
                    source="email",
                    title=email.subject,
                    status="received",
                    url=f"http://localhost:8001/mock/windows/email/{email.global_id}"
                ),
                change_type="received",
                change_summary=f"Email received: '{email.subject}'",
                timestamp=email.sent_date,
                author=email.sender,
                metadata={"recipients": len(email.recipients)}
            )
            self.pulse_items.append(pulse_item)
        
        # Outlook messages
        for outlook in self.outlook_messages:
            pulse_item = MockPulseItem(
                id=str(uuid.uuid4()),
                artifact_ref=MockArtifactRef(
                    id=outlook.global_id,
                    type="outlook",
                    source="outlook",
                    title=outlook.subject,
                    status="received",
                    url=f"http://localhost:8001/mock/windows/outlook/{outlook.global_id}"
                ),
                change_type="meeting_request" if outlook.meeting_request else "received",
                change_summary=f"{'Meeting request' if outlook.meeting_request else 'Message'}: '{outlook.subject}'",
                timestamp=outlook.sent_date,
                author=outlook.sender,
                metadata={"importance": outlook.importance, "meeting": outlook.meeting_request}
            )
            self.pulse_items.append(pulse_item)
        
        # Sort by timestamp (newest first)
        self.pulse_items.sort(key=lambda x: x.timestamp, reverse=True)
    
    # API methods
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
    
    def get_jama_relationships(self, item_id: Optional[str] = None) -> List[JamaRelationship]:
        """Get Jama relationships"""
        if item_id:
            return [rel for rel in self.jama_relationships if rel.from_item == item_id or rel.to_item == item_id]
        return self.jama_relationships
    
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
    
    def get_jira_links(self, issue_id: Optional[str] = None) -> List[JiraLink]:
        """Get Jira links"""
        if issue_id:
            return [link for link in self.jira_links if link.issue_id == issue_id or link.linked_issue_id == issue_id]
        return self.jira_links
    
    def get_windchill_parts(self, page: int = 1, size: int = 50, query: Optional[str] = None) -> List[WindchillPart]:
        """Get Windchill parts"""
        parts = self.windchill_parts
        
        if query:
            parts = [part for part in parts if query.lower() in part.name.lower() or query.lower() in part.number.lower()]
        
        start_idx = (page - 1) * size
        end_idx = start_idx + size
        return parts[start_idx:end_idx]
    
    def get_windchill_bom(self, part_id: Optional[str] = None) -> List[WindchillBOM]:
        """Get Windchill BOM"""
        if part_id:
            return [bom for bom in self.windchill_bom if bom.parent_part == part_id]
        return self.windchill_bom
    
    def get_windchill_ecn(self, status: Optional[str] = None) -> List[WindchillECN]:
        """Get Windchill ECNs"""
        ecns = self.windchill_ecn
        if status:
            ecns = [ecn for ecn in ecns if ecn.status == status]
        return ecns
    
    def get_email_messages(self, since: Optional[datetime] = None) -> List[EmailMessage]:
        """Get email messages"""
        emails = self.email_messages
        if since:
            emails = [email for email in emails if email.sent_date >= since]
        return emails
    
    def get_outlook_messages(self, since: Optional[datetime] = None) -> List[OutlookMessage]:
        """Get Outlook messages"""
        messages = self.outlook_messages
        if since:
            messages = [msg for msg in messages if msg.sent_date >= since]
        return messages
    
    def get_pulse_feed(self, since: Optional[datetime] = None, sources: Optional[List[str]] = None, 
                      types: Optional[List[str]] = None, limit: int = 50) -> List[MockPulseItem]:
        """Get filtered pulse feed"""
        items = self.pulse_items
        
        if since:
            items = [item for item in items if item.timestamp >= since]
        
        if sources:
            items = [item for item in items if item.artifact_ref.source in sources]
        
        if types:
            items = [item for item in items if item.artifact_ref.type in types]
        
        return items[:limit]
    
    def get_impact_analysis(self, entity_id: str, depth: int = 2) -> MockImpactResult:
        """Generate mock impact analysis"""
        # Find the root artifact
        root_artifact = None
        
        # Check all artifact types
        for item in self.jama_items:
            if item.global_id == entity_id:
                root_artifact = MockArtifactRef(
                    id=item.global_id,
                    type=item.item_type,
                    source="jama",
                    title=item.name,
                    status=item.status
                )
                break
        
        if not root_artifact:
            for issue in self.jira_issues:
                if issue.key == entity_id:
                    root_artifact = MockArtifactRef(
                        id=issue.key,
                        type="issue",
                        source="jira",
                        title=issue.summary,
                        status=issue.status
                    )
                    break
        
        if not root_artifact:
            # Default artifact
            root_artifact = MockArtifactRef(
                id=entity_id,
                type="requirement",
                source="jama",
                title=f"Mock Requirement {entity_id}",
                status="approved"
            )
        
        # Generate impact tree
        impact_tree = self._generate_impact_nodes(root_artifact, depth, 0)
        total_impacted = self._count_impact_nodes(impact_tree)
        
        return MockImpactResult(
            root_artifact=root_artifact,
            depth=depth,
            total_impacted=total_impacted,
            impact_tree=impact_tree,
            gap_count=random.randint(1, 5)
        )
    
    def _generate_impact_nodes(self, artifact: MockArtifactRef, max_depth: int, current_depth: int) -> List[MockImpactNode]:
        """Recursively generate impact nodes"""
        if current_depth >= max_depth:
            return []
        
        nodes = []
        child_count = random.randint(0, 4) if current_depth < max_depth - 1 else random.randint(0, 2)
        
        for i in range(child_count):
            # Create child artifact
            child_artifact = MockArtifactRef(
                id=f"MOCK-{random.choice(['REQ', 'TC', 'ENG'])}-{random.randint(1, 999):03d}",
                type=random.choice(["requirement", "test", "issue", "part"]),
                source=random.choice(["jama", "jira", "windchill"]),
                title=fake.sentence(nb_words=4),
                status=random.choice(["draft", "approved", "in_progress", "released"])
            )
            
            child_node = MockImpactNode(
                artifact_ref=child_artifact,
                impact_level=current_depth + 1,
                relationship_type=random.choice(["depends_on", "tests", "implements", "uses"]),
                children=self._generate_impact_nodes(child_artifact, max_depth, current_depth + 1)
            )
            nodes.append(child_node)
        
        return nodes
    
    def _count_impact_nodes(self, nodes: List[MockImpactNode]) -> int:
        """Count total nodes in impact tree"""
        count = len(nodes)
        for node in nodes:
            count += self._count_impact_nodes(node.children)
        return count
    
    def get_trace_graph(self, root_id: Optional[str] = None) -> TraceGraph:
        """Generate trace graph data"""
        nodes = []
        edges = []
        
        # Generate nodes from all artifacts
        for i, item in enumerate(self.jama_items[:20]):  # Limit for visualization
            node = TraceNode(
                id=item.global_id,
                label=item.name[:30] + "..." if len(item.name) > 30 else item.name,
                type=item.item_type,
                status=item.status,
                x=random.uniform(-500, 500),
                y=random.uniform(-500, 500)
            )
            nodes.append(node)
        
        # Add some Jira nodes
        for issue in self.jira_issues[:10]:
            node = TraceNode(
                id=issue.key,
                label=issue.summary[:30] + "..." if len(issue.summary) > 30 else issue.summary,
                type="issue",
                status=issue.status,
                x=random.uniform(-500, 500),
                y=random.uniform(-500, 500)
            )
            nodes.append(node)
        
        # Generate edges from relationships
        for rel in self.jama_relationships[:30]:  # Limit edges
            # Find source and target nodes
            from_node = next((n for n in nodes if any(item.id == rel.from_item for item in self.jama_items if item.global_id == n.id)), None)
            to_node = next((n for n in nodes if any(item.id == rel.to_item for item in self.jama_items if item.global_id == n.id)), None)
            
            if from_node and to_node:
                edge = TraceEdge(
                    id=str(uuid.uuid4()),
                    from_node=from_node.id,
                    to_node=to_node.id,
                    label=rel.relationship_type,
                    type=rel.relationship_type
                )
                edges.append(edge)
        
        return TraceGraph(
            nodes=nodes,
            edges=edges,
            metadata={
                "total_nodes": len(nodes),
                "total_edges": len(edges),
                "generated_at": datetime.now().isoformat()
            }
        )
    
    def get_mock_window_content(self, tool: str, item_id: str) -> str:
        """Generate mock HTML content for window views"""
        content = f"""
        <div class="field">
            <span class="label">ID:</span> {item_id}
        </div>
        <div class="field">
            <span class="label">Type:</span> {tool.title()} Item
        </div>
        <div class="field">
            <span class="label">Status:</span> {random.choice(['Active', 'Draft', 'Approved', 'Released'])}
        </div>
        <div class="field">
            <span class="label">Created:</span> {fake.date_time_between(start_date='-1y', end_date='now').strftime('%Y-%m-%d %H:%M')}
        </div>
        <div class="field">
            <span class="label">Modified:</span> {fake.date_time_between(start_date='-30d', end_date='now').strftime('%Y-%m-%d %H:%M')}
        </div>
        <div class="field">
            <span class="label">Description:</span>
            <p>{fake.text(max_nb_chars=400)}</p>
        </div>
        """
        
        if tool == "outlook":
            content += f"""
            <div class="field">
                <span class="label">From:</span> {fake.name()} &lt;{fake.email()}&gt;
            </div>
            <div class="field">
                <span class="label">To:</span> {', '.join([fake.email() for _ in range(random.randint(1, 3))])}
            </div>
            <div class="field">
                <span class="label">Subject:</span> {fake.sentence()}
            </div>
            """
        
        return content
