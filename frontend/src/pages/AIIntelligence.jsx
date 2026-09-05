import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import {
  BrainCircuit,
  Activity,
  Network,
  ShieldCheck,
  Sparkles,
  TrendingUp,
  Layers3,
  AlertTriangle,
  CheckCircle2,
} from "lucide-react";
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";

const API_URL = "http://127.0.0.1:8000";

function AIIntelligence() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`${API_URL}/api/ai-intelligence/summary`)
      .then(async (response) => {
        if (!response.ok) {
          throw new Error("Unable to load AI intelligence data");
        }

        const result = await response.json();
        setData(result);
      })
      .catch((err) => {
        setError(err.message);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <div className="flex items-center gap-3 text-slate-400">
          <BrainCircuit className="h-6 w-6 animate-pulse text-cyan-400" />
          Loading AI intelligence...
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-2xl border border-red-500/20 bg-red-500/5 p-6 text-red-400">
        {error}
      </div>
    );
  }

  const priority = data.priority_intelligence;
  const optimization = data.optimization_intelligence;
  const departments = data.department_coordination;

  const priorityData = [
    { name: "Critical", value: priority.critical },
    { name: "High", value: priority.high },
    { name: "Medium", value: priority.medium },
    { name: "Low", value: priority.low },
  ];

  const COLORS = ["#ef4444", "#f59e0b", "#38bdf8", "#64748b"];

  const risk =
    optimization.average_optimization_score >= 70
      ? "Low"
      : optimization.average_optimization_score >= 50
        ? "Medium"
        : "High";

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -15 }}
        animate={{ opacity: 1, y: 0 }}
        className="relative overflow-hidden rounded-3xl border border-cyan-400/10 bg-gradient-to-br from-cyan-500/10 via-blue-500/5 to-transparent p-7"
      >
        <div className="absolute -right-20 -top-20 h-56 w-56 rounded-full bg-cyan-400/10 blur-3xl" />

        <div className="relative flex flex-col gap-5 md:flex-row md:items-center md:justify-between">
          <div>
            <div className="mb-3 flex items-center gap-3">
              <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-cyan-400/10">
                <BrainCircuit className="h-6 w-6 text-cyan-400" />
              </div>

              <div>
                <p className="text-xs font-medium uppercase tracking-[0.2em] text-cyan-400">
                  Intelligent Planning Engine
                </p>

                <h1 className="text-2xl font-bold text-white md:text-3xl">
                  AI Intelligence
                </h1>
              </div>
            </div>

            <p className="max-w-2xl text-sm leading-6 text-slate-400">
              AI-driven insights for maintenance prioritization, coordinated
              block planning and railway operational efficiency.
            </p>
          </div>

          <div className="flex items-center gap-2 rounded-full border border-emerald-400/20 bg-emerald-400/5 px-4 py-2 text-sm text-emerald-400">
            <span className="h-2 w-2 animate-pulse rounded-full bg-emerald-400" />
            AI Engine Online
          </div>
        </div>
      </motion.div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <MetricCard
          icon={Activity}
          label="Maintenance Tasks"
          value={priority.total_tasks}
          description="Tasks analyzed by AI"
          delay={0}
        />

        <MetricCard
          icon={Layers3}
          label="Optimized Blocks"
          value={optimization.total_blocks}
          description={`${optimization.total_block_hours} block hours`}
          delay={0.05}
        />

        <MetricCard
          icon={Network}
          label="Coordinated Blocks"
          value={optimization.coordinated_blocks}
          description="Multi-department blocks"
          delay={0.1}
        />

        <MetricCard
          icon={TrendingUp}
          label="Optimization Score"
          value={optimization.average_optimization_score}
          suffix="%"
          description="Latest optimization run"
          delay={0.15}
        />
      </div>

      {/* Priority + Optimization */}
      <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">
        {/* Priority Distribution */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="rounded-2xl border border-white/10 bg-white/[0.03] p-6"
        >
          <div className="mb-5">
            <div className="flex items-center gap-2">
              <ShieldCheck className="h-5 w-5 text-cyan-400" />
              <h2 className="text-lg font-semibold text-white">
                AI Maintenance Priority
              </h2>
            </div>

            <p className="mt-1 text-sm text-slate-400">
              Maintenance workload classified by AI priority level
            </p>
          </div>

          <div className="flex flex-col items-center gap-5 sm:flex-row">
            <div className="h-56 w-full sm:w-1/2">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={priorityData}
                    dataKey="value"
                    nameKey="name"
                    innerRadius={58}
                    outerRadius={82}
                    paddingAngle={3}
                  >
                    {priorityData.map((entry, index) => (
                      <Cell key={entry.name} fill={COLORS[index]} />
                    ))}
                  </Pie>

                  <Tooltip
                    contentStyle={{
                      background: "#0f172a",
                      border: "1px solid rgba(255,255,255,0.1)",
                      borderRadius: "12px",
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>

            <div className="w-full space-y-3 sm:w-1/2">
              {priorityData.map((item, index) => (
                <div
                  key={item.name}
                  className="flex items-center justify-between"
                >
                  <div className="flex items-center gap-2">
                    <span
                      className="h-2.5 w-2.5 rounded-full"
                      style={{
                        backgroundColor: COLORS[index],
                      }}
                    />

                    <span className="text-sm text-slate-300">{item.name}</span>
                  </div>

                  <span className="font-semibold text-white">{item.value}</span>
                </div>
              ))}

              <div className="mt-4 border-t border-white/10 pt-4">
                <p className="text-xs text-slate-500">Average Priority Score</p>

                <p className="mt-1 text-2xl font-bold text-cyan-400">
                  {priority.average_priority_score}
                </p>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Optimization Intelligence */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.25 }}
          className="rounded-2xl border border-white/10 bg-white/[0.03] p-6"
        >
          <div className="mb-5">
            <div className="flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-cyan-400" />
              <h2 className="text-lg font-semibold text-white">
                Optimization Intelligence
              </h2>
            </div>

            <p className="mt-1 text-sm text-slate-400">
              Performance of the latest AI optimization run
            </p>
          </div>

          <div className="space-y-5">
            <div>
              <div className="mb-2 flex justify-between text-sm">
                <span className="text-slate-400">Optimization Efficiency</span>

                <span className="font-semibold text-cyan-400">
                  {optimization.average_optimization_score}%
                </span>
              </div>

              <div className="h-2 overflow-hidden rounded-full bg-slate-800">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{
                    width: `${optimization.average_optimization_score}%`,
                  }}
                  transition={{ duration: 1 }}
                  className="h-full rounded-full bg-gradient-to-r from-cyan-500 to-blue-500"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <InfoBox
                label="Block Hours"
                value={optimization.total_block_hours}
              />

              <InfoBox
                label="Coordinated"
                value={optimization.coordinated_blocks}
              />

              <InfoBox label="Total Blocks" value={optimization.total_blocks} />

              <InfoBox label="Risk Level" value={risk} />
            </div>
          </div>
        </motion.div>
      </div>

      {/* Department Coordination */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="rounded-2xl border border-white/10 bg-white/[0.03] p-6"
      >
        <div className="mb-5">
          <div className="flex items-center gap-2">
            <Network className="h-5 w-5 text-cyan-400" />
            <h2 className="text-lg font-semibold text-white">
              Department Coordination
            </h2>
          </div>

          <p className="mt-1 text-sm text-slate-400">
            Coordinated maintenance blocks by railway department
          </p>
        </div>

        <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
          <DepartmentCard
            name="Engineering"
            code="ENG"
            value={departments.ENG}
            delay={0.35}
          />

          <DepartmentCard
            name="Signal & Telecom"
            code="SNT"
            value={departments.SNT}
            delay={0.4}
          />

          <DepartmentCard
            name="Traction Distribution"
            code="TRD"
            value={departments.TRD}
            delay={0.45}
          />
        </div>
      </motion.div>

      {/* AI Insights */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="rounded-2xl border border-cyan-400/10 bg-gradient-to-br from-cyan-400/5 to-transparent p-6"
      >
        <div className="mb-5 flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-cyan-400/10">
            <BrainCircuit className="h-5 w-5 text-cyan-400" />
          </div>

          <div>
            <h2 className="text-lg font-semibold text-white">
              AI Planning Insights
            </h2>

            <p className="text-sm text-slate-400">
              Decisions and observations generated from current planning data
            </p>
          </div>
        </div>

        <div className="space-y-3">
          {data.ai_insights.map((insight, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{
                delay: 0.55 + index * 0.1,
              }}
              className="flex gap-3 rounded-xl border border-white/10 bg-slate-900/40 p-4"
            >
              <CheckCircle2 className="mt-0.5 h-5 w-5 shrink-0 text-cyan-400" />

              <p className="text-sm leading-6 text-slate-300">{insight}</p>
            </motion.div>
          ))}
        </div>
      </motion.div>
      {/* Developer Footer */}
      <motion.footer
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="mt-10 border-t border-white/10 pt-8 pb-4"
      >
        <div className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
          {/* Project Info */}
          <div>
            <div className="flex items-center gap-2">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-blue-400/10 text-blue-300">
                <BrainCircuit size={18} />
              </div>

              <div>
                <p className="text-sm font-semibold text-white">
                  AI-Powered Railway Block Planning
                </p>
                <p className="text-xs text-slate-500">
                  Intelligent maintenance optimization system
                </p>
              </div>
            </div>
          </div>

          {/* Developer */}
          <div className="text-left md:text-right">
            <p className="text-xs uppercase tracking-wider text-slate-500">
              Developed by
            </p>

            <p className="mt-1 text-sm font-semibold text-slate-200">
              Uttam Kumar Singh
            </p>

            <div className="mt-2 flex items-center gap-4 md:justify-end">
              <a
                href="https://github.com/singhuttam7"
                target="_blank"
                rel="noreferrer"
                className="text-xs text-slate-400 transition hover:text-blue-300"
              >
                GitHub
              </a>

              <a
                href="https://www.linkedin.com/in/uttam-singh-b936a1310/"
                target="_blank"
                rel="noreferrer"
                className="text-xs text-slate-400 transition hover:text-blue-300"
              >
                LinkedIn
              </a>

              <a
                href="https://www.instagram.com/singh_uttam790"
                target="_blank"
                rel="noreferrer"
                className="text-xs text-slate-400 transition hover:text-pink-300"
              >
                Instagram
              </a>
            </div>
          </div>
        </div>

        {/* Copyright */}
        <div className="mt-7 flex flex-col gap-2 border-t border-white/5 pt-4 text-xs text-slate-600 sm:flex-row sm:items-center sm:justify-between">
          <span>© 2026 Uttam Kumar Singh · All Rights Reserved</span>

          <span>AI • Optimization • Railway Operations</span>
        </div>
      </motion.footer>

      {/* Footer Status */}
      <div className="flex flex-col gap-2 border-t border-white/5 pt-5 text-xs text-slate-500 sm:flex-row sm:items-center sm:justify-between">
        <span>Optimization Run #{data.optimization_run_id}</span>

        <span className="flex items-center gap-2">
          <span className="h-2 w-2 rounded-full bg-emerald-400" />
          AI Intelligence System Operational
        </span>
      </div>
    </div>
  );
}

/* ---------------------------------------------------------
   Reusable Components
--------------------------------------------------------- */

function MetricCard({
  icon: Icon,
  label,
  value,
  suffix = "",
  description,
  delay,
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay }}
      className="rounded-2xl border border-white/10 bg-white/[0.03] p-5"
    >
      <div className="flex items-center justify-between">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-cyan-400/10">
          <Icon className="h-5 w-5 text-cyan-400" />
        </div>
      </div>

      <p className="mt-4 text-sm text-slate-400">{label}</p>

      <p className="mt-1 text-3xl font-bold text-white">
        {value}
        {suffix}
      </p>

      <p className="mt-1 text-xs text-slate-500">{description}</p>
    </motion.div>
  );
}

function InfoBox({ label, value }) {
  return (
    <div className="rounded-xl border border-white/10 bg-slate-900/40 p-4">
      <p className="text-xs text-slate-500">{label}</p>

      <p className="mt-1 text-xl font-bold text-white">{value}</p>
    </div>
  );
}

function DepartmentCard({ name, code, value, delay }) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.97 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay }}
      className="rounded-xl border border-white/10 bg-slate-900/40 p-5"
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs font-medium text-cyan-400">{code}</p>

          <p className="mt-1 font-medium text-white">{name}</p>
        </div>

        <div className="text-right">
          <p className="text-2xl font-bold text-white">{value}</p>

          <p className="text-xs text-slate-500">coordinated blocks</p>
        </div>
      </div>
    </motion.div>
  );
}

export default AIIntelligence;
