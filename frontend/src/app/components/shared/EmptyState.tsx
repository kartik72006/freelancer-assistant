import type { ReactNode } from "react";

interface EmptyStateProps {
  icon: ReactNode;
  title: string;
  description: string;
  action?: ReactNode;
  className?: string;
}

export function EmptyState({ icon, title, description, action, className = "" }: EmptyStateProps) {
  return (
    <div
      role="status"
      aria-label={title}
      className={`flex flex-col items-center justify-center py-14 gap-3 text-center px-6 ${className}`}
    >
      <div className="w-10 h-10 rounded-full bg-secondary flex items-center justify-center text-muted-foreground">
        {icon}
      </div>
      <div>
        <p className="text-sm font-medium text-foreground mb-1">{title}</p>
        <p className="text-xs text-muted-foreground max-w-xs leading-relaxed">{description}</p>
      </div>
      {action && <div className="mt-1">{action}</div>}
    </div>
  );
}
