import { Loader2 } from "lucide-react";

interface LoadingSpinnerProps {
  /** Short description read by screen readers */
  label?: string;
  size?: "sm" | "md" | "lg";
  className?: string;
}

const sizeMap = { sm: "w-4 h-4", md: "w-6 h-6", lg: "w-8 h-8" };

export function LoadingSpinner({
  label = "Loading…",
  size = "md",
  className = "",
}: LoadingSpinnerProps) {
  return (
    <span role="status" aria-label={label} className={`inline-flex ${className}`}>
      <Loader2 className={`${sizeMap[size]} text-accent animate-spin`} aria-hidden="true" />
    </span>
  );
}

/** Full-panel loading state used inside cards */
export function LoadingPanel({ message = "Loading…" }: { message?: string }) {
  return (
    <div
      role="status"
      aria-live="polite"
      className="flex flex-col items-center justify-center py-16 gap-4"
    >
      <LoadingSpinner size="lg" label={message} />
      <p className="text-sm text-muted-foreground">{message}</p>
    </div>
  );
}
