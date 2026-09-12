import { FileText, ArrowRight } from "lucide-react";

export const EvidenceCard = ({ item, index }) => (
  <div
    data-testid={`evidence-card-${item.rule_id}`}
    className="group rounded-xl border border-[#23355C] bg-[#0F1A30] p-6 transition-all duration-200 hover:-translate-y-0.5 hover:border-amber-500/40"
    style={{ animationDelay: `${index * 60}ms` }}
  >
    <div className="mb-3 flex flex-wrap items-center gap-2">
      <span className="rounded-md border border-cyan-500/40 bg-cyan-500/10 px-2.5 py-1 font-mono text-xs font-semibold text-cyan-300">
        {item.rule_id}
      </span>
      <span className="text-xs text-[#94A3B8]">{item.chapter}</span>
      <ArrowRight size={12} className="text-[#4a5f8a]" />
      <span className="text-xs text-[#94A3B8]">{item.section}</span>
    </div>

    <h4 className="mb-2 font-serif text-lg font-medium text-slate-100">{item.title}</h4>

    <p className="mb-4 text-sm leading-relaxed text-slate-300">
      <span className="highlight-passage">{item.exact_text}</span>
    </p>

    {item.why && (
      <div className="flex gap-2 rounded-lg border border-[#23355C] bg-[#0a1223] p-3">
        <FileText size={15} className="mt-0.5 shrink-0 text-amber-400/80" />
        <p className="text-sm text-slate-300">
          <span className="font-mono text-xs uppercase tracking-wider text-amber-400/90">Relevance </span>
          {item.why}
        </p>
      </div>
    )}
  </div>
);
