# AI Football Betting Frontend

A modern React frontend for the AI Football Betting application built with Next.js, TypeScript, and shadcn/ui.

## Features

- **Match Display**: View upcoming football matches and events
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Built with shadcn/ui components
- **Real-time Data**: Fetches match data from backend API

## Tech Stack

- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui
- **State Management**: React hooks

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables:
Create a `.env.local` file with:
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

3. Run the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
src/
├── app/                 # Next.js app router
│   ├── layout.tsx      # Root layout
│   └── page.tsx        # Home page
├── components/         # React components
│   ├── ui/            # shadcn/ui components
│   └── MatchList.tsx  # Match display component
├── lib/               # Utility functions
│   └── api.ts         # API client
└── types/             # TypeScript types
    └── api.ts         # API interfaces
```

## API Integration

The frontend fetches match data from the `/api/v1/matches` endpoint. Make sure your backend server is running and accessible at the URL specified in `NEXT_PUBLIC_API_URL`.

## Deployment

For production deployment:

1. Update `NEXT_PUBLIC_API_URL` to point to your production backend
2. Build the application:
```bash
npm run build
```
3. Deploy to your preferred platform (Vercel, Netlify, etc.)

## Development

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
