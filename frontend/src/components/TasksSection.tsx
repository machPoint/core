"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { 
  Search, 
  Filter,
  Plus,
  Calendar,
  User,
  Clock,
  CheckCircle2,
  Circle,
  AlertCircle,
  Flag,
  MoreHorizontal,
  ArrowUpDown
} from "lucide-react";
import { cn } from "@/lib/utils";
import { toast } from "sonner";

interface Task {
  id: string;
  title: string;
  description: string;
  status: "todo" | "in-progress" | "completed";
  priority: "low" | "medium" | "high";
  assignee: string;
  dueDate: string;
  tags: string[];
  project: string;
}

const mockTasks: Task[] = [
  {
    id: "1",
    title: "Implement user authentication",
    description: "Add OAuth2 login flow and session management",
    status: "in-progress",
    priority: "high",
    assignee: "Sarah Chen",
    dueDate: "2024-02-15",
    tags: ["backend", "security"],
    project: "Core Platform"
  },
  {
    id: "2",
    title: "Design dashboard wireframes",
    description: "Create initial wireframes for the main dashboard",
    status: "completed",
    priority: "medium",
    assignee: "Mike Rodriguez",
    dueDate: "2024-02-10",
    tags: ["design", "ui"],
    project: "Frontend"
  },
  {
    id: "3",
    title: "Write API documentation",
    description: "Document all endpoints and authentication requirements",
    status: "todo",
    priority: "medium",
    assignee: "Alex Kim",
    dueDate: "2024-02-20",
    tags: ["documentation", "api"],
    project: "Core Platform"
  }
];

export default function TasksSection() {
  const [tasks, setTasks] = useState(mockTasks);
  const [searchQuery, setSearchQuery] = useState("");
  const [filterStatus, setFilterStatus] = useState<"all" | "todo" | "in-progress" | "completed">("all");
  const [filterPriority, setFilterPriority] = useState<"all" | "low" | "medium" | "high">("all");
  const [sortBy, setSortBy] = useState<"dueDate" | "priority" | "status">("dueDate");

  const filteredTasks = tasks.filter(task => {
    const matchesSearch = task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         task.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         task.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()));
    const matchesStatus = filterStatus === "all" || task.status === filterStatus;
    const matchesPriority = filterPriority === "all" || task.priority === filterPriority;
    return matchesSearch && matchesStatus && matchesPriority;
  });

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "completed": return CheckCircle2;
      case "in-progress": return Clock;
      case "todo": return Circle;
      default: return Circle;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "completed": return "text-[#6e9fc1] dark:text-[#a3cae9]";
      case "in-progress": return "text-[#395a7f] dark:text-[#6e9fc1]";
      case "todo": return "text-muted-foreground";
      default: return "text-muted-foreground";
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case "high": return "bg-[#acacac]/20 text-[#acacac] dark:bg-[#acacac]/10 dark:text-[#e9ecee]";
      case "medium": return "bg-[#6e9fc1]/20 text-[#395a7f] dark:bg-[#395a7f]/20 dark:text-[#6e9fc1]";
      case "low": return "bg-[#a3cae9]/30 text-[#395a7f] dark:bg-[#395a7f]/15 dark:text-[#a3cae9]";
      default: return "bg-card text-card-foreground";
    }
  };

  const toggleTaskStatus = (taskId: string) => {
    setTasks(prev => prev.map(task => {
      if (task.id === taskId) {
        const statusOrder: Task["status"][] = ["todo", "in-progress", "completed"];
        const currentIndex = statusOrder.indexOf(task.status);
        const nextIndex = (currentIndex + 1) % statusOrder.length;
        return { ...task, status: statusOrder[nextIndex] };
      }
      return task;
    }));
  };

  return (
    <div className="flex h-full bg-background">
      {/* Sidebar */}
      <div className="w-80 border-r border-border bg-card flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-border">
          <h2 className="text-lg font-semibold">Tasks</h2>
          <Button size="sm" className="h-8">
            <Plus className="w-4 h-4 mr-1" />
            New Task
          </Button>
        </div>

        {/* Search */}
        <div className="p-4 border-b border-border">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <Input
              type="text"
              placeholder="Search tasks..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 h-9 bg-background border-border"
            />
          </div>
        </div>

        {/* Filters */}
        <div className="p-4 border-b border-border space-y-4">
          <div>
            <h4 className="text-sm font-medium mb-2">Status</h4>
            <div className="space-y-2">
              {[
                { value: "all", label: "All Tasks" },
                { value: "todo", label: "To Do" },
                { value: "in-progress", label: "In Progress" },
                { value: "completed", label: "Completed" }
              ].map((option) => (
                <label key={option.value} className="flex items-center gap-2 text-sm cursor-pointer">
                  <input
                    type="radio"
                    name="status"
                    value={option.value}
                    checked={filterStatus === option.value}
                    onChange={(e) => setFilterStatus(e.target.value as any)}
                    className="border-border"
                  />
                  <span>{option.label}</span>
                </label>
              ))}
            </div>
          </div>

          <div>
            <h4 className="text-sm font-medium mb-2">Priority</h4>
            <div className="space-y-2">
              {[
                { value: "all", label: "All Priorities" },
                { value: "high", label: "High" },
                { value: "medium", label: "Medium" },
                { value: "low", label: "Low" }
              ].map((option) => (
                <label key={option.value} className="flex items-center gap-2 text-sm cursor-pointer">
                  <input
                    type="radio"
                    name="priority"
                    value={option.value}
                    checked={filterPriority === option.value}
                    onChange={(e) => setFilterPriority(e.target.value as any)}
                    className="border-border"
                  />
                  <span>{option.label}</span>
                </label>
              ))}
            </div>
          </div>
        </div>

        {/* Stats */}
        <div className="p-4">
          <h4 className="text-sm font-medium mb-2">Overview</h4>
          <div className="space-y-2">
            <div className="flex items-center justify-between text-sm">
              <span>Total Tasks</span>
              <Badge variant="secondary">{tasks.length}</Badge>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span>In Progress</span>
              <Badge variant="secondary">{tasks.filter(t => t.status === "in-progress").length}</Badge>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span>Completed</span>
              <Badge variant="secondary">{tasks.filter(t => t.status === "completed").length}</Badge>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-border bg-card">
          <div className="flex items-center gap-4">
            <h3 className="font-medium">
              {filterStatus === "all" ? "All Tasks" : 
               filterStatus === "todo" ? "To Do" :
               filterStatus === "in-progress" ? "In Progress" : "Completed"}
            </h3>
            <Badge variant="secondary">{filteredTasks.length}</Badge>
          </div>
          
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm">
              <ArrowUpDown className="w-4 h-4 mr-1" />
              Sort
            </Button>
            <Button variant="outline" size="sm">
              <Filter className="w-4 h-4 mr-1" />
              Filter
            </Button>
          </div>
        </div>

        {/* Tasks List */}
        <ScrollArea className="flex-1">
          <div className="p-4 space-y-3">
            {filteredTasks.map((task) => {
              const StatusIcon = getStatusIcon(task.status);
              
              return (
                <div key={task.id} className="bg-card rounded-lg border border-border p-4 hover:bg-muted/50 transition-colors">
                  <div className="flex items-start gap-3">
                    <button
                      onClick={() => toggleTaskStatus(task.id)}
                      className={cn("flex-shrink-0 mt-1", getStatusColor(task.status))}
                    >
                      <StatusIcon className="w-5 h-5" />
                    </button>
                    
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between mb-1">
                        <h4 className={cn(
                          "font-medium text-sm truncate pr-2",
                          task.status === "completed" && "line-through text-muted-foreground"
                        )}>
                          {task.title}
                        </h4>
                        <Badge className={cn("text-xs ml-2", getPriorityColor(task.priority))}>
                          {task.priority}
                        </Badge>
                      </div>
                      
                      <p className="text-sm text-muted-foreground mb-3 line-clamp-2">
                        {task.description}
                      </p>
                      
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <div className="flex items-center gap-1">
                            <User className="w-3 h-3 text-muted-foreground" />
                            <span className="text-xs text-muted-foreground">{task.assignee}</span>
                          </div>
                          <div className="flex items-center gap-1">
                            <Calendar className="w-3 h-3 text-muted-foreground" />
                            <span className="text-xs text-muted-foreground">{task.dueDate}</span>
                          </div>
                        </div>
                        
                        <div className="flex items-center gap-2">
                          <div className="flex gap-1">
                            {task.tags.slice(0, 2).map((tag) => (
                              <Badge key={tag} variant="outline" className="text-xs">
                                {tag}
                              </Badge>
                            ))}
                            {task.tags.length > 2 && (
                              <Badge variant="outline" className="text-xs">
                                +{task.tags.length - 2}
                              </Badge>
                            )}
                          </div>
                          
                          <Button variant="ghost" size="sm" className="h-6 w-6 p-0">
                            <MoreHorizontal className="w-3 h-3" />
                          </Button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}

            {filteredTasks.length === 0 && (
              <div className="flex flex-col items-center justify-center py-12 text-center">
                <div className="text-4xl mb-4">✅</div>
                <h3 className="text-lg font-medium mb-2">No tasks found</h3>
                <p className="text-muted-foreground text-sm">
                  {searchQuery || filterStatus !== "all" || filterPriority !== "all"
                    ? "Try adjusting your search or filters"
                    : "Create your first task to get started"
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