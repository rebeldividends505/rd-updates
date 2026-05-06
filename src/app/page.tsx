export const dynamic = "force-static";
export const revalidate = 3600;

const UPDATE_DATE = "Wednesday, May 6, 2026";
const HYPE_PRICE = 43.0;
const RD_SHARE_PRICE = "0.00184";
const RD_DAY_CHANGE = "+1.07%";
const DAY_THEME = "replay"; // "forward" | "macro" | "webinar" | "replay"

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
          <span className="text-red-200 font-semibold">{RD_DAY_CHANGE} today</span>
          <span className="ml-auto text-red-200">106 consecutive weekly dividends</span>
        </div>
      </div>

      <div className="max-w-3xl mx-auto px-6 py-10 space-y-8">

        <div>
          <p className="text-red-600 font-semibold text-sm uppercase tracking-wide mb-1">Wednesday Update</p>
          <h1 className="text-3xl font-bold text-gray-900 leading-tight">
            Your RD Update for Wednesday — and Where We Go from Here
          </h1>
          <p className="text-gray-500 mt-2 text-sm">{UPDATE_DATE} · Rebel Dividends Daily Briefing</p>
        </div>

        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 space-y-5 text-gray-700 leading-relaxed">
          <p dangerouslySetInnerHTML={{__html: `Your shares are at <strong>$${RD_SHARE_PRICE}</strong> this morning, <strong>up ${RD_DAY_CHANGE} overnight</strong>. The underlying is HYPE, currently trading at <strong>$${HYPE_PRICE}</strong>. Clean follow-through after yesterday's session. Higher highs, higher lows, holding ground above the late-January breakout.`}} />
          <p dangerouslySetInnerHTML={{__html: `<strong style="color:#16a34a;">When HYPE breaks $60, your share price moves roughly 40% from here.</strong> That's the math of spot exposure. One-to-one with the underlying. No leverage. No leaks. When HYPE moves, you move.`}} />
          <p dangerouslySetInnerHTML={{__html: `$60 takes HYPE back to its September 2025 all-time high — a price it already proved it could reach and hold. The technical setup is clean. The buyback flywheel is mechanical. The track record is 106 consecutive weekly dividends since the April 2024 pivot, every 2026 distribution classified as Return of Capital under IRC §301(c)(2).`}} />
          <p dangerouslySetInnerHTML={{__html: `<strong style="color:#dc2626;">$60 is the first stop. $150 is the thesis.</strong> If you missed yesterday's webinar, the replay covers the full macro picture: six macro forces aligning, the buyback math, and a signal from Hyperliquid's own documentation that nobody else is talking about.`}} />
        </div>

        <div className="bg-amber-50 border border-amber-200 rounded-xl p-5">
          <p className="text-amber-800 font-semibold mb-1">Your RD share price today: <strong>${RD_SHARE_PRICE}</strong> ({RD_DAY_CHANGE})</p>
          <p className="text-amber-700 text-sm">
            Based on HYPE at ${HYPE_PRICE}. Dividends paid every Monday. <a href="https://portal.rebeldividends.com" className="underline">View your portal →</a>
          </p>
        </div>

        <div className="bg-gray-900 rounded-2xl p-8 text-center text-white">
          <p className="text-gray-400 text-sm uppercase tracking-wide mb-3">Missed Yesterday?</p>
          <h2 className="text-2xl font-bold mb-2">Watch the Webinar Replay</h2>
          <p className="text-gray-400 text-sm mb-5">Macro forces, buyback flywheel, the Hyperliquid signal, and the full $150 thesis.</p>
          <a
            href="https://www.rebeldividends.com/startwebinar/"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block bg-green-700 hover:bg-green-800 text-white font-bold px-8 py-3 rounded-xl transition-colors text-lg"
          >
            Watch the Replay →
          </a>
        </div>

        <div className="grid grid-cols-3 gap-4">
          {[
            { label: "HYPE Price", value: `$${HYPE_PRICE}` },
            { label: "RD Share Price", value: `$${RD_SHARE_PRICE}` },
            { label: "Consecutive Dividends", value: "106" },
          ].map((stat) => (
            <div key={stat.label} className="bg-white border border-gray-100 rounded-xl p-5 text-center shadow-sm">
              <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
              <p className="text-gray-500 text-xs mt-1">{stat.label}</p>
            </div>
          ))}
        </div>

        <div className="border-t border-gray-200 pt-6 text-center text-xs text-gray-400 space-y-2">
          <p>
            <a href="https://rebeldividends.com" className="text-red-500 hover:underline">rebeldividends.com</a>
            {" · "}
            <a href="https://portal.rebeldividends.com" className="text-red-500 hover:underline">Investor Portal</a>
          </p>
          <p>© 2026 Rebel Dividends Inc. · Daily updates by Jason Cox</p>
          <p className="text-gray-300">This is not financial advice. Past performance does not guarantee future results.</p>
        </div>
      </div>
    </main>
  );
}
