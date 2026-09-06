import { useEffect, useMemo, useState } from "react";
import { motion } from "framer-motion";
import {
  Search,
  Filter,
  Wrench,
  AlertTriangle,
  ShieldAlert,
  Clock3,
  CheckCircle2,
  ChevronDown,
  RefreshCw,
} from "lucide-react";

import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const priorityConfig = {
  Critical: {
    className: "text-red-300 bg-red-400/10 border-red-400/20",
    icon: ShieldAlert,
  },
  High: {
    className: "text-orange-300 bg-orange-400/10 border-orange-400/20",
    icon: AlertTriangle,
  },
  Medium: {
    className: "text-yellow-300 bg-yellow-400/10 border-yellow-400/20",
    icon: Clock3,
  },
  Low: {
    className: "text-emerald-300 bg-emerald-400/10 border-emerald-400/20",
    icon: CheckCircle2,
  },
};

function Maintenance() {
  const [tasks, setTasks] = useState([]);
  const [search, setSearch] = useState("");
  const [priority, setPriority] = useState("All");
  const [status, setStatus] = useState("All");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchTasks = () => {
    setLoading(true);
    setError(null);

    fetch(`${API_URL}/api/maintenance-tasks/`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Unable to load maintenance tasks");
        }
        return response.json();
      })
      .then((data) => {
        setTasks(data);
      })
      .catch((err) => {
        setError(err.message);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const statistics = useMemo(() => {
    return {
      total: tasks.length,
      critical: tasks.filter((task) => task.priority_level === "Critical")
        .length,
      high: tasks.filter((task) => task.priority_level === "High").length,
      medium: tasks.filter((task) => task.priority_level === "Medium").length,
      low: tasks.filter((task) => task.priority_level === "Low").length,
    };
  }, [tasks]);

  const filteredTasks = useMemo(() => {
    return tasks.filter((task) => {
      const matchesSearch =
        task.task_id?.toLowerCase().includes(search.toLowerCase()) ||
        task.asset_id?.toLowerCase().includes(search.toLowerCase()) ||
        task.task_type?.toLowerCase().includes(search.toLowerCase());

      const matchesPriority =
        priority === "All" || task.priority_level === priority;

      const matchesStatus = status === "All" || task.status === status;

      return matchesSearch && matchesPriority && matchesStatus;
    });
  }, [tasks, search, priority, status]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="flex flex-col justify-between gap-4 lg:flex-row lg:items-end">
          <div>
            <div className="mb-2 flex items-center gap-2">
              <Wrench className="h-4 w-4 text-blue-400" />
              <span className="text-xs font-medium uppercase tracking-[0.18em] text-blue-400">
                Asset Maintenance
              </span>
            </div>

            <h1 className="text-2xl font-bold tracking-tight text-white sm:text-3xl">
              Maintenance Priority
            </h1>

            <p className="mt-2 max-w-2xl text-sm text-slate-400">
              AI-assisted prioritization of railway maintenance tasks based on
              criticality, safety risk, operational impact and urgency.
            </p>
          </div>

          <button
            onClick={fetchTasks}
            className="flex w-fit items-center gap-2 rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-sm text-slate-300 transition hover:border-blue-400/20 hover:bg-blue-400/10 hover:text-white"
          >
            <RefreshCw className="h-4 w-4" />
            Refresh
          </button>
        </div>
      </motion.div>

      {/* Priority statistics */}
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-5">
        {[
          ["Total Tasks", statistics.total, Wrench, "text-blue-400"],
          ["Critical", statistics.critical, ShieldAlert, "text-red-400"],
          ["High", statistics.high, AlertTriangle, "text-orange-400"],
          ["Medium", statistics.medium, Clock3, "text-yellow-400"],
          ["Low", statistics.low, CheckCircle2, "text-emerald-400"],
        ].map(([title, value, Icon, iconColor], index) => (
          <motion.div
            key={title}
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.06 }}
            className="rounded-2xl border border-white/10 bg-white/[0.035] p-5"
          >
            <div className="flex items-center justify-between">
              <p className="text-xs text-slate-500">{title}</p>
              <Icon className={`h-4 w-4 ${iconColor}`} />
            </div>

            <p className="mt-3 text-2xl font-bold text-white">{value}</p>
          </motion.div>
        ))}
      </div>

      {/* Priority Distribution Chart */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-white/[0.045] to-white/[0.015] p-6 shadow-xl shadow-black/10"
      >
        <div className="flex flex-col justify-between gap-2 sm:flex-row sm:items-start">
          <div>
            <div className="flex items-center gap-2">
              <div className="h-2 w-2 rounded-full bg-blue-400 shadow-lg shadow-blue-400/50" />

              <h2 className="text-base font-semibold text-white">
                AI Priority Distribution
              </h2>
            </div>

            <p className="mt-1 text-xs text-slate-500">
              Intelligent classification of maintenance tasks
            </p>
          </div>

          <div className="rounded-lg border border-blue-400/10 bg-blue-400/5 px-3 py-1.5 text-xs text-blue-300">
            AI Engine
          </div>
        </div>

        <div className="mt-5 grid items-center gap-6 lg:grid-cols-[1fr_220px]">
          {/* Donut Chart */}
          <div className="relative h-[260px]">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={[
                    {
                      name: "Critical",
                      value: statistics.critical,
                    },
                    {
                      name: "High",
                      value: statistics.high,
                    },
                    {
                      name: "Medium",
                      value: statistics.medium,
                    },
                    {
                      name: "Low",
                      value: statistics.low,
                    },
                  ]}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  innerRadius={72}
                  outerRadius={100}
                  paddingAngle={4}
                  stroke="none"
                  animationDuration={900}
                >
                  <Cell fill="#ef4444" />
                  <Cell fill="#f97316" />
                  <Cell fill="#eab308" />
                  <Cell fill="#10b981" />
                </Pie>

                <Tooltip
                  contentStyle={{
                    background: "#0b1729",
                    border: "1px solid rgba(255,255,255,0.1)",
                    borderRadius: "12px",
                    color: "#fff",
                    boxShadow: "0 10px 30px rgba(0,0,0,0.35)",
                  }}
                />
              </PieChart>
            </ResponsiveContainer>

            {/* Center Text */}
            <div className="pointer-events-none absolute inset-0 flex items-center justify-center">
              <div className="text-center">
                <p className="text-3xl font-bold tracking-tight text-white">
                  {statistics.total}
                </p>

                <p className="mt-1 text-[10px] uppercase tracking-[0.18em] text-slate-500">
                  Total Tasks
                </p>
              </div>
            </div>
          </div>

          {/* Priority Legend */}
          <div className="space-y-3">
            <PriorityItem
              label="Critical"
              value={statistics.critical}
              color="bg-red-500"
              percentage={
                statistics.total
                  ? ((statistics.critical / statistics.total) * 100).toFixed(1)
                  : 0
              }
            />

            <PriorityItem
              label="High"
              value={statistics.high}
              color="bg-orange-500"
              percentage={
                statistics.total
                  ? ((statistics.high / statistics.total) * 100).toFixed(1)
                  : 0
              }
            />

            <PriorityItem
              label="Medium"
              value={statistics.medium}
              color="bg-yellow-400"
              percentage={
                statistics.total
                  ? ((statistics.medium / statistics.total) * 100).toFixed(1)
                  : 0
              }
            />

            <PriorityItem
              label="Low"
              value={statistics.low}
              color="bg-emerald-500"
              percentage={
                statistics.total
                  ? ((statistics.low / statistics.total) * 100).toFixed(1)
                  : 0
              }
            />
          </div>
        </div>
      </motion.div>

      {/* Filters */}
      <div className="rounded-2xl border border-white/10 bg-white/[0.035] p-4">
        <div className="flex flex-col gap-3 lg:flex-row">
          {/* Search */}
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" />

            <input
              type="text"
              placeholder="Search task, asset or maintenance type..."
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              className="w-full rounded-xl border border-white/10 bg-black/10 py-2.5 pl-10 pr-4 text-sm text-white outline-none transition placeholder:text-slate-600 focus:border-blue-400/30 focus:ring-2 focus:ring-blue-400/10"
            />
          </div>

          {/* Priority */}
          <div className="relative">
            <Filter className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" />

            <select
              value={priority}
              onChange={(event) => setPriority(event.target.value)}
              className="w-full appearance-none rounded-xl border border-white/10 bg-[#0a1628] py-2.5 pl-10 pr-10 text-sm text-slate-300 outline-none focus:border-blue-400/30 sm:w-48"
            >
              <option value="All">All priorities</option>
              <option value="Critical">Critical</option>
              <option value="High">High</option>
              <option value="Medium">Medium</option>
              <option value="Low">Low</option>
            </select>

            <ChevronDown className="pointer-events-none absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" />
          </div>

          {/* Status */}
          <div className="relative">
            <select
              value={status}
              onChange={(event) => setStatus(event.target.value)}
              className="w-full appearance-none rounded-xl border border-white/10 bg-[#0a1628] px-4 py-2.5 pr-10 text-sm text-slate-300 outline-none focus:border-blue-400/30 sm:w-44"
            >
              <option value="All">All statuses</option>
              <option value="Pending">Pending</option>
              <option value="Approved">Approved</option>
              <option value="Completed">Completed</option>
            </select>

            <ChevronDown className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-slate-500" />
          </div>
        </div>
      </div>

      {/* Table */}
      <div className="overflow-hidden rounded-2xl border border-white/10 bg-white/[0.035]">
        <div className="flex items-center justify-between border-b border-white/10 px-5 py-4">
          <div>
            <h2 className="text-sm font-semibold text-white">
              Maintenance Tasks
            </h2>

            <p className="mt-1 text-xs text-slate-500">
              Showing {filteredTasks.length} of {tasks.length} tasks
            </p>
          </div>
        </div>

        {loading ? (
          <div className="space-y-3 p-5">
            {[1, 2, 3, 4, 5].map((item) => (
              <div
                key={item}
                className="h-14 animate-pulse rounded-xl bg-white/5"
              />
            ))}
          </div>
        ) : error ? (
          <div className="p-10 text-center">
            <AlertTriangle className="mx-auto h-8 w-8 text-red-400" />
            <p className="mt-3 text-sm text-slate-300">{error}</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full min-w-[900px] text-left">
              <thead>
                <tr className="border-b border-white/10 text-[10px] uppercase tracking-wider text-slate-500">
                  <th className="px-5 py-4 font-medium">Task</th>
                  <th className="px-5 py-4 font-medium">Asset</th>
                  <th className="px-5 py-4 font-medium">Type</th>
                  <th className="px-5 py-4 font-medium">Priority</th>
                  <th className="px-5 py-4 font-medium">AI Score</th>
                  <th className="px-5 py-4 font-medium">Due Date</th>
                  <th className="px-5 py-4 font-medium">Duration</th>
                  <th className="px-5 py-4 font-medium">Status</th>
                </tr>
              </thead>

              <tbody>
                {filteredTasks.slice(0, 100).map((task, index) => {
                  const config =
                    priorityConfig[task.priority_level] ||
                    priorityConfig.Medium;

                  const Icon = config.icon;

                  return (
                    <motion.tr
                      key={task.task_id}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: Math.min(index * 0.015, 0.4) }}
                      className="border-b border-white/5 transition-colors hover:bg-white/[0.025]"
                    >
                      <td className="px-5 py-4">
                        <span className="font-mono text-xs font-medium text-blue-300">
                          {task.task_id}
                        </span>
                      </td>

                      <td className="px-5 py-4 text-sm text-slate-300">
                        {task.asset_id}
                      </td>

                      <td className="px-5 py-4 text-sm text-slate-400">
                        {task.task_type}
                      </td>

                      <td className="px-5 py-4">
                        <span
                          className={`inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-[11px] font-medium ${config.className}`}
                        >
                          <Icon className="h-3 w-3" />
                          {task.priority_level}
                        </span>
                      </td>

                      <td className="px-5 py-4">
                        <div className="flex items-center gap-3">
                          <div className="h-1.5 w-20 overflow-hidden rounded-full bg-white/10">
                            <div
                              className="h-full rounded-full bg-blue-400"
                              style={{
                                width: `${Math.min(
                                  task.priority_score || 0,
                                  100,
                                )}%`,
                              }}
                            />
                          </div>

                          <span className="font-mono text-xs text-slate-300">
                            {Number(task.priority_score || 0).toFixed(1)}
                          </span>
                        </div>
                      </td>

                      <td className="px-5 py-4 text-xs text-slate-400">
                        {task.due_date}
                      </td>

                      <td className="px-5 py-4 text-xs text-slate-400">
                        {task.estimated_duration_hours} hrs
                      </td>

                      <td className="px-5 py-4">
                        <span className="rounded-full bg-white/5 px-2.5 py-1 text-[11px] text-slate-400">
                          {task.status}
                        </span>
                      </td>
                    </motion.tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}

        {!loading && !error && filteredTasks.length === 0 && (
          <div className="p-10 text-center">
            <Search className="mx-auto h-8 w-8 text-slate-600" />
            <p className="mt-3 text-sm text-slate-400">
              No maintenance tasks match your filters.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
function PriorityItem({ label, value, color, percentage }) {
  return (
    <div className="rounded-xl border border-white/5 bg-black/10 p-3 transition hover:border-white/10 hover:bg-white/[0.03]">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className={`h-2.5 w-2.5 rounded-full ${color}`} />

          <span className="text-sm font-medium text-slate-300">{label}</span>
        </div>

        <span className="text-sm font-bold text-white">{value}</span>
      </div>

      <div className="mt-2 flex items-center justify-between">
        <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-white/5">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${percentage}%` }}
            transition={{ duration: 0.8 }}
            className={`h-full rounded-full ${color}`}
          />
        </div>

        <span className="ml-3 w-10 text-right text-[10px] text-slate-500">
          {percentage}%
        </span>
      </div>
    </div>
  );
}
export default Maintenance;
