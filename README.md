# AI Academy Course Platform

Professional AI/LLM learning platform with video courses and interactive content.

## 🎓 Features

- **📚 Structured Video Courses**: Complete curriculum with timestamped navigation
- **🔐 Secure Authentication**: Protected content via Supabase Auth
- **📝 AI-Powered Transcription**: Generate courses from video content
- **📊 Progress Tracking**: Track your learning journey
- **🎯 Interactive Learning**: Timestamp-based navigation and summaries

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- npm or yarn
- Supabase account

### Installation

1. Clone the repository:
```bash
git clone git@github.com:MemoriasDev/ai-academy.git
cd ai-academy
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment variables:
```bash
cp .env.example .env.local
# Edit .env.local with your Supabase credentials
```

4. Run development server:
```bash
npm run dev
```

## 🛠️ Course Generation

This repository includes Module Mind tools for generating new courses from video content.

### Setup Transcription Environment
```bash
cd ai-course-transcription-package
./setup_whisper.sh  # or setup_whisper.bat on Windows
```

### Generate New Course
```bash
npm run generate-course
```

For detailed instructions, see [WHISPER_SETUP.md](./WHISPER_SETUP.md)

## 📦 Project Structure

```
ai-academy/
├── src/                    # React application source
│   ├── components/         # React components
│   ├── contexts/          # React contexts (Auth, etc.)
│   ├── content/           # Course content (course.json)
│   └── styles/            # Global styles
├── public/                # Static assets
│   └── videos/            # Course videos (local dev)
├── ai-course-transcription-package/  # Course generation tools
├── tools/                 # Utility scripts
└── supabase/             # Database migrations
```

## 🌐 Deployment

### Vercel Deployment

1. Import repository to Vercel
2. Configure environment variables:
   - `VITE_SUPABASE_URL`
   - `VITE_SUPABASE_ANON_KEY`
3. Deploy

### Environment Variables

```env
# Supabase Configuration
VITE_SUPABASE_URL=your-project-url
VITE_SUPABASE_ANON_KEY=your-anon-key

# For admin operations only (never expose to client)
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

## 🔒 Security

- All video content is protected behind authentication
- Videos are served via signed URLs with expiration
- Row Level Security (RLS) policies enforce access control
- Service role keys are never exposed to the client

## 🧪 Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run generate-course` - Generate course from videos

### Testing

```bash
npm run build
npm run preview
# Test at http://localhost:4173
```

## 📄 License

Proprietary - All rights reserved. This is private course content for AI Academy.

## 🤝 Contributing

This is a private repository. For access or contributions, please contact the AI Academy team.

## 📞 Support

For issues or questions about the course platform, please contact the development team.

---

Built with ❤️ using [Module Mind](https://github.com/module-mind) template