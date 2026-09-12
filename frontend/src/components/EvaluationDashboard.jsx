import { useState, useEffect } from "react";
import { Play, Loader2, CheckCircle2, XCircle, Target, Layers, Crosshair } from "lucide-react";
import { toast } from "sonner";
import { runEvaluation, getLatestEvaluation } from "../lib/api";
import { STATE_CONFIG } from "./stateConfig";

const pct = (v) => (v == null ? "—" : `${(v * 100).toFixed(1)}%`);

const MetricCard = ({ icon: Icon, label, value, sub, accent }) => (
  <div className="rounded-xl border border-[#23355C] bg-[#0F1A30] p-5">
    <div className="mb-3 flex items-center gap-2">
      <Icon size={16} style={{ color: accent }} />
      <span className="font-mono text-xs uppercase tracking-wider text-[#94A3B8]">{label}</span>
    </div>
    <div className="font-serif text-3xl font-semibold text-slate-100">{value}</div>
    {sub && <div className="mt-1 text-xs text-[#94A3B8]">{sub}</div>}
  </div>
);

export const EvaluationDashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    getLatestEvaluation().then((d) => {
      if (d?.metrics) setData(d);
    }).catch(() => {});
  }, []);

  const run = async () => {
    setLoading(true);
    try {
      const d = await runEvaluation();
      setData(d);
      toast.success(`Evaluation complete · ${pct(d.metrics.overall_accuracy)} overall accuracy`);
    } catch (e) {
      toast.error("Evaluation run failed. See backend logs.");
    } finally {
      setLoading(false);
    }
  };

  const m = data?.metrics;

  return (
    <div data-testid="evaluation-dashboard" className="space-y-6">
      <div className="flex flex-col items-start justify-between gap-4 rounded-2xl border border-[#23355C] bg-[#0F1A30]/80 p-6 sm:flex-row sm:items-center">
        <div>
          <h3 className="font-serif text-2xl font-medium text-slate-100">Evaluation Suite</h3>
          <p className="mt-1 max-w-xl text-sm text-[#94A3B8]">
            Runs a fixed set of 25 labelled questions through the live retrieval + reasoning pipeline and
            reports measured accuracy. Results are dynamic — never hardcoded.
          </p>
        </div>
        <button
          data-testid="run-evaluation-button"
          onClick={run}
          disabled={loading}
          className="flex shrink-0 items-center gap-2 rounded-xl bg-amber-400 px-6 py-3 font-semibold text-[#070C18] transition-all hover:bg-amber-300 active:scale-[0.98] disabled:opacity-60"
        >
          {loading ? <Loader2 size={18} className="animate-spin" /> : <Play size={18} />}
          {loading ? "Running 25 questions…" : "Run Evaluation"}
        </button>
      </div>

      {!m && !loading && (
        <div className="rounded-2xl border border-dashed border-[#23355C] py-16 text-center text-sm text-[#94A3B8]">
          No evaluation run yet. Click “Run Evaluation” to measure the system on 25 questions.
        </div>
      )}

      {loading && !m && (
        <div className="rounded-2xl border border-[#23355C] bg-[#0F1A30] py-16 text-center">
          <Loader2 size={26} className="mx-auto mb-3 animate-spin text-amber-400" />
          <p className="font-mono text-sm text-[#94A3B8]">Evaluating 25 questions against the live pipeline…</p>
        </div>
      )}

      {m && (
        <>
          <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
            <MetricCard icon={Target} label="Overall accuracy" value={pct(m.overall_accuracy)}
              sub={`${m.correct}/${m.total_questions} correct`} accent="#E2C372" />
            <MetricCard icon={Layers} label="Retrieval accuracy" value={pct(m.retrieval_accuracy)}
              sub={`measured on ${m.retrieval_measured_on} grounded Qs`} accent="#06B6D4" />
            <MetricCard icon={Crosshair} label="Citation accuracy" value={pct(m.citation_accuracy)}
              sub={`measured on ${m.citation_measured_on} grounded Qs`} accent="#10B981" />
            <MetricCard icon={Target} label="Edge-question accuracy" value={pct(m.edge_accuracy)}
              sub={`${m.edge_total} near-miss / hard Qs`} accent="#F59E0B" />
          </div>

          {/* Per-state breakdown */}
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            {["ANSWERABLE", "NOT_ANSWERABLE", "CONTRADICTORY"].map((st) => {
              const cfg = STATE_CONFIG[st];
              const s = m.by_state[st];
              return (
                <div key={st} data-testid={`state-metric-${st}`} className={`rounded-xl border-2 p-5 ${cfg.container}`}>
                  <div className="flex items-center gap-2">
                    <cfg.Icon size={16} style={{ color: cfg.accent }} />
                    <span className="font-mono text-xs uppercase tracking-wider">{cfg.label}</span>
                  </div>
                  <div className="mt-3 font-serif text-3xl font-semibold">{pct(s.accuracy)}</div>
                  <div className="mt-1 text-xs opacity-80">{s.correct}/{s.total} correct</div>
                </div>
              );
            })}
          </div>

          {/* Results table */}
          <div className="overflow-hidden rounded-2xl border border-[#23355C]">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="bg-[#0a1223] font-mono text-xs uppercase tracking-wider text-[#94A3B8]">
                  <tr>
                    <th className="px-4 py-3">#</th>
                    <th className="px-4 py-3">Question</th>
                    <th className="px-4 py-3">Expected</th>
                    <th className="px-4 py-3">Actual</th>
                    <th className="px-4 py-3">Rules</th>
                    <th className="px-4 py-3 text-center">Result</th>
                  </tr>
                </thead>
                <tbody>
                  {data.results.map((r) => {
                    const eCfg = STATE_CONFIG[r.expected_state] || STATE_CONFIG.ERROR;
                    const aCfg = STATE_CONFIG[r.actual_state] || STATE_CONFIG.ERROR;
                    return (
                      <tr key={r.id} data-testid={`eval-row-${r.id}`} className="border-t border-[#1a2947] hover:bg-[#0F1A30]/60">
                        <td className="px-4 py-3 font-mono text-xs text-[#4a5f8a]">{r.id}</td>
                        <td className="px-4 py-3 text-slate-200">
                          <div className="max-w-md">{r.question}</div>
                          {r.expected_rule_ids?.length > 0 && (
                            <div className="mt-1 font-mono text-[11px] text-[#4a5f8a]">
                              exp: {r.expected_rule_ids.join(", ")}
                            </div>
                          )}
                        </td>
                        <td className="px-4 py-3">
                          <span className={`rounded border px-2 py-0.5 font-mono text-[10px] ${eCfg.chip}`}>{eCfg.label}</span>
                        </td>
                        <td className="px-4 py-3">
                          <span className={`rounded border px-2 py-0.5 font-mono text-[10px] ${aCfg.chip}`}>{aCfg.label}</span>
                        </td>
                        <td className="px-4 py-3 font-mono text-[11px] text-cyan-300/80">
                          {r.cited_rule_ids?.join(", ") || "—"}
                        </td>
                        <td className="px-4 py-3 text-center">
                          {r.state_correct ? (
                            <CheckCircle2 size={18} className="mx-auto text-emerald-400" />
                          ) : (
                            <XCircle size={18} className="mx-auto text-rose-400" />
                          )}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
          <p className="text-center font-mono text-xs text-[#4a5f8a]">
            Run at {new Date(data.created_at).toLocaleString()} · claims are measured, not asserted
          </p>
        </>
      )}
    </div>
  );
};
