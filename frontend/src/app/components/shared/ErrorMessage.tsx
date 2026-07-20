import { AlertCircle, RefreshCw } from "lucide-react";

interface ErrorMessageProps {
  /** Human-readable error description */
  message: string;
  /** Optional retry callback — renders a Retry button when provided */
  onRetry?: () => void;
  className?: string;
}

export function ErrorMessage({ message, onRetry, className = "" }: ErrorMessageProps) {
  return (
    <div
      role="alert"
      aria-live="assertive"
      className={`border border-red-200 bg-red-50 dark:bg-red-950/30 dark:border-red-900 rounded-lg p-4 flex gap-3 ${className}`}
    >
      <AlertCircle className="w-4 h-4 text-red-500 flex-shrink-0 mt-0.5" aria-hidden="true" />
      <div className="flex-1 min-w-0">
        <p className="text-sm text-red-700 dark:text-red-400 leading-relaxed">{message}</p>
        {onRetry && (
          <button
            onClick={onRetry}
            className="mt-2 flex items-center gap-1.5 text-xs font-medium text-red-700 dark:text-red-400 hover:text-red-800 transition-colors"
            aria-label="Retry failed action"
          >
            <RefreshCw className="w-3 h-3" aria-hidden="true" />
            Try again
          </button>
        )}
      </div>
    </div>
  );
}

/** Full-panel error state used inside cards */
export function ErrorPanel({
  message,
  onRetry,
}: {
  message: string;
  onRetry?: () => void;
}) {
  return (
    <div
      role="alert"
      aria-live="assertive"
      className="flex flex-col items-center justify-center py-16 gap-4 text-center px-6"
    >
      <div className="w-10 h-10 rounded-full bg-red-100 dark:bg-red-950 flex items-center justify-center">
        <AlertCircle className="w-5 h-5 text-red-500" aria-hidden="true" />
      </div>
      <div>
        <p className="text-sm font-medium text-foreground mb-1">Something went wrong</p>
        <p className="text-xs text-muted-foreground max-w-xs">{message}</p>
      </div>
      {onRetry && (
        <button
          onClick={onRetry}
          className="flex items-center gap-2 px-4 py-2 text-sm border border-border bg-card text-foreground rounded-md hover:bg-secondary transition-colors"
          aria-label="Retry failed action"
        >
          <RefreshCw className="w-4 h-4" aria-hidden="true" />
          Retry
        </button>
      )}
    </div>
  );
}
