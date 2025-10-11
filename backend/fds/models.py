"""
Pydantic models for Fake Data Service
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


# Jama models
class JamaItem(BaseModel):
    """Jama requirement/item"""
    id: str = Field(..., description="Jama item ID")
    global_id: str = Field(..., description="Global ID (e.g., JAMA-REQ-123)")
    document_key: str = Field(..., description="Document key")
    item_type: str = Field(..., description="Item type (requirement, test_case)")
    name: str = Field(..., description="Item name/title")
    description: str = Field(..., description="Item description")
    status: str = Field(..., description="Current status")
    created_date: datetime = Field(..., description="Creation date")
    modified_date: datetime = Field(..., description="Last modification date")
    created_by: str = Field(..., description="Creator")
    modified_by: str = Field(..., description="Last modifier")
    fields: Dict[str, Any] = Field(default_factory=dict, description="Custom fields")


class JamaRelationship(BaseModel):
    """Jama relationship between items"""
    id: str = Field(..., description="Relationship ID")
    from_item: str = Field(..., description="Source item ID")
    to_item: str = Field(..., description="Target item ID")
    relationship_type: str = Field(..., description="Type of relationship")
    created_date: datetime = Field(..., description="Creation date")


# Jira models
class JiraIssue(BaseModel):
    """Jira issue"""
    id: str = Field(..., description="Jira issue ID")
    key: str = Field(..., description="Issue key (e.g., JIRA-ENG-901)")
    summary: str = Field(..., description="Issue summary")
    description: str = Field(..., description="Issue description")
    issue_type: str = Field(..., description="Issue type (bug, story, task)")
    status: str = Field(..., description="Current status")
    priority: str = Field(..., description="Priority level")
    assignee: Optional[str] = Field(None, description="Assigned user")
    reporter: str = Field(..., description="Reporter")
    created: datetime = Field(..., description="Creation date")
    updated: datetime = Field(..., description="Last update date")
    labels: List[str] = Field(default_factory=list, description="Issue labels")


class JiraLink(BaseModel):
    """Jira issue link"""
    id: str = Field(..., description="Link ID")
    issue_id: str = Field(..., description="Source issue ID")
    linked_issue_id: str = Field(..., description="Linked issue ID")
    link_type: str = Field(..., description="Link type (blocks, relates, implements)")


# Windchill models
class WindchillPart(BaseModel):
    """Windchill part"""
    id: str = Field(..., description="Part ID")
    number: str = Field(..., description="Part number (e.g., PN-00123)")
    name: str = Field(..., description="Part name")
    description: str = Field(..., description="Part description")
    version: str = Field(..., description="Part version")
    state: str = Field(..., description="Lifecycle state")
    created_by: str = Field(..., description="Creator")
    created_date: datetime = Field(..., description="Creation date")
    modified_date: datetime = Field(..., description="Last modification date")
    classification: str = Field(..., description="Part classification")


class WindchillBOM(BaseModel):
    """Windchill Bill of Materials entry"""
    id: str = Field(..., description="BOM entry ID")
    parent_part: str = Field(..., description="Parent part number")
    child_part: str = Field(..., description="Child part number")
    quantity: float = Field(..., description="Quantity required")
    unit: str = Field(..., description="Unit of measure")
    find_number: str = Field(..., description="Find number")


class WindchillECN(BaseModel):
    """Windchill Engineering Change Notice"""
    id: str = Field(..., description="ECN ID")
    number: str = Field(..., description="ECN number (e.g., ECN-24-045)")
    title: str = Field(..., description="ECN title")
    description: str = Field(..., description="Change description")
    status: str = Field(..., description="ECN status")
    initiator: str = Field(..., description="Change initiator")
    created_date: datetime = Field(..., description="Creation date")
    target_date: Optional[datetime] = Field(None, description="Target completion date")
    affected_parts: List[str] = Field(default_factory=list, description="Affected part numbers")


# Email and Outlook models
class EmailMessage(BaseModel):
    """Email message"""
    id: str = Field(..., description="Email message ID")
    global_id: str = Field(..., description="Global ID (e.g., EMAIL-001)")
    subject: str = Field(..., description="Email subject")
    sender: str = Field(..., description="Sender email")
    recipients: List[str] = Field(..., description="Recipient emails")
    body: str = Field(..., description="Email body")
    sent_date: datetime = Field(..., description="Sent date")
    attachments: List[str] = Field(default_factory=list, description="Attachment names")
    linked_artifacts: List[str] = Field(default_factory=list, description="Referenced artifact IDs")


class OutlookMessage(BaseModel):
    """Outlook message"""
    id: str = Field(..., description="Outlook message ID")
    global_id: str = Field(..., description="Global ID (e.g., OUTLOOK-MSG-001)")
    subject: str = Field(..., description="Message subject")
    sender: str = Field(..., description="Sender")
    recipients: List[str] = Field(..., description="Recipients")
    body: str = Field(..., description="Message body")
    sent_date: datetime = Field(..., description="Sent date")
    importance: str = Field("normal", description="Message importance")
    has_attachments: bool = Field(False, description="Has attachments")
    linked_artifacts: List[str] = Field(default_factory=list, description="Referenced artifact IDs")
    meeting_request: bool = Field(False, description="Is meeting request")


# Aggregated models for backend consumption
class MockArtifactRef(BaseModel):
    """Mock artifact reference"""
    id: str = Field(..., description="Artifact ID")
    type: str = Field(..., description="Artifact type")
    source: str = Field(..., description="Source system")
    title: str = Field(..., description="Display title")
    status: Optional[str] = Field(None, description="Current status")
    url: Optional[str] = Field(None, description="Source URL")


class MockPulseItem(BaseModel):
    """Mock pulse feed item"""
    id: str = Field(..., description="Pulse item ID")
    artifact_ref: MockArtifactRef = Field(..., description="Referenced artifact")
    change_type: str = Field(..., description="Type of change")
    change_summary: str = Field(..., description="Change description")
    timestamp: datetime = Field(..., description="Change timestamp")
    author: Optional[str] = Field(None, description="Change author")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class MockImpactNode(BaseModel):
    """Mock impact analysis node"""
    artifact_ref: MockArtifactRef = Field(..., description="The artifact")
    impact_level: int = Field(..., description="Degree of separation")
    relationship_type: str = Field(..., description="Relationship type")
    children: List["MockImpactNode"] = Field(default_factory=list, description="Child nodes")


class MockImpactResult(BaseModel):
    """Mock impact analysis result"""
    root_artifact: MockArtifactRef = Field(..., description="Root artifact")
    depth: int = Field(..., description="Analysis depth")
    total_impacted: int = Field(..., description="Total impacted items")
    impact_tree: List[MockImpactNode] = Field(..., description="Impact tree")
    gap_count: int = Field(0, description="Traceability gaps")


class TraceNode(BaseModel):
    """Trace graph node"""
    id: str = Field(..., description="Node ID")
    label: str = Field(..., description="Node label")
    type: str = Field(..., description="Node type")
    status: str = Field(..., description="Node status")
    x: float = Field(..., description="X coordinate")
    y: float = Field(..., description="Y coordinate")


class TraceEdge(BaseModel):
    """Trace graph edge"""
    id: str = Field(..., description="Edge ID")
    from_node: str = Field(..., description="Source node ID")
    to_node: str = Field(..., description="Target node ID")
    label: str = Field(..., description="Edge label")
    type: str = Field(..., description="Relationship type")


class TraceGraph(BaseModel):
    """Complete trace graph"""
    nodes: List[TraceNode] = Field(..., description="Graph nodes")
    edges: List[TraceEdge] = Field(..., description="Graph edges")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Graph metadata")


# Update forward references
MockImpactNode.model_rebuild()
