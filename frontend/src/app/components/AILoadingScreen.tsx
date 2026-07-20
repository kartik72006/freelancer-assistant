import { useEffect, useState } from "react";
import { CheckCircle2, Circle, Loader2, Zap } from "lucide-react";

interface Step {
  id: string;
  label: string;
  duration: number;
}

const STEPS: Step[] = [
  { id: "analyze",    label: "Analyzing Job",              duration: 900 },
  { id: "skills",     label: "Extracting Skills",          duration: 700 },
  { id: "budget",     label: "Estimating Budget",          duration: 600 },
  { id: "projects",   label: "Finding Relevant Projects",  duration: 800 },
  { id: "generating", label: "Generating Proposal",        duration: 900 },
  { id: "reviewing",  label: "Reviewing Proposal",         duration: 600 },
];

interface AILoadingScreenProps {
  onComplete: () => void;
}

export function AILoadingScreen({ onComplete }: AILoadingScreenProps) {
  const [completedSteps, setCompletedSteps] = useState<string[]>([]);
  const [activeStep, setActiveStep] = useState<number>(0);

  useEffect(() => {
    let elapsed = 0;
    const timers: ReturnType<typeof setTimeout>[] = [];

    STEPS.forEach((step, i) => {
      const startTimer = setTimeout(() => setActiveStep(i), elapsed);
      timers.push(startTimer);
      elapsed += step.duration;
      const completeTimer = setTimeout(() => {
        setCompletedSteps((prev) => [...prev, step.id]);
      }, elapsed);
      timers.push(completeTimer);
    });

    const doneTimer = setTimeout(() => onComplete(), elapsed + 300);
    timers.push(doneTimer);

    return () => timers.forEach(clearTimeout);
  }, [onComplete]);

  const totalDuration = STEPS.reduce((acc, s) => acc + s.duration, 0);
  const elapsedDuration = STEPS.slice(0, completedSteps.length).reduce((acc, s) => acc + s.duration, 0);
  const progress = Math.round((elapsedDuration / totalDuration) * 100);

  return (
    <div className="min-h-screen bg-background flex items-center justify-center px-6">
      <div className="w-full max-w-sm">
        <div className="flex items-center gap-2 mb-10 justify-center">
          <div className="w-7 h-7 bg-primary rounded flex items-center justify-center">
            <Zap className="w-4 h-4 text-primary-foreground" />
          </div>
          <span className="font-semibold text-foreground tracking-tight">ProposalAI</span>
        </div>

        <div className="mb-8 text-center">
          <h2 className="text-foreground tracking-tight mb-1">Building your proposal</h2>
          <p className="text-sm text-muted-foreground">AI is working through your job description</p>
        </div>

        <div className="bg-card border border-border rounded-lg p-6 mb-6 space-y-4">
          {STEPS.map((step, i) => {
            const isDone = completedSteps.includes(step.id);
            const isActive = activeStep === i && !isDone;
            return (
              <div key={step.id} className="flex items-center gap-3">
                <div className="w-5 h-5 flex-shrink-0 flex items-center justify-center">
                  {isDone
                    ? <CheckCircle2 className="w-5 h-5 text-accent" />
                    : isActive
                    ? <Loader2 className="w-4 h-4 text-accent animate-spin" />
                    : <Circle className="w-4 h-4 text-border" />}
                </div>
                <span className={`text-sm transition-colors duration-300 ${
                  isDone ? "text-foreground font-medium" : isActive ? "text-foreground" : "text-muted-foreground"
                }`}>
                  {step.label}
                </span>
                {isDone && <span className="ml-auto text-xs text-accent font-medium">Done</span>}
              </div>
            );
          })}
        </div>

        <div className="space-y-2">
          <div className="flex justify-between text-xs text-muted-foreground">
            <span>Progress</span>
            <span>{progress}%</span>
          </div>
          <div className="h-1.5 rounded-full bg-secondary overflow-hidden">
            <div
              className="h-full bg-accent rounded-full transition-all duration-500"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
