'use client';

import { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { apiClient } from '@/lib/api';
import { MatchAnalysis, BettingAdvice, TeamAnalysis } from '@/types/api';

export function AIAnalysis() {
  const [homeTeam, setHomeTeam] = useState('');
  const [awayTeam, setAwayTeam] = useState('');
  const [teamName, setTeamName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [matchAnalysis, setMatchAnalysis] = useState<MatchAnalysis | null>(null);
  const [bettingAdvice, setBettingAdvice] = useState<BettingAdvice | null>(null);
  const [teamAnalysis, setTeamAnalysis] = useState<TeamAnalysis | null>(null);

  const analyzeMatch = async () => {
    try {
      setLoading(true);
      setError(null);
      const analysis = await apiClient.analyzeMatch(homeTeam, awayTeam);
      setMatchAnalysis(analysis);
    } catch (err) {
      setError('Failed to analyze match');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getBettingAdvice = async () => {
    try {
      setLoading(true);
      setError(null);
      const advice = await apiClient.getBettingAdvice(homeTeam, awayTeam);
      setBettingAdvice(advice);
    } catch (err) {
      setError('Failed to get betting advice');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const analyzeTeam = async () => {
    try {
      setLoading(true);
      setError(null);
      const analysis = await apiClient.analyzeTeamPerformance(teamName);
      setTeamAnalysis(analysis);
    } catch (err) {
      setError('Failed to analyze team');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {error && (
        <Card>
          <CardContent className="p-4">
            <div className="text-red-600">{error}</div>
          </CardContent>
        </Card>
      )}

      <Card>
        <CardContent className="p-6">
          <h3 className="text-lg font-semibold mb-4">Match Analysis</h3>
          <div className="space-y-4">
            <div className="flex gap-4">
              <Input
                placeholder="Home Team"
                value={homeTeam}
                onChange={(e) => setHomeTeam(e.target.value)}
              />
              <Input
                placeholder="Away Team"
                value={awayTeam}
                onChange={(e) => setAwayTeam(e.target.value)}
              />
            </div>
            <div className="flex gap-4">
              <Button onClick={analyzeMatch} disabled={loading || !homeTeam || !awayTeam}>
                Analyze Match
              </Button>
              <Button onClick={getBettingAdvice} disabled={loading || !homeTeam || !awayTeam}>
                Get Betting Advice
              </Button>
            </div>
          </div>

          {matchAnalysis && (
            <div className="mt-4 space-y-2">
              <Badge>Confidence: {matchAnalysis.confidence}%</Badge>
              <p className="text-sm">{matchAnalysis.analysis}</p>
              <div>
                <h4 className="font-medium">Key Factors:</h4>
                <ul className="list-disc list-inside">
                  {matchAnalysis.key_factors.map((factor, i) => (
                    <li key={i} className="text-sm">{factor}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}

          {bettingAdvice && (
            <div className="mt-4 space-y-2">
              <Badge variant={bettingAdvice.risk_level === 'high' ? 'destructive' : 'outline'}>
                Risk Level: {bettingAdvice.risk_level}
              </Badge>
              <Badge>Confidence: {bettingAdvice.confidence}%</Badge>
              <p className="text-sm">{bettingAdvice.recommendation}</p>
              <p className="text-sm">{bettingAdvice.odds_analysis}</p>
            </div>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardContent className="p-6">
          <h3 className="text-lg font-semibold mb-4">Team Analysis</h3>
          <div className="space-y-4">
            <Input
              placeholder="Team Name"
              value={teamName}
              onChange={(e) => setTeamName(e.target.value)}
            />
            <Button onClick={analyzeTeam} disabled={loading || !teamName}>
              Analyze Team
            </Button>
          </div>

          {teamAnalysis && (
            <div className="mt-4 space-y-2">
              <p className="text-sm">{teamAnalysis.performance}</p>
              <div>
                <h4 className="font-medium">Strengths:</h4>
                <ul className="list-disc list-inside">
                  {teamAnalysis.strengths.map((strength, i) => (
                    <li key={i} className="text-sm">{strength}</li>
                  ))}
                </ul>
              </div>
              <div>
                <h4 className="font-medium">Weaknesses:</h4>
                <ul className="list-disc list-inside">
                  {teamAnalysis.weaknesses.map((weakness, i) => (
                    <li key={i} className="text-sm">{weakness}</li>
                  ))}
                </ul>
              </div>
              <p className="text-sm">Recent Form: {teamAnalysis.recent_form}</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
} 