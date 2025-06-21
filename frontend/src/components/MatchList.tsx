'use client';

import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { apiClient } from '@/lib/api';
import { Match } from '@/types/api';

export function MatchList() {
  const [matches, setMatches] = useState<Match[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchMatches = async () => {
      try {
        const response = await apiClient.getMatches();
        setMatches(response.matches);
      } catch (err) {
        setError('Failed to load matches');
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

  if (matches.length === 0) {
    return (
      <Card>
        <CardContent className="p-6">
          <div className="text-center text-gray-500">No matches available</div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      {matches.map((match) => (
        <Card key={match.id} className="hover:shadow-md transition-shadow">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-4 mb-2">
                  <span className="font-semibold text-lg">{match.home_team}</span>
                  <span className="text-gray-500">vs</span>
                  <span className="font-semibold text-lg">{match.away_team}</span>
                </div>
                <div className="flex items-center gap-4 text-sm text-gray-600">
                  <span>{match.league}</span>
                  <span>•</span>
                  <span>{new Date(match.date).toLocaleDateString()}</span>
                </div>
              </div>
              <Badge variant="outline">{match.league}</Badge>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
} 