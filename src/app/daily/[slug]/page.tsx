import { notFound } from "next/navigation";
import { promises as fs } from "fs";
import path from "path";

export const dynamicParams = false;

const SLUG_RE = /^\d{4}-\d{2}-\d{2}$/;
const OUTPUTS_DIR = path.join(process.cwd(), "outputs");

async function readElementor(slug: string): Promise<string | null> {
  try {
    return await fs.readFile(path.join(OUTPUTS_DIR, slug, "elementor.html"), "utf8");
  } catch {
    return null;
  }
}

async function readSubject(slug: string): Promise<string | null> {
  try {
    const text = await fs.readFile(path.join(OUTPUTS_DIR, slug, "sms.txt"), "utf8");
    const m = text.match(/^\s*SUBJECT:\s*(.+?)\s*$/m);
    return m ? m[1].trim() : null;
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
  const subject = await readSubject(slug);
  const dateLabel = formatDate(slug);
  const title = subject
    ? `${subject} — Rebel Dividends`
    : `Rebel Dividends — ${dateLabel}`;
  const description = subject ?? `Daily Rebel Dividends update for ${dateLabel}.`;
  return {
    title,
    description,
    openGraph: {
      title,
      description,
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

  const html = await readElementor(slug);
  if (!html) notFound();

  return (
    <main
      style={{
        minHeight: "100vh",
        background: "#ffffff",
        padding: "24px 20px 48px",
      }}
    >
      <div dangerouslySetInnerHTML={{ __html: html }} />
    </main>
  );
}
