import { useState } from "react";
import {
  Check,
  CheckCircle2,
  Copy,
  Download,
  Plus,
  Save,
  Sparkles,
} from "lucide-react";
import { PageHeader } from "./shared/PageHeader";
import { SectionCard } from "./shared/SectionCard";
import { LoadingSpinner } from "./shared/LoadingSpinner";
import type { ProposalContent, SavedProposal } from "../../types";

// ─── Section metadata (mirrors ProposalGenerator) ────────────────────────────

interface SectionMeta {
  key: keyof ProposalContent;
  label: string;
}

const SECTION_ORDER: SectionMeta[] = [
  { key: "introduction", label: "Introduction" },
  { key: "relevantExperience", label: "Relevant Experience" },
  { key: "approach", label: "Approach" },
  { key: "timeline", label: "Timeline" },
  { key: "pricing", label: "Pricing" },
];

function buildFullProposal(proposal: ProposalContent): string {
  return SECTION_ORDER.map(
    (s) => `## ${s.label}\n\n${proposal[s.key]}`,
  ).join("\n\n---\n\n");
}

// ─── Types ────────────────────────────────────────────────────────────────────

type ActionState = "idle" | "pending" | "done";

interface ExportScreenProps {
    proposal: ProposalContent;

    jobDescription: string;

    onBack: () => void;

    onSave: (
        editedProposal: ProposalContent,
        metadata: Pick<SavedProposal, "title" | "client" | "budget">
    ) => Promise<void>;
}

// ─── Component ────────────────────────────────────────────────────────────────

export function ExportScreen({
  proposal: initialProposal,
  
  jobDescription,
  onBack,
  onSave,
}: ExportScreenProps) {
  // Editable local copy — changes here do not affect the upstream proposal state
  const [proposal, setProposal] =
    useState<ProposalContent>(initialProposal);
  const [originalProposal] =
    useState<ProposalContent>(initialProposal);
  const [activeSection, setActiveSection] =
    useState<keyof ProposalContent>("introduction");
  const [copyState, setCopyState] =
    useState<ActionState>("idle");
  const [saveState, setSaveState] =
    useState<ActionState>("idle");
  const [title, setTitle] = useState("");

  const [client, setClient] = useState("");

  const [budget, setBudget] = useState("");

  const [viewMode, setViewMode] = useState<"ai" | "edited">("edited");

  const [titleError, setTitleError] = useState("");
  const [clientError, setClientError] = useState("");
  const [budgetError, setBudgetError] = useState("");

  // ── Handlers ──────────────────────────────────────────────────────────────

  const handleEdit = (value: string) => {
    setProposal((prev) => ({
      ...prev,
      [activeSection]: value,
    }));
  };

  const handleCopy = async () => {
    setCopyState("pending");
    try {
      await navigator.clipboard.writeText(
        buildFullProposal(displayedProposal),
      );
      setCopyState("done");
      setTimeout(() => setCopyState("idle"), 2000);
    } catch {
      setCopyState("idle");
    }
  };

  const handleDownload = () => {
    const blob = new Blob([buildFullProposal(displayedProposal)], {
      type: "text/plain",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "proposal.txt";
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleSave = async () => {

    setSaveState("pending");

    try {
      setTitleError("");
setClientError("");
setBudgetError("");

let valid = true;

if (!title.trim()) {
    setTitleError("Project title is required.");
    valid = false;
}

if (!client.trim()) {
    setClientError("Client name is required.");
    valid = false;
}

if (!budget.trim()) {
    setBudgetError("Budget is required.");
    valid = false;
}

if (!valid) {
    setSaveState("idle");
    return;
}
      await onSave(
        proposal,{
        title,
        client,
        budget,
      });

      setSaveState("done");

    } catch (error) {

      console.error("Save failed:", error);

      setSaveState("idle");

    }

};

const displayedProposal =
    viewMode === "ai"
        ? originalProposal
        : proposal;
  // ── Render ─────────────────────────────────────────────────────────────────

  return (
    <div className="min-h-screen bg-background">
      <PageHeader
        back={{ label: "AI Review", onClick: onBack }}
        step={{ current: 4, total: 4, name: "Export & Save" }}
      />

      <main className="max-w-4xl mx-auto px-4 sm:px-6 py-10">
        {/* Page title + export actions */}
        <div className="mb-8 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded bg-accent/10 flex items-center justify-center">
              <Sparkles
                className="w-4 h-4 text-accent"
                aria-hidden="true"
              />
            </div>
            <div>
              <h1 className="text-foreground tracking-tight">
                Export & Save
              </h1>
              <p className="text-sm text-muted-foreground">
                Make final edits, then export your proposal
              </p>
            </div>
          </div>

          {/* Export action buttons */}
          

            <div className="flex gap-2 mb-6">
                <button
                    onClick={() => setViewMode("ai")}
                    className={`px-4 py-2 rounded-md transition-colors ${
                        viewMode==="ai"
                            ? "bg-primary text-white"
                            : "bg-secondary"
                    }`}
                >
                    AI Generated
                </button>

                <button
                    onClick={() => setViewMode("edited")}
                    className={`px-4 py-2 rounded-md transition-colors ${
                        viewMode==="edited"
                            ? "bg-primary text-white"
                            : "bg-secondary"
                    }`}
                >
                    Edited
                </button>
            </div>

            <div className="flex items-center gap-2 flex-wrap sm:flex-nowrap">
            <button
              onClick={handleCopy}
              disabled={
                  copyState === "pending" ||
                  saveState === "pending"
              }
              aria-label="Copy proposal to clipboard"
              className="flex items-center gap-2 px-3 sm:px-4 py-2 text-sm border border-border bg-card text-foreground rounded-md hover:bg-secondary disabled:opacity-60 transition-colors"
            >
              {copyState === "pending" ? (
                <LoadingSpinner size="sm" label="Copying…" />
              ) : copyState === "done" ? (
                <Check
                  className="w-4 h-4 text-accent"
                  aria-hidden="true"
                />
              ) : (
                <Copy className="w-4 h-4" aria-hidden="true" />
              )}
              {copyState === "done" ? "Copied!" : "Copy"}
            </button>

            <button
              onClick={handleDownload}
              disabled={
                  saveState === "pending"
              }
              aria-label="Download proposal as text file"
              className="flex items-center gap-2 px-3 sm:px-4 py-2 text-sm border border-border bg-card text-foreground rounded-md hover:bg-secondary transition-colors"
            >
              <Download
                className="w-4 h-4"
                aria-hidden="true"
              />
              Download
            </button>

            <button
              onClick={handleSave}
              disabled={
                  saveState==="pending"
              }
              aria-label="Save proposal to history"
              className="flex items-center gap-2 px-3 sm:px-4 py-2 text-sm bg-accent text-accent-foreground rounded-md hover:bg-emerald-600 disabled:opacity-70 transition-colors"
            >
              {saveState === "pending" ? (
                <LoadingSpinner size="sm" label="Saving…" />
              ) : saveState === "done" ? (
                <CheckCircle2
                  className="w-4 h-4"
                  aria-hidden="true"
                />
              ) : (
                <Save className="w-4 h-4" aria-hidden="true" />
              )}
              {saveState === "pending"
                ? "Saving…"
                : saveState === "done"
                  ? "Saved!"
                  : "Save"}
            </button>
            </div>
        </div>
        
        <div className="bg-card border border-border rounded-lg p-6 mb-8">
          <h2 className="text-lg font-semibold mb-4">
            Proposal Details
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">

            <div>
              <input
                type="text"
                placeholder="Project Title"
                value={title}
                onChange={(e) => {
                    setTitle(e.target.value);

                    if (titleError) {
                        setTitleError("");
                    }
                }}
                className="border border-border rounded-md px-3 py-2 bg-background w-full"
              />
              {titleError && (
                    <p className="mt-1 text-sm text-red-500">
                        {titleError}
                    </p>
                )}
            </div>

            <div>
              <input
                type="text"
                placeholder="Client Name"
                value={client}
                onChange={(e) => {
                    setClient(e.target.value);
                    if (clientError) {
                        setClientError("");
                    }
                }}
                className="border border-border rounded-md px-3 py-2 bg-background w-full"
              />
              {clientError && (
                  <p className="mt-1 text-sm text-red-500">
                      {clientError}
                  </p>
              )}
            </div>

            <div>
              <input
                type="text"
                placeholder="Budget"
              value={budget}
              onChange={(e) => {
                  setBudget(e.target.value);
                  if (budgetError) {
                      setBudgetError("");
                  }
              }}
              className="border border-border rounded-md px-3 py-2 bg-background"
            />
            {budgetError && (
                <p className="mt-1 text-sm text-red-500">
                    {budgetError}
                </p>
            )}
            </div>

          </div>
        </div>

        {/* Editable proposal section */}
        <div className="grid grid-cols-1 sm:grid-cols-[200px,1fr] gap-6 mb-8">
          {/* Section nav */}
          <nav aria-label="Proposal sections">
            <ul className="space-y-1">
              {SECTION_ORDER.map((s) => (
                <li key={s.key}>
                  <button
                    onClick={() => setActiveSection(s.key)}
                    aria-current={
                      activeSection === s.key
                        ? "page"
                        : undefined
                    }
                    className={`w-full text-left px-4 py-2.5 rounded-md text-sm transition-colors ${
                      activeSection === s.key
                        ? "bg-primary text-primary-foreground"
                        : "text-muted-foreground hover:text-foreground hover:bg-secondary"
                    }`}
                  >
                    {s.label}
                  </button>
                </li>
              ))}
            </ul>
          </nav>

          {/* Editor */}
          <div className="bg-card border border-border rounded-lg flex flex-col">
            <div className="border-b border-border px-5 py-3 flex items-center justify-between">
              <p className="font-medium text-foreground">
                {
                  SECTION_ORDER.find(
                    (s) => s.key === activeSection,
                  )?.label
                }
              </p>
              <span
                className="text-xs text-muted-foreground"
                aria-live="polite"
              >
                {proposal[activeSection].length} chars
              </span>
            </div>
            <label htmlFor="export-editor" className="sr-only">
              Edit{" "}
              {
                SECTION_ORDER.find(
                  (s) => s.key === activeSection,
                )?.label
              }
            </label>
            <textarea
              id="export-editor"
              key={activeSection}
              className="flex-1 min-h-[300px] p-5 bg-transparent text-foreground text-sm leading-relaxed resize-none focus:outline-none font-mono"
              value={displayedProposal[activeSection]}
              readOnly={viewMode === "ai"||saveState==="pending" }
              onChange={
                          viewMode === "edited"
                              ? (e)=>handleEdit(e.target.value)
                              : undefined
                      }
              aria-label={`Edit ${SECTION_ORDER.find((s) => s.key === activeSection)?.label}`}
            />
          </div>
        </div>

        {/* Read-only full preview */}
        <article
          aria-label="Full proposal preview"
          className="bg-card border border-border rounded-lg overflow-hidden mb-6"
        >
          <div className="bg-primary px-6 sm:px-8 py-6">
            <p className="text-primary-foreground/60 text-xs tracking-widest uppercase mb-1">
              Proposal Preview
            </p>
            <p className="text-primary-foreground font-semibold">
              {title || "Project Title"} · {client || "Client Name"} ·{" "}{budget || "Budget"}
            </p>
          </div>

          <div className="divide-y divide-border">
            {SECTION_ORDER.map((s, i) => (
              <section
                key={s.key}
                aria-label={s.label}
                className="px-6 sm:px-8 py-6"
              >
                <div className="flex items-baseline gap-4 mb-3">
                  <span
                    className="font-mono text-xs text-muted-foreground w-5"
                    aria-hidden="true"
                  >
                    {String(i + 1).padStart(2, "0")}
                  </span>
                  <h2 className="text-foreground tracking-tight">
                    {s.label}
                  </h2>
                </div>
                <div className="pl-9">
                  <p className="text-sm text-foreground leading-relaxed whitespace-pre-line">
                    {displayedProposal[s.key]}
                  </p>
                </div>
              </section>
            ))}
          </div>

          <footer className="border-t border-border px-6 sm:px-8 py-5 flex items-center justify-between bg-secondary/40">
            <p className="text-xs text-muted-foreground">
              Generated with ProposalAI · {new Date().toLocaleDateString()}
            </p>
            <div className="flex items-center gap-1.5">
              <div
                className="w-1.5 h-1.5 rounded-full bg-accent"
                aria-hidden="true"
              />
              <p className="text-xs text-muted-foreground">
                Ready to send
              </p>
            </div>
          </footer>
        </article>

        {/* Tips + Generate New */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <SectionCard label="Tips for sending">
            <p className="text-xs font-medium text-accent mb-2 uppercase tracking-widest">
              Tips for sending
            </p>
            <ul className="space-y-1.5" role="list">
              {[
                "Personalise the introduction with the client's name if you know it",
                "Reference a specific detail from their job post to show you read it carefully",
                "Send within 2 hours of the job posting for the best response rate",
              ].map((tip) => (
                <li
                  key={tip}
                  className="flex items-start gap-2 text-xs text-muted-foreground"
                >
                  <CheckCircle2
                    className="w-3.5 h-3.5 text-accent mt-0.5 flex-shrink-0"
                    aria-hidden="true"
                  />
                  {tip}
                </li>
              ))}
            </ul>
          </SectionCard>

          <SectionCard label="Start a new proposal">
            <p className="text-xs font-medium text-muted-foreground mb-2 uppercase tracking-widest">
              New Proposal
            </p>
            <p className="text-xs text-muted-foreground mb-4 leading-relaxed">
              Done with this one? Head back to the dashboard to
              start a new proposal for a different job.
            </p>
            <button
              onClick={onBack}
              aria-label="Generate a new proposal from the dashboard"
              className="w-full flex items-center justify-center gap-2 px-4 py-2.5 text-sm border border-border bg-card text-foreground rounded-md hover:bg-secondary transition-colors"
            >
              <Plus className="w-4 h-4" aria-hidden="true" />
              Generate New Proposal
            </button>
          </SectionCard>
        </div>
      </main>
    </div>
  );
}