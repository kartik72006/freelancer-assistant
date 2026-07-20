// ─── Shared domain types ───────────────────────────────────────────────────────
// All interfaces used across screens. Extend these when connecting to FastAPI.

export type Complexity = "Low" | "Medium" | "High";
export type ProposalStatus =
    | "Draft"
    | "Saved"
    | "Sent"
    | "Accepted"
    | "Rejected";

// A single detected skill with the reason it was extracted
export interface SkillEntry {
  label: string;
  reason: string;
}

// Result returned by the job analysis step
export interface AnalysisResult {
  projectType: string;
  skills: SkillEntry[];
  complexity: Complexity;
  estimatedBudget: string;
  timeline: string;
  budgetConfidence: number;
  timelineConfidence: number;
  summary: string;
  clientGoal: string;
  toneSignals: string[];
  redFlags: string[];
}

export interface JobMetadata {
    title: string;
    client: string;
    budget: string;
}

// Five-section proposal content
export interface ProposalContent {
  introduction: string;
  relevantExperience: string;
  approach: string;
  timeline: string;
  pricing: string;
}

// A saved proposal entry shown in the dashboard history list
export interface SavedProposal {
    id: number;

    title: string;

    client: string;

    budget: string;

    category: string;

    overall_score: number;

    status: ProposalStatus;

    created_at: string;
}

export interface ProposalDetails {
    id: number;

    title: string;

    client: string;

    budget: string;

    created_at: string;

    category: string;

    status: ProposalStatus;

    overall_score: number;

    job_description: string;

    analysis: AnalysisResult;

    proposal: ProposalContent;
    
    final_proposal: ProposalContent | null;

    pricing: string;

    timeline: string;

    review: ReviewResult;
}

export interface ReviewMetrics {
  professionalism: number;
  personalization: number;
  clarity: number;
  tone: number;
}

export interface ReviewResult {
  overallScore: number;
  verdict: string;
  metrics: ReviewMetrics;
  strengths: string[];
  improvements: string[];
}

// Generic async operation state — wrap any data-loading operation with this
export type AsyncStatus = "idle" | "loading" | "success" | "error";

export interface AsyncState<T> {
  status: AsyncStatus;
  data: T | null;
  error: string | null;
}

// Form validation result
export interface ValidationResult {
  valid: boolean;
  message: string;
}

export interface DashboardStats {
    total_proposals: number;
        proposals_sent: number;
        accepted_proposals: number;
        acceptance_rate: number;
        average_ai_score: number;
        average_response_days: number;
}

export interface AnalyticsDashboardStats {
    total_proposals: number;
    proposals_sent: number;
    accepted_proposals: number;
    acceptance_rate: number;
    average_ai_score: number;
    average_response_days: number;
}

export interface StatusDistributionItem {
    status: string;
    name: string;
    count: number;
}

export interface StatusDistributionResponse {
    data: StatusDistributionItem[];
}

export interface ProposalTrendItem {
    month: string;
    proposals: number;
    accepted: number;
}

export interface ProposalTrendResponse {
    data: ProposalTrendItem[];
}

export interface AIScoreTrendItem {
    month: string;
    aiScore: number;
}

export interface AIScoreTrendResponse {
    data: AIScoreTrendItem[];
}

export interface AcceptanceTrendItem {
    month: string;
    rate: number;
}

export interface AcceptanceTrendResponse {
    data: AcceptanceTrendItem[];
}

export interface RecentActivityItem {
    id: number;
    type:
        | "accepted"
        | "rejected"
        | "sent"
        | "saved"
        | "draft"
        | "duplicated"
        | "deleted";

    title: string;
    client: string;
    description: string;
    created_at: string;
}

export interface RecentActivityResponse {
    data: RecentActivityItem[];
}

export interface TopClient {
    client_name: string;
    won: number;
    total: number;
    revenue: number;
    win_rate: number;
}

export interface TopClientsResponse {
    data: TopClient[];
}

export interface ProductHealth {
  health_status: string;
  total_proposals: number;
  proposal_success_rate: number;
  acceptance_rate: number;
  average_ai_score: number;
  most_used_feature: string;
  top_client: string;
}

export interface ProposalFunnelCounts {
  generated: number;
  sent: number;
  accepted: number;
}

export interface ProposalFunnelConversion {
  send_rate: number;
  acceptance_rate: number;
  overall_success_rate: number;
}

export interface ProposalFunnel {
  counts: ProposalFunnelCounts;
  conversion: ProposalFunnelConversion;
}

export interface FeatureUsage {
  feature: string;
  count: number;
}

export interface FeatureUsageResponse {
  data: FeatureUsage[];
}