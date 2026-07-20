import { ArrowLeft, ArrowRight, CheckCircle2, AlertCircle, Sparkles } from "lucide-react";
import { PageHeader } from "./shared/PageHeader";
import { SectionCard, SectionCardHeader } from "./shared/SectionCard";
import type { ProposalContent, ReviewResult } from "../../types";

// ─── Props ────────────────────────────────────────────────────────────────────

interface ReviewScreenProps {
  proposal: ProposalContent;
  review: ReviewResult;
  onBack: () => void;
  onContinue: () => void;
}

// ─── Metric progress bar ──────────────────────────────────────────────────────

interface MetricBarProps {
  label: string;
  value: number; // 0–100
}

function MetricBar({ label, value }: MetricBarProps) {
  const color =
    value >= 80 ? "bg-emerald-500"
    : value >= 60 ? "bg-accent"
    : value >= 40 ? "bg-amber-400"
    : "bg-red-400";

  const textColor =
    value >= 80 ? "text-emerald-600"
    : value >= 60 ? "text-accent"
    : value >= 40 ? "text-amber-600"
    : "text-red-500";

  return (
    <div>
      <div className="flex items-center justify-between mb-1.5">
        <span className="text-sm text-foreground">{label}</span>
        <span className={`text-sm font-semibold ${textColor}`}>{value}</span>
      </div>
      <div
        className="h-2 rounded-full bg-secondary overflow-hidden"
        role="progressbar"
        aria-label={`${label}: ${value} out of 100`}
        aria-valuenow={value}
        aria-valuemin={0}
        aria-valuemax={100}
      >
        <div
          className={`h-full rounded-full transition-all duration-700 ${color}`}
          style={{ width: `${value}%` }}
        />
      </div>
    </div>
  );
}

// ─── Score ring ───────────────────────────────────────────────────────────────

function ScoreRing({ score }: { score: number }) {
  const color =
    score >= 80 ? "text-emerald-500"
    : score >= 60 ? "text-accent"
    : score >= 40 ? "text-amber-500"
    : "text-red-500";

  const ringColor =
    score >= 80 ? "border-emerald-500"
    : score >= 60 ? "border-accent"
    : score >= 40 ? "border-amber-400"
    : "border-red-400";

  return (
    <div
      className={`w-20 h-20 rounded-full border-4 ${ringColor} flex items-center justify-center flex-shrink-0`}
      aria-label={`Overall score: ${score} out of 100`}
    >
      <span className={`text-2xl font-bold tracking-tight ${color}`}>{score}</span>
    </div>
  );
}

// ─── Component ────────────────────────────────────────────────────────────────

export function ReviewScreen({ proposal: _proposal, review, onBack, onContinue }: ReviewScreenProps) {
  
  const metricEntries: { label: string; value: number }[] = [
    { label: "Professionalism", value: review.metrics.professionalism },
    { label: "Personalization", value: review.metrics.personalization },
    { label: "Clarity",         value: review.metrics.clarity },
    { label: "Tone",            value: review.metrics.tone },
  ];

  return (
    <div className="min-h-screen bg-background">
      <PageHeader
        back={{ label: "Proposal Generator", onClick: onBack }}
        step={{ current: 3, total: 4, name: "AI Review" }}
      />

      <main className="max-w-3xl mx-auto px-4 sm:px-6 py-10">
        {/* Page title */}
        <div className="mb-8 flex items-center gap-3">
          <div className="w-8 h-8 rounded bg-accent/10 flex items-center justify-center">
            <Sparkles className="w-4 h-4 text-accent" aria-hidden="true" />
          </div>
          <div>
            <h1 className="text-foreground tracking-tight">AI Proposal Review</h1>
            <p className="text-sm text-muted-foreground">Review your proposal before exporting</p>
          </div>
        </div>

        <div className="space-y-4">
          {/* Overall Score */}
          <SectionCard label="Overall score">
            <div className="flex items-center gap-6">
              <ScoreRing score={review.overallScore} />
              <div>
                <p className="text-xs text-muted-foreground uppercase tracking-widest mb-1">Overall Score</p>
                <p className="text-lg font-semibold text-foreground tracking-tight">{review.verdict}</p>
                <p className="text-sm text-muted-foreground mt-1">
                  Based on professionalism, clarity, tone, and personalisation
                </p>
              </div>
            </div>
          </SectionCard>

          {/* Metrics */}
          <SectionCard label="Evaluation metrics">
            <SectionCardHeader icon={<Sparkles className="w-4 h-4" />} label="Metrics" />
            <div className="space-y-4 mt-1">
              {metricEntries.map((m) => (
                <MetricBar key={m.label} label={m.label} value={m.value} />
              ))}
            </div>
          </SectionCard>

          {/* Strengths */}
          {review.strengths.length > 0 && (
            <SectionCard label="Strengths">
              <SectionCardHeader icon={<CheckCircle2 className="w-4 h-4" />} label="Strengths" />
              <ul className="space-y-2 mt-1" role="list">
                {review.strengths.map((strength) => (
                  <li
                    key={strength}
                    className="flex items-start gap-3 p-3 bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-100 dark:border-emerald-900 rounded-md"
                  >
                    <CheckCircle2 className="w-4 h-4 text-emerald-500 flex-shrink-0 mt-0.5" aria-hidden="true" />
                    <p className="text-sm text-foreground leading-relaxed">{strength}</p>
                  </li>
                ))}
              </ul>
            </SectionCard>
          )}

          {/* Improvements */}
          {review.improvements.length > 0 && (
            <SectionCard label="Suggested improvements">
              <SectionCardHeader icon={<AlertCircle className="w-4 h-4" />} label="Suggested Improvements" />
              <ul className="space-y-2 mt-1" role="list">
                {review.improvements.map((improvement) => (
                  <li
                    key={improvement}
                    className="flex items-start gap-3 p-3 bg-amber-50 dark:bg-amber-950/30 border border-amber-100 dark:border-amber-900 rounded-md"
                  >
                    <AlertCircle className="w-4 h-4 text-amber-500 flex-shrink-0 mt-0.5" aria-hidden="true" />
                    <p className="text-sm text-foreground leading-relaxed">{improvement}</p>
                  </li>
                ))}
              </ul>
            </SectionCard>
          )}

          {/* Navigation */}
          <div className="pt-2 flex items-center justify-between">
            <button
              onClick={onBack}
              aria-label="Go back to proposal generator"
              className="flex items-center gap-2 px-5 py-2.5 text-sm border border-border bg-card text-foreground rounded-md hover:bg-secondary transition-colors"
            >
              <ArrowLeft className="w-4 h-4" aria-hidden="true" />
              Back to Proposal
            </button>
            <button
              onClick={onContinue}
              aria-label="Continue to export"
              className="flex items-center gap-2 bg-accent text-accent-foreground px-6 py-2.5 rounded-md hover:bg-emerald-600 transition-colors"
            >
              Continue to Export
              <ArrowRight className="w-4 h-4" aria-hidden="true" />
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}
