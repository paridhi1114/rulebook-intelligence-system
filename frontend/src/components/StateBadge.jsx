import { STATE_CONFIG } from "./stateConfig";

export const StateBadge = ({ state }) => {
  const cfg = STATE_CONFIG[state] || STATE_CONFIG.ERROR;
  const { Icon } = cfg;
  return (
    <div
      data-testid="state-classification-badge"
      data-state={state}
      className={`relative flex items-center gap-5 rounded-xl border-2 px-6 py-5 ${cfg.container} ${cfg.glow} animate-fade-up`}
    >
      <div
        className="flex h-14 w-14 shrink-0 items-center justify-center rounded-lg border"
        style={{ borderColor: cfg.accent, background: `${cfg.accent}18` }}
      >
        <Icon size={30} style={{ color: cfg.accent }} strokeWidth={2.2} />
      </div>
      <div className="min-w-0">
        <div className="font-mono text-xs uppercase tracking-[0.25em] opacity-80">Classification</div>
        <div className="font-serif text-2xl sm:text-3xl font-semibold leading-tight tracking-tight">
          {cfg.label}
        </div>
        <div className="text-sm opacity-90">{cfg.sub}</div>
      </div>
    </div>
  );
};
