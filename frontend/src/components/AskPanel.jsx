import { useState } from "react";
import { Search, Loader2, ScrollText, Sparkles, ChevronDown, ChevronUp } from "lucide-react";
import { toast } from "sonner";
import { ask } from "../lib/api";
import { StateBadge } from "./StateBadge";
import { EvidenceCard } from "./EvidenceCard";
import { ConflictCards } from "./ConflictCards";

const EXAMPLES = [
  { q: "What minimum attendance percentage do I need to sit the end-semester exam?", tag: "Likely conflict" },
  { q: "How many days of medical leave am I entitled to in a semester?", tag: "Likely conflict" },
  { q: "What is the maximum number of transfer credits I can bring toward my degree?", tag: "Answerable" },
  { q: "Does the university provide health insurance coverage to students?", tag: "Not answerable" },
];

export const AskPanel = () => {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [showRetrieved, setShowRetrieved] = useState(false);

  const submit = async (q) => {
    const query = (q ?? question).trim();
    if (!query) {
      toast.error("Please enter a question about the rulebook.");
      return;
    }
    setQuestion(query);
    setLoading(true);
    setResult(null);
    setShowRetrieved(false);
    try {
      const data = await ask(query);
      setResult(data);
    } catch (e) {
      toast.error(e?.response?.data?.detail || "Something went wrong while querying the rulebook.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto max-w-5xl space-y-8">
      {/* Input */}
      <form
        data-testid="question-input-form"
        onSubmit={(e) => {
          e.preventDefault();
          submit();
        }}
        className="rounded-2xl border border-[#23355C] bg-[#0F1A30]/80 p-6 md:p-8"
      >
        <label className="mb-3 block font-mono text-xs uppercase tracking-[0.25em] text-amber-400/90">
          Ask the rulebook
        </label>
        <div className="flex flex-col gap-3 sm:flex-row">
          <div className="relative flex-1">
            <Search size={18} className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-[#4a5f8a]" />
            <input
              data-testid="question-input"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="e.g. How many times can I attempt a supplementary exam?"
              className="w-full rounded-xl border border-[#23355C] bg-[#0a1223] py-4 pl-11 pr-4 text-slate-100 placeholder:text-[#4a5f8a] outline-none transition-colors focus:border-amber-500/60"
            />
          </div>
          <button
            data-testid="ask-button"
            type="submit"
            disabled={loading}
            className="flex items-center justify-center gap-2 rounded-xl bg-amber-400 px-7 py-4 font-semibold text-[#070C18] transition-all duration-150 hover:bg-amber-300 active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-60"
          >
            {loading ? <Loader2 size={18} className="animate-spin" /> : <Sparkles size={18} />}
            {loading ? "Analysing" : "Ask Rulebook"}
          </button>
        </div>

        <div className="mt-5 flex flex-wrap gap-2">
          {EXAMPLES.map((ex) => (
            <button
              key={ex.q}
              type="button"
              data-testid="example-question"
              onClick={() => submit(ex.q)}
              disabled={loading}
              className="group flex max-w-full items-center gap-2 rounded-full border border-[#23355C] bg-[#0a1223] px-3.5 py-1.5 text-left text-xs text-slate-300 transition-all hover:border-amber-500/40 hover:text-slate-100 disabled:opacity-50"
            >
              <span className="min-w-0 max-w-[180px] truncate sm:max-w-[280px]">{ex.q}</span>
              <span className="shrink-0 font-mono text-[10px] uppercase tracking-wider text-[#4a5f8a]">{ex.tag}</span>
            </button>
          ))}
        </div>
      </form>

      {/* Loading */}
      {loading && (
        <div className="relative overflow-hidden rounded-2xl border border-[#23355C] bg-[#0F1A30] p-10 text-center">
          <div className="scanline" />
          <ScrollText size={30} className="mx-auto mb-4 animate-pulse text-amber-400/80" />
          <p className="font-serif text-lg text-slate-200">Scanning the rulebook…</p>
          <p className="mt-1 font-mono text-xs text-[#94A3B8]">
            Hybrid retrieval across 101 rules · Gemini grounded reasoning
          </p>
        </div>
      )}

      {/* Result */}
      {result && !loading && (
        <div data-testid="result-panel" className="space-y-6">
          <StateBadge state={result.state} />

          {/* Answer / explanation */}
          <div className="rounded-2xl border border-[#23355C] bg-[#0F1A30] p-6 md:p-8 animate-fade-up">
            <h3 className="mb-2 font-mono text-xs uppercase tracking-[0.25em] text-amber-400/90">
              {result.state === "NOT_ANSWERABLE" ? "Determination" : "Answer"}
            </h3>
            <p data-testid="answer-text" className="mb-5 font-serif text-xl leading-snug text-slate-100">
              {result.answer}
            </p>
            {result.explanation && (
              <p className="text-sm leading-relaxed text-slate-300">{result.explanation}</p>
            )}
            {result.state === "NOT_ANSWERABLE" && result.missing_information && (
              <div className="mt-4 rounded-lg border border-rose-500/30 bg-rose-950/30 p-4">
                <span className="font-mono text-xs uppercase tracking-wider text-rose-300">Missing information </span>
                <span className="text-sm text-rose-100/90">{result.missing_information}</span>
              </div>
            )}
          </div>

          {/* Conflicts */}
          {result.conflicts?.length > 0 && (
            <div data-testid="conflict-cards-container" className="space-y-4">
              <h3 className="font-serif text-2xl font-medium text-amber-300">Conflicting provisions</h3>
              {result.conflicts.map((c, i) => (
                <ConflictCards key={i} conflict={c} groupIndex={i} />
              ))}
            </div>
          )}

          {/* Evidence */}
          {result.evidence?.length > 0 && (
            <div data-testid="evidence-cards-container" className="space-y-4">
              <h3 className="font-serif text-2xl font-medium text-slate-100">
                {result.state === "CONTRADICTORY" ? "Cited passages" : "Supporting evidence"}
              </h3>
              <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
                {result.evidence.map((e, i) => (
                  <EvidenceCard key={e.rule_id + i} item={e} index={i} />
                ))}
              </div>
            </div>
          )}

          {/* Retrieved passages (transparency) */}
          {result.retrieved?.length > 0 && (
            <div className="rounded-2xl border border-[#23355C] bg-[#0a1223] p-5">
              <button
                data-testid="toggle-retrieved"
                onClick={() => setShowRetrieved((s) => !s)}
                className="flex w-full items-center justify-between text-left"
              >
                <span className="font-mono text-xs uppercase tracking-[0.2em] text-[#94A3B8]">
                  Retrieval trace · {result.retrieved.length} passages · model {result.model}
                </span>
                {showRetrieved ? <ChevronUp size={16} className="text-[#94A3B8]" /> : <ChevronDown size={16} className="text-[#94A3B8]" />}
              </button>
              {showRetrieved && (
                <div className="mt-4 space-y-2">
                  {result.retrieved.map((p) => (
                    <div key={p.rule_id} className="flex items-center gap-3 rounded-lg border border-[#1a2947] bg-[#0F1A30] px-3 py-2 text-xs">
                      <span className="font-mono font-semibold text-cyan-300">{p.rule_id}</span>
                      <span className="flex-1 truncate text-slate-300">{p.title}</span>
                      <span className="font-mono text-[#4a5f8a]">
                        fused {p.scores.fused} · bm25 {p.scores.bm25} · vec {p.scores.vector}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
