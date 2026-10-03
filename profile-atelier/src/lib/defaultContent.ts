import { Content } from "../types";

export const DEFAULT_CONTENT: Content = {
  handle: "solacode-SC",
  name: "Solayman El Mouden",
  role: "Software Engineer",
  pillars: "AI  |  Math  |  Newest Technologies",
  tagline: [
    "Building systems, web applications,",
    "developer tools and intelligent",
    "software for a better tomorrow."
  ],
  github: "https://github.com/solacode-SC",
  linkedin: "https://www.linkedin.com/in/YOUR-LINKEDIN",
  portfolio: "https://solaymantech.me",
  location: "Morocco",
  brand: {
    latin: "NashirTech",
    arabic: "ناشر تك"
  },
  about: [
    "I'm Solayman El Mouden, a software engineer focused on systems, web technologies, artificial intelligence and mathematics.",
    "I enjoy understanding how things work underneath the abstraction and turning that knowledge into useful software."
  ],
  journey: [
    { lang: "C / C++", area: "Systems" },
    { lang: "Python", area: "Backend & AI" },
    { lang: "TypeScript", area: "Web & Tools" },
    { lang: "Docker", area: "Infrastructure" },
    { lang: "Linux", area: "DevOps" }
  ],
  skills: [
    { label: "C/C++", mono: "C++" },
    { label: "Python", mono: "Py" },
    { label: "JavaScript", mono: "JS" },
    { label: "TypeScript", mono: "TS" },
    { label: "React", mono: "Rx" },
    { label: "Next.js", mono: "N" },
    { label: "Django", mono: "dj" },
    { label: "FastAPI", mono: "FA" },
    { label: "PostgreSQL", mono: "Pg" },
    { label: "Docker", mono: "Dk" },
    { label: "Linux", mono: "Lx" },
    { label: "Git", mono: "Git" }
  ],
  projects: [
    {
      title: "LazyEquation",
      slug: "lazyequation",
      line1: "Interactive math & physics",
      line2: "visualization platform.",
      tags: ["React", "TS", "Fastify", "PostgreSQL"]
    },
    {
      title: "LeetResume",
      slug: "leetresume",
      line1: "AI-powered resume",
      line2: "builder and optimizer.",
      tags: ["Next.js", "Prisma", "Postgres"]
    },
    {
      title: "Libora",
      slug: "libora",
      line1: "Flutter PDF reader with",
      line2: "modern experience.",
      tags: ["Flutter", "Dart", "Riverpod"]
    },
    {
      title: "Webserv",
      slug: "webserv",
      line1: "C++98 HTTP server",
      line2: "from scratch.",
      tags: ["C++98", "Networking"]
    },
    {
      title: "solaJobs v2",
      slug: "solajobs-v2",
      line1: "Arabic-first job board",
      line2: "platform.",
      tags: ["Arabic-first", "Jobs"]
    },
    {
      title: "Alert Generator",
      slug: "prometheus-alert-generator",
      line1: "AI generator for",
      line2: "Prometheus alert rules.",
      tags: ["AI", "Prometheus"]
    },
    {
      title: "Compose Dashboard",
      slug: "docker-compose-dashboard",
      line1: "Docker Compose",
      line2: "dashboard.",
      tags: ["Docker", "Compose"]
    }
  ],
  footer: {
    line1: "Build · Explore · Understand",
    line2: "Software Engineering · Systems · AI · Mathematics",
    arabic: "أبني · أستكشف · أفهم"
  },
  options: {
    useArabic: true,
    useCJK: true
  }
};
