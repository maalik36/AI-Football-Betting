export interface Match {
  home_team: string;
  away_team: string;
  date: string;
  time: string;
  competition: string;
}

export interface EnhancedMatch {
  original_data: Match;
  home_team_logo: string;
  away_team_logo: string;
  match_description: string;
  key_players: string[];
  rivalry_history: string | null;
}

export interface GamesResponse {
  raw_games: string;
  enhanced_matches: EnhancedMatch[];
  count: number;
  source: string;
}

export interface MatchAnalysis {
  analysis: string;
  confidence: number;
  key_factors: string[];
  prediction?: string;
}

export interface BettingAdvice {
  recommendation: string;
  confidence: number;
  odds_analysis: string;
  risk_level: string;
}

export interface TeamAnalysis {
  performance: string;
  strengths: string[];
  weaknesses: string[];
  recent_form: string;
} 