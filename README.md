# AI Academy Course Platform

Professional AI/LLM learning platform featuring the Aitra Legacy Content - a comprehensive 10-week course on developer productivity using artificial intelligence.

## 🎓 Features

- **📚 Structured Video Courses**: Complete curriculum with timestamped navigation
- **🔐 Secure Authentication**: Protected content via Supabase Auth
- **📝 AI-Powered Transcription**: Generate courses from video content
- **📊 Progress Tracking**: Track your learning journey *(Note: Currently in development, not yet active)*
- **🎯 Interactive Learning**: Timestamp-based navigation and summaries

## 📚 Course Curriculum: Aitra Legacy Content

This platform hosts the complete Aitra Legacy Course on AI/LLM development, featuring 22 video lessons across 9 weeks:

### **Weeks 1-2: LLM Foundations & Prompting**
- Introduction to LLMs and Generative AI
- Zero-shot, One-shot, and Few-shot prompting techniques
- Context management and chat history
- Open source LLMs and model selection
- LangChain and LangSmith fundamentals

### **Weeks 3-4: Retrieval Augmented Generation (RAG)**
- Understanding RAG architecture and benefits
- Vector databases and embeddings
- Semantic search implementation
- Mitigating hallucination with external knowledge
- RAG optimization techniques

### **Weeks 5-6: Chaining & Tool Integration**
- Building complex LLM chains
- Integrating multiple tools and APIs
- Error handling and retry strategies
- Workflow orchestration
- Memory and state management

### **Weeks 7-8: Agent Development**
- Building autonomous agents
- AWS Bedrock integration
- Production deployment strategies
- Agent reasoning and decision-making
- Tool selection and execution

### **Week 9: Multi-Agent Systems**
- Crew.ai and multi-agent architectures
- Agent communication protocols
- Scaling multi-agent systems
- Real-world implementation examples

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
│   └── videos/            # Video structure only (actual videos in Supabase)
├── ai-course-transcription-package/  # Course generation tools
│   ├── cohorts/           # Transcriptions and analysis
│   ├── scripts/           # Batch processing tools
│   └── setup_whisper.sh  # Transcription environment setup
├── tools/                 # Utility scripts
│   ├── fix_video_paths.py # Video path management
│   └── audit_timestamps.py # Timestamp validation
└── supabase/             # Database migrations & RLS policies
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
# Supabase Configuration (Client-safe)
VITE_SUPABASE_URL=your-project-url
VITE_SUPABASE_ANON_KEY=your-anon-key

# For admin operations only (NEVER use VITE_ prefix for secrets)
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key  # Only for server-side/tools
```

**⚠️ Security Note**: 
- Variables prefixed with `VITE_` are exposed to the client bundle
- The `VITE_SUPABASE_ANON_KEY` is designed to be public and safe for client-side use
- It only works with Row Level Security (RLS) policies enabled
- Never prefix sensitive keys with `VITE_` in a Vite application

## 🔒 Security & Video Storage

### Video Content Management
- **Videos are stored in Supabase Storage**, not in this repository
- The `public/videos/` directory exists for structure but contains no video files
- All 22 course videos (>100MB each) are hosted in Supabase bucket `course-videos`
- To recreate this setup, you'll need:
  1. Original video files (contact course administrators)
  2. Supabase storage bucket configured with RLS policies
  3. Upload videos using the provided tools in `tools/` directory

### Security Features
- All video content is protected behind authentication (Supabase Auth)
- Videos are served via signed URLs with 15-minute expiration
- Row Level Security (RLS) policies enforce access control at the database level
- Service role keys are never exposed to the client (no VITE_ prefix)
- Anon key is safe for client-side use when RLS is enabled

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