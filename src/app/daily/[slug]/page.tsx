import { notFound } from "next/navigation";
import { promises as fs } from "fs";
import path from "path";

export const dynamicParams = false;

const SLUG_RE = /^\d{4}-\d{2}-\d{2}$/;
const OUTPUTS_DIR = path.join(process.cwd(), "outputs");

async function readDeployNotes(slug: string): Promise<Record<string, string>> {
  const notesPath = path.join(OUTPUTS_DIR, slug, "deploy-notes.md");
  let text: string;
  try {
    text = await fs.readFile(notesPath, "utf8");
  } catch {
    return {};
  }
  const patterns: Record<string, RegExp> = {
    hype_price: /\*\*HYPE:\*\*\s*\$?([\d.]+)/,
    share_price: /\*\*(?:RD\s+)?[Ss]hare\s+price:\*\*\s*\$?([\d.]+)/,
    day_pct: /\*\*[Dd]ay\s+over\s+[Dd]ay:\*\*\s*([+\-]?\d+\.?\d*%?)/,
    week_num: /\*\*[Ww]eek\s*#?:\*\*\s*(\d+)/,
  };
  const out: Record<string, string> = {};
  for (const [k, re] of Object.entries(patterns)) {
    const m = text.match(re);
    if (m) out[k] = m[1].trim();
  }
  return out;
}

async function readEmailHtml(slug: string): Promise<string | null> {
  const emailPath = path.join(OUTPUTS_DIR, slug, "email.html");
  try {
    return await fs.readFile(emailPath, "utf8");
  } catch {
    return null;
  }
}

export async function generateStaticParams() {
  let entries: string[];
  try {
    entries = await fs.readdir(OUTPUTS_DIR);
  } catch {
    return [];
  }
  const slugs: { slug: string }[] = [];
  for (const name of entries) {
    if (!SLUG_RE.test(name)) continue;
    try {
      const stat = await fs.stat(path.join(OUTPUTS_DIR, name));
      if (stat.isDirectory()) slugs.push({ slug: name });
    } catch {
      // ignore
    }
  }
  return slugs;
}

function formatDate(slug: string): string {
  const [y, m, d] = slug.split("-").map(Number);
  const dt = new Date(Date.UTC(y, m - 1, d));
  return dt.toLocaleDateString("en-US", {
    weekday: "long",
    month: "long",
    day: "numeric",
    year: "numeric",
    timeZone: "UTC",
  });
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  if (!SLUG_RE.test(slug)) return {};
  return {
    title: `Rebel Dividends — ${formatDate(slug)}`,
    description: `Daily Rebel Dividends update for ${formatDate(slug)}.`,
    openGraph: {
      title: `Rebel Dividends — ${formatDate(slug)}`,
      description: `Daily Rebel Dividends update for ${formatDate(slug)}.`,
      url: `https://updates.rebeldividends.com/daily/${slug}`,
      siteName: "Rebel Dividends",
    },
  };
}

export default async function DailyUpdate({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  if (!SLUG_RE.test(slug)) notFound();

  const html = await readEmailHtml(slug);
  if (!html) notFound();

  const notes = await readDeployNotes(slug);
  const updateDate = formatDate(slug);
  const hypePrice = notes.hype_price ?? null;
  const sharePrice = notes.share_price ?? null;
  const dayPct = notes.day_pct ?? null;
  const weekNum = notes.week_num ?? null;

  return (
    <main className="min-h-screen bg-gray-50">
      <header className="bg-gray-900 text-white">
        <div className="max-w-3xl mx-auto px-6 py-5 flex items-center justify-between">
          <a href="/" className="block">
            <span className="text-red-500 font-bold text-xl tracking-tight">REBEL</span>
            <span className="text-white font-bold text-xl tracking-tight"> DIVIDENDS</span>
          </a>
          <div className="text-gray-400 text-sm">{updateDate}</div>
        </div>
      </header>

      <div className="bg-red-600 text-white">
        <div className="max-w-3xl mx-auto px-6 py-2 flex flex-wrap gap-x-6 gap-y-1 text-sm font-medium">
          {hypePrice && (
            <span>
              HYPE <strong>${hypePrice}</strong>
            </span>
          )}
          {sharePrice && (
            <span>
              RD Share <strong>${sharePrice}</strong>
            </span>
          )}
          {dayPct && <span className="text-red-200 font-semibold">{dayPct} today</span>}
          {weekNum && (
            <span className="ml-auto text-red-200">
              {weekNum} consecutive weekly dividends
            </span>
          )}
        </div>
      </div>

      <div className="max-w-3xl mx-auto px-6 py-10 space-y-8">
        <div>
          <p className="text-red-600 font-semibold text-sm uppercase tracking-wide mb-1">
            Daily Update
          </p>
          <p className="text-gray-500 text-sm">
            {updateDate} · Rebel Dividends Daily Briefing
          </p>
        </div>

        <article
          className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden rd-email-content"
          dangerouslySetInnerHTML={{ __html: html }}
        />

        <div className="border-t border-gray-200 pt-6 text-center text-xs text-gray-400 space-y-2">
          <p>
            <a href="https://rebeldividends.com" className="text-red-500 hover:underline">
              rebeldividends.com
            </a>
            {" · "}
            <a
              href="https://portal.rebeldividends.com"
              className="text-red-500 hover:underline"
            >
              Investor Portal
            </a>
          </p>
          <p>© 2026 Rebel Dividends Inc. · Daily updates by Jason Cox</p>
          <p className="text-gray-300">
            This is not financial advice. Past performance does not guarantee future
            results.
          </p>
        </div>
      </div>
    </main>
  );
}
