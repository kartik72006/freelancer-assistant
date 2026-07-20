import { useState } from "react";
import {
  ArrowRight, CheckCircle2, Clock, DollarSign,
  Layers, Sparkles, Tag, TrendingUp, AlertCircle, Info, X,
} from "lucide-react";
import { PageHeader } from "./shared/PageHeader";
import { SectionCard, SectionCardHeader } from "./shared/SectionCard";
import { ErrorPanel } from "./shared/ErrorMessage";
import { AILoadingScreen } from "./AILoadingScreen";
import type { AnalysisResult, SkillEntry, Complexity } from "../../types";


// ─── Style helpers ────────────────────────────────────────────────────────────

const complexityMeta: Record<Complexity, { color: string; bar: string; width: string; desc: string }> = {
  Low:    { color: "text-emerald-700 bg-emerald-50 border-emerald-200", bar: "bg-emerald-500", width: "w-1/3",  desc: "Well-scoped, straightforward build. Lower risk of scope creep." },
  Medium: { color: "text-amber-700 bg-amber-50 border-amber-200",       bar: "bg-amber-400",   width: "w-2/3",  desc: "Moderate complexity with some moving parts. Good for experienced freelancers." },
  High:   { color: "text-red-700 bg-red-50 border-red-200",             bar: "bg-red-500",     width: "w-full", desc: "High complexity — set clear milestones and agree on scope in writing before starting." },
};

// ─── Sub-components ───────────────────────────────────────────────────────────

function ConfidencePill({ value }: { value: number }) {
  const color = value >= 85 ? "text-emerald-600" : value >= 70 ? "text-amber-600" : "text-red-500";
  return (
    <span className={`text-xs font-medium ${color}`} aria-label={`Confidence: ${value}%`}>
      Confidence: {value}%
    </span>
  );
}

/** Read-only skill badge with explainability popover */
function SkillBadge({ skill }: { skill: SkillEntry }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="relative">
      <span className="flex items-center gap-1.5 text-xs px-3 py-1.5 bg-secondary text-foreground rounded border border-border">
        <CheckCircle2 className="w-3 h-3 text-accent flex-shrink-0" aria-hidden="true" />
        {skill.label}
        <button
          onClick={() => setOpen((v) => !v)}
          aria-label={`Why was ${skill.label} detected?`}
          aria-expanded={open}
          className="ml-0.5 text-muted-foreground hover:text-accent transition-colors"
        >
          <Info className="w-3 h-3" aria-hidden="true" />
        </button>
      </span>
      {open && (
        <div
          role="tooltip"
          className="absolute left-0 top-full mt-1.5 z-20 w-56 bg-card border border-border rounded-lg shadow-lg p-3"
        >
          <p className="text-xs text-muted-foreground leading-relaxed">{skill.reason}</p>
          <button
            onClick={() => setOpen(false)}
            aria-label="Close explanation"
            className="absolute top-2 right-2 text-muted-foreground hover:text-foreground"
          >
            <X className="w-3 h-3" aria-hidden="true" />
          </button>
        </div>
      )}
    </div>
  );
}

// ─── Component ────────────────────────────────────────────────────────────────

interface JobAnalysisProps {
  analysis: AnalysisResult | null;
  jobDescription: string;
  onBack: () => void;
  onNext: () => void;
}

export function JobAnalysis({ analysis, jobDescription, onBack, onNext }: JobAnalysisProps) {
  const [phase, setPhase]           = useState<"loading" | "analysis?" | "error">("loading");
  const [errorMessage, setErrorMessage] = useState("");

  const handleLoadComplete = () => {
    try {
      if (!analysis) {
        setErrorMessage("No analysis available.");
        setPhase("error");
        return;
    }

      setPhase("analysis?");
    } catch {
      setErrorMessage("Failed to analyse the job description. Please go back and try again.");
      setPhase("error");
    }
  };

  if (phase === "loading") return <AILoadingScreen onComplete={handleLoadComplete} />;

  if (phase === "error") {
    return (
      <div className="min-h-screen bg-background">
        <PageHeader back={{ label: "Dashboard", onClick: onBack }} step={{ current: 1, total: 3, name: "Job Analysis" }} />
        <main className="max-w-3xl mx-auto px-4 sm:px-6 py-10">
          <SectionCard>
            <ErrorPanel message={errorMessage} onRetry={() => setPhase("loading")} />
          </SectionCard>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <PageHeader
        back={{ label: "Dashboard", onClick: onBack }}
        step={{ current: 1, total: 3, name: "Job Analysis" }}
      />

      <main className="max-w-3xl mx-auto px-4 sm:px-6 py-10">
        {/* Page title */}
        <div className="mb-8 flex items-center gap-3">
          <div className="w-8 h-8 rounded bg-accent/10 flex items-center justify-center">
            <Sparkles className="w-4 h-4 text-accent" aria-hidden="true" />
          </div>
          <div>
            <h1 className="text-foreground tracking-tight">Job Analysis</h1>
            <p className="text-sm text-muted-foreground">
              AI preview — your full job description will be sent to generate the proposal
            </p>
          </div>
        </div>

        {analysis && (
          <div className="space-y-4">
            {/* AI Summary banner */}
            <div className="bg-primary text-primary-foreground rounded-lg p-5">
              <p className="text-xs opacity-60 uppercase tracking-widest mb-2">AI Summary</p>
              <p className="text-sm leading-relaxed">{analysis?.summary}</p>
              <div className="mt-4 pt-4 border-t border-white/10 grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <p className="text-xs opacity-60 uppercase tracking-widest mb-1.5">Client goal</p>
                  <p className="text-sm flex items-center gap-1.5">
                    <TrendingUp className="w-3.5 h-3.5 opacity-70" aria-hidden="true" />
                    {analysis?.clientGoal}
                  </p>
                </div>
                <div>
                  <p className="text-xs opacity-60 uppercase tracking-widest mb-1.5">Tone signals</p>
                  <div className="flex flex-wrap gap-1.5">
                    {analysis?.toneSignals.map((t) => (
                      <span key={t} className="text-xs px-2 py-0.5 rounded-full bg-white/10">{t}</span>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Red flags */}
            {analysis?.redFlags.length > 0 && (
              <div role="alert" className="border border-amber-200 bg-amber-50 dark:bg-amber-950/30 dark:border-amber-900 rounded-lg p-4 flex gap-3">
                <AlertCircle className="w-4 h-4 text-amber-600 flex-shrink-0 mt-0.5" aria-hidden="true" />
                <div>
                  <p className="text-xs font-medium text-amber-700 uppercase tracking-widest mb-1.5">Watch out</p>
                  <ul className="space-y-1">
                    {analysis?.redFlags.map((f) => (
                      <li key={f} className="text-sm text-amber-700">{f}</li>
                    ))}
                  </ul>
                </div>
              </div>
            )}

            {/* Project Type — read-only */}
            <SectionCard label="Project type">
              <SectionCardHeader icon={<Layers className="w-4 h-4" />} label="Project Type" />
              <p className="font-medium text-foreground">{analysis?.projectType}</p>
            </SectionCard>

            {/* Required Skills — read-only with explainability */}
            <SectionCard label="Required skills">
              <SectionCardHeader icon={<Tag className="w-4 h-4" />} label="Required Skills" />
              <div className="flex flex-wrap gap-2">
                {analysis?.skills.map((skill) => (
                  <SkillBadge key={skill.label} skill={skill} />
                ))}
              </div>
              <p className="text-xs text-muted-foreground mt-3 flex items-center gap-1">
                <Info className="w-3 h-3" aria-hidden="true" />
                Tap the info icon on any skill to see why it was detected
              </p>
            </SectionCard>

            {/* Budget & Timeline — read-only with confidence */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <SectionCard label="Estimated budget">
                <SectionCardHeader icon={<DollarSign className="w-4 h-4" />} label="Estimated Budget" />
                <p className="font-semibold text-foreground mt-1">{analysis?.estimatedBudget}</p>
                <div className="mt-2 pt-2 border-t border-border">
                  <ConfidencePill value={analysis?.budgetConfidence} />
                  <div
                    className="h-1 rounded-full bg-secondary mt-1.5 overflow-hidden"
                    role="progressbar"
                    aria-valuenow={analysis?.budgetConfidence}
                    aria-valuemin={0}
                    aria-valuemax={100}
                  >
                    <div className="h-full bg-accent rounded-full transition-all duration-700" style={{ width: `${analysis?.budgetConfidence}%` }} />
                  </div>
                </div>
              </SectionCard>

              <SectionCard label="Estimated timeline">
                <SectionCardHeader icon={<Clock className="w-4 h-4" />} label="Estimated Timeline" />
                <p className="font-semibold text-foreground mt-1">{analysis?.timeline}</p>
                <div className="mt-2 pt-2 border-t border-border">
                  <ConfidencePill value={analysis?.timelineConfidence} />
                  <div
                    className="h-1 rounded-full bg-secondary mt-1.5 overflow-hidden"
                    role="progressbar"
                    aria-valuenow={analysis?.timelineConfidence}
                    aria-valuemin={0}
                    aria-valuemax={100}
                  >
                    <div className="h-full bg-accent rounded-full transition-all duration-700" style={{ width: `${analysis?.timelineConfidence}%` }} />
                  </div>
                </div>
              </SectionCard>
            </div>

            {/* Complexity — read-only */}
            <SectionCard label="Estimated complexity">
              <div className="flex items-center justify-between mb-3">
                <SectionCardHeader icon={<Layers className="w-4 h-4" />} label="Estimated Complexity" />
                <span className={`text-xs px-3 py-1 rounded border font-medium ${complexityMeta[analysis?.complexity].color}`}>
                  {analysis?.complexity}
                </span>
              </div>
              <div
                className="h-1.5 rounded-full bg-secondary overflow-hidden mb-2"
                role="progressbar"
                aria-label={`Complexity: ${analysis?.complexity}`}
              >
                <div className={`h-full rounded-full transition-all duration-500 ${complexityMeta[analysis?.complexity].bar} ${complexityMeta[analysis?.complexity].width}`} />
              </div>
              <p className="text-xs text-muted-foreground">{complexityMeta[analysis?.complexity].desc}</p>
            </SectionCard>

            {/* CTA */}
            <div className="pt-2 flex justify-end">
              <button
                onClick={onNext}
                aria-label="Proceed to proposal generator"
                className="flex items-center gap-2 bg-accent text-accent-foreground px-6 py-2.5 rounded-md hover:bg-emerald-600 transition-colors"
              >
                Generate Proposal
                <ArrowRight className="w-4 h-4" aria-hidden="true" />
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
