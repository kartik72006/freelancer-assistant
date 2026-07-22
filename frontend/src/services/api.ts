/**
 * API Service Layer
 *
 * Every function accepts only `jobDescription: string` — matching the FastAPI
 * backend contract. The backend handles all parsing and inference internally.
 *
 * Base URL via environment variable:
 *   VITE_API_BASE_URL=http://localhost:8000
 */

import type { 
    AnalysisResult, 
    ProposalContent, 
    SavedProposal, 
    ReviewResult, 
    ProposalDetails, 
    DashboardStats,
    AnalyticsDashboardStats,
    TopClientsResponse,
    StatusDistributionResponse,
    ProposalTrendResponse,
    AIScoreTrendResponse,
    AcceptanceTrendResponse,
    RecentActivityResponse,
    ProductHealth,
    ProposalFunnel,
    FeatureUsageResponse,
} from "../types";
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

  console.log("API_BASE_URL =", API_BASE_URL);

  async function apiRequest<T>(
  endpoint: string,
  options: RequestInit,
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers ?? {}),
    },
    ...options,
  });

  if (!response.ok) {
    let message = `HTTP ${response.status}`;

    try {
      const error = await response.json();
      message = error.detail ?? message;
    } catch {
      // Ignore non-JSON error bodies
    }

    throw new Error(message);
  }

  return response.json() as Promise<T>;
}
// ---------------------------------------------------------------------------
// Job Analysis
// ---------------------------------------------------------------------------

/**
 * Analyse the raw job description and return structured project metadata.
 *@param jobDescription - The raw pasted job description text
 */
  export async function generateAnalysis(jobDescription: string,): Promise<AnalysisResult> {
    return apiRequest<AnalysisResult>("/analysis/analyze",{method: "POST",
                                                          body: JSON.stringify({job_description: jobDescription,}),
                                                          },
                                      );
  }

// ---------------------------------------------------------------------------
// Proposal Generator
// ---------------------------------------------------------------------------
interface ProposalResponse {
    proposal: ProposalContent;
}
/**
 * Generate a full five-section proposal directly from the job description.
 * The backend handles all inference — no intermediate analysis object is sent.
 * @param jobDescription - The raw job description
 */
export async function generateProposal(jobDescription: string): Promise<ProposalContent> {
  const result = await apiRequest<ProposalResponse>(
        "/proposal/generate",
        {
            method: "POST",
            body: JSON.stringify({
                job_description: jobDescription,
            }),
        }
    );

    return result.proposal;
}

// ---------------------------------------------------------------------------
// Review & Export
// ---------------------------------------------------------------------------

/**
 * Submit the final edited proposal (plus the original job description) for
 * AI review and quality scoring.
 * @param jobDescription - The original job description for context
 * @param proposal - The fully edited ProposalContent
 */
export async function generateReview(
    jobDescription: string,
    proposal: ProposalContent
): Promise<ReviewResult> {

    return await apiRequest<ReviewResult>(
        "/review/generate",
        {
            method: "POST",
            body: JSON.stringify({
                job_description: jobDescription,
                proposal: proposal,
            }),
        }
    );
}

/**
 * Save a finalised proposal to the user's history.
 * @param jobDescription - The original job description
 * @param proposal - The final proposal content
 * @param metadata - Title, client name, budget
 */
export async function saveProposal(
    jobDescription: string,
    proposal: ProposalContent,
    analysis: AnalysisResult,
    review: ReviewResult,
    metadata: Pick<SavedProposal, "title" | "client" | "budget">,
): Promise<SavedProposal> {

    return await apiRequest<SavedProposal>(
        "/proposal/save",
        {
            method: "POST",
            body: JSON.stringify({
                job_description: jobDescription,

                title: metadata.title,
                client_name: metadata.client,
                budget: metadata.budget,

                analysis,
                proposal,
                pricing: proposal.pricing,
                review,
                timeline: proposal.timeline
            })
        }
    );
}

/**
 * Fetch the authenticated user's saved proposal history.
 */

export async function fetchProposalHistory(): Promise<SavedProposal[]> {

    return await apiRequest<SavedProposal[]>(
        "/proposal/history",
        {
            method: "GET"
        }
    );

}

export async function fetchProposalDetails(
    proposalId: number
): Promise<ProposalDetails> {
    return await apiRequest<ProposalDetails>(
        `/proposal/${proposalId}`,
        {
            method: "GET",
        }
    );
}

export async function fetchDashboardStats(): Promise<DashboardStats> {
    return apiRequest<DashboardStats>("/proposal/stats", {
        method: "GET",
    });
}

export async function updateProposalStatus(
    proposalId: number,
    status: string
) {
    return apiRequest(`/proposal/${proposalId}/status`, {
        method: "PUT",
        body: JSON.stringify({ status }),
    });
}

export async function updateFinalProposal(
    proposalId: number,
    finalProposal: ProposalContent
) {
    return apiRequest(
        `/proposal/${proposalId}/final`,
        {
            method: "PUT",
            body: JSON.stringify({
                final_proposal: finalProposal
            })
        }
    );
}

export async function duplicateProposal(
    proposalId: number
): Promise<SavedProposal> {

    return apiRequest<SavedProposal>(
        `/proposal/${proposalId}/duplicate`,
        {
            method: "POST",
        }
    );
}

export async function deleteProposal(
    proposalId: number
) {
    return apiRequest(
        `/proposal/${proposalId}`,
        {
            method: "DELETE",
        }
    );
}

export async function fetchAnalyticsDashboard() {
    return apiRequest<AnalyticsDashboardStats>(
        "/analytics/dashboard",
        {
            method: "GET",
        }
    );
}

export async function fetchTopClients() {
    return apiRequest<TopClientsResponse>(
        "/analytics/top-clients",
        {
            method: "GET",
        }
    );
}

export async function fetchStatusDistribution() {
    return apiRequest<StatusDistributionResponse>(
        "/analytics/status-distribution",
        {
            method: "GET",
        }
    );
}

export async function fetchProposalTrend() {
    return apiRequest<ProposalTrendResponse>(
        "/analytics/proposal-trend",
        {
            method: "GET",
        }
    );
}

export async function fetchAIScoreTrend() {
    return apiRequest<AIScoreTrendResponse>(
        "/analytics/ai-score-trend",
        {
            method: "GET",
        }
    );
}

export async function fetchAcceptanceTrend() {
    return apiRequest<AcceptanceTrendResponse>(
        "/analytics/acceptance-trend",
        {
            method: "GET",
        }
    );
}

export async function fetchRecentActivity() {
    return apiRequest<RecentActivityResponse>(
        "/analytics/recent-activity",
        {
            method: "GET",
        }
    );
}

export async function fetchProductHealth() {
    return apiRequest<ProductHealth>(
        "/analytics/product-health",
        {
            method: "GET",
        }
    );
}

export async function fetchFeatureUsage() {
    return apiRequest<FeatureUsageResponse>(
        "/analytics/feature-usage",
        {
            method: "GET",
        }
    );
}

export async function fetchProposalFunnel() {
    return apiRequest<ProposalFunnel>(
        "/analytics/proposal-funnel",
        {
            method: "GET",
        }
    );
}