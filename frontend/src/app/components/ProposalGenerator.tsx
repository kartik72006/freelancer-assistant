import { useEffect, useState } from "react";
import { ArrowLeft, ArrowRight, Sparkles } from "lucide-react";
import { PageHeader } from "./shared/PageHeader";
import { SectionCard } from "./shared/SectionCard";
import { LoadingPanel } from "./shared/LoadingSpinner";
import { ErrorPanel } from "./shared/ErrorMessage";
import { EmptyState } from "./shared/EmptyState";
import { FileText } from "lucide-react";
import type { ProposalContent, ReviewResult } from "../../types";
import { generateProposal, generateReview } from "../../services/api";
// ─── Exported type (re-exported from types for backwards-compat) ──────────────
export type { ProposalContent };

// ─── Section metadata ─────────────────────────────────────────────────────────

interface SectionMeta {
  key: keyof ProposalContent;
  label: string;
}

const SECTIONS: SectionMeta[] = [
  { key: "introduction",       label: "Introduction" },
  { key: "relevantExperience", label: "Relevant Experience" },
  { key: "approach",           label: "Approach" },
  { key: "timeline",           label: "Timeline" },
  { key: "pricing",            label: "Pricing" },
];

// ─── Component ────────────────────────────────────────────────────────────────

type GeneratorPhase = "loading" | "ready" | "error";

interface ProposalGeneratorProps {
  jobDescription: string;
  onBack: () => void;
  onNext: (
    proposal: ProposalContent,
    review: ReviewResult
  ) => void;
}

export function ProposalGenerator({ jobDescription, onBack, onNext }: ProposalGeneratorProps) {
  const [phase, setPhase]                       = useState<GeneratorPhase>("loading");
  const [errorMessage, setErrorMessage]         = useState("");
  const [proposal, setProposal]                 = useState<ProposalContent | null>(null);
  const [activeSection, setActiveSection]       = useState<keyof ProposalContent>("introduction");

  useEffect(() => {
    const timer = setTimeout(async () => {
      try {
        const result = await generateProposal(jobDescription);

        setProposal(result);
        setPhase("ready");
      } catch {
        setErrorMessage("Failed to generate the proposal. Please try again.");
        setPhase("error");
      }
    }, 800);
    return () => clearTimeout(timer);
  }, [jobDescription]);

  const handleEdit = (value: string) => {
    if (!proposal) return;
    setProposal({ ...proposal, [activeSection]: value });
  };

  const handleRetry = () => {
    setPhase("loading");
    setErrorMessage("");
  };

  return (
    <div className="min-h-screen bg-background">
      <PageHeader
        back={{ label: "Job Analysis", onClick: onBack }}
        step={{ current: 2, total: 3, name: "Proposal Generator" }}
      />

      <main className="max-w-4xl mx-auto px-4 sm:px-6 py-10">
        {/* Page title */}
        <div className="mb-8 flex items-center gap-3">
          <div className="w-8 h-8 rounded bg-accent/10 flex items-center justify-center">
            <Sparkles className="w-4 h-4 text-accent" aria-hidden="true" />
          </div>
          <div>
            <h1 className="text-foreground tracking-tight">Generated Proposal</h1>
            <p className="text-sm text-muted-foreground">Edit any section before exporting</p>
          </div>
        </div>

        {/* Loading */}
        {phase === "loading" && (
          <SectionCard>
            <LoadingPanel message="Crafting your proposal…" />
          </SectionCard>
        )}

        {/* Error */}
        {phase === "error" && (
          <SectionCard>
            <ErrorPanel message={errorMessage} onRetry={handleRetry} />
          </SectionCard>
        )}

        {/* Ready */}
        {phase === "ready" && !proposal && (
          <SectionCard>
            <EmptyState
              icon={<FileText className="w-5 h-5" />}
              title="No proposal generated"
              description="Something went wrong. Go back and try again."
              action={
                <button
                  onClick={onBack}
                  className="text-sm text-accent hover:underline"
                  aria-label="Go back to job analysis"
                >
                  Go back
                </button>
              }
            />
          </SectionCard>
        )}

        {phase === "ready" && proposal && (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-[200px,1fr] gap-6">
              {/* Section nav */}
              <nav aria-label="Proposal sections">
                <ul className="space-y-1">
                  {SECTIONS.map((s) => (
                    <li key={s.key}>
                      <button
                        onClick={() => setActiveSection(s.key)}
                        aria-current={activeSection === s.key ? "page" : undefined}
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
                    {SECTIONS.find((s) => s.key === activeSection)?.label}
                  </p>
                  <span className="text-xs text-muted-foreground" aria-live="polite">
                    {proposal[activeSection].length} chars
                  </span>
                </div>
                <label htmlFor="section-editor" className="sr-only">
                  Edit {SECTIONS.find((s) => s.key === activeSection)?.label}
                </label>
                <textarea
                  id="section-editor"
                  key={activeSection}
                  className="flex-1 min-h-[360px] p-5 bg-transparent text-foreground text-sm leading-relaxed resize-none focus:outline-none font-mono"
                  value={proposal[activeSection]}
                  onChange={(e) => handleEdit(e.target.value)}
                  aria-label={`Edit ${SECTIONS.find((s) => s.key === activeSection)?.label}`}
                />
              </div>
            </div>

            {/* CTA */}
            <div className="flex justify-end mt-6">
              <button
                onClick={async () => {
                  if (!proposal) return;
                  try {
                    const review = await generateReview(
                      jobDescription,
                      proposal
                    );

                    onNext(proposal, review);

                  } catch (error) {
                    console.error("Review generation failed:", error);
                  }
                }}
                aria-label="Proceed to review and export"
                className="flex items-center gap-2 bg-accent text-accent-foreground px-6 py-2.5 rounded-md hover:bg-emerald-600 transition-colors"
              >
                Review & Export
                <ArrowRight className="w-4 h-4" aria-hidden="true" />
              </button>
            </div>
          </>
        )}
      </main>
    </div>
  );
}
