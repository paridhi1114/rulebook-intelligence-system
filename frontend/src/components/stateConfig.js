import { CheckCircle2, HelpCircle, AlertTriangle } from "lucide-react";

export const STATE_CONFIG = {
  ANSWERABLE: {
    label: "ANSWERABLE",
    sub: "Grounded in the rulebook",
    Icon: CheckCircle2,
    accent: "#10B981",
    container: "bg-emerald-950/70 border-emerald-500/70 text-emerald-200",
    glow: "shadow-[0_0_40px_-8px_rgba(16,185,129,0.55)]",
    chip: "bg-emerald-500/15 text-emerald-300 border-emerald-500/40",
  },
  NOT_ANSWERABLE: {
    label: "NOT ANSWERABLE",
    sub: "Absent in the regulations",
    Icon: HelpCircle,
    accent: "#F43F5E",
    container: "bg-rose-950/70 border-rose-500/70 text-rose-200",
    glow: "shadow-[0_0_40px_-8px_rgba(244,63,94,0.5)]",
    chip: "bg-rose-500/15 text-rose-300 border-rose-500/40",
  },
  CONTRADICTORY: {
    label: "CONTRADICTORY",
    sub: "Regulatory conflict detected",
    Icon: AlertTriangle,
    accent: "#F59E0B",
    container: "bg-amber-950/70 border-amber-500/70 text-amber-200",
    glow: "shadow-[0_0_46px_-8px_rgba(245,158,11,0.6)]",
    chip: "bg-amber-500/15 text-amber-300 border-amber-500/40",
  },
  ERROR: {
    label: "ERROR",
    sub: "System error",
    Icon: AlertTriangle,
    accent: "#94A3B8",
    container: "bg-slate-800/70 border-slate-500/70 text-slate-200",
    glow: "",
    chip: "bg-slate-500/15 text-slate-300 border-slate-500/40",
  },
};
