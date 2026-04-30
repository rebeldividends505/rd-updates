export const dynamic = "force-static";
export const revalidate = 3600;

const UPDATE_DATE = "Thursday, April 30, 2026";
const HYPE_PRICE = 19.82; // update daily
const RD_SHARE_PRICE = (0.001776 * (HYPE_PRICE / 39.41)).toFixed(6);

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-gray-900 text-white">
        <div className="max-w-3xl mx-auto px-6 py-5 flex items-center justify-between">
          <div>
            <span className="text-red-500 font-bold text-xl tracking-tight">REBEL</span>
            <span className="text-white font-bold text-xl tracking-tight"> DIVIDENDS</span>
          </div>
          <div className="text-gray-400 text-sm">{UPDATE_DATE}</div>
        </div>
      </header>

      {/* Price ticker */}
      <div className="bg-red-600 text-white">
        <div className="max-w-3xl mx-auto px-6 py-2 flex gap-6 text-sm font-medium">
          <span>HYPE <strong>${HYPE_PRICE}</strong></span>
          <span>RD Share <strong>${RD_SHARE_PRICE}</strong></span>
          <span className="ml-auto text-red-200">Weekly dividends, paid every Friday</span>
        </div>
      </div>

      <div className="max-w-3xl mx-auto px-6 py-10 space-y-8">

        {/* Today's Update Header */}
        <div>
          <p className="text-red-600 font-semibold text-sm uppercase tracking-wide mb-1">Thursday Update</p>
          <h1 className="text-3xl font-bold text-gray-900 leading-tight">
            Hyperliquid Is Still the Most Important Trade of the Decade
          </h1>
          <p className="text-gray-500 mt-2 text-sm">{UPDATE_DATE} · Rebel Dividends Daily Briefing</p>
        </div>

        {/* Main content */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 space-y-5 text-gray-700 leading-relaxed">
          <p>
            While the rest of the market debates the next rate cut, Rebel Dividends investors are collecting weekly dividends — and watching HYPE build a case for a run to <strong>$150 or higher</strong>.
          </p>
          <p>
            This is not a speculative call. It&apos;s a structural one.
          </p>
          <p>
            Hyperliquid is the only DEX in history that has reached <strong>top-5 derivatives volume globally</strong> without a venture capital raise. No VC unlock. No whale dumping. Just organic growth from real traders who choose it over every centralized alternative.
          </p>
          <p>
            The thesis is simple: when a platform generates $300M+ in annualized real revenue, controls its own chain, and its token is still trading at a fraction of what comparable platforms command — the only question is timing.
          </p>
          <p>
            Our model puts HYPE at <strong>$150+ within 12 months</strong>. That&apos;s not a moonshot — that&apos;s a valuation re-rating.
          </p>

          <div className="bg-amber-50 border border-amber-200 rounded-xl p-5">
            <p className="text-amber-800 font-semibold mb-1">Meanwhile, RD investors don&apos;t just hold HYPE.</p>
            <p className="text-amber-700 text-sm">
              Every week, we distribute dividends back to investors. Today&apos;s RD share price sits at <strong>${RD_SHARE_PRICE}</strong>. That&apos;s real yield, paid every Friday, tied directly to HYPE&apos;s performance.
            </p>
          </div>

          <p>
            If you&apos;ve been sitting on the sidelines, today&apos;s update is a simple one: <strong>the window is still open.</strong>
          </p>
          <p>
            Read the full thesis, see the numbers, and decide for yourself.
          </p>
        </div>

        {/* CTA */}
        <div className="bg-gray-900 rounded-2xl p-8 text-center text-white">
          <p className="text-gray-400 text-sm uppercase tracking-wide mb-3">Featured This Week</p>
          <h2 className="text-2xl font-bold mb-2">How Hyperliquid Hits $150 in 12 Months or Less</h2>
          <p className="text-gray-400 mb-6">The full breakdown of our thesis, the math, and what it means for your dividend income.</p>
          <a
            href="https://rebeldividends.com/forward/"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block bg-red-600 hover:bg-red-700 text-white font-bold px-8 py-3 rounded-xl transition-colors text-lg"
          >
            Read the Full Breakdown →
          </a>
        </div>

        {/* Quick stats */}
        <div className="grid grid-cols-3 gap-4">
          {[
            { label: "HYPE Price", value: `$${HYPE_PRICE}` },
            { label: "RD Share Price", value: `$${RD_SHARE_PRICE}` },
            { label: "Dividend Day", value: "Every Friday" },
          ].map((stat) => (
            <div key={stat.label} className="bg-white border border-gray-100 rounded-xl p-5 text-center shadow-sm">
              <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
              <p className="text-gray-500 text-xs mt-1">{stat.label}</p>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="border-t border-gray-200 pt-6 text-center text-xs text-gray-400 space-y-2">
          <p>
            <a href="https://rebeldividends.com" className="text-red-500 hover:underline">rebeldividends.com</a>
            {" · "}
            <a href="https://portal.rebeldividends.com" className="text-red-500 hover:underline">Investor Portal</a>
          </p>
          <p>© 2026 Rebel Dividends Inc. · Daily updates by Jason Cox</p>
          <p className="text-gray-300">
            This is not financial advice. Past performance does not guarantee future results.
          </p>
        </div>
      </div>
    </main>
  );
}
