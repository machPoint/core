// Fake data generators for demo mode without server dependencies

export interface FakeJamaItem {
  id: string;
  global_id: string;
  document_key: string;
  item_type: 'requirement' | 'test_case';
  name: string;
  description: string;
  status: string;
  created_date: string;
  modified_date: string;
  created_by: string;
  modified_by: string;
  fields: {
    priority?: string;
    verification_method?: string;
    safety_level?: string;
    certification_basis?: string;
  };
}

export interface FakeJiraIssue {
  id: string;
  key: string;
  summary: string;
  description: string;
  issue_type: string;
  status: string;
  priority: string;
  assignee?: string;
  reporter: string;
  created: string;
  updated: string;
  labels: string[];
}

export interface FakeWindchillPart {
  id: string;
  number: string;
  name: string;
  description: string;
  version: string;
  state: string;
  created_by: string;
  created_date: string;
  modified_date: string;
  classification: string;
}

export interface FakePulseItem {
  id: string;
  artifact_ref: {
    id: string;
    type: string;
    source: string;
    title: string;
    status?: string;
  };
  change_type: string;
  change_summary: string;
  timestamp: string;
  author?: string;
}

const names = ['Sarah Chen', 'Mike Rodriguez', 'Alex Kim', 'Jordan Lee', 'Taylor Smith', 'Morgan Davis'];
const statuses = ['draft', 'approved', 'under_review', 'verified', 'validated'];
const priorities = ['critical', 'high', 'medium', 'low'];
const issueStatuses = ['open', 'in_progress', 'testing', 'review', 'resolved', 'closed'];

function randomItem<T>(arr: T[]): T {
  return arr[Math.floor(Math.random() * arr.length)];
}

function randomDate(daysAgo: number): string {
  const date = new Date();
  date.setDate(date.getDate() - Math.floor(Math.random() * daysAgo));
  return date.toISOString();
}

export function generateFakeJamaItems(count: number = 50): FakeJamaItem[] {
  const items: FakeJamaItem[] = [];
  
  for (let i = 1; i <= count; i++) {
    const isRequirement = i <= count * 0.6; // 60% requirements, 40% test cases
    const itemType = isRequirement ? 'requirement' : 'test_case';
    const prefix = isRequirement ? 'SYS' : 'FTC';
    const globalId = `JAMA-${prefix}-${String(i).padStart(3, '0')}`;
    
    items.push({
      id: `jama-${i}`,
      global_id: globalId,
      document_key: isRequirement ? 'SRD-2024' : 'FTP-2024',
      item_type: itemType,
      name: isRequirement 
        ? `Flight Control System Requirement ${i}`
        : `Flight Test Case ${i}`,
      description: isRequirement
        ? `The system shall provide automated flight control capabilities with redundancy and fail-safe mechanisms compliant with DO-178C Level A requirements.`
        : `Verify flight control system response time under various flight conditions including normal operations and failure scenarios.`,
      status: randomItem(statuses),
      created_date: randomDate(365),
      modified_date: randomDate(30),
      created_by: randomItem(names),
      modified_by: randomItem(names),
      fields: {
        priority: randomItem(priorities),
        verification_method: randomItem(['flight_test', 'ground_test', 'simulation', 'analysis']),
        safety_level: randomItem(['DAL-A', 'DAL-B', 'DAL-C']),
        certification_basis: randomItem(['FAR-25', 'DO-178C', 'ARP4754A']),
      },
    });
  }
  
  return items;
}

export function generateFakeJiraIssues(count: number = 25): FakeJiraIssue[] {
  const issues: FakeJiraIssue[] = [];
  
  for (let i = 1; i <= count; i++) {
    const key = `JIRA-AERO-${String(i).padStart(3, '0')}`;
    
    issues.push({
      id: `jira-${i}`,
      key,
      summary: `Flight Test Issue: ${randomItem(['Sensor Calibration', 'Hydraulic Pressure', 'Avionics Integration', 'Control Surface Response'])}`,
      description: `Issue identified during flight test operations requiring investigation and resolution before certification.`,
      issue_type: randomItem(['defect', 'flight_test_issue', 'certification_task', 'design_change']),
      status: randomItem(issueStatuses),
      priority: randomItem(priorities),
      assignee: Math.random() > 0.3 ? randomItem(names) : undefined,
      reporter: randomItem(names),
      created: randomDate(180),
      updated: randomDate(7),
      labels: ['flight-safety', 'certification', randomItem(['FAA', 'DO-178C', 'flight-test'])],
    });
  }
  
  return issues;
}

export function generateFakeWindchillParts(count: number = 20): FakeWindchillPart[] {
  const parts: FakeWindchillPart[] = [];
  const partTypes = ['Flight Control Module', 'Sensor Assembly', 'Hydraulic Actuator', 'Avionics Unit', 'Control Surface'];
  
  for (let i = 1; i <= count; i++) {
    const number = `AN${1000 + i}`;
    
    parts.push({
      id: `part-${i}`,
      number,
      name: `${randomItem(partTypes)} ${number}`,
      description: `Aerospace component for flight control and avionics systems`,
      version: `${String.fromCharCode(65 + Math.floor(i / 10))}.${i % 10}`,
      state: randomItem(['in_work', 'released', 'production', 'obsolete']),
      created_by: randomItem(names),
      created_date: randomDate(730),
      modified_date: randomDate(90),
      classification: randomItem(['avionics', 'mechanical', 'electrical', 'hydraulic']),
    });
  }
  
  return parts;
}

export function generateFakePulseItems(count: number = 30): FakePulseItem[] {
  const items: FakePulseItem[] = [];
  const sources = ['jama', 'jira', 'windchill', 'outlook', 'email'];
  const changeTypes = ['created', 'updated', 'status_change'];
  
  for (let i = 1; i <= count; i++) {
    const source = randomItem(sources);
    const changeType = randomItem(changeTypes);
    
    let artifactRef;
    switch (source) {
      case 'jama':
        artifactRef = {
          id: `JAMA-SYS-${String(i).padStart(3, '0')}`,
          type: 'requirement',
          source: 'jama',
          title: `Flight Control Requirement ${i}`,
          status: randomItem(statuses),
        };
        break;
      case 'jira':
        artifactRef = {
          id: `JIRA-AERO-${String(i).padStart(3, '0')}`,
          type: 'issue',
          source: 'jira',
          title: `Flight Test Issue ${i}`,
          status: randomItem(issueStatuses),
        };
        break;
      case 'windchill':
        artifactRef = {
          id: `AN${1000 + i}`,
          type: 'part',
          source: 'windchill',
          title: `Flight Control Module AN${1000 + i}`,
          status: randomItem(['in_work', 'released', 'production']),
        };
        break;
      case 'outlook':
        artifactRef = {
          id: `OUTLOOK-MSG-${String(i).padStart(3, '0')}`,
          type: 'message',
          source: 'outlook',
          title: `Flight Test Coordination Meeting`,
        };
        break;
      default:
        artifactRef = {
          id: `EMAIL-${String(i).padStart(3, '0')}`,
          type: 'email',
          source: 'email',
          title: `Certification Status Update`,
        };
    }
    
    items.push({
      id: `pulse-${i}`,
      artifact_ref: artifactRef,
      change_type: changeType,
      change_summary: `${changeType === 'status_change' ? 'Status changed to' : changeType === 'created' ? 'Created new' : 'Updated'} ${artifactRef.type}`,
      timestamp: randomDate(7),
      author: randomItem(names),
    });
  }
  
  // Sort by timestamp descending
  return items.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
}

// Streaming data generator - returns new items periodically
export class StreamingDataGenerator {
  private intervalId: NodeJS.Timeout | null = null;
  private counter = 0;
  
  start(callback: (item: FakePulseItem) => void, intervalMs: number = 5000) {
    this.stop(); // Clear any existing interval
    
    this.intervalId = setInterval(() => {
      this.counter++;
      const newItem = this.generateStreamingItem(this.counter);
      callback(newItem);
    }, intervalMs);
  }
  
  stop() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
  }
  
  private generateStreamingItem(id: number): FakePulseItem {
    const sources = ['jama', 'jira', 'windchill', 'outlook'];
    const source = randomItem(sources);
    const changeTypes = ['created', 'updated', 'status_change'];
    const changeType = randomItem(changeTypes);
    
    let artifactRef;
    switch (source) {
      case 'jama':
        artifactRef = {
          id: `JAMA-SYS-${String(Math.floor(Math.random() * 100)).padStart(3, '0')}`,
          type: 'requirement',
          source: 'jama',
          title: `Flight Control Requirement (Live Update)`,
          status: randomItem(statuses),
        };
        break;
      case 'jira':
        artifactRef = {
          id: `JIRA-AERO-${String(Math.floor(Math.random() * 50)).padStart(3, '0')}`,
          type: 'issue',
          source: 'jira',
          title: `Flight Test Issue (Live Update)`,
          status: randomItem(issueStatuses),
        };
        break;
      case 'windchill':
        artifactRef = {
          id: `AN${1000 + Math.floor(Math.random() * 50)}`,
          type: 'part',
          source: 'windchill',
          title: `Component Update (Live)`,
          status: randomItem(['in_work', 'released']),
        };
        break;
      default:
        artifactRef = {
          id: `OUTLOOK-MSG-${String(Math.floor(Math.random() * 20)).padStart(3, '0')}`,
          type: 'message',
          source: 'outlook',
          title: `New Message (Live)`,
        };
    }
    
    return {
      id: `stream-${id}-${Date.now()}`,
      artifact_ref: artifactRef,
      change_type: changeType,
      change_summary: `[LIVE] ${changeType === 'status_change' ? 'Status changed' : changeType === 'created' ? 'Created' : 'Updated'} ${artifactRef.type}`,
      timestamp: new Date().toISOString(),
      author: randomItem(names),
    };
  }
}
