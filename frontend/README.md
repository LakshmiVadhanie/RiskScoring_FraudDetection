# Frontend (Next.js + TypeScript)

Quick setup instructions to finish installing dependencies and run locally.

1. From project root:

```bash
cd frontend
```

2. Install Next.js, React, TypeScript and types:

```bash
npm install next@latest react@latest react-dom@latest typescript @types/react @types/node
```

3. Install UI & utility deps:

```bash
npm install tailwindcss postcss autoprefixer
npm install recharts lucide-react
npm install @tanstack/react-query axios date-fns
```

4. Initialize Tailwind (optional if you keep provided config):

```bash
npx tailwindcss init -p
```

5. Start dev server:

```bash
npm run dev
```

Notes: The repo already contains a minimal scaffold (`pages`, `styles`, and Tailwind/PostCSS configs). Run the `npm install` commands above to populate `node_modules` and then `npm run dev`.
