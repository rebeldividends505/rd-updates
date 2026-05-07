import { notFound } from "next/navigation";
import { promises as fs } from "fs";
import path from "path";

export const dynamicParams = false;

const SLUG_RE = /^\d{4}-\d{2}-\d{2}$/;
const OUTPUTS_DIR = path.join(process.cwd(), "outputs");

const CAPTION_OVERRIDES: Array<{ match: string; caption: string }> = [
  { match: "btc-vs-m2-chart.png", caption: "BTC vs Global M2 Money Supply — Largest Gap on Record" },
  { match: "buyback-flywheel.png", caption: "Hyperliquid Buyback Flywheel — $1.3B burned, 97% of fees to holders" },
  { match: "hype-airdrop-history-chart.png", caption: "Last Airdrop: HYPE went from $4 to $35 in 23 days" },
  { match: "projection-chart.png", caption: "$100K invested at the April 2024 pivot → $277K today (reinvestor)" },
  { match: "reinvestor-chart-may06.png", caption: "Your RD investment since the April 2024 pivot" },
  { match: "reinvestor-chart-", caption: "Your RD investment since the April 2024 pivot" },
];

function captionFor(src: string, alt: string): string {
  for (const { match, caption } of CAPTION_OVERRIDES) {
    if (src.includes(match)) return caption;
  }
  return alt;
}

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

// ---------- Email parser ----------

type Block =
  | { kind: "banner"; eyebrow: string; subhead: string; tone: "red" | "green" }
  | { kind: "h2"; text: string; lead: string[] }
  | { kind: "section"; eyebrow: string; subhead: string; paragraphs: string[]; tone: "red" | "green" | "amber" | "gray" }
  | { kind: "image"; src: string; alt: string }
  | { kind: "callout"; eyebrow: string; subhead: string; paragraphs: string[]; tone: "red" | "green" }
  | { kind: "cta"; href: string; text: string }
  | { kind: "questions"; html: string }
  | { kind: "byline" }
  | { kind: "disclaimers"; paragraphs: string[] };

function decodeEntities(s: string): string {
  return s
    .replace(/&nbsp;/g, " ")
    .replace(/&sect;/g, "§")
    .replace(/&rarr;/g, "→")
    .replace(/&mdash;/g, "—")
    .replace(/&ndash;/g, "–")
    .replace(/&ldquo;/g, "“")
    .replace(/&rdquo;/g, "”")
    .replace(/&lsquo;/g, "‘")
    .replace(/&rsquo;/g, "’")
    .replace(/&hellip;/g, "…")
    .replace(/&amp;/g, "&");
}

function stripTags(html: string): string {
  return decodeEntities(html.replace(/<[^>]+>/g, "").replace(/\s+/g, " ").trim());
}

function cleanInlineHtml(html: string): string {
  // Keep <strong>, <em>, <a> tags but strip their inline styles. Drop <br>.
  let out = html
    .replace(/<br\s*\/?>/gi, " ")
    .replace(/<strong\s+style="[^"]*"\s*>/gi, "<strong>")
    .replace(/<em\s+style="[^"]*"\s*>/gi, "<em>")
    .replace(/<a\s+([^>]+)>/gi, (_m, attrs: string) => {
      const href = attrs.match(/href="([^"]+)"/)?.[1];
      return href ? `<a href="${href}">` : "<a>";
    });
  out = decodeEntities(out).replace(/\s+/g, " ").trim();
  return out;
}

function getOuterTableContent(html: string): string {
  const start = html.indexOf("<table");
  if (start < 0) return "";
  const tagEnd = html.indexOf(">", start);
  if (tagEnd < 0) return "";
  let depth = 1;
  let i = tagEnd + 1;
  while (i < html.length) {
    if (html.startsWith("<table", i)) {
      depth++;
      const end = html.indexOf(">", i);
      i = end < 0 ? html.length : end + 1;
    } else if (html.startsWith("</table>", i)) {
      depth--;
      if (depth === 0) return html.substring(tagEnd + 1, i);
      i += "</table>".length;
    } else {
      i++;
    }
  }
  return html.substring(tagEnd + 1);
}

function topLevelRows(outerContent: string): string[] {
  const rows: string[] = [];
  let i = 0;
  let depth = 0;
  let trStart = -1;
  while (i < outerContent.length) {
    if (outerContent.startsWith("<table", i)) {
      depth++;
      const end = outerContent.indexOf(">", i);
      i = end < 0 ? outerContent.length : end + 1;
    } else if (outerContent.startsWith("</table>", i)) {
      depth--;
      i += "</table>".length;
    } else if (depth === 0 && outerContent.startsWith("<tr", i)) {
      if (trStart < 0) trStart = i;
      const end = outerContent.indexOf(">", i);
      i = end < 0 ? outerContent.length : end + 1;
    } else if (depth === 0 && outerContent.startsWith("</tr>", i) && trStart >= 0) {
      const rowEnd = i + "</tr>".length;
      rows.push(outerContent.substring(trStart, rowEnd));
      trStart = -1;
      i = rowEnd;
    } else {
      i++;
    }
  }
  return rows;
}

function findEyebrowText(row: string): { text: string; tone: "red" | "green" | "amber" | "gray" } | null {
  const re = /<div\s+style="([^"]*)"[^>]*>([\s\S]*?)<\/div>/g;
  for (const m of row.matchAll(re)) {
    const style = m[1];
    if (/letter-spacing:2px/.test(style) && /text-transform:uppercase/.test(style)) {
      const text = stripTags(m[2]);
      if (!text) continue;
      const color = (style.match(/color:(#[0-9a-fA-F]+)/)?.[1] ?? "").toLowerCase();
      let tone: "red" | "green" | "amber" | "gray" = "gray";
      if (color === "#c41e3a" || color === "#dc2626") tone = "red";
      else if (color === "#0a7c42" || color === "#16a34a") tone = "green";
      else if (color === "#92400e" || color === "#d97706") tone = "amber";
      return { text, tone };
    }
  }
  return null;
}

function findSubheadText(row: string): string | null {
  const re = /<div\s+style="([^"]*)"[^>]*>([\s\S]*?)<\/div>/g;
  for (const m of row.matchAll(re)) {
    const style = m[1];
    if (/font-size:(20|18)px/.test(style) && /font-weight:700/.test(style)) {
      const text = stripTags(m[2]);
      if (text) return text;
    }
  }
  return null;
}

function findContentParagraphs(row: string): string[] {
  const out: string[] = [];
  const re = /<p\s+style="([^"]*)"[^>]*>([\s\S]*?)<\/p>/g;
  for (const m of row.matchAll(re)) {
    const style = m[1];
    if (/font-size:12px/.test(style)) continue;
    const inner = m[2];
    const stripped = stripTags(inner);
    if (!stripped) continue;
    if (/^—\s*Jason Cox/.test(stripped)) continue;
    if (/^Questions\?/.test(stripped)) continue;
    out.push(cleanInlineHtml(inner));
  }
  return out;
}

function findDisclaimerParagraphs(row: string): string[] {
  const out: string[] = [];
  const re = /<p\s+style="([^"]*)"[^>]*>([\s\S]*?)<\/p>/g;
  for (const m of row.matchAll(re)) {
    if (/font-size:12px/.test(m[1])) {
      out.push(cleanInlineHtml(m[2]));
    }
  }
  return out;
}

function findFirstImage(row: string): { src: string; alt: string } | null {
  const m = row.match(/<img\s+([^>]+?)\/?>/);
  if (!m) return null;
  const src = m[1].match(/src="([^"]+)"/)?.[1];
  if (!src) return null;
  const alt = m[1].match(/alt="([^"]+)"/)?.[1] ?? "";
  return { src, alt };
}

function classifyRow(row: string): Block | null {
  // Skip pure spacer rows
  if (/height:\d+px/.test(row) && !/<h2|<p\s+style|<img|<a\s+href|letter-spacing:2px/.test(row)) {
    return null;
  }

  // Skip the email's own header row (uppercase "Rebel Dividends" + price)
  if (
    /text-transform:uppercase/.test(row) &&
    /Rebel Dividends/i.test(row) &&
    /\$0\.0/.test(row) &&
    !/<h2|<img|<p\s+style="[^"]*font-size:1[56]px/.test(row)
  ) {
    return null;
  }

  // Check for callout (nested table with border-left or border:2px solid)
  const nestedTableStyle = row.match(/<table[^>]*role="presentation"[^>]*style="([^"]*)"/);
  const nestedStyle = nestedTableStyle?.[1] ?? "";
  const isRedCallout = /border-left:6px solid #c41e3a/.test(nestedStyle) || /background:#fff4f4/.test(nestedStyle);
  const isGreenCallout = /border:2px solid #0a7c42/.test(nestedStyle) || /background:#f0fff4/.test(nestedStyle);

  // h2 row?
  const h2Match = row.match(/<h2[^>]*>([\s\S]*?)<\/h2>/);
  if (h2Match) {
    const h2Inner = h2Match[1];
    const aMatch = h2Inner.match(/<a[^>]*>([\s\S]*?)<\/a>/);
    const text = stripTags(aMatch ? aMatch[1] : h2Inner);
    const lead = findContentParagraphs(row);
    return { kind: "h2", text, lead };
  }

  if (isRedCallout || isGreenCallout) {
    const tone: "red" | "green" = isRedCallout ? "red" : "green";
    const eyebrow = findEyebrowText(row)?.text ?? "";
    const subhead = findSubheadText(row) ?? "";
    const paragraphs = findContentParagraphs(row);
    if (!eyebrow && !subhead && paragraphs.length === 0) return null;
    if (paragraphs.length === 0) {
      return { kind: "banner", eyebrow, subhead, tone };
    }
    return { kind: "callout", eyebrow, subhead, paragraphs, tone };
  }

  // CTA button row: green styled link
  const ctaMatch = row.match(/<a\s+href="([^"]+)"[^>]*background-color:#0a7c42[^>]*>([\s\S]*?)<\/a>/);
  if (ctaMatch && !/<h2|<img|<div\s+style="[^"]*letter-spacing:2px/.test(row)) {
    return { kind: "cta", href: ctaMatch[1], text: stripTags(ctaMatch[2]) };
  }

  // Questions box?
  if (/Questions\?/.test(row) && /background-color:#f8f8f8/.test(row)) {
    const pMatch = row.match(/<p[^>]*>([\s\S]*?)<\/p>/);
    return { kind: "questions", html: cleanInlineHtml(pMatch?.[1] ?? "") };
  }

  // Byline?
  if (/—\s*Jason Cox/.test(row)) {
    return { kind: "byline" };
  }

  // Disclaimers (12px paragraphs)
  if (/font-size:12px/.test(row)) {
    const paragraphs = findDisclaimerParagraphs(row);
    if (paragraphs.length > 0) {
      return { kind: "disclaimers", paragraphs };
    }
  }

  // Image-only row (no eyebrow / paragraph)
  const img = findFirstImage(row);
  if (img && !findEyebrowText(row) && findContentParagraphs(row).length === 0) {
    return { kind: "image", src: img.src, alt: img.alt };
  }

  // Section: eyebrow + subhead + paragraphs
  const eyebrow = findEyebrowText(row);
  const subhead = findSubheadText(row);
  const paragraphs = findContentParagraphs(row);
  if (eyebrow && (subhead || paragraphs.length > 0)) {
    return {
      kind: "section",
      eyebrow: eyebrow.text,
      subhead: subhead ?? "",
      paragraphs,
      tone: eyebrow.tone,
    };
  }

  return null;
}

function parseEmail(html: string): Block[] {
  const outer = getOuterTableContent(html);
  const rows = topLevelRows(outer);
  const blocks: Block[] = [];
  for (const row of rows) {
    const b = classifyRow(row);
    if (b) blocks.push(b);
  }
  return blocks;
}

// ---------- Render helpers ----------

function ParagraphHtml({ html, className = "" }: { html: string; className?: string }) {
  return (
    <p
      className={`text-[17px] sm:text-lg leading-[1.75] text-gray-800 ${className}`}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}

const eyebrowColorClass: Record<string, string> = {
  red: "text-red-600",
  green: "text-emerald-700",
  amber: "text-amber-700",
  gray: "text-gray-500",
};

function Eyebrow({ text, tone }: { text: string; tone: keyof typeof eyebrowColorClass }) {
  return (
    <p className={`text-[11px] tracking-[0.2em] font-bold uppercase ${eyebrowColorClass[tone] ?? "text-gray-500"} mb-2`}>
      {text}
    </p>
  );
}

function ImageCard({ src, alt }: { src: string; alt: string }) {
  const caption = captionFor(src, alt);
  return (
    <figure className="my-10">
      <div className="rounded-2xl shadow-lg ring-1 ring-gray-200 overflow-hidden bg-white">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src={src} alt={alt} className="block w-full h-auto" />
      </div>
      {caption && (
        <figcaption className="mt-3 text-sm text-gray-500 text-center px-4">
          {caption}
        </figcaption>
      )}
    </figure>
  );
}

// ---------- Page ----------

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

  const blocks = parseEmail(html);

  const banner = blocks.find((b) => b.kind === "banner") as Extract<Block, { kind: "banner" }> | undefined;
  const h2 = blocks.find((b) => b.kind === "h2") as Extract<Block, { kind: "h2" }> | undefined;
  const cta = blocks.find((b) => b.kind === "cta") as Extract<Block, { kind: "cta" }> | undefined;
  const questions = blocks.find((b) => b.kind === "questions") as Extract<Block, { kind: "questions" }> | undefined;
  const allDisclaimers = blocks
    .filter((b) => b.kind === "disclaimers")
    .flatMap((b) => (b as Extract<Block, { kind: "disclaimers" }>).paragraphs);

  // The body sequence: everything after h2 except cta/questions/byline/disclaimers/banner.
  const h2Idx = blocks.findIndex((b) => b.kind === "h2");
  const bodyBlocks = blocks
    .slice(h2Idx >= 0 ? h2Idx + 1 : 0)
    .filter(
      (b) =>
        b.kind !== "cta" &&
        b.kind !== "questions" &&
        b.kind !== "byline" &&
        b.kind !== "disclaimers" &&
        b.kind !== "banner" &&
        b.kind !== "h2",
    );

  const ctaHref = cta?.href ?? "https://www.rebeldividends.com/startwebinar/";
  const ctaText = cta?.text ?? "Watch the Webinar Replay →";

  return (
    <main className="min-h-screen bg-white">
      {/* Header */}
      <header className="bg-[#111827] text-white">
        <div className="max-w-[1100px] mx-auto px-6 h-16 flex items-center justify-between">
          <a href="/" className="block leading-none">
            <span className="text-red-500 font-extrabold text-2xl tracking-tight">REBEL</span>
            <span className="text-white font-extrabold text-2xl tracking-tight"> DIVIDENDS</span>
          </a>
          <div className="text-gray-300 text-sm hidden sm:block">{updateDate}</div>
        </div>
      </header>

      {/* Price strip */}
      <div className="bg-[#dc2626] text-white">
        <div className="max-w-[1100px] mx-auto px-6 py-2 flex flex-wrap gap-x-6 gap-y-1 text-sm font-medium">
          {sharePrice && (
            <span>
              RD <strong className="font-semibold">${sharePrice}</strong>
              {dayPct && (
                <span className="ml-1 text-red-100">({dayPct})</span>
              )}
            </span>
          )}
          {hypePrice && (
            <span>
              HYPE <strong className="font-semibold">${hypePrice}</strong>
            </span>
          )}
          {weekNum && (
            <span className="ml-auto">
              Week <strong className="font-semibold">{weekNum}</strong>
            </span>
          )}
        </div>
      </div>

      <div className="sm:hidden bg-gray-50 border-b border-gray-200 text-center py-2 text-xs text-gray-500">
        {updateDate}
      </div>

      {/* Hero */}
      <section className="max-w-[760px] mx-auto px-6 pt-12 pb-6">
        <p className="text-red-600 font-bold text-xs uppercase tracking-[0.2em] mb-4">Daily Briefing</p>
        {h2 && (
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-gray-900 leading-[1.15] tracking-tight mb-6">
            {h2.text}
          </h1>
        )}
        {h2 && h2.lead.length > 0 && (
          <div className="space-y-5">
            {h2.lead.map((p, i) => (
              <ParagraphHtml
                key={`lead-${i}`}
                html={p}
                className={i === 0 ? "text-gray-700 text-[18px] sm:text-[19px]" : ""}
              />
            ))}
          </div>
        )}
      </section>

      {/* Urgency banner */}
      {banner && (
        <section className="max-w-[760px] mx-auto px-6 my-2">
          <div
            className={
              banner.tone === "red"
                ? "border-l-4 border-red-600 bg-red-50 px-5 py-4 rounded-r-md"
                : "border-l-4 border-emerald-600 bg-emerald-50 px-5 py-4 rounded-r-md"
            }
          >
            {banner.eyebrow && (
              <p
                className={`text-[11px] tracking-[0.2em] font-bold uppercase mb-2 ${
                  banner.tone === "red" ? "text-red-600" : "text-emerald-700"
                }`}
              >
                {banner.eyebrow}
              </p>
            )}
            {banner.subhead && (
              <p className="text-lg sm:text-xl font-bold text-gray-900 leading-snug">{banner.subhead}</p>
            )}
          </div>
        </section>
      )}

      {/* Body */}
      <section className="max-w-[760px] mx-auto px-6 pt-6 pb-2">
        {bodyBlocks.map((b, idx) => {
          if (b.kind === "section") {
            return (
              <div key={`b-${idx}`} className="mt-10 first:mt-2">
                <Eyebrow text={b.eyebrow} tone={b.tone} />
                {b.subhead && (
                  <h2 className="text-2xl sm:text-3xl font-extrabold text-gray-900 leading-tight tracking-tight mb-4">
                    {b.subhead}
                  </h2>
                )}
                <div className="space-y-5">
                  {b.paragraphs.map((p, j) => (
                    <ParagraphHtml key={`p-${idx}-${j}`} html={p} />
                  ))}
                </div>
              </div>
            );
          }
          if (b.kind === "image") {
            return <ImageCard key={`b-${idx}`} src={b.src} alt={b.alt} />;
          }
          if (b.kind === "callout") {
            const isRed = b.tone === "red";
            return (
              <div
                key={`b-${idx}`}
                className={
                  isRed
                    ? "mt-10 border-l-4 border-red-600 bg-red-50 px-6 py-6 rounded-r-xl"
                    : "mt-10 border-2 border-emerald-600 bg-emerald-50 px-6 py-6 rounded-xl"
                }
              >
                {b.eyebrow && (
                  <p
                    className={`text-[11px] tracking-[0.2em] font-bold uppercase mb-2 ${
                      isRed ? "text-red-600" : "text-emerald-700"
                    }`}
                  >
                    {b.eyebrow}
                  </p>
                )}
                {b.subhead && (
                  <h3 className="text-xl sm:text-2xl font-bold text-gray-900 leading-tight mb-4">{b.subhead}</h3>
                )}
                <div className="space-y-4">
                  {b.paragraphs.map((p, j) => (
                    <ParagraphHtml
                      key={`callp-${idx}-${j}`}
                      html={p}
                      className="text-[16px] leading-[1.7]"
                    />
                  ))}
                </div>
              </div>
            );
          }
          return null;
        })}
      </section>

      {/* CTA */}
      <section className="max-w-[760px] mx-auto px-6 pt-10 pb-8">
        <a
          href={ctaHref}
          className="block sm:inline-block sm:mx-auto bg-[#16a34a] hover:bg-[#15803d] transition-colors text-white font-bold text-lg px-10 py-4 rounded-md text-center shadow-md w-full sm:w-auto"
          style={{ display: "block", textAlign: "center" }}
        >
          {ctaText}
        </a>
      </section>

      {/* Dean / Questions box */}
      <section className="max-w-[680px] mx-auto px-6 pb-10">
        <div className="border border-gray-300 rounded-xl bg-gray-50 px-6 py-6 text-center">
          <p className="text-base text-gray-700 leading-relaxed">
            {questions ? (
              <span dangerouslySetInnerHTML={{ __html: questions.html }} />
            ) : (
              <>
                <strong>Questions?</strong> Call Dean at{" "}
                <a href="tel:5053227515" className="text-red-600 font-semibold hover:underline">
                  505-322-7515
                </a>
                .
              </>
            )}
          </p>
        </div>
      </section>

      {/* Byline */}
      <section className="max-w-[760px] mx-auto px-6 pb-10">
        <p className="text-gray-700">
          — <strong>Jason Cox</strong>
          <br />
          <span className="text-sm text-gray-500">Rebel Dividends</span>
        </p>
      </section>

      {/* Footer + disclaimers */}
      <footer className="border-t border-gray-200 bg-gray-50">
        <div className="max-w-[760px] mx-auto px-6 py-8 space-y-4">
          {allDisclaimers.map((d, i) => (
            <p
              key={`disc-${i}`}
              className="text-xs text-gray-500 leading-relaxed"
              dangerouslySetInnerHTML={{ __html: d }}
            />
          ))}
          <div className="pt-4 border-t border-gray-200 text-center text-xs text-gray-400 space-y-2">
            <p>
              <a href="https://rebeldividends.com" className="text-red-600 hover:underline">
                rebeldividends.com
              </a>
              {" · "}
              <a href="https://portal.rebeldividends.com" className="text-red-600 hover:underline">
                Investor Portal
              </a>
            </p>
            <p>© 2026 Rebel Dividends Corporation · Daily updates by Jason Cox</p>
          </div>
        </div>
      </footer>
    </main>
  );
}
