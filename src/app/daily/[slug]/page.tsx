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
        background: "#f4f6f8",
        padding: "24px 20px 48px",
      }}
    >
      <style>{`
        /* === Daily update wrapper overrides ===
           The embedded HTML is an email template (680px max). On desktop
           we widen it to 1000px so charts render at near-native size; on
           mobile we force every fixed-width <td>/<table> to fit viewport. */
        .rd-daily-wrap { display: flex; justify-content: center; }
        .rd-daily-card {
          width: 100%;
          max-width: 1000px;
          background: #ffffff;
          border-radius: 10px;
          box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 12px 32px rgba(15,23,42,0.08);
          overflow: hidden;
        }
        .rd-daily-card, .rd-daily-card * { box-sizing: border-box; }
        .rd-daily-card img { max-width: 100% !important; height: auto !important; }
        .rd-daily-card table { max-width: 100% !important; }
        .rd-daily-card .rd-container { max-width: 1000px !important; width: 100% !important; }
        .rd-daily-card .rd-container img { max-width: 100% !important; }
        @media screen and (max-width: 720px) {
          .rd-daily-card { border-radius: 6px; box-shadow: 0 1px 2px rgba(0,0,0,0.06); }
          .rd-daily-card table { table-layout: fixed !important; width: 100% !important; max-width: 100% !important; }
          .rd-daily-card td, .rd-daily-card th {
            width: auto !important; max-width: 100% !important;
            word-wrap: break-word; overflow-wrap: break-word;
          }
          .rd-daily-card img {
            width: 100% !important; max-width: 100% !important; height: auto !important;
          }
          .rd-daily-card .rd-container { padding: 0 !important; }
          .rd-daily-card .rd-stat-cell { width: 100% !important; display: block !important; padding: 8px 12px !important; }
          .rd-daily-card .rd-milestone { font-size: 64px !important; }
        }
      `}</style>
      <div className="rd-daily-wrap">
        <div className="rd-daily-card" dangerouslySetInnerHTML={{ __html: html }} />
      </div>
    </main>
  );
}
