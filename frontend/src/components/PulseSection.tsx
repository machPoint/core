"use client";

import { useState, useMemo } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { 
  Search, 
  Filter,
  Calendar,
  User,
  MessageSquare,
  FileText,
  GitCommit,
  Mail,
  Bell,
  BarChart3,
  TrendingUp,
  Clock,
  ChevronDown,
  ChevronRight,
  Eye,
  MoreHorizontal
} from "lucide-react";
import { cn } from "@/lib/utils";
import { toast } from "sonner";

interface ActivityItem {
  id: string;
  type: "commit" | "comment" | "document" | "meeting" | "notification";
  title: string;
  description: string;
  timestamp: string;
  user: {
    name: string;
    avatar: string;
  };
  source: string;
  isRead: boolean;
  metadata?: {
    repository?: string;
    branch?: string;
    fileName?: string;
    meetingType?: string;
    participants?: number;
  };
}

const mockActivities: ActivityItem[] = [
  {
    id: "1",
    type: "commit",
    title: "Updated authentication service",
    description: "Implemented OAuth2 flow and session management",
    timestamp: "2 hours ago",
    user: { name: "Sarah Chen", avatar: "SC" },
    source: "GitHub",
    isRead: false,
    metadata: { repository: "auth-service", branch: "main", fileName: "auth.ts" }
  },
  {
    id: "2",
    type: "document",
    title: "API Documentation Updated",
    description: "Added new endpoints for user management",
    timestamp: "4 hours ago",
    user: { name: "Mike Rodriguez", avatar: "MR" },
    source: "Confluence",
    isRead: true,
    metadata: { fileName: "api-docs.md" }
  },
  {
    id: "3",
    type: "meeting",
    title: "Sprint Planning Meeting",
    description: "Discussed upcoming features and priorities",
    timestamp: "1 day ago",
    user: { name: "Alex Kim", avatar: "AK" },
    source: "Zoom",
    isRead: true,
    metadata: { meetingType: "Sprint Planning", participants: 8 }
  }
];

export default function PulseSection() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedSources, setSelectedSources] = useState<string[]>([]);
  const [selectedTypes, setSelectedTypes] = useState<string[]>([]);
  const [expandedItems, setExpandedItems] = useState<string[]>([]);
  const [activities] = useState(mockActivities);

  const sources = ["GitHub", "Jira", "Confluence", "Slack", "Zoom", "Email"];
  const types = ["commit", "comment", "document", "meeting", "notification"];

  const filteredItems = useMemo(() => {
    return activities.filter(item => {
      const matchesSearch = item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                           item.description.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesSource = selectedSources.length === 0 || selectedSources.includes(item.source);
      const matchesType = selectedTypes.length === 0 || selectedTypes.includes(item.type);
      return matchesSearch && matchesSource && matchesType;
    });
  }, [activities, searchQuery, selectedSources, selectedTypes]);

  const toggleSource = (source: string) => {
    setSelectedSources(prev => 
      prev.includes(source) 
        ? prev.filter(s => s !== source)
        : [...prev, source]
    );
  };

  const toggleType = (type: string) => {
    setSelectedTypes(prev => 
      prev.includes(type) 
        ? prev.filter(t => t !== type)
        : [...prev, type]
    );
  };

  const toggleExpanded = (id: string) => {
    setExpandedItems(prev => 
      prev.includes(id) 
        ? prev.filter(i => i !== id)
        : [...prev, id]
    );
  };

  const getActivityIcon = (type: string) => {
    switch (type) {
      case "commit": return GitCommit;
      case "comment": return MessageSquare;
      case "document": return FileText;
      case "meeting": return Calendar;
      case "notification": return Bell;
      default: return FileText;
    }
  };

  const getSourceColor = (source: string) => {
    switch (source) {
      case "GitHub": return "bg-card text-card-foreground border-border";
      case "Jira": return "bg-card text-card-foreground border-border";
      case "Confluence": return "bg-card text-card-foreground border-border";
      case "Slack": return "bg-card text-card-foreground border-border";
      case "Zoom": return "bg-card text-card-foreground border-border";
      case "Email": return "bg-card text-card-foreground border-border";
      default: return "bg-card text-card-foreground border-border";
    }
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case "commit": return "bg-[#a3cae9]/30 text-[#395a7f] dark:bg-[#395a7f]/15 dark:text-[#a3cae9]";
      case "comment": return "bg-[#6e9fc1]/20 text-[#395a7f] dark:bg-[#395a7f]/20 dark:text-[#6e9fc1]";
      case "document": return "bg-[#e9ecee]/70 text-[#6e9fc1] dark:bg-[#6e9fc1]/10 dark:text-[#e9ecee]";
      case "meeting": return "bg-[#e9ecee]/80 text-[#6e9fc1] dark:bg-[#6e9fc1]/10 dark:text-[#e9ecee]";
      case "notification": return "bg-[#acacac]/20 text-[#acacac] dark:bg-[#acacac]/10 dark:text-[#e9ecee]";
      default: return "bg-card text-card-foreground border-border";
    }
  };

  return (
    <div className="flex h-full bg-background">
      {/* Filter Sidebar */}
      <div className="w-64 border-r border-border bg-card flex flex-col">
        <div className="p-4 border-b border-border">
          <h3 className="font-medium text-sm mb-3">Filters</h3>
          
          {/* Search */}
          <div className="relative mb-4">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <Input
              type="text"
              placeholder="Search activities..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 h-9 bg-background border-border"
            />
          </div>

          {/* Sources Filter */}
          <div className="mb-4">
            <h4 className="text-xs font-medium text-muted-foreground mb-2">Sources</h4>
            <div className="space-y-2">
              {sources.map((source) => (
                <label key={source} className="flex items-center gap-2 text-sm cursor-pointer">
                  <input
                    type="checkbox"
                    checked={selectedSources.includes(source)}
                    onChange={() => toggleSource(source)}
                    className="rounded border-border"
                  />
                  <span>{source}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Types Filter */}
          <div>
            <h4 className="text-xs font-medium text-muted-foreground mb-2">Types</h4>
            <div className="space-y-2">
              {types.map((type) => (
                <label key={type} className="flex items-center gap-2 text-sm cursor-pointer">
                  <input
                    type="checkbox"
                    checked={selectedTypes.includes(type)}
                    onChange={() => toggleType(type)}
                    className="rounded border-border"
                  />
                  <span className="capitalize">{type}</span>
                </label>
              ))}
            </div>
          </div>
        </div>

        {/* Stats */}
        <div className="p-4 border-b border-border">
          <h4 className="text-xs font-medium text-muted-foreground mb-2">Today's Activity</h4>
          <div className="space-y-2">
            <div className="flex items-center justify-between text-sm">
              <span>Total Events</span>
              <Badge variant="secondary">24</Badge>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span>Unread</span>
              <Badge variant="secondary">3</Badge>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span>Active Sources</span>
              <Badge variant="secondary">6</Badge>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-border bg-card">
          <div>
            <h2 className="text-lg font-semibold">Activity Pulse</h2>
            <p className="text-sm text-muted-foreground">Real-time feed of all project activities</p>
          </div>
          
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm">
              <BarChart3 className="w-4 h-4 mr-1" />
              Analytics
            </Button>
            <Button size="sm">
              <Bell className="w-4 h-4 mr-1" />
              Subscribe
            </Button>
          </div>
        </div>

        {/* Activity Feed */}
        <ScrollArea className="flex-1">
          <div className="p-4 space-y-4">
            {filteredItems.map((item) => {
              const Icon = getActivityIcon(item.type);
              const isExpanded = expandedItems.includes(item.id);
              
              return (
                <div key={item.id} className="bg-card rounded-lg border border-border p-4 hover:bg-muted/50 transition-colors">
                  <div className="flex items-start gap-3">
                    <div className="flex-shrink-0">
                      <div className="w-8 h-8 rounded-full bg-muted flex items-center justify-center">
                        <Icon className="w-4 h-4" />
                      </div>
                    </div>
                    
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between mb-1">
                        <h4 className="font-medium text-sm truncate pr-2">{item.title}</h4>
                        <div className="flex items-center gap-2">
                          {!item.isRead && (
                            <div className="w-2 h-2 rounded-full" style={{ backgroundColor: '#6e9fc1' }} />
                          )}
                          <Badge className={cn("text-xs", getSourceColor(item.source))}>
                            {item.source}
                          </Badge>
                        </div>
                      </div>
                      
                      <p className="text-sm text-muted-foreground mb-2">{item.description}</p>
                      
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <Badge className={cn("text-xs", getTypeColor(item.type))}>
                            {item.type}
                          </Badge>
                          <span className="text-xs text-muted-foreground">{item.user.name}</span>
                          <span className="text-xs text-muted-foreground">•</span>
                          <span className="text-xs text-muted-foreground">{item.timestamp}</span>
                        </div>
                        
                        <div className="flex items-center gap-1">
                          <Button variant="ghost" size="sm" className="h-6 w-6 p-0">
                            <Eye className="w-3 h-3" />
                          </Button>
                          <Button 
                            variant="ghost" 
                            size="sm" 
                            className="h-6 w-6 p-0"
                            onClick={() => toggleExpanded(item.id)}
                          >
                            {isExpanded ? (
                              <ChevronDown className="w-3 h-3" />
                            ) : (
                              <ChevronRight className="w-3 h-3" />
                            )}
                          </Button>
                        </div>
                      </div>

                      {/* Expanded Content */}
                      {isExpanded && item.metadata && (
                        <div className="mt-3 pt-3 border-t border-border">
                          <div className="grid grid-cols-2 gap-4 text-xs">
                            {item.metadata.repository && (
                              <div>
                                <span className="text-muted-foreground">Repository:</span>
                                <span className="ml-1 font-medium">{item.metadata.repository}</span>
                              </div>
                            )}
                            {item.metadata.branch && (
                              <div>
                                <span className="text-muted-foreground">Branch:</span>
                                <span className="ml-1 font-medium">{item.metadata.branch}</span>
                              </div>
                            )}
                            {item.metadata.fileName && (
                              <div>
                                <span className="text-muted-foreground">File:</span>
                                <span className="ml-1 font-medium">{item.metadata.fileName}</span>
                              </div>
                            )}
                            {item.metadata.participants && (
                              <div>
                                <span className="text-muted-foreground">Participants:</span>
                                <span className="ml-1 font-medium">{item.metadata.participants}</span>
                              </div>
                            )}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}

            {filteredItems.length === 0 && (
              <div className="flex flex-col items-center justify-center py-12 text-center">
                <div className="text-4xl mb-4">📊</div>
                <h3 className="text-lg font-medium mb-2">No activities found</h3>
                <p className="text-muted-foreground text-sm">
                  {searchQuery || selectedSources.length > 0 || selectedTypes.length > 0
                    ? "Try adjusting your filters"
                    : "Activity feed will appear here as events occur"
                  }
                </p>
              </div>
            )}
          </div>
        </ScrollArea>
      </div>
    </div>
  );
}