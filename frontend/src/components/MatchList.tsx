'use client';

import { useEffect, useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { apiClient } from '@/lib/api';
import { GamesResponse, EnhancedMatch, Match } from '@/types/api';

export function MatchList() {
  const [gamesData, setGamesData] = useState<GamesResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showRawJson, setShowRawJson] = useState(false);

  useEffect(() => {
    const fetchMatches = async () => {
      try {
        const response = await apiClient.getMatches();
        setGamesData(response);
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Failed to load matches';
        setError(errorMessage);
        console.error('Error fetching matches:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchMatches();
  }, []);

  if (loading) {
    return (
      <Card>
        <CardContent className="p-6">
          <div className="text-center">Loading matches...</div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardContent className="p-6">
          <div className="text-center text-red-600">{error}</div>
        </CardContent>
      </Card>
    );
  }

  if (!gamesData) {
    return (
      <Card>
        <CardContent className="p-6">
          <div className="text-center text-gray-500">No matches available</div>
        </CardContent>
      </Card>
    );
  }

  // Parse raw games if enhanced data is not available
  let games: Match[] = [];
  try {
    if (!gamesData.enhanced_matches || gamesData.enhanced_matches.length === 0) {
      games = JSON.parse(gamesData.raw_games);
    }
  } catch (e) {
    console.error('Failed to parse raw games:', e);
  }

  const hasEnhancedMatches = Array.isArray(gamesData.enhanced_matches) && gamesData.enhanced_matches.length > 0;

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center mb-4">
        <Badge variant="outline">{gamesData.source}</Badge>
        <button
          onClick={() => setShowRawJson(!showRawJson)}
          className="text-sm text-blue-600 hover:underline"
        >
          {showRawJson ? 'Hide Raw JSON' : 'Show Raw JSON'}
        </button>
      </div>

      {showRawJson && (
        <Card>
          <CardContent className="p-6">
            <pre className="bg-gray-50 p-4 rounded overflow-auto text-sm">
              {gamesData.raw_games}
            </pre>
          </CardContent>
        </Card>
      )}

      {/* Show basic cards when no enhanced data */}
      {!hasEnhancedMatches && games.map((game, index) => (
        <Card key={index} className="hover:shadow-md transition-shadow">
          <CardContent className="p-6">
            <div className="flex flex-col space-y-4">
              {/* Teams */}
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center">
                    <span className="text-lg font-bold">{game.home_team.split(' ')[0]}</span>
                  </div>
                  <span className="font-semibold text-lg">{game.home_team}</span>
                </div>
                <div className="flex flex-col items-center space-y-1">
                  <span className="text-gray-500 font-bold">VS</span>
                  <Badge variant="outline" className="mt-1">{game.competition}</Badge>
                </div>
                <div className="flex items-center space-x-4">
                  <span className="font-semibold text-lg">{game.away_team}</span>
                  <div className="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center">
                    <span className="text-lg font-bold">{game.away_team.split(' ')[0]}</span>
                  </div>
                </div>
              </div>

              {/* Date and Time */}
              <div className="flex items-center justify-center gap-2 text-sm text-gray-600">
                <span className="font-medium">{game.date}</span>
                <span>•</span>
                <span>{game.time}</span>
              </div>

              {/* Stadium Info if available */}
              {game.home_team.includes('(') && (
                <div className="text-center text-sm text-gray-500">
                  🏟️ {game.home_team.match(/\((.*?)\)/)?.[1] || ''}
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      ))}

      {/* Show enhanced cards if available */}
      {hasEnhancedMatches && gamesData.enhanced_matches.map((match, index) => (
        <Card key={index} className="hover:shadow-md transition-shadow">
          <CardContent className="p-6">
            <div className="flex flex-col space-y-4">
              {/* Teams and Logos */}
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <img
                    src={match.home_team_logo}
                    alt={match.original_data.home_team}
                    className="w-12 h-12 object-contain"
                  />
                  <span className="font-semibold text-lg">{match.original_data.home_team}</span>
                </div>
                <span className="text-gray-500 font-bold">VS</span>
                <div className="flex items-center space-x-4">
                  <span className="font-semibold text-lg">{match.original_data.away_team}</span>
                  <img
                    src={match.away_team_logo}
                    alt={match.original_data.away_team}
                    className="w-12 h-12 object-contain"
                  />
                </div>
              </div>

              {/* Match Details */}
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <Badge variant="outline">{match.original_data.competition}</Badge>
                <span>•</span>
                <span>{match.original_data.date}</span>
                <span>•</span>
                <span>{match.original_data.time}</span>
              </div>

              {/* Match Description */}
              <div className="text-sm">
                <p className="text-gray-700">{match.match_description}</p>
              </div>

              {/* Key Players */}
              <div className="text-sm">
                <h4 className="font-medium mb-1">Key Players to Watch:</h4>
                <div className="flex flex-wrap gap-2">
                  {match.key_players.map((player, i) => (
                    <Badge key={i} variant="secondary">{player}</Badge>
                  ))}
                </div>
              </div>

              {/* Rivalry History */}
              {match.rivalry_history && (
                <div className="text-sm">
                  <h4 className="font-medium mb-1">Rivalry History:</h4>
                  <p className="text-gray-700">{match.rivalry_history}</p>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
} 