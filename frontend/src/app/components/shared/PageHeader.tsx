import type { ReactNode } from "react";
import { ArrowLeft } from "lucide-react";
import { ThemeToggle } from "../ThemeToggle";

interface BackLink {
  label: string;
  onClick: () => void;
}

interface StepLabel {
  current: number;
  total: number;
  name: string;
}

interface PageHeaderProps {
  back?: BackLink;
  step?: StepLabel;
  /** Slot for right-side extra content alongside the theme toggle */
  right?: ReactNode;
}

export function PageHeader({ back, step, right }: PageHeaderProps) {
  return (
    <header className="bg-card border-b border-border px-4 sm:px-6 py-4 flex items-center justify-between">
      {/* Left: back button or empty spacer */}
      <div className="w-28 sm:w-32 flex-shrink-0">
        {back && (
          <button
            onClick={back.onClick}
            aria-label={`Go back to ${back.label}`}
            className="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors"
          >
            <ArrowLeft className="w-4 h-4" aria-hidden="true" />
            <span className="hidden sm:inline">{back.label}</span>
          </button>
        )}
      </div>

      {/* Centre: step indicator */}
      {step && (
        <div className="flex items-center gap-2 text-sm text-muted-foreground" aria-label={`Step ${step.current} of ${step.total}: ${step.name}`}>
          <span className="text-foreground font-medium">Step {step.current}</span>
          <span aria-hidden="true">/</span>
          <span>{step.name}</span>
        </div>
      )}

      {/* Right: theme toggle + optional extra */}
      <div className="w-28 sm:w-32 flex-shrink-0 flex items-center justify-end gap-2">
        {right}
        <ThemeToggle />
      </div>
    </header>
  );
}
