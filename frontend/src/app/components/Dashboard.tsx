import { useState, useEffect } from "react";
import {
  FileText, Zap, Clock, Plus, Briefcase,
  X, BarChart2, TrendingUp, CheckCircle2, AlertCircle, Timer, Star,
  Search, Copy, Download, Trash2, ChevronRight,
  DollarSign, Users, Activity, ArrowUpRight, ArrowDownRight,
  Lightbulb,Sparkles
} 
from "lucide-react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./ui/select";
import { ThemeToggle } from "./ThemeToggle";
import { EmptyState } from "./shared/EmptyState";
import { InlineError } from "./shared/InlineError";
import { SectionCard } from "./shared/SectionCard";
import {
  AreaChart, Area, XAxis, YAxis, Tooltip,
  ResponsiveContainer, BarChart, Bar, LineChart, Line,
  PieChart, Pie, Cell, Legend,CartesianGrid
} from "recharts";
import type { SavedProposal, 
  ProposalStatus, 
  ProposalDetails, 
  DashboardStats,
  AnalyticsDashboardStats,
  TopClientsResponse,
  StatusDistributionItem,
  ProposalTrendItem,
  AIScoreTrendItem,
  AcceptanceTrendItem,
  RecentActivityItem,
  TopClient,
  ProductHealth,
  ProposalFunnel,
  FeatureUsage, } from "../../types";
import { 
  fetchProposalHistory,
  fetchProposalDetails, 
  fetchDashboardStats, 
  updateProposalStatus, 
  duplicateProposal, 
  deleteProposal,
  fetchAnalyticsDashboard,
  fetchTopClients,
  fetchStatusDistribution,
  fetchProposalTrend,
  fetchAIScoreTrend,
  fetchAcceptanceTrend,
  fetchRecentActivity,
  fetchProposalFunnel,
  fetchFeatureUsage,
  fetchProductHealth,} from "../../services/api";

// ─── Validation ───────────────────────────────────────────────────────────────

const MIN_LENGTH = 20;
const MAX_LENGTH = 5000;

function validateJobDescription(value: string): string {
  if (!value.trim()) return "Please paste a job description before continuing.";
  if (value.trim().length < MIN_LENGTH) return `Job description must be at least ${MIN_LENGTH} characters.`;
  if (value.length > MAX_LENGTH) return `Job description must be under ${MAX_LENGTH} characters.`;
  return "";
}


// ─── Style maps ───────────────────────────────────────────────────────────────

const statusColor: Record<ProposalStatus, string> = {
  Draft:
    "bg-amber-50 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300",

  Saved:
    "bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300",

  Sent:
    "bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300",

  Accepted:
    "bg-emerald-50 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300",

  Rejected:
    "bg-red-50 text-red-700 dark:bg-red-900/30 dark:text-red-300",
};

const outcomeColor: Record<ProposalStatus, string> = {
    Draft: "text-yellow-500",
    Saved: "text-indigo-500",
    Sent: "text-blue-500",
    Accepted: "text-emerald-600",
    Rejected: "text-red-500",
};

const categoryColor: Record<SavedProposal["category"], string> = {
  Backend:  "bg-violet-50 text-violet-700 dark:bg-violet-900/30 dark:text-violet-300",
  Frontend: "bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300",
  AI:       "bg-emerald-50 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300",
  Design:   "bg-pink-50 text-pink-700 dark:bg-pink-900/30 dark:text-pink-300",
  DevOps:   "bg-orange-50 text-orange-700 dark:bg-orange-900/30 dark:text-orange-300",
  Content:  "bg-amber-50 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300",
};

function scoreColors(score: number): { badge: string; bar: string; ring: string } {
  if (score >= 90) return {
    badge: "bg-emerald-50 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300",
    bar:   "bg-emerald-500",
    ring:  "text-emerald-600",
  };
  if (score >= 75) return {
    badge: "bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300",
    bar:   "bg-blue-500",
    ring:  "text-blue-600",
  };
  if (score >= 60) return {
    badge: "bg-amber-50 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300",
    bar:   "bg-amber-500",
    ring:  "text-amber-600",
  };
  return {
    badge: "bg-red-50 text-red-700 dark:bg-red-900/30 dark:text-red-300",
    bar:   "bg-red-500",
    ring:  "text-red-600",
  };
}

// Sparkline data aligned with monthlyData months
const kpiSparkData = {
  proposals:   [{ v: 2 }, { v: 3 }, { v: 4 }, { v: 3 }, { v: 5 }, { v: 4 }],
  acceptance:  [{ v: 50 }, { v: 67 }, { v: 75 }, { v: 67 }, { v: 80 }, { v: 75 }],
  aiScore:     [{ v: 76 }, { v: 79 }, { v: 82 }, { v: 80 }, { v: 85 }, { v: 87 }],
  revenue:     [{ v: 3.2 }, { v: 5.1 }, { v: 8.4 }, { v: 6.2 }, { v: 14.1 }, { v: 26.9 }],
};

// ─── Shared chart config ──────────────────────────────────────────────────────

const TOOLTIP_STYLE = {
  contentStyle: {
    background: "var(--card)",
    border: "1px solid var(--border)",
    borderRadius: 8,
    fontSize: 12,
    padding: "8px 12px",
    boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
  },
  labelStyle: { color: "var(--foreground)", fontWeight: 500, marginBottom: 2 },
  itemStyle: { color: "var(--muted-foreground)" },
  cursor: { stroke: "var(--border)", strokeWidth: 1 },
};

const AXIS_PROPS = {
  tick: { fontSize: 11, fill: "var(--muted-foreground)" },
  tickLine: false as const,
  axisLine: false as const,
};


// ─── Proposal Detail Modal ────────────────────────────────────────────────────

interface ProposalDetailModalProps {
  proposal: ProposalDetails;
  onClose: () => void;
  onStatusChange: (
        proposalId: number,
        status: ProposalStatus
    ) => void;

  onDuplicate: (proposalId: number) => void;

  onDelete: (proposalId: number) => void;
}

function ProposalDetailModal({ proposal, onClose, onStatusChange, onDuplicate, onDelete }: ProposalDetailModalProps) {
  const [tab, setTab] = useState<"job" | "generated" | "final" | "outcome" | "review">("job");
  const [duplicating, setDuplicating] = useState(false);
  const [deleting, setDeleting] =
    useState(false);

  // Lock body scroll while modal is open
  useEffect(() => {
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => { document.body.style.overflow = prev; };
  }, []);

  const tabs: { id: typeof tab; label: string }[] = [
    { id: "job",       label: "Job Description" },
    { id: "generated", label: "Generated" },
    { id: "final",     label: "Final Edited" },
    { id: "outcome",   label: "Outcome" },
    { id: "review",    label: "Review" },
  ];

  const overallScore = proposal.overall_score;
  const sc = scoreColors(overallScore);

  const reviewMetrics = [
  {
    label: "Professionalism",
    score: proposal.review.metrics.professionalism,
    note: "Tone and vocabulary are polished and client-appropriate.",
  },
  {
    label: "Personalization",
    score: proposal.review.metrics.personalization,
    note: "References several client-specific details from the brief.",
  },
  {
    label: "Clarity",
    score: proposal.review.metrics.clarity,
    note: "Proposal is easy to understand and well structured.",
  },
  {
    label: "Tone",
    score: proposal.review.metrics.tone,
    note: "Writing style aligns with the client's communication style.",
  },
];

  const handleCopy = () => {
    const text = proposal.proposal.introduction || proposal.proposal.introduction;
    navigator.clipboard.writeText(text).catch(() => {});
  };

  const handleDownload = () => {
    const text = proposal.proposal.introduction || proposal.proposal.introduction;
    const blob = new Blob([text], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${proposal.title.replace(/\s+/g, "-").toLowerCase()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm"
    >
      <div className="bg-card border border-border rounded-xl shadow-2xl w-full max-w-2xl flex flex-col overflow-hidden" style={{ maxHeight: "min(88vh, 720px)" }}>

        {/* Header */}
        <div className="flex items-start justify-between px-6 py-5 border-b border-border">
          <div className="flex items-start gap-3 min-w-0">
            <div className="min-w-0">
              <h2 id="modal-title" className="text-foreground font-semibold tracking-tight truncate">
                {proposal.title}
              </h2>
              <p className="text-sm text-muted-foreground mt-0.5">
                {proposal.client} · {new Date(proposal.created_at).toLocaleDateString()}
              </p>
            </div>
            {/* Compact score badge in header */}
            <span className={`flex-shrink-0 mt-0.5 text-xs px-2 py-0.5 rounded-full font-medium ${sc.badge}`}>
              {overallScore}/100
            </span>
          </div>
          <button
            onClick={onClose}
            aria-label="Close proposal details"
            className="ml-3 flex-shrink-0 text-muted-foreground hover:text-foreground transition-colors"
          >
            <X className="w-5 h-5" aria-hidden="true" />
          </button>
        </div>

        {/* Tabs */}
        <div role="tablist" className="flex px-6 border-b border-border">
          {tabs.map((t) => (
            <button
              key={t.id}
              role="tab"
              aria-selected={tab === t.id}
              onClick={() => setTab(t.id)}
              className={`px-3 py-2.5 text-xs font-medium whitespace-nowrap transition-colors border-b-2 -mb-px ${
                tab === t.id
                  ? "text-accent border-accent"
                  : "text-muted-foreground border-transparent hover:text-foreground"
              }`}
            >
              {t.label}
            </button>
          ))}
        </div>

        {/* Tab content */}
        <div role="tabpanel" className="flex-1 min-h-0 overflow-y-auto no-scrollbar px-6 py-5">

          {tab === "job" && (
            <div>
              <p className="text-xs text-muted-foreground uppercase tracking-widest mb-3">Original Job Description</p>
              <p className="text-sm text-foreground leading-relaxed">{proposal.job_description}</p>
            </div>
          )}

          {tab === "generated" && (
    <div className="space-y-6">

        <SectionCard>
          <h4 className="font-semibold mb-2">Introduction</h4>
          <p>{proposal.proposal.introduction}</p>
        </SectionCard>

        <SectionCard>
          <h4 className="font-semibold mb-2">Relevant Experience</h4>
          <p>{proposal.proposal.relevantExperience}</p>
        </SectionCard>

        <SectionCard>
          <h4 className="font-semibold mb-2">Approach</h4>
          <p>{proposal.proposal.approach}</p>
        </SectionCard>

        <SectionCard>
          <h4 className="font-semibold mb-2">Timeline</h4>
          <p>{proposal.proposal.timeline}</p>
        </SectionCard>

            <SectionCard>
          <h4 className="font-semibold mb-2">Pricing</h4>
          <p>{proposal.proposal.pricing}</p>
        </SectionCard>

    </div>
)}

          {tab === "final" && (
    <div className="space-y-6">

        <SectionCard>
          <h4 className="font-semibold mb-2">Introduction</h4>
          <p>{proposal.final_proposal?.introduction}</p>
        </SectionCard>

        <SectionCard>
          <h4 className="font-semibold mb-2">Relevant Experience</h4>
          <p>{proposal.final_proposal?.relevantExperience}</p>
        </SectionCard>

        <SectionCard>
          <h4 className="font-semibold mb-2">Approach</h4>
          <p>{proposal.final_proposal?.approach}</p>
        </SectionCard>

        <SectionCard>
          <h4 className="font-semibold mb-2">Timeline</h4>
          <p>{proposal.final_proposal?.timeline}</p>
        </SectionCard>

            <SectionCard>
          <h4 className="font-semibold mb-2">Pricing</h4>
          <p>{proposal.final_proposal?.pricing}</p>
        </SectionCard>

    </div>
)}

          {tab === "outcome" && (
            <div className="space-y-4">
              <p className="text-xs text-muted-foreground uppercase tracking-widest mb-3">Outcome</p>
              <div className="flex items-center gap-3 p-4 bg-secondary rounded-lg">
                {proposal.status === "Accepted" && <CheckCircle2 className="w-5 h-5 text-emerald-500" aria-hidden="true" />}
                {proposal.status === "Rejected" && <AlertCircle className="w-5 h-5 text-red-500" aria-hidden="true" />}
                {(proposal.status === "Sent" ) && <Timer className="w-5 h-5 text-amber-500" aria-hidden="true" />}
                <div>
                  <p className={`font-medium ${outcomeColor[proposal.status]}`}>
                    {proposal.status}
                  </p>
                  <p className="text-xs text-muted-foreground mt-0.5">
                    {proposal.status === "Accepted"
                        ? "Client accepted this proposal."
                        : proposal.status === "Rejected"
                            ? "Client rejected this proposal."
                            : proposal.status === "Sent"
                                ? "Awaiting client response."
                                : proposal.status === "Saved"
                                    ? "Proposal saved but not yet sent."
                                    : "Draft proposal."}
                  </p>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="p-4 bg-secondary rounded-lg">
                  <p className="text-xs text-muted-foreground mb-1">Proposed Budget</p>
                  <p className="font-semibold text-foreground">{proposal.pricing}</p>
                </div>
                <div className="p-4 bg-secondary rounded-lg">
                  <p className="text-xs text-muted-foreground mb-1">Status</p>
                  <Select
                      value={proposal.status}
                      onValueChange={(value) =>
                          onStatusChange(
                              proposal.id,
                              value as ProposalStatus
                          )
                      }
                  >
                      <SelectTrigger
                          className={`h-8 w-[120px] rounded-full border-0 text-xs font-medium ${statusColor[proposal.status]}`}
                      >
                          <SelectValue />
                      </SelectTrigger>

                      <SelectContent>
                          <SelectItem value="Draft">Draft</SelectItem>
                          <SelectItem value="Saved">Saved</SelectItem>
                          <SelectItem value="Sent">Sent</SelectItem>
                          <SelectItem value="Accepted">Accepted</SelectItem>
                          <SelectItem value="Rejected">Rejected</SelectItem>
                      </SelectContent>
                  </Select>
                </div>
              </div>
            </div>
          )}

          {/* ── Review tab ── */}
          {/* TODO: Replace placeholder AI review with backend response from POST /proposal/review */}
          {tab === "review" && (
            <div className="space-y-6">

              {/* Overall score */}
              <div className="flex items-center gap-4 p-4 bg-secondary rounded-xl">
                <div className={`w-16 h-16 rounded-full border-4 flex items-center justify-center flex-shrink-0 ${
                  overallScore >= 90 ? "border-emerald-400" :
                  overallScore >= 75 ? "border-blue-400" :
                  overallScore >= 60 ? "border-amber-400" : "border-red-400"
                }`}>
                  <span className={`text-xl font-bold ${sc.ring}`}>{overallScore}</span>
                </div>
                <div>
                  <p className="text-xs text-muted-foreground uppercase tracking-widest mb-1">Overall AI Score</p>
                  <p className="text-foreground font-semibold">
                  {proposal.review.verdict}
                </p>
                  <p className="text-xs text-muted-foreground mt-0.5">
                    AI evaluation based on professionalism, personalization, clarity, and tone.
                  </p>
                </div>
              </div>

              {/* Metric bars */}
              <div>
                <p className="text-xs text-muted-foreground uppercase tracking-widest mb-3">Quality Metrics</p>
                <div className="space-y-3">
                  {reviewMetrics.map((m) => {
                    const msc = scoreColors(m.score);
                    return (
                      <div key={m.label}>
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-xs font-medium text-foreground">{m.label}</span>
                          <span className={`text-xs font-semibold ${msc.ring}`}>{m.score}</span>
                        </div>
                        <div className="h-1.5 bg-secondary rounded-full overflow-hidden">
                          <div
                            className={`h-full rounded-full transition-all ${msc.bar}`}
                            style={{ width: `${m.score}%` }}
                            role="progressbar"
                            aria-valuenow={m.score}
                            aria-valuemin={0}
                            aria-valuemax={100}
                            aria-label={m.label}
                          />
                        </div>
                        <p className="text-[11px] text-muted-foreground mt-1">{m.note}</p>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Strengths */}
              <div>
                <p className="text-xs text-muted-foreground uppercase tracking-widest mb-3">Strengths</p>
                <ul className="space-y-2">
                  {proposal.review.strengths.map((s, i) => (
                    <li key={i} className="flex items-start gap-2.5 p-3 bg-emerald-50 dark:bg-emerald-900/15 rounded-lg">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 mt-0.5 flex-shrink-0" aria-hidden="true" />
                      <span className="text-xs text-foreground leading-relaxed">{s}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Suggestions */}
              <div>
                <p className="text-xs text-muted-foreground uppercase tracking-widest mb-3">Suggestions</p>
                <ul className="space-y-2">
                  {proposal.review.improvements.map((s, i) => (
                    <li key={i} className="flex items-start gap-2.5 p-3 bg-amber-50 dark:bg-amber-900/15 rounded-lg">
                      <Lightbulb className="w-3.5 h-3.5 text-amber-600 mt-0.5 flex-shrink-0" aria-hidden="true" />
                      <span className="text-xs text-foreground leading-relaxed">{s}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>

        {/* Footer actions */}
        <div className="flex items-center justify-between gap-2 px-6 py-4 border-t border-border bg-secondary/30 rounded-b-xl">
          <div className="flex items-center gap-1.5">
            <button
              onClick={handleCopy}
              aria-label="Copy proposal text"
              className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-muted-foreground hover:text-foreground bg-card border border-border rounded-md hover:bg-secondary transition-colors"
            >
              <Copy className="w-3.5 h-3.5" aria-hidden="true" />
              Copy
            </button>
            <button
              onClick={handleDownload}
              aria-label="Download proposal as text file"
              className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-muted-foreground hover:text-foreground bg-card border border-border rounded-md hover:bg-secondary transition-colors"
            >
              <Download className="w-3.5 h-3.5" aria-hidden="true" />
              Download
            </button>
            <button
              aria-label="Duplicate proposal"
              onClick={async () => {
                      try {
                        setDuplicating(true);
                        await onDuplicate(proposal.id as number);
                      } finally {
                        setDuplicating(false);
                      }
              }}
              className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-muted-foreground hover:text-foreground bg-card border border-border rounded-md hover:bg-secondary transition-colors"
            >
              <Plus className="w-3.5 h-3.5" aria-hidden="true" />
              {
                  duplicating
                      ? "Duplicating..."
                      : "Duplicate"
              }
            </button>
            <button
              aria-label="Delete proposal"
              onClick={async () => {
                setDeleting(true);
                try{
                  await onDelete(proposal.id);
                } finally {
                  setDeleting(false);
                }
              }}
              className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-red-500 hover:text-red-600 bg-card border border-border rounded-md hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
            >
              <Trash2 className="w-3.5 h-3.5" aria-hidden="true" />
              {
    deleting
        ? "Deleting..."
        : "Delete"
}
            </button>
          </div>
          <button
            onClick={onClose}
            aria-label="Close modal"
            className="flex items-center gap-1.5 px-4 py-1.5 text-xs font-medium bg-primary text-primary-foreground rounded-md hover:opacity-90 transition-opacity"
          >
            Close
          </button>
        </div>

      </div>
    </div>
  );
}

// ─── Proposals Tab ────────────────────────────────────────────────────────────

type FilterChip = "All" | ProposalStatus | "Rejected";

const FILTER_CHIPS: FilterChip[] = ["All", "Draft", "Sent", "Accepted", "Rejected"];

interface ProposalsTabProps {
    proposals: SavedProposal[];
    onOpen: (proposal: SavedProposal) => void;
}

function ProposalsTab({ proposals, onOpen }: ProposalsTabProps) {
  const [search, setSearch] = useState("");
  const [chip, setChip] = useState<FilterChip>("All");

  const filtered = proposals.filter((p) => {
    const matchesSearch =
      p.title.toLowerCase().includes(search.toLowerCase()) ||
      p.client.toLowerCase().includes(search.toLowerCase());
    const matchesChip =
      chip === "All"      ? true
      : chip === "Rejected" ? p.status === "Rejected"
      : p.status === chip;
    return matchesSearch && matchesChip;
  });

  return (
    <section aria-label="Previous proposals" role="tabpanel" className="space-y-4">
      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground pointer-events-none" aria-hidden="true" />
        <input
          type="search"
          placeholder="Search by title or client…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          aria-label="Search proposals"
          className="w-full pl-9 pr-4 py-2.5 text-sm bg-card border border-border rounded-lg text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-accent/40 focus:border-accent transition-colors"
        />
      </div>

      {/* Filter chips */}
      <div className="flex flex-wrap gap-1.5" role="group" aria-label="Filter proposals by status">
        {FILTER_CHIPS.map((f) => (
          <button
            key={f}
            onClick={() => setChip(f)}
            aria-pressed={chip === f}
            className={`px-3 py-1 text-xs font-medium rounded-full border transition-colors ${
              chip === f
                ? "bg-accent text-accent-foreground border-accent"
                : "bg-card text-muted-foreground border-border hover:border-accent/40 hover:text-foreground"
            }`}
          >
            {f}
          </button>
        ))}
      </div>

      {/* List */}
      {filtered.length === 0 ? (
        <EmptyState
          icon={<FileText className="w-6 h-6" />}
          title={search || chip !== "All" ? "No proposals match" : "No proposals yet"}
          description={
            search || chip !== "All"
              ? "Try a different search term or clear the filter."
              : "Paste a job description above and click Generate Proposal to create your first one."
          }
          action={
            search || chip !== "All" ? (
              <button
                onClick={() => { setSearch(""); setChip("All"); }}
                className="px-3 py-1.5 text-xs font-medium bg-accent text-accent-foreground rounded-md hover:bg-emerald-600 transition-colors"
              >
                Clear filters
              </button>
            ) : undefined
          }
        />
      ) : (
        <div className="space-y-2">
          {filtered.map((proposal) => {
            const sc = scoreColors(proposal.overall_score);
            return (
              <div
                key={proposal.id}
                onClick={() => onOpen(proposal)}
                role="button"
                tabIndex={0}
                aria-label={`Open proposal: ${proposal.title} for ${proposal.client}`}
                onKeyDown={(e) => e.key === "Enter" && onOpen(proposal)}
                className="w-full bg-card border border-border rounded-lg px-4 sm:px-5 py-3.5 flex items-center gap-3 hover:border-accent/40 hover:shadow-sm transition-all cursor-pointer group"
              >
                {/* File icon */}
                <div className="w-9 h-9 rounded-lg bg-secondary flex items-center justify-center flex-shrink-0">
                  <FileText className="w-4 h-4 text-muted-foreground" aria-hidden="true" />
                </div>

                {/* Title + client + category */}
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-medium text-foreground truncate leading-tight">{proposal.title}</p>
                  <div className="flex items-center gap-1.5 mt-1 flex-wrap">
                    <p className="text-xs text-muted-foreground truncate">{proposal.client}</p>
                    <span className={`text-[10px] px-1.5 py-0.5 rounded font-medium leading-tight ${categoryColor[proposal.category]}`}>
                      {proposal.category}
                    </span>
                  </div>
                </div>

                {/* Right side */}
                <div className="flex items-center gap-2.5 flex-shrink-0">
                  {/* AI Score badge — larger, two-line */}
                  <div className={`hidden sm:flex flex-col items-center px-2.5 py-1.5 rounded-lg min-w-[54px] ${sc.badge}`}>
                    <span className="text-[9px] font-semibold uppercase tracking-wide opacity-60 leading-none mb-0.5">
                      AI Score
                    </span>
                    <span className="text-sm font-bold leading-none">
                      {proposal.overall_score}
                      <span className="text-[10px] font-normal opacity-50">/100</span>
                    </span>
                  </div>

                  {/* Budget + date */}
                  <div className="text-right hidden md:block">
                    <p className="text-sm font-medium text-foreground">{proposal.budget}</p>
                    <p className="text-xs text-muted-foreground flex items-center gap-1 justify-end mt-0.5">
                      <Clock className="w-3 h-3" aria-hidden="true" />
                      {new Date(proposal.created_at).toLocaleDateString()}
                    </p>
                  </div>

                  {/* Status badge */}
                  <span className={`text-xs px-2 py-0.5 rounded-full font-medium whitespace-nowrap ${statusColor[proposal.status]}`}>
                    {proposal.status}
                  </span>

                  {/* Chevron */}
                  <ChevronRight className="w-4 h-4 text-muted-foreground group-hover:text-accent transition-colors" aria-hidden="true" />
                </div>
              </div>
            );
          })}

          {/* New blank button */}
          <button
            className="w-full flex items-center justify-center gap-1.5 py-3 text-xs text-muted-foreground hover:text-foreground border border-dashed border-border rounded-lg transition-colors hover:border-accent/30"
            aria-label="Create a new blank proposal"
          >
            <Plus className="w-3.5 h-3.5" aria-hidden="true" />
            New blank proposal
          </button>
        </div>
      )}
    </section>
  );
}

// ─── Analytics Tab ────────────────────────────────────────────────────────────

interface KPIData {
  label: string;
  value: string;
  sub: string;
  trendUp: boolean;
  icon: React.ElementType;
  iconBg: string;
  iconColor: string;
  sparkData: { v: number }[];
  sparkColor: string;
}

function formatRelativeTime(dateString: string) {
    const now = new Date();
    const date = new Date(dateString);

    const diff = now.getTime() - date.getTime();

    const minutes = Math.floor(diff / 60000);

    if (minutes < 1) return "Just now";
    if (minutes < 60) return `${minutes} min ago`;

    const hours = Math.floor(minutes / 60);

    if (hours < 24) return `${hours} hr ago`;

    const days = Math.floor(hours / 24);

    if (days < 30) return `${days} day${days > 1 ? "s" : ""} ago`;

    return date.toLocaleDateString();
}

function AnalyticsTab() {
  const [dashboard, setDashboard] = useState<AnalyticsDashboardStats | null>(null);

  const [loading, setLoading] = useState(true);
  const [revenue, setRevenue] =
    useState(0);
  const [statusData, setStatusData] =
    useState<StatusDistributionItem[]>([]);
  const [proposalTrend, setProposalTrend] =
    useState<ProposalTrendItem[]>([]);

  const [aiScoreTrend, setAIScoreTrend] =
      useState<AIScoreTrendItem[]>([]);

  const [acceptanceTrend, setAcceptanceTrend] =
      useState<AcceptanceTrendItem[]>([]);

  const [activityFeed, setActivityFeed] =
      useState<RecentActivityItem[]>([]);

  const [clients, setClients] =
      useState<TopClient[]>([]);

  const [productHealth, setProductHealth] =
    useState<ProductHealth | null>(null);

  const [proposalFunnel, setProposalFunnel] =
      useState<ProposalFunnel | null>(null);

  const [featureUsage, setFeatureUsage] =
      useState<FeatureUsage[]>([]);

  const STATUS_COLORS = {
    Accepted: "#10b981",
    Sent: "#3b82f6",
    Draft: "#f59e0b",
    Rejected: "#ef4444",
};
  useEffect(() => {

    async function loadAnalytics() {

        try {

            const [
                dashboardData,
                clientsData,
                statusDistribution,
                proposalTrendData,
                aiTrendData,
                acceptanceTrendData,
                activityData,
                health,
                funnel,
                features,
            ] = await Promise.all([
                fetchAnalyticsDashboard(),
                fetchTopClients(),
                fetchStatusDistribution(),
                fetchProposalTrend(),
                fetchAIScoreTrend(),
                fetchAcceptanceTrend(),
                fetchRecentActivity(),
                fetchProductHealth(),
                fetchProposalFunnel(),
                fetchFeatureUsage(),
            ]);

            setDashboard(dashboardData);
            setStatusData(
                    statusDistribution.data.map(item => ({
                        ...item,
                        name: item.status,
                    }))
                );
            setProposalTrend(proposalTrendData.data);

            setAIScoreTrend(aiTrendData.data);

            setAcceptanceTrend(acceptanceTrendData.data);

            setActivityFeed(activityData.data);

            setClients(clientsData.data);

            setProductHealth(health);

            setProposalFunnel(funnel);

            setFeatureUsage(features.data);

            const revenue =
                clientsData.data.reduce(
                    (sum, client) => sum + client.revenue,
                    0
                );

            setRevenue(revenue);

        } catch (error) {

            console.error(error);

        } finally {

            setLoading(false);

        }

    }

    loadAnalytics();

}, []);

  const kpis: KPIData[] = [
    {
      label: "Total Proposals",
      value: dashboard ? dashboard.total_proposals.toString() : "--",
      sub: "+3 this month",
      trendUp: true,
      icon: FileText,
      iconBg: "bg-blue-50 dark:bg-blue-900/20",
      iconColor: "text-blue-500",
      sparkData: kpiSparkData.proposals,
      sparkColor: "#3b82f6",
    },
    {
      label: "Acceptance Rate",
      value: dashboard ? `${dashboard.acceptance_rate}%` : "--",
      sub: "+4% vs last month",
      trendUp: true,
      icon: TrendingUp,
      iconBg: "bg-emerald-50 dark:bg-emerald-900/20",
      iconColor: "text-emerald-500",
      sparkData: kpiSparkData.acceptance,
      sparkColor: "#059669",
    },
    {
      label: "Average AI Score",
      value: dashboard ? dashboard.average_ai_score.toString() : "--",
      sub: "+2pts this month",
      trendUp: true,
      icon: Star,
      iconBg: "bg-amber-50 dark:bg-amber-900/20",
      iconColor: "text-amber-500",
      sparkData: kpiSparkData.aiScore,
      sparkColor: "#f59e0b",
    },
    {
      label: "Quoted Revenue",
      value: `$${(revenue / 1000).toFixed(1)}k`,
      sub: "+$5.6k this month",
      trendUp: true,
      icon: DollarSign,
      iconBg: "bg-violet-50 dark:bg-violet-900/20",
      iconColor: "text-violet-500",
      sparkData: kpiSparkData.revenue,
      sparkColor: "#8b5cf6",
    },
  ];

  const kpiBorderColors = ["border-l-blue-400", "border-l-emerald-400", "border-l-amber-400", "border-l-violet-400"];

  /* ── client avatar colors cycling ── */
  const avatarPalette = [
    "bg-blue-100 text-blue-700",
    "bg-emerald-100 text-emerald-700",
    "bg-violet-100 text-violet-700",
    "bg-amber-100 text-amber-700",
    "bg-rose-100 text-rose-700",
  ];

  return (
    <section aria-label="Analytics overview" className="space-y-5 pt-2">

      {/* ── KPI row ── */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {kpis.map((kpi, i) => (
          <div
            key={kpi.label}
            className={`bg-card border border-border border-l-4 ${kpiBorderColors[i]} rounded-xl p-4 flex flex-col gap-3 hover:shadow-md transition-shadow`}
          >
            <div className="flex items-center justify-between">
              <div className={`w-9 h-9 rounded-lg flex items-center justify-center ${kpi.iconBg}`}>
                <kpi.icon className={`w-4.5 h-4.5 ${kpi.iconColor}`} aria-hidden="true" />
              </div>
              <span className={`flex items-center gap-0.5 text-[11px] font-semibold px-1.5 py-0.5 rounded-full ${kpi.trendUp ? "text-emerald-700 bg-emerald-50 dark:bg-emerald-900/20" : "text-red-600 bg-red-50 dark:bg-red-900/20"}`}>
                {kpi.trendUp
                  ? <ArrowUpRight className="w-3 h-3" aria-hidden="true" />
                  : <ArrowDownRight className="w-3 h-3" aria-hidden="true" />}
                {kpi.trendUp ? "Up" : "Down"}
              </span>
            </div>
            <div>
              <p className="text-3xl font-bold text-foreground tracking-tight leading-none">{kpi.value}</p>
              <p className="text-xs text-muted-foreground mt-1.5 leading-snug">{kpi.label}</p>
              <p className="text-[11px] text-muted-foreground/60 mt-0.5">{kpi.sub}</p>
            </div>
          </div>
        ))}
      </div>

      {/* ── Product Health + Proposal Funnel ── */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">

        {/* Product Health */}
        <SectionCard label="Product Health">
          <div className="flex items-start justify-between mb-5">
            <div>
              <p className="text-base font-semibold text-foreground">Product Health</p>
              <p className="text-xs text-muted-foreground mt-0.5">Overall platform performance and business metrics</p>
            </div>
            <div className="inline-flex items-center gap-1.5 rounded-full border border-emerald-200 bg-emerald-50 dark:bg-emerald-900/20 dark:border-emerald-800 px-2.5 py-1 ring-1 ring-emerald-200 dark:ring-emerald-800">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
              <span className="text-xs font-semibold text-emerald-700 dark:text-emerald-400">Good</span>
            </div>
          </div>

          {/* Top client */}
          <div className="flex items-center gap-2 mb-5 p-3 rounded-lg bg-sky-50 dark:bg-sky-900/15 border border-sky-100 dark:border-sky-800">
            <Users className="w-4 h-4 text-sky-500 flex-shrink-0" />
            <div className="min-w-0">
              <p className="text-[10px] uppercase tracking-wide text-sky-600 dark:text-sky-400 font-semibold">Top Client</p>
              <p className="text-sm font-bold text-foreground truncate">{productHealth?.top_client ?? "—"}</p>
            </div>
          </div>

          {/* KPI grid */}
          <div className="grid grid-cols-2 gap-3 mb-5">
            {[
              { label: "Total", value: productHealth?.total_proposals, suffix: "" },
              { label: "Success Rate", value: productHealth?.proposal_success_rate, suffix: "%" },
              { label: "Acceptance", value: productHealth?.acceptance_rate, suffix: "%" },
              { label: "Avg AI Score", value: productHealth?.average_ai_score, suffix: "" },
            ].map((item) => (
              <div key={item.label} className="p-3 rounded-lg bg-secondary/60 border border-border/60">
                <p className="text-[10px] uppercase tracking-wide text-muted-foreground font-semibold mb-1">{item.label}</p>
                <p className="text-2xl font-bold text-foreground leading-none">
                  {item.value ?? "—"}<span className="text-sm font-medium text-muted-foreground">{item.suffix}</span>
                </p>
              </div>
            ))}
          </div>

          {/* Most used feature */}
          <div className="flex items-center gap-2 p-3 rounded-lg border border-amber-200 bg-amber-50 dark:bg-amber-900/15 dark:border-amber-800">
            <Sparkles className="w-4 h-4 text-amber-500 flex-shrink-0" />
            <div>
              <p className="text-[10px] uppercase tracking-wide text-amber-600 dark:text-amber-400 font-semibold">Most Used Feature</p>
              <p className="text-sm font-semibold text-amber-800 dark:text-amber-300">{productHealth?.most_used_feature ?? "—"}</p>
            </div>
          </div>
        </SectionCard>

        {/* Proposal Funnel */}
        <SectionCard label="Proposal Funnel">
          <p className="text-base font-semibold text-foreground mb-0.5">Proposal Funnel</p>
          <p className="text-xs text-muted-foreground mb-6">Conversion from proposal generation to acceptance</p>

          <div className="space-y-5">
            {[
              {
                label: "Generated",
                count: proposalFunnel?.counts.generated,
                width: "100%",
                color: "bg-blue-500",
                sub: null,
                step: "01",
              },
              {
                label: "Sent",
                count: proposalFunnel?.counts.sent,
                width: `${proposalFunnel?.conversion.send_rate ?? 0}%`,
                color: "bg-indigo-500",
                sub: `${proposalFunnel?.conversion.send_rate ?? 0}% of generated`,
                step: "02",
              },
              {
                label: "Accepted",
                count: proposalFunnel?.counts.accepted,
                width: `${proposalFunnel?.conversion.overall_success_rate ?? 0}%`,
                color: "bg-emerald-500",
                sub: `${proposalFunnel?.conversion.overall_success_rate ?? 0}% overall success`,
                step: "03",
              },
            ].map((stage) => (
              <div key={stage.label}>
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] font-bold text-muted-foreground/50 tabular-nums">{stage.step}</span>
                    <span className="text-sm font-semibold text-foreground">{stage.label}</span>
                  </div>
                  <span className="text-sm font-bold text-foreground tabular-nums">{stage.count ?? "—"}</span>
                </div>
                <div className="w-full bg-secondary rounded-full h-3 overflow-hidden">
                  <div
                    className={`${stage.color} h-3 rounded-full transition-all duration-700`}
                    style={{ width: stage.width }}
                  />
                </div>
                {stage.sub && (
                  <p className="text-[11px] text-muted-foreground mt-1.5">{stage.sub}</p>
                )}
              </div>
            ))}
          </div>
        </SectionCard>
      </div>

      {/* ── Charts row 1: Donut + Proposals Over Time ── */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">

        <SectionCard label="Proposal status distribution">
          <div className="flex items-center gap-2 mb-1">
            <span className="w-2 h-2 rounded-full bg-emerald-500" />
            <p className="text-base font-semibold text-foreground">Status Distribution</p>
          </div>
          <p className="text-xs text-muted-foreground mb-4">All-time breakdown by outcome</p>
          <ResponsiveContainer width="100%" height={190}>
            <PieChart>
              <Pie
                data={statusData}
                cx="40%"
                cy="50%"
                innerRadius={54}
                outerRadius={78}
                paddingAngle={3}
                dataKey="count"
                startAngle={90}
                endAngle={-270}
                isAnimationActive
                animationBegin={0}
                animationDuration={600}
              >
                {statusData.map((entry) => (
                  <Cell
                    key={`cell-${entry.status}`}
                    fill={STATUS_COLORS[entry.status as keyof typeof STATUS_COLORS] ?? "#94a3b8"}
                    stroke="transparent"
                  />
                ))}
              </Pie>
              <Tooltip
                contentStyle={TOOLTIP_STYLE.contentStyle}
                formatter={(value: number, _name: string, props: any) => [
                  `${value} proposals`,
                  props.payload.status,
                ]}
              />
              <Legend
                layout="vertical"
                align="right"
                verticalAlign="middle"
                iconType="circle"
                iconSize={8}
                wrapperStyle={{ fontSize: 11, lineHeight: "24px" }}
              />
            </PieChart>
          </ResponsiveContainer>
        </SectionCard>

        <SectionCard label="Proposals generated over time">
          <div className="flex items-center gap-2 mb-1">
            <span className="w-2 h-2 rounded-full bg-blue-500" />
            <p className="text-base font-semibold text-foreground">Proposals Over Time</p>
          </div>
          <p className="text-xs text-muted-foreground mb-4">Generated vs. accepted per month</p>
          <ResponsiveContainer width="100%" height={190}>
            <LineChart data={proposalTrend} margin={{ top: 8, right: 8, bottom: 0, left: -16 }}>
              <XAxis dataKey="month" {...AXIS_PROPS} />
              <YAxis {...AXIS_PROPS} />
              <Tooltip {...TOOLTIP_STYLE} />
              <Line
                type="monotone" dataKey="proposals" stroke="#3b82f6" strokeWidth={2}
                dot={{ r: 3, fill: "#3b82f6", strokeWidth: 0 }}
                activeDot={{ r: 4 }}
                name="Generated"
                isAnimationActive animationDuration={600}
              />
              <Line
                type="monotone" dataKey="accepted" stroke="#059669" strokeWidth={2}
                dot={{ r: 3, fill: "#059669", strokeWidth: 0 }}
                activeDot={{ r: 4 }}
                name="Accepted"
                strokeDasharray="4 3"
                isAnimationActive animationDuration={800}
              />
            </LineChart>
          </ResponsiveContainer>
        </SectionCard>
      </div>

      {/* ── Charts row 2: AI Score + Acceptance Rate ── */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">

        <SectionCard label="AI score trend">
          <div className="flex items-center gap-2 mb-1">
            <span className="w-2 h-2 rounded-full bg-emerald-500" />
            <p className="text-base font-semibold text-foreground">AI Score Trend</p>
          </div>
          <p className="text-xs text-muted-foreground mb-4">Average proposal quality score per month</p>
          <ResponsiveContainer width="100%" height={160}>
            <BarChart data={aiScoreTrend} margin={{ top: 4, right: 8, bottom: 0, left: -16 }} barCategoryGap="30%">
              <XAxis dataKey="month" {...AXIS_PROPS} />
              <YAxis {...AXIS_PROPS} domain={[60, 100]} tickCount={5} />
              <Tooltip {...TOOLTIP_STYLE} formatter={(v: number) => [`${v}`, "Avg. Score"]} />
              <Bar
                dataKey="aiScore" name="AI Score" fill="#059669" radius={[5, 5, 0, 0]} maxBarSize={28}
                isAnimationActive animationDuration={500}
              />
            </BarChart>
          </ResponsiveContainer>
        </SectionCard>

        <SectionCard label="Acceptance rate trend">
          <div className="flex items-center gap-2 mb-1">
            <span className="w-2 h-2 rounded-full bg-emerald-400" />
            <p className="text-base font-semibold text-foreground">Acceptance Rate Trend</p>
          </div>
          <p className="text-xs text-muted-foreground mb-4">Monthly acceptance rate (%)</p>
          <ResponsiveContainer width="100%" height={160}>
            <AreaChart data={acceptanceTrend} margin={{ top: 8, right: 8, bottom: 0, left: -16 }}>
              <defs>
                <linearGradient id="rateGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%"  stopColor="#059669" stopOpacity={0.18} />
                  <stop offset="95%" stopColor="#059669" stopOpacity={0} />
                </linearGradient>
              </defs>
              <XAxis dataKey="month" {...AXIS_PROPS} />
              <YAxis {...AXIS_PROPS} domain={[0, 100]} tickFormatter={(v: number) => `${v}%`} tickCount={5} />
              <Tooltip {...TOOLTIP_STYLE} formatter={(v: number) => [`${v}%`, "Rate"]} />
              <Area
                type="monotone" dataKey="rate" stroke="#059669" strokeWidth={2}
                fill="url(#rateGrad)" name="Acceptance Rate"
                dot={{ r: 3, fill: "#059669", strokeWidth: 0 }}
                activeDot={{ r: 4 }}
                isAnimationActive animationDuration={600}
              />
            </AreaChart>
          </ResponsiveContainer>
        </SectionCard>
      </div>

      {/* ── Feature Usage + Top Clients ── */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">

        <SectionCard label="Feature Usage">
          <div className="flex items-center gap-2 mb-1">
            <span className="w-2 h-2 rounded-full bg-blue-500" />
            <p className="text-base font-semibold text-foreground">Feature Usage</p>
          </div>
          <p className="text-xs text-muted-foreground mb-4">Most frequently used product features</p>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart
              data={featureUsage}
              margin={{ top: 4, right: 8, left: -4, bottom: 48 }}
            >
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--border)" />
              <XAxis
                dataKey="feature"
                {...AXIS_PROPS}
                angle={-30}
                textAnchor="end"
                interval={0}
                height={56}
              />
              <YAxis {...AXIS_PROPS} />
              <Tooltip {...TOOLTIP_STYLE} />
              <Bar
                dataKey="count"
                fill="#3b82f6"
                radius={[6, 6, 0, 0]}
                maxBarSize={22}
                isAnimationActive
                animationDuration={500}
              />
            </BarChart>
          </ResponsiveContainer>
        </SectionCard>

        <SectionCard label="Top clients">
          <div className="flex items-center gap-2 mb-4">
            <Users className="w-4 h-4 text-muted-foreground" aria-hidden="true" />
            <p className="text-base font-semibold text-foreground">Top Clients</p>
          </div>
          <table className="w-full text-xs" aria-label="Top clients by revenue">
            <thead>
              <tr className="border-b border-border">
                <th className="text-left pb-2.5 text-muted-foreground font-medium pl-1">Client</th>
                <th className="text-right pb-2.5 text-muted-foreground font-medium">Won</th>
                <th className="text-right pb-2.5 text-muted-foreground font-medium">Revenue</th>
                <th className="text-right pb-2.5 text-muted-foreground font-medium">Rate</th>
              </tr>
            </thead>
            <tbody>
              {clients.map((client, idx) => (
                <tr
                  key={client.client_name}
                  className="border-b border-border/40 last:border-0 hover:bg-secondary/40 transition-colors rounded"
                >
                  <td className="py-2.5 pl-1">
                    <div className="flex items-center gap-2">
                      <span className={`w-7 h-7 rounded-full flex items-center justify-center text-[10px] font-bold flex-shrink-0 ${avatarPalette[idx % avatarPalette.length]}`}>
                        {client.client_name.slice(0, 2).toUpperCase()}
                      </span>
                      <span className="text-foreground font-semibold truncate max-w-[70px]">{client.client_name}</span>
                    </div>
                  </td>
                  <td className="py-2.5 text-right text-muted-foreground tabular-nums">{client.won}/{client.total}</td>
                  <td className={`py-2.5 text-right font-semibold tabular-nums ${client.revenue > 0 ? "text-emerald-600 dark:text-emerald-400" : "text-muted-foreground"}`}>
                    ${client.revenue.toLocaleString()}
                  </td>
                  <td className="py-2.5 text-right">
                    <span className={`inline-block px-1.5 py-0.5 rounded font-bold tabular-nums ${
                      client.win_rate >= 75
                        ? "text-emerald-700 bg-emerald-50 dark:bg-emerald-900/20 dark:text-emerald-400"
                        : client.win_rate >= 40
                        ? "text-amber-700 bg-amber-50 dark:bg-amber-900/20 dark:text-amber-400"
                        : "text-red-600 bg-red-50 dark:bg-red-900/20 dark:text-red-400"
                    }`}>
                      {client.win_rate}%
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </SectionCard>
      </div>

      {/* ── Recent Activity ── */}
      <SectionCard label="Recent activity">
        <div className="flex items-center gap-2 mb-5">
          <Activity className="w-4 h-4 text-muted-foreground" aria-hidden="true" />
          <p className="text-base font-semibold text-foreground">Recent Activity</p>
        </div>
        <ol className="space-y-3 relative border-l-2 border-border ml-2">
          {activityFeed.map((item) => {
            const dotColor =
              item.type === "accepted" ? "bg-emerald-500"
              : item.type === "rejected" ? "bg-red-400"
              : item.type === "sent"     ? "bg-blue-500"
              : "bg-amber-400";
            const labelColor =
              item.type === "accepted" ? "text-emerald-700 bg-emerald-50 dark:bg-emerald-900/20 dark:text-emerald-400"
              : item.type === "rejected" ? "text-red-600 bg-red-50 dark:bg-red-900/20 dark:text-red-400"
              : item.type === "sent"     ? "text-blue-700 bg-blue-50 dark:bg-blue-900/20 dark:text-blue-400"
              : "text-amber-700 bg-amber-50 dark:bg-amber-900/20 dark:text-amber-400";
            return (
              <li key={item.id} className="pl-5 relative">
                <span className={`absolute -left-[7px] top-3 w-3.5 h-3.5 rounded-full border-2 border-card ${dotColor}`} aria-hidden="true" />
                <div className="bg-secondary/40 border border-border/60 rounded-lg p-3 hover:bg-secondary/70 transition-colors">
                  <div className="flex items-start justify-between gap-2 mb-1">
                    <span className={`text-[10px] font-bold uppercase tracking-wide px-1.5 py-0.5 rounded ${labelColor}`}>
                      {item.description}
                    </span>
                    <span className="text-[11px] text-muted-foreground/60 whitespace-nowrap flex-shrink-0">
                      {formatRelativeTime(item.created_at)}
                    </span>
                  </div>
                  <p className="text-xs font-semibold text-foreground leading-snug">{item.title}</p>
                  <p className="text-[11px] text-muted-foreground mt-0.5">{item.client}</p>
                </div>
              </li>
            );
          })}
        </ol>
      </SectionCard>

    </section>
  );
}

// ─── Dashboard ────────────────────────────────────────────────────────────────

interface DashboardProps {
  onGenerate: (description: string) => void;
  proposalHistory: SavedProposal[];

  dashboardStats: DashboardStats;

  onRefresh: () => Promise<void>;
}

export function Dashboard({ onGenerate, proposalHistory, dashboardStats, onRefresh }: DashboardProps) {
  const [jobDescription, setJobDescription] = useState("");
  const [validationError, setValidationError] = useState("");
  const [activeTab, setActiveTab] = useState<"proposals" | "analytics">("proposals");
  const [selectedProposal, setSelectedProposal] = useState<ProposalDetails | null>(null);
  const proposals = proposalHistory;

  const handleGenerateClick = () => {
    const error = validateJobDescription(jobDescription);
    if (error) {
      setValidationError(error);
      return;
    }
    setValidationError("");
    onGenerate(jobDescription);
  };

  const handleDescriptionChange = (value: string) => {
    setJobDescription(value);
    if (validationError) setValidationError(validateJobDescription(value));
  };

  const handleProposalClick = async (
    proposal: SavedProposal
) => {

    try {

        const details =
            await fetchProposalDetails(proposal.id);

        setSelectedProposal(details);

    }

    catch (error) {

        console.error(
            "Failed to load proposal details:",
            error
        );

    }
};


const handleStatusChange = async (
    proposalId: number,
    status: ProposalStatus
) => {
    try {
        await updateProposalStatus(
    proposalId,
    status
);

await onRefresh();

if (selectedProposal) {
    const updated = await fetchProposalDetails(proposalId);
    setSelectedProposal(updated);
}
        setSelectedProposal((prev) =>
    prev && prev.id === proposalId
        ? { ...prev, status }
        : prev
);

    } catch (error) {
        console.error(error);
    }
};

const handleDuplicate = async (
    proposalId: number
) => {

    try {

        await duplicateProposal(proposalId);

        await onRefresh();

        if (selectedProposal) {

            setSelectedProposal(null);

        }

    } catch (error) {

        console.error(error);

    }

};

const handleDelete = async (
    proposalId: number
) => {

    const confirmed = window.confirm(
        "Are you sure you want to delete this proposal?"
    );

    if (!confirmed) return;

    try {

        await deleteProposal(
            proposalId
        );

        await onRefresh();

        setSelectedProposal(null);

    } catch (error) {

        console.error(error);

    }
};


  return (
    <div className="min-h-screen bg-background">
      {/* ── Nav ── */}
      <header className="bg-card border-b border-border px-4 sm:px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 bg-primary rounded flex items-center justify-center" aria-hidden="true">
            <Zap className="w-4 h-4 text-primary-foreground" />
          </div>
          <span className="font-semibold text-foreground tracking-tight">ProposalAI</span>
        </div>
        <div className="flex items-center gap-2">
          <ThemeToggle />
          <div
            className="w-8 h-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center text-xs font-semibold"
            aria-label="User avatar"
          >
            JD
          </div>
        </div>
      </header>

      <main className="max-w-3xl mx-auto px-4 sm:px-6 py-8 sm:py-10">
        {/* Welcome */}
        <div className="mb-8 sm:mb-10">
          <p className="text-muted-foreground text-sm tracking-widest uppercase mb-1">Good morning</p>
          <h1 className="text-foreground tracking-tight">Ready to win your next project?</h1>
        </div>

        {/* Stats — "Avg. response time" replaced with "Avg. AI Score" */}
        {/* TODO: Connect to FastAPI backend — replace static values with fetchStats() */}
        <div className="grid grid-cols-3 gap-3 sm:gap-4 mb-8 sm:mb-10">
          {[
  {
    label: "Proposals Generated",
    value: dashboardStats.total_proposals.toString(),
  },
  {
    label: "Acceptance rate",
    value: `${dashboardStats.acceptance_rate}%`,
  },
  {
    label: "Avg. AI Score",
    value: dashboardStats.average_ai_score.toString(),
  },
].map((stat) => (
            <div key={stat.label} className="bg-card border border-border rounded-lg p-3 sm:p-4">
              <p className="text-xl sm:text-2xl font-semibold text-foreground tracking-tight">{stat.value}</p>
              <p className="text-xs text-muted-foreground mt-1">{stat.label}</p>
            </div>
          ))}
        </div>

        {/* Job Description Input */}
        <SectionCard className="mb-8" label="Paste job description">
          <div className="flex items-center gap-2 mb-4">
            <Briefcase className="w-4 h-4 text-muted-foreground" aria-hidden="true" />
            <label htmlFor="job-description" className="text-foreground tracking-tight font-medium">
              Paste Job Description
            </label>
          </div>
          <textarea
            id="job-description"
            aria-describedby={validationError ? "jd-error" : undefined}
            aria-invalid={!!validationError}
            className={`w-full h-44 bg-background border rounded-md p-4 text-foreground placeholder:text-muted-foreground resize-none focus:outline-none focus:ring-2 focus:ring-accent/50 focus:border-accent transition-colors font-mono text-sm ${
              validationError ? "border-red-400" : "border-border"
            }`}
            placeholder="Paste the full job description here — include requirements, budget, timeline, and any technical details..."
            value={jobDescription}
            onChange={(e) => handleDescriptionChange(e.target.value)}
            maxLength={MAX_LENGTH}
          />
          {validationError && <InlineError id="jd-error" message={validationError} />}
          <div className="flex items-center justify-between mt-4">
            <span className="text-xs text-muted-foreground" aria-live="polite">
              {jobDescription.length}/{MAX_LENGTH} characters
            </span>
            <button
              onClick={handleGenerateClick}
              aria-label="Generate proposal from job description"
              className="flex items-center gap-2 bg-accent text-accent-foreground px-4 sm:px-5 py-2.5 rounded-md hover:bg-emerald-600 transition-colors"
            >
              <Zap className="w-4 h-4" aria-hidden="true" />
              <span>Generate Proposal</span>
            </button>
          </div>
        </SectionCard>

        {/* Tabs */}
        <div role="tablist" aria-label="Dashboard sections" className="flex gap-1 mb-5 border-b border-border">
          {([
            { id: "proposals" as const, label: "Previous Proposals", icon: FileText },
            { id: "analytics" as const, label: "Analytics",          icon: BarChart2 },
          ] as const).map((t) => (
            <button
              key={t.id}
              role="tab"
              aria-selected={activeTab === t.id}
              onClick={() => setActiveTab(t.id)}
              className={`flex items-center gap-1.5 px-3 sm:px-4 py-2.5 text-sm font-medium transition-colors border-b-2 -mb-px ${
                activeTab === t.id
                  ? "text-accent border-accent"
                  : "text-muted-foreground border-transparent hover:text-foreground"
              }`}
            >
              <t.icon className="w-3.5 h-3.5" aria-hidden="true" />
              {t.label}
            </button>
          ))}
        </div>

        {activeTab === "proposals" && (
          <ProposalsTab
    proposals={proposals}
    onOpen={handleProposalClick}
/>
        )}

        {activeTab === "analytics" && (
          <div role="tabpanel">
            <AnalyticsTab />
          </div>
        )}
      </main>

      {/* Proposal detail modal */}
      {selectedProposal && (
        <ProposalDetailModal
          proposal={selectedProposal}
          onClose={() => setSelectedProposal(null)}
          onStatusChange={handleStatusChange}
          onDuplicate={handleDuplicate}
          onDelete={handleDelete}
        />
      )}
    </div>
  );
}