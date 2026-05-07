import { redirect } from "next/navigation";
import { promises as fs } from "fs";
import path from "path";

export const dynamic = "force-static";

const SLUG_RE = /^\d{4}-\d{2}-\d{2}$/;
const OUTPUTS_DIR = path.join(process.cwd(), "outputs");
const LATEST_JSON = path.join(process.cwd(), "public", "daily", "latest.json");

async function resolveLatestSlug(): Promise<string | null> {
  try {
    const raw = await fs.readFile(LATEST_JSON, "utf8");
    const parsed = JSON.parse(raw) as { slug?: string; date?: string };
    const candidate = parsed.slug || parsed.date;
    if (candidate && SLUG_RE.test(candidate)) return candidate;
  } catch {
    // fall through to scan
  }
  try {
    const entries = await fs.readdir(OUTPUTS_DIR);
    const slugs = entries.filter((n) => SLUG_RE.test(n)).sort();
    return slugs.length ? slugs[slugs.length - 1] : null;
  } catch {
    return null;
  }
}

export default async function Home() {
  const slug = await resolveLatestSlug();
  if (slug) redirect(`/daily/${slug}`);

  return (
    <main className="min-h-screen bg-gray-50 flex items-center justify-center px-6">
      <div className="max-w-md text-center space-y-3">
        <p className="text-red-500 font-bold text-xl tracking-tight">
          REBEL <span className="text-gray-900">DIVIDENDS</span>
        </p>
        <p className="text-gray-600">
          No daily update is available yet. Check back soon.
        </p>
        <p className="text-sm text-gray-400">
          <a href="https://rebeldividends.com" className="text-red-500 hover:underline">
            rebeldividends.com
          </a>
        </p>
      </div>
    </main>
  );
}
