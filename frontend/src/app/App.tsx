import { useEffect, useState } from "react";
import { ThemeProvider } from "./ThemeContext";
import { Dashboard } from "./components/Dashboard";
import { JobAnalysis } from "./components/JobAnalysis";
import { ProposalGenerator } from "./components/ProposalGenerator";
import { ReviewScreen } from "./components/ReviewScreen";
import { ExportScreen } from "./components/ExportScreen";
import type { ReviewResult, SavedProposal } from "../types";
import { fetchDashboardStats, fetchProposalHistory, generateAnalysis, saveProposal, updateFinalProposal } from "../services/api";
import type { AnalysisResult, ProposalContent, JobMetadata } from "../types";

// ─── Screen types ─────────────────────────────────────────────────────────----

type Screen =
  | "dashboard"
  | "analysis"
  | "generator"
  | "review"
  | "export";

const PROGRESS_WIDTH: Record<Screen, string> = {
  dashboard: "0%",
  analysis: "25%",
  generator: "50%",
  review: "75%",
  export: "100%",
};

// ─── App state ────────────────────────────────────────────────────────────────
// Shared state is lifted here and passed down as props.
// When the FastAPI backend is connected, API calls will live in services/api.ts
// and be invoked from this component or from the individual screens.

function AppInner() {
  const [screen, setScreen]                     = useState<Screen>("dashboard");
  const [jobDescription, setJobDescription]     = useState<string>("");
  const [analysis, setAnalysis]                 = useState<AnalysisResult | null>(null); 
  const [proposal, setProposal]                 = useState<ProposalContent | null>(null);
  const [review, setReview]                     = useState<ReviewResult | null>(null);

  const handleGenerate = async (description: string) => {
    try {

        setJobDescription(description);

        const result = await generateAnalysis(description);

        setAnalysis(result);

        setScreen("analysis");

    } catch (error) {
        console.error("Analysis failed:", error);
    }
  };

  const handleProposalReady = (
    proposal: ProposalContent,
    review: ReviewResult
) => {

    setProposal(proposal);
    setReview(review);

    setScreen("review");
};

  const handleSave = async (
      editedProposal: ProposalContent,
      metadata: Pick<SavedProposal, "title" | "client" | "budget">
  ) => {

      if (!proposal || !analysis || !review) {
          console.error("Nothing to save.");
          return;
      }

      try {

          const savedProposal = await saveProposal(
              jobDescription,
              proposal,
              analysis,
              review,
              metadata
          );

          await updateFinalProposal(
              savedProposal.id,
              editedProposal
          );
          await refreshDashboard();

          

          setScreen("dashboard");

          // We'll add a success toast and history refresh later.

      } catch (error) {

          console.error("Save failed:", error);

      }

  };

  const [proposalHistory, setProposalHistory] = useState<SavedProposal[]>([]);
  const [dashboardStats, setDashboardStats] = useState({
  total_proposals: 0,
        proposals_sent: 0,
        accepted_proposals: 0,
        acceptance_rate: 0,
        average_ai_score: 0,
        average_response_days: 0,
});


  const refreshDashboard = async () => {

    const [history, stats] = await Promise.all([
    fetchProposalHistory(),
    fetchDashboardStats(),
]);

setProposalHistory(history);
setDashboardStats(stats);

};
useEffect(() => {
              refreshDashboard();
          }, []);
  const isAtDashboard = screen === "dashboard";

  return (
    <div
      className="size-full overflow-y-auto"
      style={{ fontFamily: "'DM Sans', system-ui, sans-serif" }}
    >
      {/* Progress bar — hidden on dashboard */}
      {!isAtDashboard && (
        <div
          className="fixed top-0 left-0 right-0 z-50 h-0.5 bg-secondary"
          role="progressbar"
          aria-label="Workflow progress"
          aria-valuenow={screen === "analysis" ? 33 : screen === "generator" ? 66 : 100}
          aria-valuemin={0}
          aria-valuemax={100}
        >
          <div
            className="h-full bg-accent transition-all duration-500"
            style={{ width: PROGRESS_WIDTH[screen] }}
          />
        </div>
      )}

      {/* Screens */}
      {screen === "dashboard" && (
        <Dashboard 
          onGenerate={handleGenerate} 
          proposalHistory={proposalHistory}
          dashboardStats={dashboardStats}
          onRefresh={refreshDashboard}
        />
      )}

      {screen === "analysis" && (
        <JobAnalysis
            analysis={analysis}
            jobDescription={jobDescription}
            onBack={() => setScreen("dashboard")}
            onNext={() => setScreen("generator")}
        />
      )}

      {screen === "generator" && (
        <ProposalGenerator
          jobDescription={jobDescription}
          onBack={() => setScreen("analysis")}
          onNext={handleProposalReady}
        />
      )}

      

      {screen === "review" && proposal && review && (
          <ReviewScreen
            proposal={proposal}
            review={review}
            onBack={() => setScreen("generator")}
            onContinue={() => setScreen("export")}
          />
      )}

      {screen === "export" && proposal && (
        <ExportScreen
          proposal={proposal}
          jobDescription={jobDescription}
          onBack={() => setScreen("review")}
          onSave={handleSave}
        />
      )}
    </div>
  );
}

export default function App() {
  return (
    <ThemeProvider>
      <AppInner />
    </ThemeProvider>
  );
}
