'use client';

import { MatchList } from '@/components/MatchList';
import { AIAnalysis } from '@/components/AIAnalysis';

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            AI Football Betting
          </h1>
          <p className="text-gray-600">
            View upcoming matches and get AI-powered analysis
          </p>
        </header>

        <div className="max-w-4xl mx-auto">
          <div className="mb-6">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">
              Upcoming Matches
            </h2>
            <MatchList />
          </div>

          <div className="mb-6">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">
              AI Analysis
            </h2>
            <AIAnalysis />
          </div>
        </div>
      </div>
    </div>
  );
}
