import { AlertTriangle, Zap } from "lucide-react";

const clauseLabels = ["A", "B", "C", "D"];

export const ConflictCards = ({ conflict, groupIndex = 0 }) => {
  const passages = conflict.passages || [];
  return (
    <div data-testid="conflict-group" className="rounded-xl border border-amber-500/30 bg-amber-950/20 p-5">
      <div className="mb-4 flex items-start gap-2">
        <Zap size={16} className="mt-0.5 shrink-0 text-amber-400" />
        <p className="text-sm text-amber-200/90">
          <span className="font-mono text-xs uppercase tracking-wider text-amber-400">Nature of conflict </span>
          {conflict.nature}
        </p>
      </div>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        {passages.map((p, i) => (
          <div
            key={p.rule_id}
            data-testid={`conflict-card-${p.rule_id}`}
            className="relative rounded-xl border border-amber-500/50 bg-[#140f04] p-5"
          >
            <div className="mb-3 flex items-center justify-between">
              <span className="flex h-7 w-7 items-center justify-center rounded-md border border-amber-500/60 bg-amber-500/15 font-serif text-sm font-semibold text-amber-300">
                {clauseLabels[i] || i + 1}
              </span>
              <span className="rounded-md border border-amber-500/40 bg-amber-500/10 px-2.5 py-1 font-mono text-xs font-semibold text-amber-300">
                {p.rule_id}
              </span>
            </div>
            <div className="mb-2 font-mono text-xs text-[#94A3B8]">
              {p.chapter} · {p.section}
            </div>
            <h4 className="mb-2 font-serif text-base font-medium text-slate-100">{p.title}</h4>
            <p className="text-sm leading-relaxed text-slate-300">"{p.exact_text}"</p>
          </div>
        ))}
      </div>

      {passages.length >= 2 && (
        <div className="mt-4 flex items-center justify-center gap-2 text-xs text-amber-400/80">
          <AlertTriangle size={13} />
          <span className="font-mono uppercase tracking-wider">
            {passages.map((p) => p.rule_id).join("  ⚔  ")} govern the same matter but disagree
          </span>
        </div>
      )}
    </div>
  );
};
