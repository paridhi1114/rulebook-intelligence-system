import { Scale } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { getStats } from "../lib/api";

const TABS = [
  { id: "ask", label: "Ask Intelligence" },
  { id: "browse", label: "Browse Rulebook" },
  { id: "evaluate", label: "Accuracy Evaluation" },
];

export const Header = ({ tab, setTab }) => {
  const { data: stats } = useQuery({ queryKey: ["stats"], queryFn: getStats });

  return (
    <header className="sticky top-0 z-30 border-b border-[#23355C] bg-[#070C18]/85 backdrop-blur-md">
      <div className="mx-auto flex max-w-6xl flex-col gap-3 px-5 py-4 md:flex-row md:items-center md:justify-between">
        <div className="flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-lg border border-amber-500/40 bg-amber-500/10">
            <Scale size={22} className="text-amber-400" />
          </div>
          <div>
            <h1 className="font-serif text-xl font-semibold leading-none tracking-tight text-slate-100">
              The Rulebook That Argues With Itself
            </h1>
            <p className="mt-1 font-mono text-[11px] uppercase tracking-[0.2em] text-[#94A3B8]">
              {stats
                ? `${stats.total_words.toLocaleString()} words · ${stats.total_rules} rules · ${stats.total_chapters} chapters · ${stats.intentional_contradictions} known conflicts`
                : "Academic Regulations Intelligence"}
            </p>
          </div>
        </div>

        <nav className="flex gap-1 rounded-xl border border-[#23355C] bg-[#0F1A30] p-1">
          {TABS.map((t) => (
            <button
              key={t.id}
              data-testid={`tab-${t.id}`}
              onClick={() => setTab(t.id)}
              className={`rounded-lg px-4 py-2 text-sm font-medium transition-all duration-200 ${
                tab === t.id
                  ? "bg-amber-400 text-[#070C18]"
                  : "text-slate-300 hover:text-slate-100"
              }`}
            >
              {t.label}
            </button>
          ))}
        </nav>
      </div>
    </header>
  );
};
