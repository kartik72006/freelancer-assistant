import type { ReactNode } from "react";

interface SectionCardProps {
  children: ReactNode;
  className?: string;
  /** Accessible label for the card region */
  label?: string;
}

export function SectionCard({ children, className = "", label }: SectionCardProps) {
  return (
    <section
      aria-label={label}
      className={`bg-card border border-border rounded-lg p-5 ${className}`}
    >
      {children}
    </section>
  );
}

interface SectionCardHeaderProps {
  icon: ReactNode;
  label: string;
  action?: ReactNode;
}

export function SectionCardHeader({ icon, label, action }: SectionCardHeaderProps) {
  return (
    <div className="flex items-center justify-between mb-3">
      <div className="flex items-center gap-2">
        <span className="text-muted-foreground" aria-hidden="true">{icon}</span>
        <p className="text-xs text-muted-foreground uppercase tracking-widest">{label}</p>
      </div>
      {action && <div>{action}</div>}
    </div>
  );
}
