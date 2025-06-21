import { Match, GamesResponse, MatchAnalysis, BettingAdvice, TeamAnalysis } from '@/types/api';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    console.log('Making API request to:', url);
    
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
      ...options,
    });

    const data = await response.json();
    console.log('API response:', data);
    
    // Check for error in response data
    if ('error' in data) {
      throw new Error(data.error);
    }

    if (!response.ok) {
      throw new Error(data.detail || `API request failed: ${response.statusText}`);
    }

    return data;
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