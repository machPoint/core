"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { 
  Search, 
  Filter,
  Settings,
  Users,
  Database,
  Shield,
  Activity,
  BarChart3,
  RefreshCw,
  Download,
  Upload,
  AlertTriangle,
  CheckCircle,
  Clock,
  TrendingUp,
  Server,
  HardDrive,
  Cpu,
  Wifi,
  MoreHorizontal,
  Factory,
  Trash2,
  PlayCircle,
  StopCircle,
  RotateCcw,
  FileText,
  PlusCircle
} from "lucide-react";
import { cn } from "@/lib/utils";
import { toast } from "sonner";
import { useDataMode, DataMode } from "@/contexts/DataModeContext";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";

interface SystemMetric {
  id: string;
  name: string;
  value: string;
  status: "healthy" | "warning" | "critical";
  trend: "up" | "down" | "stable";
  lastUpdated: string;
}

interface AdminUser {
  id: string;
  name: string;
  email: string;
  role: "admin" | "moderator" | "user";
  status: "active" | "inactive" | "suspended";
  lastActive: string;
  permissions: string[];
}

const mockSystemMetrics: SystemMetric[] = [
  {
    id: "1",
    name: "CPU Usage",
    value: "23%",
    status: "healthy",
    trend: "stable",
    lastUpdated: "2 minutes ago"
  },
  {
    id: "2",
    name: "Memory Usage",
    value: "78%",
    status: "warning",
    trend: "up",
    lastUpdated: "2 minutes ago"
  },
  {
    id: "3",
    name: "Disk Space",
    value: "45%",
    status: "healthy",
    trend: "stable",
    lastUpdated: "2 minutes ago"
  },
  {
    id: "4",
    name: "Network I/O",
    value: "1.2 GB/s",
    status: "healthy",
    trend: "down",
    lastUpdated: "2 minutes ago"
  }
];

const mockUsers: AdminUser[] = [
  {
    id: "1",
    name: "Sarah Chen",
    email: "sarah.chen@company.com",
    role: "admin",
    status: "active",
    lastActive: "5 minutes ago",
    permissions: ["read", "write", "delete", "admin"]
  },
  {
    id: "2",
    name: "Mike Rodriguez",
    email: "mike.rodriguez@company.com",
    role: "moderator",
    status: "active",
    lastActive: "1 hour ago",
    permissions: ["read", "write", "moderate"]
  },
  {
    id: "3",
    name: "Alex Kim",
    email: "alex.kim@company.com",
    role: "user",
    status: "inactive",
    lastActive: "2 days ago",
    permissions: ["read", "write"]
  }
];

interface FDSStatus {
  isRunning: boolean;
  dataStats: {
    jamaItems: number;
    jiraIssues: number;
    windchillParts: number;
    emailMessages: number;
    outlookMessages: number;
    pulseItems: number;
  };
  lastSeeded: string | null;
}

export default function AdminSection() {
  const { dataMode, setDataMode, isUsingFakeData, isStreaming } = useDataMode();
  const [activeTab, setActiveTab] = useState<"dashboard" | "users" | "system" | "security" | "data">("dashboard");
  const [searchQuery, setSearchQuery] = useState("");
  const [metrics, setMetrics] = useState(mockSystemMetrics);
  const [users] = useState(mockUsers);
  const [isLoading, setIsLoading] = useState(false);
  const [fdsStatus, setFdsStatus] = useState<FDSStatus>({
    isRunning: true,
    dataStats: {
      jamaItems: 142,
      jiraIssues: 28,
      windchillParts: 19,
      emailMessages: 10,
      outlookMessages: 10,
      pulseItems: 89
    },
    lastSeeded: "2 hours ago"
  });
  const [isSeeding, setIsSeeding] = useState(false);

  const refreshMetrics = () => {
    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
      toast.success("System metrics refreshed");
    }, 1000);
  };

  const seedFakeData = async () => {
    setIsSeeding(true);
    try {
      const response = await fetch('http://localhost:4000/mock/admin/seed', {
        method: 'POST',
      });
      
      if (response.ok) {
        // Update stats with new random numbers
        setFdsStatus(prev => ({
          ...prev,
          dataStats: {
            jamaItems: Math.floor(Math.random() * 50) + 120,
            jiraIssues: Math.floor(Math.random() * 15) + 20,
            windchillParts: Math.floor(Math.random() * 10) + 15,
            emailMessages: 10,
            outlookMessages: 10,
            pulseItems: Math.floor(Math.random() * 30) + 70
          },
          lastSeeded: "Just now"
        }));
        toast.success("Fake data regenerated successfully!");
      } else {
        throw new Error('Failed to seed data');
      }
    } catch (error) {
      toast.error("Failed to seed fake data. Make sure FDS is running on port 4000.");
    } finally {
      setIsSeeding(false);
    }
  };

  const checkFDSHealth = async () => {
    try {
      const response = await fetch('http://localhost:4000/health');
      const isHealthy = response.ok;
      setFdsStatus(prev => ({ ...prev, isRunning: isHealthy }));
      return isHealthy;
    } catch (error) {
      setFdsStatus(prev => ({ ...prev, isRunning: false }));
      return false;
    }
  };

  const resetFakeData = () => {
    toast.info("Reset functionality would clear all generated data");
  };

  const exportData = () => {
    toast.info("Data export would download current dataset");
  };

  useEffect(() => {
    // Check FDS health on component mount
    checkFDSHealth();
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case "healthy": return "text-green-600 dark:text-green-400";
      case "warning": return "text-yellow-600 dark:text-yellow-400";
      case "critical": return "text-red-600 dark:text-red-400";
      case "active": return "text-green-600 dark:text-green-400";
      case "inactive": return "text-yellow-600 dark:text-yellow-400";
      case "suspended": return "text-red-600 dark:text-red-400";
      default: return "text-muted-foreground";
    }
  };

  const getStatusBadgeColor = (status: string) => {
    switch (status) {
      case "healthy": return "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200";
      case "warning": return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200";
      case "critical": return "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200";
      case "active": return "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200";
      case "inactive": return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200";
      case "suspended": return "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200";
      default: return "bg-card text-card-foreground";
    }
  };

  const getRoleColor = (role: string) => {
    switch (role) {
      case "admin": return "bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200";
      case "moderator": return "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200";
      case "user": return "bg-card text-card-foreground";
      default: return "bg-card text-card-foreground";
    }
  };

  const getMetricIcon = (name: string) => {
    switch (name.toLowerCase()) {
      case "cpu usage": return Cpu;
      case "memory usage": return HardDrive;
      case "disk space": return Database;
      case "network i/o": return Wifi;
      default: return Activity;
    }
  };

  const filteredUsers = users.filter(user =>
    user.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    user.email.toLowerCase().includes(searchQuery.toLowerCase()) ||
    user.role.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const renderDashboard = () => (
    <div className="space-y-6">
      {/* System Overview */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-medium">System Overview</h3>
          <Button variant="outline" size="sm" onClick={refreshMetrics} disabled={isLoading}>
            <RefreshCw className={cn("w-4 h-4 mr-1", isLoading && "animate-spin")} />
            Refresh
          </Button>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {metrics.map((metric) => {
            const Icon = getMetricIcon(metric.name);
            return (
              <div key={metric.id} className="bg-card rounded-lg border border-border p-4">
                <div className="flex items-center justify-between mb-2">
                  <Icon className="w-5 h-5 text-muted-foreground" />
                  <Badge className={cn("text-xs", getStatusBadgeColor(metric.status))}>
                    {metric.status}
                  </Badge>
                </div>
                <div className="space-y-1">
                  <p className="text-2xl font-bold">{metric.value}</p>
                  <p className="text-sm text-muted-foreground">{metric.name}</p>
                  <p className="text-xs text-muted-foreground">Updated {metric.lastUpdated}</p>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Quick Actions */}
      <div>
        <h3 className="text-lg font-medium mb-4">Quick Actions</h3>
        <div className="grid grid-cols-2 lg:grid-cols-5 gap-4">
          <Button 
            variant="outline" 
            className="h-auto p-4 flex flex-col items-center gap-2"
            onClick={() => setActiveTab("users")}
          >
            <Users className="w-6 h-6" />
            <span className="text-sm">Manage Users</span>
          </Button>
          <Button 
            variant="outline" 
            className="h-auto p-4 flex flex-col items-center gap-2"
            onClick={() => setActiveTab("data")}
          >
            <Factory className="w-6 h-6" />
            <span className="text-sm">Data Generator</span>
          </Button>
          <Button variant="outline" className="h-auto p-4 flex flex-col items-center gap-2">
            <Database className="w-6 h-6" />
            <span className="text-sm">Database</span>
          </Button>
          <Button variant="outline" className="h-auto p-4 flex flex-col items-center gap-2">
            <Shield className="w-6 h-6" />
            <span className="text-sm">Security</span>
          </Button>
          <Button variant="outline" className="h-auto p-4 flex flex-col items-center gap-2">
            <BarChart3 className="w-6 h-6" />
            <span className="text-sm">Analytics</span>
          </Button>
        </div>
      </div>

      {/* Recent Activity */}
      <div>
        <h3 className="text-lg font-medium mb-4">Recent Activity</h3>
        <div className="bg-card rounded-lg border border-border p-4">
          <div className="space-y-3">
            {[
              { action: "User login", user: "sarah.chen@company.com", time: "2 minutes ago", status: "success" },
              { action: "Database backup", user: "System", time: "1 hour ago", status: "success" },
              { action: "Failed login attempt", user: "unknown@example.com", time: "3 hours ago", status: "warning" },
              { action: "Permission change", user: "mike.rodriguez@company.com", time: "5 hours ago", status: "info" }
            ].map((activity, index) => (
              <div key={index} className="flex items-center justify-between py-2 border-b border-border last:border-b-0">
                <div>
                  <p className="text-sm font-medium">{activity.action}</p>
                  <p className="text-xs text-muted-foreground">{activity.user}</p>
                </div>
                <div className="text-right">
                  <p className="text-xs text-muted-foreground">{activity.time}</p>
                  <Badge variant="outline" className="text-xs">
                    {activity.status}
                  </Badge>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );

  const renderDataManagement = () => (
    <div className="space-y-6">
      {/* Data Mode Selector */}
      <div>
        <h3 className="text-lg font-medium mb-4">Data Source Mode</h3>
        <div className="bg-card rounded-lg border border-border p-6">
          <div className="space-y-4">
            <p className="text-sm text-muted-foreground mb-4">
              Choose how the application retrieves data. Switch between real server connections or demo modes without server dependencies.
            </p>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Real Data Mode */}
              <button
                onClick={() => {
                  setDataMode('real');
                  toast.success('Switched to Real Data mode - connecting to OPAL and FDS servers');
                }}
                className={cn(
                  "p-4 rounded-lg border-2 transition-all text-left",
                  dataMode === 'real'
                    ? "border-[#6e9fc1] bg-[#6e9fc1]/10"
                    : "border-border hover:border-[#6e9fc1]/50"
                )}
              >
                <div className="flex items-center gap-2 mb-2">
                  <Server className="w-5 h-5 text-[#6e9fc1]" />
                  <h4 className="font-semibold">Real Data</h4>
                  {dataMode === 'real' && (
                    <Badge className="ml-auto bg-[#6e9fc1] text-white">Active</Badge>
                  )}
                </div>
                <p className="text-sm text-muted-foreground">
                  Connect to OPAL MCP Server and FDS. Requires both servers running.
                </p>
              </button>

              {/* Static Fake Data Mode */}
              <button
                onClick={() => {
                  setDataMode('fake-static');
                  toast.success('Switched to Static Fake Data mode - using pre-generated demo data');
                }}
                className={cn(
                  "p-4 rounded-lg border-2 transition-all text-left",
                  dataMode === 'fake-static'
                    ? "border-[#a3cae9] bg-[#a3cae9]/10"
                    : "border-border hover:border-[#a3cae9]/50"
                )}
              >
                <div className="flex items-center gap-2 mb-2">
                  <Database className="w-5 h-5 text-[#a3cae9]" />
                  <h4 className="font-semibold">Static Fake Data</h4>
                  {dataMode === 'fake-static' && (
                    <Badge className="ml-auto bg-[#a3cae9] text-white">Active</Badge>
                  )}
                </div>
                <p className="text-sm text-muted-foreground">
                  Use pre-generated fake data. No server connection needed.
                </p>
              </button>

              {/* Streaming Fake Data Mode */}
              <button
                onClick={() => {
                  setDataMode('fake-streaming');
                  toast.success('Switched to Streaming Fake Data mode - live updates enabled');
                }}
                className={cn(
                  "p-4 rounded-lg border-2 transition-all text-left",
                  dataMode === 'fake-streaming'
                    ? "border-[#395a7f] bg-[#395a7f]/10"
                    : "border-border hover:border-[#395a7f]/50"
                )}
              >
                <div className="flex items-center gap-2 mb-2">
                  <Activity className="w-5 h-5 text-[#395a7f]" />
                  <h4 className="font-semibold">Streaming Fake Data</h4>
                  {dataMode === 'fake-streaming' && (
                    <Badge className="ml-auto bg-[#395a7f] text-white">Active</Badge>
                  )}
                </div>
                <p className="text-sm text-muted-foreground">
                  Fake data with live streaming updates. Perfect for demos.
                </p>
              </button>
            </div>

            {/* Current Mode Info */}
            <div className="pt-4 border-t border-border">
              <div className="flex items-center gap-2">
                <div className={cn(
                  "w-2 h-2 rounded-full",
                  dataMode === 'real' ? "bg-[#6e9fc1]" : 
                  dataMode === 'fake-static' ? "bg-[#a3cae9]" : "bg-[#395a7f]"
                )} />
                <p className="text-sm font-medium">
                  Current Mode: {
                    dataMode === 'real' ? 'Real Data (Server Connected)' :
                    dataMode === 'fake-static' ? 'Static Fake Data (Offline Demo)' :
                    'Streaming Fake Data (Live Demo)'
                  }
                </p>
              </div>
              {isUsingFakeData && (
                <p className="text-xs text-muted-foreground mt-2">
                  ⚠️ Running in demo mode - no server connection required. All data is simulated.
                </p>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* FDS Status - Only show when in real mode */}
      {dataMode === 'real' && (
        <div>
          <h3 className="text-lg font-medium mb-4">Fake Data Service Status</h3>
        <div className="bg-card rounded-lg border border-border p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <div className={cn(
                "w-3 h-3 rounded-full",
                fdsStatus.isRunning ? "bg-[#6e9fc1]" : "bg-[#acacac]"
              )} />
              <div>
                <p className="font-medium">
                  {fdsStatus.isRunning ? "Service Running" : "Service Offline"}
                </p>
                <p className="text-sm text-muted-foreground">
                  {fdsStatus.isRunning 
                    ? "Fake Data Service is operational on port 4000"
                    : "Cannot connect to Fake Data Service"
                  }
                </p>
              </div>
            </div>
            <Button variant="outline" size="sm" onClick={checkFDSHealth}>
              <RefreshCw className="w-4 h-4 mr-1" />
              Check Status
            </Button>
          </div>
          
          {fdsStatus.lastSeeded && (
            <p className="text-sm text-muted-foreground">
              Last data generation: {fdsStatus.lastSeeded}
            </p>
          )}
        </div>
        </div>
      )}

      {/* Data Statistics - Only show when in real mode */}
      {dataMode === 'real' && (
      <div>
        <h3 className="text-lg font-medium mb-4">Current Dataset</h3>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {[
            { label: "Jama Items", value: fdsStatus.dataStats.jamaItems, icon: FileText, color: "text-[#395a7f]" },
            { label: "Jira Issues", value: fdsStatus.dataStats.jiraIssues, icon: AlertTriangle, color: "text-[#6e9fc1]" },
            { label: "Windchill Parts", value: fdsStatus.dataStats.windchillParts, icon: Settings, color: "text-[#a3cae9]" },
            { label: "Email Messages", value: fdsStatus.dataStats.emailMessages, icon: Activity, color: "text-[#acacac]" },
            { label: "Outlook Messages", value: fdsStatus.dataStats.outlookMessages, icon: Activity, color: "text-[#395a7f]" },
            { label: "Pulse Items", value: fdsStatus.dataStats.pulseItems, icon: TrendingUp, color: "text-[#6e9fc1]" }
          ].map((stat) => {
            const Icon = stat.icon;
            return (
              <div key={stat.label} className="bg-card rounded-lg border border-border p-4">
                <div className="flex items-center justify-between mb-2">
                  <Icon className={cn("w-5 h-5", stat.color)} />
                </div>
                <div className="space-y-1">
                  <p className="text-2xl font-bold">{stat.value}</p>
                  <p className="text-sm text-muted-foreground">{stat.label}</p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
      )}

      {/* Data Management Actions - Only show when in real mode */}
      {dataMode === 'real' && (
      <div>
        <h3 className="text-lg font-medium mb-4">Data Management</h3>
        <div className="bg-card rounded-lg border border-border p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <Button 
              onClick={seedFakeData}
              disabled={isSeeding || !fdsStatus.isRunning}
              className="h-auto p-4 flex flex-col items-center gap-2"
            >
              <PlusCircle className={cn("w-6 h-6", isSeeding && "animate-spin")} />
              <span className="text-sm font-medium">
                {isSeeding ? "Generating..." : "Generate New Data"}
              </span>
              <span className="text-xs text-muted-foreground">
                Create fresh dataset
              </span>
            </Button>
            
            <Button 
              variant="outline"
              onClick={resetFakeData}
              disabled={!fdsStatus.isRunning}
              className="h-auto p-4 flex flex-col items-center gap-2"
            >
              <RotateCcw className="w-6 h-6" />
              <span className="text-sm font-medium">Reset Data</span>
              <span className="text-xs text-muted-foreground">
                Clear all generated data
              </span>
            </Button>
            
            <Button 
              variant="outline"
              onClick={exportData}
              disabled={!fdsStatus.isRunning}
              className="h-auto p-4 flex flex-col items-center gap-2"
            >
              <Download className="w-6 h-6" />
              <span className="text-sm font-medium">Export Data</span>
              <span className="text-xs text-muted-foreground">
                Download current dataset
              </span>
            </Button>
            
            <Button 
              variant="outline"
              onClick={() => window.open('http://localhost:4000/docs', '_blank')}
              disabled={!fdsStatus.isRunning}
              className="h-auto p-4 flex flex-col items-center gap-2"
            >
              <FileText className="w-6 h-6" />
              <span className="text-sm font-medium">API Docs</span>
              <span className="text-xs text-muted-foreground">
                View FDS documentation
              </span>
            </Button>
          </div>
        </div>
      </div>
      )}

      {/* Data Generation Settings - Only show when in real mode */}
      {dataMode === 'real' && (
      <div>
        <h3 className="text-lg font-medium mb-4">Generation Settings</h3>
        <div className="bg-card rounded-lg border border-border p-6">
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium mb-2 block">Requirements Count</label>
                <div className="text-sm text-muted-foreground">80-100 items (randomized)</div>
              </div>
              <div>
                <label className="text-sm font-medium mb-2 block">Test Cases Count</label>
                <div className="text-sm text-muted-foreground">40-60 items (randomized)</div>
              </div>
              <div>
                <label className="text-sm font-medium mb-2 block">Traceability Gaps</label>
                <div className="text-sm text-muted-foreground">~15% coverage gaps</div>
              </div>
              <div>
                <label className="text-sm font-medium mb-2 block">Outlook Integration</label>
                <div className="text-sm text-muted-foreground">10 messages with meeting requests</div>
              </div>
            </div>
            <div className="pt-4 border-t border-border">
              <p className="text-sm text-muted-foreground">
                Data generation follows the PRD specifications with realistic engineering artifacts,
                proper cross-linking between systems, and intentional gaps for demo purposes.
              </p>
            </div>
          </div>
        </div>
      </div>
      )}
    </div>
  );

  const renderUsers = () => (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-medium">User Management</h3>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm">
            <Download className="w-4 h-4 mr-1" />
            Export
          </Button>
          <Button size="sm">
            <Upload className="w-4 h-4 mr-1" />
            Import
          </Button>
        </div>
      </div>

      <div className="bg-card rounded-lg border border-border">
        <div className="p-4 border-b border-border">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <Input
              type="text"
              placeholder="Search users..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 bg-background border-border"
            />
          </div>
        </div>

        <div className="divide-y divide-border">
          {filteredUsers.map((user) => (
            <div key={user.id} className="p-4 hover:bg-muted/50 transition-colors">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-muted flex items-center justify-center">
                    <span className="text-sm font-medium">
                      {user.name.split(' ').map(n => n[0]).join('')}
                    </span>
                  </div>
                  <div>
                    <p className="font-medium text-sm">{user.name}</p>
                    <p className="text-xs text-muted-foreground">{user.email}</p>
                  </div>
                </div>
                
                <div className="flex items-center gap-3">
                  <div className="text-right">
                    <Badge className={cn("text-xs mb-1", getRoleColor(user.role))}>
                      {user.role}
                    </Badge>
                    <p className="text-xs text-muted-foreground">Last active: {user.lastActive}</p>
                  </div>
                  
                  <Badge className={cn("text-xs", getStatusBadgeColor(user.status))}>
                    {user.status}
                  </Badge>
                  
                  <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
                    <MoreHorizontal className="w-4 h-4" />
                  </Button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderContent = () => {
    if (isLoading) {
      return (
        <div className="flex items-center justify-center h-64 bg-card rounded-lg border border-border">
          <div className="text-center">
            <RefreshCw className="w-8 h-8 animate-spin mx-auto mb-2 text-muted-foreground" />
            <p className="text-muted-foreground">Loading...</p>
          </div>
        </div>
      );
    }

    switch (activeTab) {
      case "dashboard": return renderDashboard();
      case "users": return renderUsers();
      case "data": return renderDataManagement();
      case "system":
      case "security":
        return (
          <div className="flex flex-col items-center justify-center py-12 text-center">
            <div className="text-4xl mb-4">🚧</div>
            <h3 className="text-lg font-medium mb-2">Coming Soon</h3>
            <p className="text-muted-foreground text-sm">
              {activeTab === "system" ? "System configuration" : "Security settings"} panel will be available soon
            </p>
          </div>
        );
      default: return renderDashboard();
    }
  };

  return (
    <div className="flex h-full bg-background">
      {/* Sidebar */}
      <div className="w-64 border-r border-border bg-card flex flex-col">
        <div className="p-4 border-b border-border">
          <h2 className="text-lg font-semibold">Administration</h2>
        </div>
        
        <div className="flex-1 p-4">
          <nav className="space-y-2">
            {[
              { id: "dashboard", label: "Dashboard", icon: BarChart3 },
              { id: "users", label: "Users", icon: Users },
              { id: "data", label: "Data Management", icon: Factory },
              { id: "system", label: "System", icon: Server },
              { id: "security", label: "Security", icon: Shield }
            ].map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={cn(
                    "w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors",
                    activeTab === tab.id
                      ? "bg-primary text-primary-foreground"
                      : "hover:bg-muted text-muted-foreground hover:text-foreground"
                  )}
                >
                  <Icon className="w-4 h-4" />
                  {tab.label}
                </button>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        <div className="flex items-center justify-between p-4 border-b border-border bg-card">
          <div>
            <h3 className="text-lg font-medium capitalize">{activeTab}</h3>
            <p className="text-sm text-muted-foreground">
              {activeTab === "dashboard" && "System overview and quick actions"}
              {activeTab === "users" && "Manage user accounts and permissions"}
              {activeTab === "data" && "Control fake data generation and manage datasets"}
              {activeTab === "system" && "Configure system settings"}
              {activeTab === "security" && "Security and access control"}
            </p>
          </div>
          
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm">
              <Settings className="w-4 h-4 mr-1" />
              Settings
            </Button>
          </div>
        </div>

        <ScrollArea className="flex-1">
          <div className="p-6">
            {renderContent()}
          </div>
        </ScrollArea>
      </div>
    </div>
  );
}
