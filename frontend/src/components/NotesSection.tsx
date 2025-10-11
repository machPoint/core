"use client";

import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { ScrollArea } from "@/components/ui/scroll-area";
import { 
  Save, 
  Plus, 
  Search, 
  FileText, 
  Clock, 
  Tag,
  Folder,
  Link2,
  Star,
  MoreHorizontal,
  Edit,
  Trash2,
  ExternalLink
} from "lucide-react";
import { toast } from "sonner";
import { cn } from "@/lib/utils";
import { Dialog, DialogContent, DialogHeader, DialogFooter, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { formatDistanceToNow } from "date-fns";

interface Note {
  id: string;
  title: string;
  content: string;
  tags: string[];
  folder: string;
  lastSynced: Date;
  isSourced: boolean;
  sourceType?: string;
}

const mockNotes: Note[] = [
  {
    id: "1",
    title: "System Architecture Overview",
    content: "# System Architecture\n\nThis document outlines the high-level architecture for our distributed system...\n\n## Components\n- API Gateway\n- Microservices\n- Database Layer\n- Caching Layer\n\n## Design Principles\n- Scalability\n- Reliability\n- Security",
    tags: ["engineering", "architecture"],
    folder: "Architecture",
    lastSynced: new Date(),
    isSourced: false
  },
  {
    id: "2", 
    title: "API Requirements Document",
    content: "# API Requirements\n\nRequirements imported from Jira ticket @REQ-456\n\n## Functional Requirements\n- User authentication\n- Data validation\n- Rate limiting\n\n## Non-functional Requirements\n- 99.9% uptime\n- < 200ms response time\n- Handle 10k concurrent users",
    tags: ["requirements"],
    folder: "Requirements",
    lastSynced: new Date(),
    isSourced: true,
    sourceType: "jira"
  }
];

export default function NotesSection() {
  const [notes, setNotes] = useState(mockNotes);
  const [selectedNote, setSelectedNote] = useState<Note | null>(notes[0]);
  const [searchQuery, setSearchQuery] = useState("");
  const [content, setContent] = useState(selectedNote?.content || "");
  const [title, setTitle] = useState(selectedNote?.title || "");
  const [isEditing, setIsEditing] = useState(false);
  const [autoSaveEnabled, setAutoSaveEnabled] = useState(true);
  const editorRef = useRef<HTMLTextAreaElement>(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newNoteTitle, setNewNoteTitle] = useState("");
  const [newNoteFolder, setNewNoteFolder] = useState("");

  useEffect(() => {
    if (selectedNote) {
      setContent(selectedNote.content);
      setTitle(selectedNote.title);
    }
  }, [selectedNote]);

  const handleSave = () => {
    if (!selectedNote || selectedNote.isSourced) {
      toast.error("Cannot edit sourced notes");
      return;
    }

    const updatedNote = {
      ...selectedNote,
      title,
      content,
      lastSynced: new Date()
    };

    setNotes(prev => prev.map(note => 
      note.id === selectedNote.id ? updatedNote : note
    ));
    setSelectedNote(updatedNote);
    
    toast.success("Note saved successfully");
    setIsEditing(false);
  };

  const handleCreateNote = () => {
    const newNote: Note = {
      id: Date.now().toString(),
      title: "Untitled Note",
      content: "",
      tags: [],
      folder: "General",
      lastSynced: new Date(),
      isSourced: false
    };

    setNotes(prev => [newNote, ...prev]);
    setSelectedNote(newNote);
    setTitle("Untitled Note");
    setContent("");
    setIsEditing(true);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Tab') {
      e.preventDefault();
      const textarea = e.target as HTMLTextAreaElement;
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const newValue = content.substring(0, start) + '  ' + content.substring(end);
      setContent(newValue);
      
      setTimeout(() => {
        textarea.selectionStart = textarea.selectionEnd = start + 2;
      }, 0);
    }
  };

  const filteredNotes = notes.filter(note =>
    note.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    note.content.toLowerCase().includes(searchQuery.toLowerCase()) ||
    note.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  return (
    <div className="flex h-full bg-[var(--color-main-panel)]">
      {/* Note List */}
      <div className="w-80 border-r border-border bg-[var(--color-left-panel)] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-border bg-[var(--color-left-panel)]">
          <h2 className="text-lg font-semibold text-[var(--color-text-primary)]">Notes</h2>
          <div className="flex items-center gap-2">
            <Button
              size="sm"
              onClick={() => setShowCreateModal(true)}
              className="h-8 px-3 text-xs bg-primary hover:bg-primary/90"
            >
              <Plus className="w-3 h-3 mr-1" />
              New
            </Button>
          </div>
        </div>

        {/* Search */}
        <div className="p-4 border-b border-border">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <Input
              type="text"
              placeholder="Search notes..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 h-9 bg-card border-border"
            />
          </div>
        </div>

        {/* Notes List */}
        <div className="flex-1 overflow-auto">
          {filteredNotes.map((note) => (
            <div
              key={note.id}
              onClick={() => setSelectedNote(note)}
              className={cn(
                "p-4 border-b border-border cursor-pointer hover:bg-card transition-colors",
                selectedNote?.id === note.id && "bg-card"
              )}
            >
              <div className="flex items-center justify-between mb-1">
                <h4 className="font-medium text-sm truncate pr-2">{note.title}</h4>
                {note.isSourced && (
                  <Badge variant="outline" className="text-xs">
                    <Link2 className="w-3 h-3 mr-1" />
                    {note.sourceType}
                  </Badge>
                )}
              </div>
              
              <p className="text-xs text-muted-foreground line-clamp-2 mb-2">
                {note.content.substring(0, 100)}...
              </p>
              
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-1">
                  <Folder className="w-3 h-3 text-muted-foreground" />
                  <span className="text-xs text-muted-foreground">{note.folder}</span>
                </div>
                <div className="flex items-center gap-1">
                  <Clock className="w-3 h-3 text-muted-foreground" />
                  <span className="text-xs text-muted-foreground">
                    {note.lastSynced.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </span>
                </div>
              </div>
              
              {note.tags.length > 0 && (
                <div className="flex flex-wrap gap-1 mt-2">
                  {note.tags.slice(0, 3).map((tag) => (
                    <Badge key={tag} variant="secondary" className="text-xs">
                      #{tag}
                    </Badge>
                  ))}
                  {note.tags.length > 3 && (
                    <Badge variant="secondary" className="text-xs">
                      +{note.tags.length - 3}
                    </Badge>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Note Editor */}
      <div className="flex-1 flex flex-col">
        {selectedNote ? (
          <>
            {/* Note Header */}
            <div className="flex items-center justify-between p-4 border-b border-border bg-[var(--color-main-panel)]">
              <div className="flex-1">
                <Input
                  value={selectedNote.title}
                  onChange={(e) => {
                    const updatedNote = { ...selectedNote, title: e.target.value };
                    setSelectedNote(updatedNote);
                    setNotes(notes.map(n => n.id === updatedNote.id ? updatedNote : n));
                  }}
                  className="text-lg font-semibold border-none shadow-none p-0 h-auto bg-transparent focus-visible:ring-0"
                />
              </div>
              
              <div className="flex items-center gap-2 ml-4">
                {selectedNote.isSourced && (
                  <span className="text-xs px-2 py-1 rounded bg-blue-600 text-white">
                    {selectedNote.sourceType}
                  </span>
                )}
                <span className="text-xs text-muted-foreground">
                  Last synced: {formatDistanceToNow(selectedNote.lastSynced, { addSuffix: true })}
                </span>
                <Button
                  size="sm"
                  variant="ghost"
                  onClick={() => {
                    setNotes(notes.filter(n => n.id !== selectedNote.id));
                    setSelectedNote(null);
                  }}
                  className="h-8 w-8 p-0 text-muted-foreground hover:text-destructive"
                >
                  <Trash2 className="w-4 h-4" />
                </Button>
              </div>
            </div>

            {/* Note Content */}
            <div className="flex-1 p-4">
              {selectedNote.isSourced ? (
                <div className="h-full bg-card rounded border border-border p-4">
                  <div className="flex items-center gap-2 mb-4">
                    <ExternalLink className="w-4 h-4 text-muted-foreground" />
                    <span className="text-sm text-muted-foreground">Read-only content from {selectedNote.sourceType}</span>
                  </div>
                  <div className="prose prose-sm dark:prose-invert max-w-none">
                    <pre className="whitespace-pre-wrap text-sm">{selectedNote.content}</pre>
                  </div>
                </div>
              ) : (
                <Textarea
                  ref={editorRef}
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Start writing your note..."
                  className="min-h-[500px] border-none shadow-none resize-none focus-visible:ring-0 text-sm leading-relaxed bg-[var(--color-main-panel)]"
                />
              )}
            </div>
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center text-muted-foreground">
            <div className="text-center">
              <FileText className="w-12 h-12 mx-auto mb-4 opacity-20" />
              <p>Select a note to start editing</p>
            </div>
          </div>
        )}
      </div>

      {/* Create Note Modal */}
      <Dialog open={showCreateModal} onOpenChange={setShowCreateModal}>
        <DialogContent className="bg-card">
          <DialogHeader>
            <DialogTitle>Create New Note</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium text-foreground">Title</label>
              <Input
                value={newNoteTitle}
                onChange={(e) => setNewNoteTitle(e.target.value)}
                placeholder="Enter note title..."
                className="mt-1 bg-background border-border"
              />
            </div>
            <div>
              <label className="text-sm font-medium text-foreground">Folder</label>
              <select
                value={newNoteFolder}
                onChange={(e) => setNewNoteFolder(e.target.value)}
                className="w-full mt-1 p-2 rounded border border-border bg-background text-foreground"
              >
                <option value="">Select a folder...</option>
                <option value="Architecture">Architecture</option>
                <option value="Requirements">Requirements</option>
                <option value="Meeting Notes">Meeting Notes</option>
                <option value="Ideas">Ideas</option>
              </select>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowCreateModal(false)}>
              Cancel
            </Button>
            <Button onClick={handleCreateNote}>
              Create Note
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}