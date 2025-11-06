"use client";

import { 
  FileText, 
  Activity, 
  FileCheck, 
  Palette, 
  Shield, 
  Network, 
  TrendingUp, 
  Brain, 
  CheckSquare, 
  Bot, 
  Settings, 
  TestTube,
  Database,
  Monitor,
  GitBranch
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface LeftNavProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
  className?: string;
}

const navItems = [
  { id: "pulse", label: "Flow", icon: Activity },
  { id: "tasks", label: "Tasks", icon: CheckSquare },
  { id: "notes", label: "Notes", icon: FileText },
  { id: "requirements", label: "Requirements", icon: FileCheck },
  { id: "trace", label: "Trace Graph", icon: Network },
  { id: "impact", label: "Impact Analysis", icon: TrendingUp },
  { id: "relationships", label: "Relationships", icon: GitBranch },
  { id: "verification", label: "Verification", icon: Shield },
  { id: "design", label: "Interfaces", icon: Palette },
  { id: "test", label: "Test", icon: TestTube },
  { id: "data-engine", label: "Data Engine", icon: Database },
  { id: "knowledge", label: "Library", icon: Brain },
  { id: "agents", label: "Agents", icon: Bot },
  { id: "system-admin", label: "System Admin", icon: Monitor },
];

export default function LeftNav({ activeTab, onTabChange, className }: LeftNavProps) {
  return (
    <nav className={cn(
      "border-r border-border bg-[#1c1c1c] dark:bg-[#1c1c1c] p-4 flex flex-col gap-2",
      className
    )}>
      <div className="space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          
          return (
            <Button
              key={item.id}
              variant={isActive ? "default" : "ghost"}
              className={cn(
                "w-full justify-start gap-3 h-10 px-3 text-sm font-medium",
                isActive 
                  ? "bg-primary text-primary-foreground" 
                  : "text-[#dbdbdb] dark:text-[#dbdbdb] hover:bg-[#2b2b2b] dark:hover:bg-[#2b2b2b] hover:text-[#dbdbdb] dark:hover:text-[#dbdbdb]"
              )}
              onClick={() => onTabChange(item.id)}
            >
              <Icon className="h-4 w-4 flex-shrink-0" />
              <span className="truncate">{item.label}</span>
            </Button>
          );
        })}
      </div>
    </nav>
  );
}