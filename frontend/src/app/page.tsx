"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Toaster } from "sonner";
import { ChevronDown, ChevronRight, Folder, Hash, NotepadText } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { ScrollArea } from "@/components/ui/scroll-area";
import { ThemeProvider, useTheme } from "@/hooks/use-theme";
import { Panel, PanelGroup, PanelResizeHandle } from "react-resizable-panels";
import TopBar from "@/components/TopBar";
import LeftNav from "@/components/LeftNav";
import RightContextPanel from "@/components/RightContextPanel";
import AIChatPanel from "@/components/AIChatPanel";
import NotesSection from "@/components/NotesSection";
import PulseSection from "@/components/PulseSection";
import TasksSection from "@/components/TasksSection";
import ToolWindowSection from "@/components/ToolWindowSection";
import TraceImpactSection from "@/components/TraceImpactSection";
import KnowledgeAgentsSection from "@/components/KnowledgeAgentsSection";
import AdminSection from "@/components/AdminSection";
import TestSection from "@/components/TestSection";
import DataEngineSection from "@/components/DataEngineSection";
import RelationshipsSection from "@/components/RelationshipsSection";
import AgentsSection from "@/components/AgentsSection";
import SystemAdminSection from "@/components/SystemAdminSection";

// Generate mock context data
function generateContextData() {
  return {
    relatedItems: [
      {
        id: "1",
        type: "requirement" as const,
        title: "API Documentation v2.1",
        owner: "Sarah Chen",
        lastUpdated: "2 hours ago",
        sourceColor: "#3b82f6",
        isReadOnly: false
      },
      {
        id: "2", 
        type: "test" as const,
        title: "OAuth2 Integration Tests",
        owner: "Mike Rodriguez",
        lastUpdated: "4 hours ago",
        sourceColor: "#10b981",
        isReadOnly: true
      },
      {
        id: "3",
        type: "issue" as const,
        title: "Database Schema Changes",
        owner: "Alex Kim",
        lastUpdated: "1 day ago",
        sourceColor: "#f59e0b",
        isReadOnly: false
      }
    ],
    aiInsights: [
      {
        id: "1",
        type: "coverage" as const,
        title: "Test Coverage Analysis",
        description: "Current test coverage is at 78% across all modules. Consider adding tests for edge cases.",
        severity: "medium" as const,
        source: "AI Analysis",
        timestamp: "1 hour ago",
        percentage: 78
      },
      {
        id: "2",
        type: "suggestion" as const,
        title: "Performance Optimization",
        description: "Database queries can be optimized by adding proper indexes to user table.",
        severity: "low" as const,
        source: "Performance AI",
        timestamp: "3 hours ago"
      },
      {
        id: "3",
        type: "risk" as const,
        title: "Security Vulnerability",
        description: "Potential SQL injection risk detected in user input validation.",
        severity: "high" as const,
        source: "Security AI",
        timestamp: "5 hours ago"
      }
    ]
  };
}

// Generate mock folders data
function generateFoldersData() {
  return [
    { id: "1", name: "Architecture", count: 12, color: "#395a7f" },
    { id: "2", name: "Requirements", count: 8, color: "#6e9fc1" },
    { id: "3", name: "Meeting Notes", count: 15, color: "#a3cae9" },
    { id: "4", name: "Ideas", count: 5, color: "#acacac" }
  ];
}

// Generate mock tags data
function generateTagsData() {
  return [
    { id: "1", name: "engineering", count: 20, color: "#395a7f" },
    { id: "2", name: "design", count: 12, color: "#6e9fc1" },
    { id: "3", name: "research", count: 8, color: "#a3cae9" },
    { id: "4", name: "urgent", count: 3, color: "#acacac" }
  ];
}

// Generate mock notes data
function generateNotesData() {
  return [
    {
      id: "1",
      title: "System Architecture Overview",
      content: "# System Architecture This document outlines the high-level architecture for our distributed...",
      tags: ["engineering", "architecture"],
      folder: "Architecture",
      lastSynced: new Date(),
      isSourced: false
    },
    {
      id: "2", 
      title: "API Requirements Document",
      content: "Requirements imported from Jira ticket @REQ-456...",
      tags: ["requirements"],
      folder: "Requirements",
      lastSynced: new Date(),
      isSourced: true,
      sourceType: "jira"
    },
    {
      id: "3",
      title: "Database Schema Design",
      content: "Database design patterns and schema definitions...",
      tags: ["engineering", "design"],
      folder: "Architecture",
      lastSynced: new Date(Date.now() - 86400000),
      isSourced: false
    },
    {
      id: "4",
      title: "Meeting Notes - Sprint Planning",
      content: "Sprint planning meeting notes and action items...",
      tags: ["urgent"],
      folder: "Meeting Notes",
      lastSynced: new Date(Date.now() - 3600000),
      isSourced: false
    }
  ];
}

function PageContent() {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState("pulse");
  const [leftNavCollapsed, setLeftNavCollapsed] = useState(false);
  const [contextPanelCollapsed, setContextPanelCollapsed] = useState(false);
  const [foldersPanelCollapsed, setFoldersPanelCollapsed] = useState(false);
  const [tagsPanelCollapsed, setTagsPanelCollapsed] = useState(false);
  const [notesPanelCollapsed, setNotesPanelCollapsed] = useState(false);
  const [showAdminDialog, setShowAdminDialog] = useState(false);
  const [useAIChat, setUseAIChat] = useState(true); // Toggle between AI Chat and Related Items
  const { theme } = useTheme();

  const foldersData = generateFoldersData();
  const tagsData = generateTagsData();
  const notesData = generateNotesData();


  const renderActiveSection = () => {
    switch (activeTab) {
      case "notes":
        return <NotesSection />;
      case "pulse":
        return <PulseSection />;
      case "requirements":
        return <ToolWindowSection />;
      case "design":
        return <ToolWindowSection />;
      case "verification":
        return <ToolWindowSection />;
      case "trace":
        return <TraceImpactSection />;
      case "impact":
        return <TraceImpactSection />;
      case "relationships":
        return <RelationshipsSection />;
      case "knowledge":
        return <KnowledgeAgentsSection />;
      case "tasks":
        return <TasksSection />;
      case "test":
        return <TestSection />;
      case "data-engine":
        return <DataEngineSection />;
      case "agents":
        return <AgentsSection />;
      case "system-admin":
        return <SystemAdminSection />;
      default:
        return <PulseSection />;
    }
  };

  return (
    <div className="h-screen flex flex-col bg-[var(--color-background)]">
      {/* Top Bar */}
      <TopBar 
        breadcrumbs={[
          { id: "workspace", label: "Aerospace Engineering Workspace" },
          { id: "section", label: activeTab.charAt(0).toUpperCase() + activeTab.slice(1) }
        ]}
        onSearchSubmit={(query) => console.log("Search:", query)}
        onBreadcrumbClick={(id) => console.log("Breadcrumb clicked:", id)}
        onAdminClick={() => setShowAdminDialog(true)}
        className="flex-shrink-0 h-16"
      />

      {/* Main Content Grid with Resizable Panels */}
      <div className="flex-1 overflow-hidden">
        <PanelGroup direction="horizontal" className="h-full">
          {/* Left Panel Stack - Navigation + Folders + Tags + Notes */}
          <Panel defaultSize={12} minSize={10} maxSize={40} className="bg-[var(--color-left-panel)] border-r border-border flex flex-col">
          {/* Navigation Panel */}
          <div className="border-b border-border/50">
            <div className="flex items-center justify-between p-4">
              <h3 className="text-sm font-medium text-[var(--color-text-primary)]">Navigation</h3>
              <button
                onClick={() => setLeftNavCollapsed(!leftNavCollapsed)}
                className="p-1 hover:bg-muted rounded transition-colors"
              >
                {leftNavCollapsed ? (
                  <ChevronRight className="w-4 h-4 text-[var(--color-text-primary)]" />
                ) : (
                  <ChevronDown className="w-4 h-4 text-[var(--color-text-primary)]" />
                )}
              </button>
            </div>
            
            <div className={`transition-all duration-200 overflow-hidden ${
              leftNavCollapsed ? "h-0" : "h-auto"
            }`}>
              <LeftNav
                activeTab={activeTab}
                onTabChange={setActiveTab}
                className="border-none bg-transparent"
              />
            </div>
          </div>

          {/* Folders Panel */}
          <div className="border-b border-border/50">
            <div className="flex items-center justify-between p-4">
              <h3 className="text-sm font-medium text-[var(--color-text-primary)] flex items-center gap-2">
                <Folder className="w-4 h-4" />
                Folders
              </h3>
              <button
                onClick={() => setFoldersPanelCollapsed(!foldersPanelCollapsed)}
                className="p-1 hover:bg-muted rounded transition-colors"
              >
                {foldersPanelCollapsed ? (
                  <ChevronRight className="w-4 h-4 text-[var(--color-text-primary)]" />
                ) : (
                  <ChevronDown className="w-4 h-4 text-[var(--color-text-primary)]" />
                )}
              </button>
            </div>
            
            <div className={`transition-all duration-200 overflow-hidden ${
              foldersPanelCollapsed ? "h-0" : "h-auto"
            }`}>
              <div className="px-4 pb-4 space-y-2">
                {foldersData.map((folder) => (
                  <div
                    key={folder.id}
                    className="flex items-center justify-between p-2 rounded hover:bg-[#2b2b2b] cursor-pointer group"
                  >
                    <div className="flex items-center gap-2">
                      <div 
                        className="w-2 h-2 rounded-full"
                        style={{ backgroundColor: folder.color }}
                      />
                      <span className="text-sm text-[var(--color-text-primary)] group-hover:text-white">
                        {folder.name}
                      </span>
                    </div>
                    <span className="text-xs px-2 py-1 rounded-full bg-[#2b2b2b] text-[#888]">
                      {folder.count}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Tags Panel */}
          <div className="border-b border-border/50">
            <div className="flex items-center justify-between p-4">
              <h3 className="text-sm font-medium text-[var(--color-text-primary)] flex items-center gap-2">
                <Hash className="w-4 h-4" />
                Tags
              </h3>
              <button
                onClick={() => setTagsPanelCollapsed(!tagsPanelCollapsed)}
                className="p-1 hover:bg-muted rounded transition-colors"
              >
                {tagsPanelCollapsed ? (
                  <ChevronRight className="w-4 h-4 text-[var(--color-text-primary)]" />
                ) : (
                  <ChevronDown className="w-4 h-4 text-[var(--color-text-primary)]" />
                )}
              </button>
            </div>
            
            <div className={`transition-all duration-200 overflow-hidden ${
              tagsPanelCollapsed ? "h-0" : "h-auto"
            }`}>
              <div className="px-4 pb-4 space-y-2">
                {tagsData.map((tag) => (
                  <div
                    key={tag.id}
                    className="flex items-center justify-between p-2 rounded hover:bg-[#2b2b2b] cursor-pointer group"
                  >
                    <div className="flex items-center gap-2">
                      <span className="text-sm text-[#888]">#</span>
                      <span className="text-sm text-[var(--color-text-primary)] group-hover:text-white">
                        {tag.name}
                      </span>
                    </div>
                    <span className="text-xs px-2 py-1 rounded-full bg-[#2b2b2b] text-[#888]">
                      {tag.count}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Notes Panel */}
          <div className="flex-1">
            <div className="flex items-center justify-between p-4 border-b border-border/50">
              <h3 className="text-sm font-medium text-[var(--color-text-primary)] flex items-center gap-2">
                <NotepadText className="w-4 h-4" />
                Notes
              </h3>
              <button
                onClick={() => setNotesPanelCollapsed(!notesPanelCollapsed)}
                className="p-1 hover:bg-muted rounded transition-colors"
              >
                {notesPanelCollapsed ? (
                  <ChevronRight className="w-4 h-4 text-[var(--color-text-primary)]" />
                ) : (
                  <ChevronDown className="w-4 h-4 text-[var(--color-text-primary)]" />
                )}
              </button>
            </div>
            
            <div className={`transition-all duration-200 overflow-hidden flex-1 ${
              notesPanelCollapsed ? "h-0" : "h-auto"
            }`}>
              <div className="px-4 pb-4 pt-4 space-y-2 overflow-auto">
                {notesData.map((note) => (
                  <div
                    key={note.id}
                    className="p-2 rounded hover:bg-[#2b2b2b] cursor-pointer group"
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm text-[var(--color-text-primary)] group-hover:text-white truncate">
                        {note.title}
                      </span>
                      {note.isSourced && (
                        <span className="text-xs px-1.5 py-0.5 rounded bg-blue-600 text-white ml-2">
                          {note.sourceType}
                        </span>
                      )}
                    </div>
                    <div className="flex items-center gap-1 mb-2">
                      {note.tags.slice(0, 2).map((tag, index) => (
                        <span key={index} className="text-xs px-1.5 py-0.5 rounded bg-[#2b2b2b] text-[#888]">
                          #{tag}
                        </span>
                      ))}
                      {note.tags.length > 2 && (
                        <span className="text-xs px-1.5 py-0.5 rounded bg-[#2b2b2b] text-[#888]">
                          +{note.tags.length - 2}
                        </span>
                      )}
                    </div>
                    <p className="text-xs text-[#888] line-clamp-2">
                      {note.content.substring(0, 80)}...
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>
          </Panel>

          {/* Resize Handle */}
          <PanelResizeHandle className="w-2 resize-handle cursor-col-resize" />

          {/* Central Content Area */}
          <Panel defaultSize={50} minSize={30} className="bg-[var(--color-main-panel)]">
            <ScrollArea className="h-full">
              {renderActiveSection()}
            </ScrollArea>
          </Panel>

          {/* Resize Handle */}
          <PanelResizeHandle className="w-2 resize-handle cursor-col-resize" />

          {/* Right Panel - AI Chat or Related Items */}
          <Panel defaultSize={25} minSize={20} maxSize={50} className="border-l border-border bg-[var(--color-right-panel)]">
            <div className="h-full flex flex-col">
              {/* Panel Header with Toggle */}
              <div className="flex items-center justify-between p-3 border-b border-border bg-[var(--color-right-panel)]">
                <h3 className="text-sm font-medium text-[var(--color-text-primary)]">
                  {useAIChat ? "AI Assistant" : "Related Items"}
                </h3>
                <Button 
                  variant="ghost" 
                  size="sm"
                  onClick={() => setUseAIChat(!useAIChat)}
                  className="text-xs h-7 px-2 text-[var(--color-text-primary)] hover:bg-[var(--color-main-panel)]"
                >
                  {useAIChat ? "Show Items" : "Show AI"}
                </Button>
              </div>
              
              {/* Panel Content */}
              <div className="flex-1 overflow-hidden">
                {useAIChat ? (
                  <AIChatPanel 
                    onContextChange={(context) => {
                      console.log('AI Chat context changed:', context);
                    }}
                  />
                ) : (
                  <ScrollArea className="h-full">
                    <div className="p-4">
                      <RightContextPanel contextData={generateContextData()} />
                    </div>
                  </ScrollArea>
                )}
              </div>
            </div>
          </Panel>
        </PanelGroup>
      </div>

      {/* Admin Dialog */}
      <Dialog open={showAdminDialog} onOpenChange={setShowAdminDialog}>
        <DialogContent className="max-w-6xl max-h-[90vh] overflow-hidden">
          <DialogHeader>
            <DialogTitle>Admin Settings</DialogTitle>
            <DialogDescription>
              System administration and configuration
            </DialogDescription>
          </DialogHeader>
          <div className="flex-1 overflow-auto">
            <AdminSection />
          </div>
        </DialogContent>
      </Dialog>

      {/* Toast Notifications */}
      <Toaster 
        position="top-right"
        expand={false}
        theme={theme}
        closeButton
      />
    </div>
  );
}

export default function Page() {
  return (
    <ThemeProvider>
      <PageContent />
    </ThemeProvider>
  );
}