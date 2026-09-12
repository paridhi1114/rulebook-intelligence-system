import { useState, useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import { Search, BookOpen, AlertTriangle, ChevronRight } from "lucide-react";
import { getRulebook, getStats } from "../lib/api";

export const RulebookViewer = () => {
  const { data: rulebook, isLoading } = useQuery({ queryKey: ["rulebook"], queryFn: getRulebook });
  const { data: stats } = useQuery({ queryKey: ["stats"], queryFn: getStats });
  const [query, setQuery] = useState("");
  const [activeChapter, setActiveChapter] = useState(null);

  const conflictIds = useMemo(() => {
    const set = new Set();
    (stats?.contradictions || []).forEach((c) => c.rules.forEach((r) => set.add(r)));
    return set;
  }, [stats]);

  const chapters = rulebook?.chapters || [];

  const filtered = useMemo(() => {
    if (!query.trim()) return chapters;
    const q = query.toLowerCase();
    return chapters
      .map((ch) => ({
        ...ch,
        rules: ch.rules.filter(
          (r) =>
            r.rule_id.toLowerCase().includes(q) ||
            r.title.toLowerCase().includes(q) ||
            r.exact_text.toLowerCase().includes(q)
        ),
      }))
      .filter((ch) => ch.rules.length > 0);
  }, [chapters, query]);

  const shownChapters = activeChapter
    ? filtered.filter((c) => c.code === activeChapter)
    : filtered;

  if (isLoading) {
    return <div className="py-20 text-center font-mono text-sm text-[#94A3B8]">Loading rulebook…</div>;
  }

  return (
    <div data-testid="rulebook-source-viewer" className="grid grid-cols-1 gap-6 lg:grid-cols-[280px_1fr]">
      {/* Sidebar */}
      <aside className="space-y-2">
        <div className="relative mb-3">
          <Search size={16} className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-[#4a5f8a]" />
          <input
            data-testid="rulebook-search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search rules…"
            className="w-full rounded-lg border border-[#23355C] bg-[#0a1223] py-2.5 pl-9 pr-3 text-sm text-slate-100 outline-none focus:border-amber-500/50"
          />
        </div>
        <button
          onClick={() => setActiveChapter(null)}
          className={`flex w-full items-center justify-between rounded-lg px-3 py-2 text-left text-sm transition-colors ${
            !activeChapter ? "bg-amber-500/10 text-amber-300" : "text-slate-300 hover:bg-[#0F1A30]"
          }`}
        >
          All chapters
          <span className="font-mono text-xs text-[#4a5f8a]">{rulebook?.total_rules}</span>
        </button>
        {chapters.map((ch) => (
          <button
            key={ch.code}
            data-testid={`chapter-nav-${ch.code}`}
            onClick={() => setActiveChapter(ch.code)}
            className={`flex w-full items-center justify-between rounded-lg px-3 py-2 text-left text-sm transition-colors ${
              activeChapter === ch.code ? "bg-amber-500/10 text-amber-300" : "text-slate-300 hover:bg-[#0F1A30]"
            }`}
          >
            <span className="truncate">
              <span className="font-mono text-xs text-[#4a5f8a]">{ch.number}. </span>
              {ch.title}
            </span>
            <ChevronRight size={13} className="shrink-0 text-[#4a5f8a]" />
          </button>
        ))}
      </aside>

      {/* Rules */}
      <div className="space-y-8">
        {shownChapters.map((ch) => (
          <section key={ch.code} data-testid={`chapter-section-${ch.code}`}>
            <div className="mb-4 flex items-center gap-3 border-b border-[#23355C] pb-3">
              <BookOpen size={18} className="text-amber-400/80" />
              <h3 className="font-serif text-2xl font-medium text-slate-100">
                <span className="text-amber-400/70">Chapter {ch.number}</span> · {ch.title}
              </h3>
            </div>
            <div className="space-y-3">
              {ch.rules.map((r) => {
                const isConflict = conflictIds.has(r.rule_id);
                return (
                  <div
                    key={r.rule_id}
                    data-testid={`rule-${r.rule_id}`}
                    className={`rounded-xl border bg-[#0F1A30] p-5 transition-colors ${
                      isConflict ? "border-amber-500/40" : "border-[#23355C] hover:border-[#33477a]"
                    }`}
                  >
                    <div className="mb-2 flex flex-wrap items-center gap-2">
                      <span className="rounded-md border border-cyan-500/40 bg-cyan-500/10 px-2 py-0.5 font-mono text-xs font-semibold text-cyan-300">
                        {r.rule_id}
                      </span>
                      <span className="font-mono text-xs text-[#94A3B8]">{r.section}</span>
                      <span className="font-mono text-xs text-[#4a5f8a]">· {r.subsection}</span>
                      {isConflict && (
                        <span className="ml-auto flex items-center gap-1 rounded-md border border-amber-500/40 bg-amber-500/10 px-2 py-0.5 font-mono text-[10px] uppercase tracking-wider text-amber-300">
                          <AlertTriangle size={11} /> Conflict flag
                        </span>
                      )}
                    </div>
                    <h4 className="mb-1.5 font-serif text-lg text-slate-100">{r.title}</h4>
                    <p className="text-sm leading-relaxed text-slate-300">{r.exact_text}</p>
                  </div>
                );
              })}
            </div>
          </section>
        ))}
        {shownChapters.length === 0 && (
          <div className="py-16 text-center font-mono text-sm text-[#94A3B8]">No rules match “{query}”.</div>
        )}
      </div>
    </div>
  );
};
