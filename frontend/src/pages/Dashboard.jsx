import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import {
  CalendarDays,
  Clock3,
  Layers3,
  Network,
  BrainCircuit,
  TrendingUp,
  ShieldCheck,
  ArrowUpRight,
  Sparkles,
} from "lucide-react";

import {
  BarChart,
  Bar,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const API_URL = "http://127.0.0.1:8000";

const cardData = [
  {
    title: "Optimized Blocks",
    key: "total_blocks",
    icon: CalendarDays,
    suffix: "",
    description: "Planned maintenance blocks",
  },
  {
    title: "Block Utilization",
    key: "total_block_hours",
    icon: Clock3,
    suffix: " hrs",
    description: "Total planned block hours",
  },
  {
    title: "Coordinated Blocks",
    key: "multi_department_blocks",
    icon: Network,
    suffix: "",
    description: "Multi-department coordination",
  },
  {
    title: "Planning Days",
    key: "total_planning_days",
    icon: Layers3,
    suffix: "",
    description: "Current planning horizon",
  },
];

function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState(null);
  const [optimizedBlocks, setOptimizedBlocks] = useState([]);
  const [departmentCoordination, setDepartmentCoordination] = useState(null);
  const [corridors, setCorridors] = useState([]);

  useEffect(() => {
    Promise.all([
      fetch(`${API_URL}/api/dashboard/summary`),
      fetch(`${API_URL}/api/optimized-blocks/`),
      fetch(`${API_URL}/api/dashboard/department-coordination`),
      fetch(`${API_URL}/api/corridors/`),
    ])
      .then(
        async ([
          summaryResponse,
          blocksResponse,
          departmentResponse,
          corridorsResponse,
        ]) => {
          if (!summaryResponse.ok) {
            throw new Error("Unable to load dashboard data");
          }

          if (!blocksResponse.ok) {
            throw new Error("Unable to load optimized blocks");
          }
          if (!corridorsResponse.ok) {
            throw new Error("Unable to load corridors");
          }

          const summaryData = await summaryResponse.json();
          const blocksData = await blocksResponse.json();
          const departmentData = await departmentResponse.json();
          const corridorsData = await corridorsResponse.json();

          setSummary(summaryData);
          setOptimizedBlocks(blocksData);
          setDepartmentCoordination(departmentData);
          setCorridors(corridorsData);
        },
      )
      .catch((err) => setError(err.message));
  }, []);

  if (error) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <div className="rounded-2xl border border-red-400/20 bg-red-400/5 p-8 text-center">
          <ShieldCheck className="mx-auto mb-4 h-10 w-10 text-red-400" />
          <h2 className="text-lg font-semibold text-white">
            Dashboard unavailable
          </h2>
          <p className="mt-2 text-sm text-slate-400">{error}</p>
        </div>
      </div>
    );
  }

  if (!summary) {
    return (
      <div className="space-y-6">
        <div className="h-10 w-72 animate-pulse rounded-lg bg-white/5" />
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          {[1, 2, 3, 4].map((item) => (
            <div
              key={item}
              className="h-36 animate-pulse rounded-2xl bg-white/5"
            />
          ))}
        </div>
      </div>
    );
  }
  const corridorChartData = ["C001", "C002", "C003", "C004", "C005"].map(
    (corridor) => ({
      corridor,
      blocks: optimizedBlocks.filter((block) => block.corridor_id === corridor)
        .length,
    }),
  );
  return (
    <div className="space-y-6">
      {/* Page heading */}
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="flex flex-col justify-between gap-4 md:flex-row md:items-end">
          <div>
            <div className="mb-2 flex items-center gap-2">
              <span className="h-2 w-2 rounded-full bg-emerald-400" />
              <span className="text-xs font-medium uppercase tracking-[0.18em] text-emerald-400">
                Operations Live
              </span>
            </div>

            <h1 className="text-2xl font-bold tracking-tight text-white sm:text-3xl">
              Railway Maintenance Dashboard
            </h1>

            <p className="mt-2 max-w-2xl text-sm text-slate-400">
              AI-powered planning and coordination of infrastructure maintenance
              blocks across railway corridors.
            </p>
          </div>

          <div className="flex items-center gap-2 rounded-xl border border-white/10 bg-white/[0.03] px-4 py-3">
            <CalendarDays className="h-4 w-4 text-blue-400" />
            <div>
              <p className="text-[10px] uppercase tracking-wider text-slate-500">
                Optimization Run
              </p>
              <p className="text-sm font-semibold text-white">
                #{summary.optimization_run_id}
              </p>
            </div>
          </div>
        </div>
      </motion.div>

      {/* KPI Cards */}
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {cardData.map((card, index) => {
          const Icon = card.icon;

          return (
            <motion.div
              key={card.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.08 }}
              whileHover={{ y: -4 }}
              className="group rounded-2xl border border-white/10 bg-white/[0.035] p-5 shadow-xl shadow-black/10 transition-colors duration-300 hover:border-blue-400/20 hover:bg-white/[0.05]"
            >
              <div className="flex items-start justify-between">
                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-500/10 text-blue-400 ring-1 ring-blue-400/10">
                  <Icon className="h-5 w-5" />
                </div>

                <ArrowUpRight className="h-4 w-4 text-slate-600 transition-colors group-hover:text-blue-400" />
              </div>

              <p className="mt-5 text-sm text-slate-400">{card.title}</p>

              <p className="mt-1 text-3xl font-bold tracking-tight text-white">
                {summary[card.key]}
                <span className="ml-1 text-lg font-medium text-slate-500">
                  {card.suffix}
                </span>
              </p>

              <p className="mt-2 text-xs text-slate-500">{card.description}</p>
            </motion.div>
          );
        })}
      </div>

      {/* Optimization Score + AI Intelligence */}
      <div className="grid gap-6 xl:grid-cols-3">
        {/* Score */}
        <motion.div
          initial={{ opacity: 0, x: -15 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.35 }}
          className="rounded-2xl border border-white/10 bg-white/[0.035] p-6 xl:col-span-1"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-slate-300">
                Optimization Score
              </p>
              <p className="mt-1 text-xs text-slate-500">
                Overall planning quality
              </p>
            </div>

            <TrendingUp className="h-5 w-5 text-emerald-400" />
          </div>

          <div className="mt-7 flex flex-col gap-6 2xl:flex-row 2xl:items-center">
            <div className="relative mx-auto flex h-28 w-28 shrink-0 items-center justify-center rounded-full border-[9px] border-blue-500/20 2xl:mx-0">
              <div className="absolute inset-0 rounded-full border-[10px] border-transparent border-t-blue-400 border-r-blue-400 rotate-[-35deg]" />

              <div className="text-center">
                <p className="text-3xl font-bold text-white">
                  {summary.average_optimization_score}
                </p>
                <p className="text-[10px] uppercase tracking-wider text-slate-500">
                  Score
                </p>
              </div>
            </div>

            <div className="min-w-0 text-center 2xl:text-left">
              <p className="text-sm font-semibold text-emerald-400">
                Optimization Active
              </p>
              <p className="mt-2 text-xs leading-relaxed text-slate-500">
                The planning engine evaluates maintenance priority, coordination
                opportunities and operational constraints.
              </p>
            </div>
          </div>
        </motion.div>

        {/* AI Intelligence */}
        <motion.div
          initial={{ opacity: 0, x: 15 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4 }}
          className="relative overflow-hidden rounded-2xl border border-blue-400/20 bg-gradient-to-br from-blue-500/10 via-indigo-500/5 to-transparent p-6 xl:col-span-2"
        >
          <div className="pointer-events-none absolute -right-16 -top-16 h-48 w-48 rounded-full bg-blue-500/10 blur-3xl" />

          <div className="relative">
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-3">
                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-500/15 ring-1 ring-blue-400/20">
                  <BrainCircuit className="h-5 w-5 text-blue-400" />
                </div>

                <div>
                  <div className="flex items-center gap-2">
                    <h2 className="font-semibold text-white">
                      AI Intelligence
                    </h2>

                    <span className="rounded-full border border-blue-400/20 bg-blue-400/10 px-2 py-0.5 text-[9px] font-semibold uppercase tracking-wider text-blue-300">
                      Live
                    </span>
                  </div>

                  <p className="text-xs text-slate-500">
                    Intelligent planning insights
                  </p>
                </div>
              </div>

              <Sparkles className="h-5 w-5 text-blue-400" />
            </div>

            <div className="mt-6 grid gap-3 sm:grid-cols-2">
              <div className="rounded-xl border border-white/10 bg-black/10 p-4">
                <p className="text-xs text-slate-500">Coordination</p>
                <p className="mt-1 text-sm font-semibold text-white">
                  {summary.multi_department_blocks} opportunities identified
                </p>
                <p className="mt-1 text-xs text-slate-500">
                  Multiple departments can share optimized blocks.
                </p>
              </div>

              <div className="rounded-xl border border-white/10 bg-black/10 p-4">
                <p className="text-xs text-slate-500">Asset Availability</p>
                <p className="mt-1 text-sm font-semibold text-white">
                  Downtime optimization enabled
                </p>
                <p className="mt-1 text-xs text-slate-500">
                  Maintenance is prioritized using operational impact.
                </p>
              </div>
            </div>

            <div className="mt-4 flex items-center gap-2 text-xs text-blue-300">
              <span className="h-1.5 w-1.5 rounded-full bg-blue-400" />
              AI-assisted planning engine ready
            </div>
          </div>
        </motion.div>
      </div>

      {/* Optimized Blocks by Corridor */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.45 }}
        className="rounded-2xl border border-white/10 bg-white/[0.035] p-6"
      >
        <div className="flex items-start justify-between">
          <div>
            <h2 className="text-base font-semibold text-white">
              Optimized Blocks by Corridor
            </h2>

            <p className="mt-1 text-xs text-slate-500">
              Distribution of planned maintenance blocks across railway
              corridors
            </p>
          </div>

          <div className="rounded-xl bg-blue-500/10 p-2.5 text-blue-400">
            <Network className="h-5 w-5" />
          </div>
        </div>

        <div className="mt-6 h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={corridorChartData}
              margin={{ top: 10, right: 10, left: -20, bottom: 0 }}
            >
              <CartesianGrid
                strokeDasharray="3 3"
                stroke="rgba(255,255,255,0.06)"
                vertical={false}
              />

              <XAxis
                dataKey="corridor"
                tick={{ fill: "#64748b", fontSize: 12 }}
                axisLine={false}
                tickLine={false}
              />

              <YAxis
                allowDecimals={false}
                tick={{ fill: "#64748b", fontSize: 12 }}
                axisLine={false}
                tickLine={false}
              />

              <Tooltip
                cursor={{ fill: "rgba(59,130,246,0.05)" }}
                content={({ active, payload, label }) => {
                  if (!active || !payload || !payload.length) return null;

                  return (
                    <div
                      style={{
                        background: "#0b1729",
                        border: "1px solid rgba(255,255,255,0.12)",
                        borderRadius: "12px",
                        padding: "12px 16px",
                        boxShadow: "0 10px 30px rgba(0,0,0,0.35)",
                      }}
                    >
                      <p
                        style={{
                          color: "#ffffff",
                          fontSize: "14px",
                          fontWeight: 600,
                          margin: "0 0 6px",
                        }}
                      >
                        {label}
                      </p>

                      <p
                        style={{
                          color: "#60a5fa",
                          fontSize: "13px",
                          fontWeight: 500,
                          margin: 0,
                        }}
                      >
                        Optimized Blocks: {payload[0].value}
                      </p>
                    </div>
                  );
                }}
              />

              <Bar
                dataKey="blocks"
                name="Optimized Blocks"
                radius={[7, 7, 0, 0]}
                animationDuration={900}
              >
                {corridorChartData.map((entry, index) => {
                  const colors = [
                    "#38bdf8", // C001 - Cyan
                    "#8b5cf6", // C002 - Purple
                    "#ec4899", // C003 - Pink
                    "#f59e0b", // C004 - Amber
                    "#10b981", // C005 - Emerald
                  ];

                  return (
                    <Cell
                      key={`cell-${index}`}
                      fill={colors[index % colors.length]}
                    />
                  );
                })}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </motion.div>

      {/* Department Coordination */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="rounded-2xl border border-white/10 bg-white/[0.035] p-6"
      >
        <div className="flex items-start justify-between">
          <div>
            <h2 className="text-base font-semibold text-white">
              Department Coordination
            </h2>

            <p className="mt-1 text-xs text-slate-500">
              Optimized blocks involving each railway maintenance department
            </p>
          </div>

          <div className="rounded-xl bg-indigo-500/10 p-2.5 text-indigo-400">
            <Network className="h-5 w-5" />
          </div>
        </div>

        <div className="mt-6 grid gap-4 md:grid-cols-3">
          {[
            {
              name: "Engineering",
              code: "ENG",
              value: departmentCoordination?.ENG ?? 0,
              color: "#38bdf8",
            },
            {
              name: "Signal & Telecom",
              code: "SNT",
              value: departmentCoordination?.SNT ?? 0,
              color: "#a78bfa",
            },
            {
              name: "Traction Distribution",
              code: "TRD",
              value: departmentCoordination?.TRD ?? 0,
              color: "#34d399",
            },
          ].map((department, index) => (
            <motion.div
              key={department.code}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.55 + index * 0.08 }}
              whileHover={{ y: -3 }}
              className="rounded-xl border border-white/10 bg-black/10 p-5 transition-colors duration-300 hover:border-white/20"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs font-medium uppercase tracking-wider text-slate-500">
                    {department.code}
                  </p>

                  <p className="mt-1 text-sm font-semibold text-white">
                    {department.name}
                  </p>
                </div>

                <div
                  className="h-3 w-3 rounded-full"
                  style={{
                    backgroundColor: department.color,
                    boxShadow: `0 0 12px ${department.color}`,
                  }}
                />
              </div>

              <div className="mt-5 flex items-end justify-between">
                <div>
                  <p className="text-3xl font-bold text-white">
                    {department.value}
                  </p>

                  <p className="mt-1 text-xs text-slate-500">
                    Optimized blocks
                  </p>
                </div>

                <Network
                  className="h-5 w-5"
                  style={{ color: department.color }}
                />
              </div>

              <div className="mt-4 h-1.5 overflow-hidden rounded-full bg-white/5">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{
                    width: `${Math.min(
                      (department.value /
                        Math.max(
                          departmentCoordination?.ENG ?? 0,
                          departmentCoordination?.SNT ?? 0,
                          departmentCoordination?.TRD ?? 0,
                          1,
                        )) *
                        100,
                      100,
                    )}%`,
                  }}
                  transition={{
                    duration: 0.9,
                    delay: 0.6 + index * 0.08,
                  }}
                  className="h-full rounded-full"
                  style={{ backgroundColor: department.color }}
                />
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Railway Corridor Map */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.55 }}
        className="rounded-2xl border border-white/10 bg-white/[0.035] p-6"
      >
        <div className="flex items-start justify-between">
          <div>
            <h2 className="text-base font-semibold text-white">
              Railway Corridor Network
            </h2>

            <p className="mt-1 text-xs text-slate-500">
              Active maintenance corridors and their kilometer ranges
            </p>
          </div>

          <div className="rounded-xl bg-cyan-500/10 p-2.5 text-cyan-400">
            <Network className="h-5 w-5" />
          </div>
        </div>

        <div className="mt-8 space-y-6">
          {corridors.map((corridor, index) => (
            <motion.div
              key={corridor.corridor_id}
              initial={{ opacity: 0, x: -15 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.6 + index * 0.08 }}
              className="group"
            >
              <div className="mb-2 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <span className="flex h-8 w-12 items-center justify-center rounded-lg bg-blue-500/10 text-xs font-bold text-blue-400">
                    {corridor.corridor_id}
                  </span>

                  <div>
                    <p className="text-sm font-semibold text-white">
                      {corridor.corridor_name}
                    </p>

                    <p className="text-[11px] text-slate-500">
                      {corridor.start_km} km — {corridor.end_km} km
                    </p>
                  </div>
                </div>

                <span className="text-xs text-slate-500">
                  {corridor.end_km - corridor.start_km} km
                </span>
              </div>

              <div className="relative h-8">
                {/* Railway line */}
                <div className="absolute left-0 right-0 top-1/2 h-1 -translate-y-1/2 rounded-full bg-slate-700/70" />

                {/* Highlighted line */}
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: "100%" }}
                  transition={{
                    duration: 1,
                    delay: 0.7 + index * 0.08,
                  }}
                  className="absolute left-0 top-1/2 h-1 -translate-y-1/2 rounded-full bg-gradient-to-r from-blue-500 via-cyan-400 to-emerald-400"
                />

                {/* Railway nodes */}
                <div className="absolute left-0 top-1/2 h-3 w-3 -translate-y-1/2 rounded-full border-2 border-cyan-400 bg-[#07111f] shadow-[0_0_12px_rgba(34,211,238,0.7)]" />

                <div className="absolute right-0 top-1/2 h-3 w-3 -translate-y-1/2 rounded-full border-2 border-emerald-400 bg-[#07111f] shadow-[0_0_12px_rgba(52,211,153,0.7)]" />

                {/* Moving signal */}
                <motion.div
                  animate={{ left: ["0%", "100%", "0%"] }}
                  transition={{
                    duration: 8,
                    repeat: Infinity,
                    ease: "linear",
                  }}
                  className="absolute top-1/2 h-2 w-2 -translate-y-1/2 rounded-full bg-white shadow-[0_0_10px_rgba(255,255,255,0.9)]"
                />
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>
      {/* Bottom status */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
        className="flex flex-col gap-3 rounded-2xl border border-white/10 bg-white/[0.025] px-5 py-4 sm:flex-row sm:items-center sm:justify-between"
      >
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-500/10">
            <ShieldCheck className="h-4 w-4 text-emerald-400" />
          </div>

          <div>
            <p className="text-xs font-medium text-slate-300">
              Planning Engine Operational
            </p>
            <p className="text-[11px] text-slate-500">
              Latest completed optimization run: #{summary.optimization_run_id}
            </p>
          </div>
        </div>

        <p className="text-xs text-slate-500">
          {summary.total_block_hours} hours of maintenance capacity planned
        </p>
      </motion.div>
    </div>
  );
}

export default Dashboard;
