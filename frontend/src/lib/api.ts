import { Match, GamesResponse, MatchAnalysis, BettingAdvice, TeamAnalysis } from '@/types/api';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
      ...options,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: response.statusText }));
      throw new Error(errorData.detail || `API request failed: ${response.statusText}`);
    }

    return response.json();
  }

  async getMatches(): Promise<GamesResponse> {
    return this.request('/games/next');
  }

  // AI Agent Routes
  async analyzeMatch(homeTeam: string, awayTeam: string, matchData?: string): Promise<MatchAnalysis> {
    return this.request('/agent/analyze', {
      method: 'POST',
      body: JSON.stringify({ home_team: homeTeam, away_team: awayTeam, match_data: matchData || '' }),
    });
  }

  async getBettingAdvice(homeTeam: string, awayTeam: string, matchData?: string): Promise<BettingAdvice> {
    return this.request('/agent/betting-advice', {
      method: 'POST',
      body: JSON.stringify({ home_team: homeTeam, away_team: awayTeam, match_data: matchData || '' }),
    });
  }

  async analyzeTeamPerformance(teamName: string, performanceData?: string): Promise<TeamAnalysis> {
    return this.request('/agent/team-analysis', {
      method: 'POST',
      body: JSON.stringify({ team_name: teamName, performance_data: performanceData || '' }),
    });
  }
}

export const apiClient = new ApiClient(); 