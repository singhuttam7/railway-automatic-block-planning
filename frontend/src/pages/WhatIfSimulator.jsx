import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  BrainCircuit,
  CalendarDays,
  Clock3,
  Network,
  Sparkles,
  ShieldCheck,
  Zap,
  ArrowRight,
  Activity,
  CircleCheck,
  AlertTriangle,
  TrendingUp,
  ExternalLink,
} from "lucide-react";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const presets = [
  {
    title: "Corridor Unavailable",
    description: "Evaluate impact of corridor unavailability",
    icon: Network,
  },
  {
    title: "Extended Block",
    description: "Simulate a longer maintenance window",
    icon: Clock3,
  },
  {
    title: "High Priority Work",
    description: "Analyze critical maintenance priority",
    icon: AlertTriangle,
  },
];

function WhatIfSimulator() {
  const [corridor, setCorridor] = useState("");
  const [date, setDate] = useState("");
  const [duration, setDuration] = useState("");
  const [simulationStarted, setSimulationStarted] = useState(false);
  const [startTime, setStartTime] = useState("10:00");
  const [scenarioType, setScenarioType] = useState("");

  const [corridors, setCorridors] = useState([]);
  const [loadingCorridors, setLoadingCorridors] = useState(true);

  const [simulationResult, setSimulationResult] = useState(null);
  const [simulationLoading, setSimulationLoading] = useState(false);
  const [simulationError, setSimulationError] = useState("");

  useEffect(() => {
    fetch(`${API_URL}/api/corridors/`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Unable to load corridors");
        }

        return response.json();
      })
      .then((data) => {
        setCorridors(data);
      })
      .catch((error) => {
        console.error("Corridor loading error:", error);
      })
      .finally(() => {
        setLoadingCorridors(false);
      });
  }, []);

  const runSimulation = async () => {
    if (!scenarioType || !corridor || !date || !startTime || !duration) {
      return;
    }

    setSimulationStarted(false);
    setSimulationResult(null);
    setSimulationError("");
    setSimulationLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/what-if/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          corridor_id: corridor,
          unavailable_date: date,
          start_time: `${startTime}:00`,
          duration_hours: Number(duration),
          scenario_type: scenarioType,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Unable to run simulation");
      }

      setSimulationResult(data);
      setSimulationStarted(true);
    } catch (error) {
      console.error("What-If simulation error:", error);
      setSimulationError(error.message || "Unable to run simulation");
      setSimulationStarted(false);
    } finally {
      setSimulationLoading(false);
    }
  };

  return (
    <div className="min-h-full space-y-8 pb-10">
      {/* HERO */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="relative overflow-hidden rounded-3xl border border-indigo-400/10 bg-gradient-to-br from-indigo-500/[0.10] via-white/[0.035] to-cyan-400/[0.05] p-7 md:p-8"
      >
        <motion.div
          animate={{
            scale: [1, 1.15, 1],
            opacity: [0.15, 0.25, 0.15],
          }}
          transition={{
            duration: 5,
            repeat: Infinity,
            ease: "easeInOut",
          }}
          className="absolute -right-20 -top-20 h-56 w-56 rounded-full bg-indigo-500/20 blur-3xl"
        />

        <div className="relative flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-indigo-400/20 bg-indigo-400/10 px-3 py-1.5 text-[11px] font-medium text-indigo-300">
              <motion.span
                animate={{ opacity: [1, 0.4, 1] }}
                transition={{ duration: 1.8, repeat: Infinity }}
                className="h-1.5 w-1.5 rounded-full bg-emerald-400"
              />
              AI SIMULATION ENGINE ONLINE
            </div>

            <h1 className="text-3xl font-bold tracking-tight text-white md:text-4xl">
              What-If{" "}
              <span className="bg-gradient-to-r from-indigo-400 to-cyan-400 bg-clip-text text-transparent">
                Simulator
              </span>
            </h1>

            <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-400">
              Simulate operational constraints and evaluate how the intelligent
              block planning engine can adapt maintenance schedules,
              coordination, and asset availability.
            </p>
          </div>

          <motion.div
            animate={{ y: [0, -5, 0] }}
            transition={{ duration: 4, repeat: Infinity }}
            className="hidden rounded-2xl border border-indigo-400/20 bg-indigo-500/10 p-5 lg:block"
          >
            <BrainCircuit className="h-12 w-12 text-indigo-400" />
          </motion.div>
        </div>
      </motion.div>

      {/* AI PIPELINE */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1, duration: 0.5 }}
        className="rounded-2xl border border-white/10 bg-white/[0.035] p-5"
      >
        <div className="mb-5 flex items-center justify-between">
          <div>
            <h2 className="text-sm font-semibold text-white">
              Intelligent Planning Pipeline
            </h2>
            <p className="mt-1 text-xs text-slate-500">
              Scenario → AI Analysis → Optimization → Recommendation
            </p>
          </div>

          <Activity className="h-5 w-5 text-cyan-400" />
        </div>

        <div className="grid gap-3 md:grid-cols-4">
          {[
            ["01", "Scenario Input", "Define constraint"],
            ["02", "AI Analysis", "Assess impact"],
            ["03", "Optimization", "Find alternatives"],
            ["04", "Recommendation", "Best action"],
          ].map(([number, title, text], index) => (
            <motion.div
              key={title}
              whileHover={{ y: -3 }}
              transition={{ duration: 0.2 }}
              className="group rounded-xl border border-white/5 bg-slate-900/40 p-4 transition hover:border-indigo-400/20 hover:bg-indigo-500/[0.05]"
            >
              <div className="flex items-center gap-3">
                <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-500/10 text-[10px] font-bold text-indigo-400">
                  {number}
                </span>

                <div>
                  <p className="text-xs font-semibold text-slate-200">
                    {title}
                  </p>

                  <p className="mt-0.5 text-[10px] text-slate-500">{text}</p>
                </div>
              </div>

              {index < 3 && (
                <div className="mt-4 hidden h-px bg-gradient-to-r from-indigo-400/20 to-transparent md:block" />
              )}
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* PRESETS */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2, duration: 0.5 }}
      >
        <div className="mb-4">
          <h2 className="text-base font-semibold text-white">
            Scenario Templates
          </h2>

          <p className="mt-1 text-xs text-slate-500">
            Start with a predefined operational scenario.
          </p>
        </div>

        <div className="grid gap-4 md:grid-cols-3">
          {presets.map((preset, index) => {
            const Icon = preset.icon;

            return (
              <motion.button
                key={preset.title}
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.25 + index * 0.08 }}
                whileHover={{ y: -4, scale: 1.01 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => {
                  setScenarioType(preset.title);

                  if (preset.title === "Corridor Unavailable") {
                    setDuration("4");
                  }

                  if (preset.title === "Extended Block") {
                    setDuration("12");
                  }

                  if (preset.title === "High Priority Work") {
                    setDuration("2");
                  }
                }}
                className={`group rounded-2xl border p-5 text-left transition ${
                  scenarioType === preset.title
                    ? "border-indigo-400/40 bg-indigo-500/[0.10]"
                    : "border-white/10 bg-white/[0.035] hover:border-indigo-400/25 hover:bg-indigo-500/[0.06]"
                }`}
              >
                <div className="flex items-start justify-between">
                  <div
                    className={`rounded-xl p-3 transition ${
                      scenarioType === preset.title
                        ? "bg-indigo-500/20 text-indigo-300"
                        : "bg-indigo-500/10 text-indigo-400 group-hover:bg-indigo-500/20"
                    }`}
                  >
                    <Icon className="h-5 w-5" />
                  </div>

                  <ArrowRight
                    className={`h-4 w-4 transition ${
                      scenarioType === preset.title
                        ? "translate-x-1 text-indigo-400"
                        : "text-slate-600 group-hover:translate-x-1 group-hover:text-indigo-400"
                    }`}
                  />
                </div>

                <h3 className="mt-5 text-sm font-semibold text-white">
                  {preset.title}
                </h3>

                <p className="mt-1 text-xs leading-5 text-slate-500">
                  {preset.description}
                </p>

                {scenarioType === preset.title && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: "auto" }}
                    className="mt-4 flex items-center gap-2 text-[10px] font-medium text-indigo-300"
                  >
                    <CircleCheck className="h-3.5 w-3.5" />
                    Scenario selected
                  </motion.div>
                )}
              </motion.button>
            );
          })}
        </div>
      </motion.div>

      {/* SCENARIO CONFIGURATION */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.5 }}
        className="rounded-2xl border border-white/10 bg-white/[0.035] p-6 md:p-7"
      >
        <div className="flex items-start justify-between">
          <div>
            <div className="flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-indigo-400" />

              <h2 className="text-base font-semibold text-white">
                Configure Simulation
              </h2>
            </div>

            <p className="mt-1 text-xs text-slate-500">
              Define a hypothetical constraint for the planning engine.
            </p>
          </div>

          <div className="hidden rounded-xl bg-emerald-500/10 p-2.5 text-emerald-400 sm:block">
            <ShieldCheck className="h-5 w-5" />
          </div>
        </div>

        <div className="mt-7 grid gap-5 md:grid-cols-2 xl:grid-cols-4">
          {/* Corridor */}
          <div>
            <label className="mb-2 block text-xs font-medium text-slate-400">
              Corridor
            </label>

            <div className="relative">
              <Network className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" />

              <select
                value={corridor}
                onChange={(e) => setCorridor(e.target.value)}
                className="w-full appearance-none rounded-xl border border-white/10 bg-slate-900/70 py-3 pl-10 pr-4 text-sm text-white outline-none transition duration-300 hover:border-white/20 focus:border-indigo-400/50 focus:ring-2 focus:ring-indigo-500/10"
              >
                <option value="">Select corridor</option>

                {loadingCorridors ? (
                  <option value="">Loading corridors...</option>
                ) : (
                  corridors.map((item) => (
                    <option key={item.corridor_id} value={item.corridor_id}>
                      {item.corridor_id} — {item.corridor_name}
                    </option>
                  ))
                )}
              </select>
            </div>
          </div>

          {/* Date */}
          <div>
            <label className="mb-2 block text-xs font-medium text-slate-400">
              Unavailable Date
            </label>

            <div className="relative">
              <CalendarDays className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" />

              <input
                type="date"
                value={date}
                onChange={(e) => setDate(e.target.value)}
                className="w-full rounded-xl border border-white/10 bg-slate-900/70 py-3 pl-10 pr-4 text-sm text-white outline-none transition duration-300 hover:border-white/20 focus:border-indigo-400/50 focus:ring-2 focus:ring-indigo-500/10"
              />
            </div>
          </div>

          {/* Start Time */}
          <div>
            <label className="mb-2 block text-xs font-medium text-slate-400">
              Unavailable From
            </label>

            <div className="relative">
              <Clock3 className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" />

              <input
                type="time"
                value={startTime}
                onChange={(e) => setStartTime(e.target.value)}
                className="w-full rounded-xl border border-white/10 bg-slate-900/70 py-3 pl-10 pr-4 text-sm text-white outline-none transition duration-300 hover:border-white/20 focus:border-indigo-400/50 focus:ring-2 focus:ring-indigo-500/10"
              />
            </div>
          </div>

          {/* Duration */}
          <div>
            <label className="mb-2 block text-xs font-medium text-slate-400">
              Unavailability Duration
            </label>

            <div className="relative">
              <Clock3 className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" />

              <select
                value={duration}
                onChange={(e) => setDuration(e.target.value)}
                className="w-full appearance-none rounded-xl border border-white/10 bg-slate-900/70 py-3 pl-10 pr-4 text-sm text-white outline-none transition duration-300 hover:border-white/20 focus:border-indigo-400/50 focus:ring-2 focus:ring-indigo-500/10"
              >
                <option value="">Select duration</option>
                <option value="2">2 hours</option>
                <option value="4">4 hours</option>
                <option value="8">8 hours</option>
                <option value="12">12 hours</option>
                <option value="24">24 hours</option>
              </select>
            </div>
          </div>
        </div>

        {/* Run simulation */}
        <div className="mt-7 flex flex-col gap-3 border-t border-white/5 pt-6 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-center gap-2 text-[11px] text-slate-500">
            <Zap className="h-4 w-4 text-amber-400" />
            AI optimization will evaluate available alternatives.
          </div>

          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={runSimulation}
            disabled={
              !scenarioType ||
              !corridor ||
              !date ||
              !startTime ||
              !duration ||
              simulationLoading
            }
            className="flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-indigo-500 to-blue-500 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-indigo-500/10 transition duration-300 hover:from-indigo-400 hover:to-blue-400 disabled:cursor-not-allowed disabled:opacity-40"
          >
            <BrainCircuit className="h-4 w-4" />

            {simulationLoading ? "Analyzing Scenario..." : "Run AI Simulation"}
          </motion.button>
        </div>
      </motion.div>

      {/* ERROR */}
      <AnimatePresence>
        {simulationError && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="rounded-2xl border border-red-400/20 bg-red-500/[0.05] p-5"
          >
            <div className="flex items-start gap-3">
              <AlertTriangle className="mt-0.5 h-5 w-5 text-red-400" />

              <div>
                <h3 className="text-sm font-semibold text-red-300">
                  Simulation Failed
                </h3>

                <p className="mt-1 text-xs text-red-400/80">
                  {simulationError}
                </p>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* RESULTS */}
      <AnimatePresence mode="wait">
        {!simulationStarted ? (
          <motion.div
            key="empty"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="rounded-2xl border border-dashed border-white/10 bg-white/[0.02] p-12 text-center"
          >
            <motion.div
              animate={{
                scale: [1, 1.05, 1],
                opacity: [0.6, 1, 0.6],
              }}
              transition={{
                duration: 3,
                repeat: Infinity,
              }}
              className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-indigo-500/10"
            >
              <BrainCircuit className="h-8 w-8 text-indigo-400" />
            </motion.div>

            <h3 className="mt-5 text-sm font-semibold text-slate-300">
              Awaiting Simulation
            </h3>

            <p className="mx-auto mt-2 max-w-lg text-xs leading-5 text-slate-500">
              Configure a scenario above to evaluate maintenance impact,
              optimized block alternatives, and operational consequences.
            </p>
          </motion.div>
        ) : (
          <motion.div
            key="results"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-5"
          >
            {/* AI recommendation */}
            <div className="rounded-2xl border border-emerald-400/10 bg-emerald-500/[0.04] p-6">
              <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <CircleCheck className="h-5 w-5 text-emerald-400" />

                    <h2 className="text-base font-semibold text-white">
                      AI Recommendation
                    </h2>
                  </div>

                  <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-300">
                    {simulationResult?.recommendation}
                  </p>
                </div>

                <div className="flex items-center gap-3">
                  {/* Scenario */}
                  <div className="rounded-xl border border-emerald-400/20 bg-emerald-400/10 px-4 py-3 text-center">
                    <p className="text-[10px] uppercase tracking-wider text-emerald-400">
                      Scenario
                    </p>

                    <p className="mt-1 text-sm font-bold text-white">
                      {simulationResult?.scenario?.scenario_type}
                    </p>
                  </div>

                  {/* Confidence */}
                  <div className="rounded-xl border border-emerald-400/20 bg-emerald-400/10 px-4 py-3 text-center min-w-[100px]">
                    <p className="text-[10px] uppercase tracking-wider text-emerald-400">
                      Confidence
                    </p>

                    <p className="mt-1 text-2xl font-bold text-white">
                      {simulationResult?.confidence ?? 0}%
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Impact cards */}
            <div className="grid gap-4 md:grid-cols-3">
              {[
                {
                  label: "Affected Blocks",
                  value: simulationResult?.affected_block_count ?? 0,
                  icon: Network,
                  text: "blocks affected",
                },
                {
                  label: "Alternative Slots",
                  value: simulationResult?.alternative_slot_count ?? 0,
                  icon: Clock3,
                  text: "feasible windows",
                },
                {
                  label: "Unavailable Window",
                  value: simulationResult?.scenario
                    ? `${simulationResult.scenario.start_time} – ${simulationResult.scenario.end_time}`
                    : "--",
                  icon: TrendingUp,
                  text: `${simulationResult?.scenario?.corridor_id ?? corridor} · ${simulationResult?.scenario?.unavailable_date ?? date}`,
                },
              ].map((item, index) => {
                const Icon = item.icon;

                return (
                  <motion.div
                    key={item.label}
                    initial={{ opacity: 0, y: 15 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    whileHover={{ y: -3 }}
                    className="rounded-2xl border border-white/10 bg-white/[0.035] p-5 transition hover:border-indigo-400/20"
                  >
                    <Icon className="h-5 w-5 text-indigo-400" />

                    <p className="mt-5 text-xs text-slate-500">{item.label}</p>

                    <p className="mt-1 text-2xl font-bold text-white">
                      {item.value}
                    </p>

                    <p className="mt-1 text-[11px] text-slate-600">
                      {item.text}
                    </p>
                  </motion.div>
                );
              })}
            </div>

            {/* Affected blocks */}
            {simulationResult?.affected_blocks?.length > 0 && (
              <div className="rounded-2xl border border-white/10 bg-white/[0.035] p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <h2 className="text-base font-semibold text-white">
                      Affected Optimized Blocks
                    </h2>

                    <p className="mt-1 text-xs text-slate-500">
                      Blocks overlapping the simulated unavailable window
                    </p>
                  </div>

                  <Network className="h-5 w-5 text-indigo-400" />
                </div>

                <div className="mt-6 space-y-3">
                  {simulationResult.affected_blocks.map((block, index) => (
                    <motion.div
                      key={block.optimized_block_id}
                      initial={{ opacity: 0, x: -15 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{
                        delay: 0.1 + index * 0.05,
                      }}
                      className="flex flex-col gap-3 rounded-xl border border-white/5 bg-slate-900/40 p-4 sm:flex-row sm:items-center sm:justify-between"
                    >
                      <div>
                        <p className="text-sm font-semibold text-white">
                          {block.optimized_block_id}
                        </p>

                        <p className="mt-1 text-[11px] text-slate-500">
                          {block.start_time} – {block.end_time}
                          {" · "}
                          {block.duration_hours} hours
                        </p>
                      </div>

                      <div className="flex items-center gap-4">
                        <span className="rounded-full bg-indigo-500/10 px-3 py-1 text-[10px] font-medium text-indigo-300">
                          {block.department_count} departments
                        </span>

                        <span className="text-sm font-bold text-emerald-400">
                          {block.optimization_score}
                        </span>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>
            )}

            {/* Operational Impact */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.15 }}
              className="mt-6 rounded-2xl border border-white/10 bg-white/[0.03] p-5"
            >
              <div className="flex items-center justify-between mb-5">
                <div>
                  <div className="flex items-center gap-2">
                    <Activity className="w-5 h-5 text-cyan-400" />
                    <h3 className="text-lg font-semibold text-white">
                      Operational Impact
                    </h3>
                  </div>

                  <p className="mt-1 text-sm text-slate-400">
                    AI analysis of trains and goods traffic affected by this
                    scenario
                  </p>
                </div>

                <div
                  className={`rounded-full px-3 py-1 text-xs font-semibold ${
                    simulationResult?.operational_impact?.risk_level === "High"
                      ? "bg-red-500/10 text-red-400 border border-red-500/20"
                      : simulationResult?.operational_impact?.risk_level ===
                          "Medium"
                        ? "bg-amber-500/10 text-amber-400 border border-amber-500/20"
                        : "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                  }`}
                >
                  {simulationResult?.operational_impact?.risk_level ?? "Low"}{" "}
                  Risk
                </div>
              </div>

              <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
                {/* Affected Trains */}
                <div className="rounded-xl border border-white/10 bg-slate-900/50 p-4">
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-500/10">
                      <Network className="h-5 w-5 text-blue-400" />
                    </div>

                    <div>
                      <p className="text-xs text-slate-400">Affected Trains</p>
                      <p className="text-2xl font-bold text-white">
                        {simulationResult?.operational_impact
                          ?.affected_trains ?? 0}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Goods Forecast Conflicts */}
                <div className="rounded-xl border border-white/10 bg-slate-900/50 p-4">
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-500/10">
                      <TrendingUp className="h-5 w-5 text-amber-400" />
                    </div>

                    <div>
                      <p className="text-xs text-slate-400">
                        Goods Forecast Conflicts
                      </p>
                      <p className="text-2xl font-bold text-white">
                        {simulationResult?.operational_impact
                          ?.goods_forecast_conflicts ?? 0}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Expected Goods Trains */}
                <div className="rounded-xl border border-white/10 bg-slate-900/50 p-4">
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-purple-500/10">
                      <CalendarDays className="h-5 w-5 text-purple-400" />
                    </div>

                    <div>
                      <p className="text-xs text-slate-400">
                        Expected Goods Trains
                      </p>
                      <p className="text-2xl font-bold text-white">
                        {simulationResult?.operational_impact
                          ?.expected_goods_trains ?? 0}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>

            {/* Alternatives */}
            <div className="rounded-2xl border border-white/10 bg-white/[0.035] p-6">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-base font-semibold text-white">
                    Recommended Alternative Windows
                  </h2>

                  <p className="mt-1 text-xs text-slate-500">
                    Feasible planning options identified by the simulation
                  </p>
                </div>

                <Sparkles className="h-5 w-5 text-indigo-400" />
              </div>

              {simulationResult?.alternative_slots?.length > 0 ? (
                <div className="mt-6 space-y-3">
                  {simulationResult.alternative_slots.map((slot, index) => (
                    <motion.div
                      key={`${slot.start_time}-${slot.end_time}`}
                      initial={{ opacity: 0, x: -15 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{
                        delay: 0.2 + index * 0.08,
                      }}
                      className="flex flex-col gap-3 rounded-xl border border-white/5 bg-slate-900/40 p-4 transition hover:border-indigo-400/20 sm:flex-row sm:items-center sm:justify-between"
                    >
                      <div>
                        <div className="flex items-center gap-2">
                          <p className="text-sm font-semibold text-white">
                            {slot.start_time} – {slot.end_time}
                          </p>

                          {index === 0 && (
                            <span className="rounded-full bg-emerald-500/10 px-2 py-1 text-[9px] font-semibold uppercase text-emerald-400">
                              Best Option
                            </span>
                          )}
                        </div>

                        <p className="mt-1 text-[11px] text-slate-500">
                          {simulationResult.scenario.corridor_id}
                          {" · "}
                          {simulationResult.scenario.unavailable_date}
                        </p>
                      </div>

                      <div className="flex items-center gap-5">
                        {/* AI Score */}
                        <div className="text-center">
                          <p className="text-[9px] uppercase tracking-wider text-slate-500">
                            AI Score
                          </p>

                          <p className="text-lg font-bold text-emerald-400">
                            {slot.score}
                          </p>
                        </div>

                        {/* Goods Impact */}
                        <div className="text-center">
                          <p className="text-[9px] uppercase tracking-wider text-slate-500">
                            Goods Impact
                          </p>

                          <p className="text-sm font-semibold text-white">
                            {slot.goods_conflicts} conflict
                            {slot.goods_conflicts !== 1 ? "s" : ""}
                          </p>

                          <p className="text-[10px] text-slate-500">
                            {slot.expected_goods_trains} expected trains
                          </p>
                        </div>

                        {/* Status */}
                        <div className="text-center">
                          <span
                            className={`rounded-full px-3 py-1 text-[10px] font-medium ${
                              slot.status === "Recommended"
                                ? "bg-emerald-500/10 text-emerald-400"
                                : slot.status === "Good"
                                  ? "bg-cyan-500/10 text-cyan-400"
                                  : "bg-amber-500/10 text-amber-400"
                            }`}
                          >
                            {slot.status}
                          </span>

                          <p className="mt-1 text-[10px] text-slate-500">
                            Train conflicts: {slot.train_conflicts}
                          </p>
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </div>
              ) : (
                <div className="mt-6 rounded-xl border border-dashed border-white/10 p-6 text-center">
                  <p className="text-xs text-slate-500">
                    No feasible alternative windows were found.
                  </p>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* FOOTER */}
      <motion.footer
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.6 }}
        className="border-t border-white/5 pt-6"
      >
        <div className="flex flex-col gap-4 text-center sm:flex-row sm:items-center sm:justify-between sm:text-left">
          <div>
            <p className="text-xs font-medium text-slate-400">
              RAILOPTIMA · Intelligent Railway Block Planning
            </p>

            <p className="mt-1 text-[11px] text-slate-600">
              © {new Date().getFullYear()} Uttam Kumar Singh. All rights
              reserved.
            </p>
          </div>

          <div className="flex justify-center gap-5 sm:justify-end">
            <a
              href="#"
              className="flex items-center gap-1 text-[11px] text-slate-500 transition hover:text-indigo-400"
            >
              Documentation
              <ExternalLink className="h-3 w-3" />
            </a>

            <a
              href="#"
              className="flex items-center gap-1 text-[11px] text-slate-500 transition hover:text-indigo-400"
            >
              System Status
              <ExternalLink className="h-3 w-3" />
            </a>

            <a
              href="#"
              className="flex items-center gap-1 text-[11px] text-slate-500 transition hover:text-indigo-400"
            >
              About
              <ExternalLink className="h-3 w-3" />
            </a>
          </div>
        </div>
      </motion.footer>
    </div>
  );
}

export default WhatIfSimulator;
