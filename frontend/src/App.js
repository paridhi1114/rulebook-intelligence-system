import { useState } from "react";
import "@/App.css";
import { Toaster } from "sonner";
import { Header } from "@/components/Header";
import { AskPanel } from "@/components/AskPanel";
import { RulebookViewer } from "@/components/RulebookViewer";
import { EvaluationDashboard } from "@/components/EvaluationDashboard";

function App() {
  const [tab, setTab] = useState("ask");

  return (
    <div className="App ink-backdrop grain min-h-screen">
      <Toaster position="top-right" theme="dark" richColors />
      <Header tab={tab} setTab={setTab} />

      <main className="relative z-10 mx-auto max-w-6xl px-5 py-10">
        {tab === "ask" && (
          <>
            <section className="mb-10 text-center">
              <p className="mb-3 font-mono text-xs uppercase tracking-[0.3em] text-amber-400/90">
                Grounded regulatory reasoning
              </p>
              <h2 className="mx-auto max-w-3xl font-serif text-4xl font-semibold leading-tight tracking-tight text-slate-100 sm:text-5xl">
                Ask a question. Get a grounded verdict, not a guess.
              </h2>
              <p className="mx-auto mt-4 max-w-2xl text-base leading-relaxed text-[#94A3B8]">
                Every response is one of three states — <span className="text-emerald-400">Answerable</span>,{" "}
                <span className="text-rose-400">Not Answerable</span>, or{" "}
                <span className="text-amber-400">Contradictory</span> — with the exact rulebook passages it relied on.
              </p>
            </section>
            <AskPanel />
          </>
        )}

        {tab === "browse" && <RulebookViewer />}
        {tab === "evaluate" && <EvaluationDashboard />}
      </main>

      <footer className="relative z-10 border-t border-[#23355C] py-6 text-center">
        <p className="font-mono text-xs text-[#4a5f8a]">
          Hybrid retrieval (BM25 + Gemini / semantic embeddings) · Gemini reasoning · answers grounded in retrieved passages only
        </p>
      </footer>
    </div>
  );
}

export default App;
