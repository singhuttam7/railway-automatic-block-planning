import { useEffect, useMemo, useState } from "react";
import { motion } from "framer-motion";
import {
  TrainFront,
  Package,
  Search,
  RefreshCw,
  Route,
  Clock3,
  TrendingUp,
} from "lucide-react";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

function TrainsForecast() {
  const [trains, setTrains] = useState([]);
  const [forecasts, setForecasts] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [search, setSearch] = useState("");
  const [corridorFilter, setCorridorFilter] = useState("All");
  const [trainTypeFilter, setTrainTypeFilter] = useState("All");

  const fetchData = async () => {
    try {
      setLoading(true);
      setError("");

      const [trainsResponse, forecastsResponse] = await Promise.all([
        fetch(`${API_URL}/api/trains/`),
        fetch(`${API_URL}/api/goods-forecasts/`),
      ]);

      if (!trainsResponse.ok || !forecastsResponse.ok) {
        throw new Error("Unable to load train and forecast data");
      }

      const [trainsData, forecastsData] = await Promise.all([
        trainsResponse.json(),
        forecastsResponse.json(),
      ]);

      setTrains(trainsData);
      setForecasts(forecastsData);
    } catch (err) {
      console.error(err);
      setError("Unable to connect to railway operations data.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const corridors = useMemo(() => {
    return ["All", ...new Set(trains.map((train) => train.corridor_id))];
  }, [trains]);

  const trainTypes = useMemo(() => {
    return ["All", ...new Set(trains.map((train) => train.train_type))];
  }, [trains]);

  const filteredTrains = useMemo(() => {
    return trains
      .filter((train) => {
        const matchesSearch =
          train.train_id?.toLowerCase().includes(search.toLowerCase()) ||
          train.train_number?.toLowerCase().includes(search.toLowerCase());

        const matchesCorridor =
          corridorFilter === "All" || train.corridor_id === corridorFilter;

        const matchesType =
          trainTypeFilter === "All" || train.train_type === trainTypeFilter;

        return matchesSearch && matchesCorridor && matchesType;
      })
      .slice(0, 50);
  }, [trains, search, corridorFilter, trainTypeFilter]);

  const filteredForecasts = useMemo(() => {
    return forecasts
      .filter((forecast) => {
        return (
          corridorFilter === "All" || forecast.corridor_id === corridorFilter
        );
      })
      .slice(0, 30);
  }, [forecasts, corridorFilter]);

  const goodsTrains = trains.filter(
    (train) => train.train_type === "Goods",
  ).length;

  const totalExpectedGoods = forecasts.reduce(
    (sum, forecast) => sum + Number(forecast.expected_goods_trains || 0),
    0,
  );

  const activeCorridors = new Set(trains.map((train) => train.corridor_id))
    .size;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col justify-between gap-4 lg:flex-row lg:items-end">
        <div>
          <div className="mb-2 flex items-center gap-2 text-xs uppercase tracking-[0.18em] text-blue-400">
            <TrainFront size={15} />
            Traffic Intelligence
          </div>

          <h1 className="text-3xl font-bold tracking-tight text-white">
            Trains & Goods Forecast
          </h1>

          <p className="mt-2 max-w-2xl text-sm text-slate-400">
            Monitor train movements and forecasted goods traffic to support
            conflict-aware railway block planning.
          </p>
        </div>

        <button
          onClick={fetchData}
          className="inline-flex items-center justify-center gap-2 rounded-xl border border-white/10 bg-white/[0.04] px-4 py-2.5 text-sm font-medium text-slate-200 transition hover:bg-white/[0.08]"
        >
          <RefreshCw size={16} />
          Refresh Data
        </button>
      </div>

      {/* KPI Cards */}
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <KpiCard
          icon={<TrainFront size={19} />}
          label="Total Trains"
          value={trains.length}
          description="Scheduled movements"
        />

        <KpiCard
          icon={<Package size={19} />}
          label="Goods Trains"
          value={goodsTrains}
          description="From timetable data"
        />

        <KpiCard
          icon={<TrendingUp size={19} />}
          label="Forecast Goods"
          value={totalExpectedGoods}
          description="Expected movements"
        />

        <KpiCard
          icon={<Route size={19} />}
          label="Active Corridors"
          value={activeCorridors}
          description="Operational corridors"
        />
      </div>

      {/* Error */}
      {error && (
        <div className="rounded-xl border border-red-400/20 bg-red-400/5 p-4 text-sm text-red-300">
          {error}
        </div>
      )}

      {/* Filters */}
      <div className="rounded-2xl border border-white/10 bg-white/[0.025] p-4">
        <div className="grid gap-3 lg:grid-cols-[1fr_auto_auto]">
          <div className="relative">
            <Search
              size={17}
              className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500"
            />

            <input
              type="text"
              placeholder="Search train ID or train number..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full rounded-xl border border-white/10 bg-black/10 py-2.5 pl-10 pr-4 text-sm text-white outline-none placeholder:text-slate-600 focus:border-blue-400/40"
            />
          </div>

          <select
            value={corridorFilter}
            onChange={(e) => setCorridorFilter(e.target.value)}
            className="rounded-xl border border-white/10 bg-[#0b1729] px-4 py-2.5 text-sm text-slate-300 outline-none"
          >
            {corridors.map((corridor) => (
              <option key={corridor} value={corridor}>
                Corridor: {corridor}
              </option>
            ))}
          </select>

          <select
            value={trainTypeFilter}
            onChange={(e) => setTrainTypeFilter(e.target.value)}
            className="rounded-xl border border-white/10 bg-[#0b1729] px-4 py-2.5 text-sm text-slate-300 outline-none"
          >
            {trainTypes.map((type) => (
              <option key={type} value={type}>
                Type: {type}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid gap-6 xl:grid-cols-[1.5fr_1fr] xl:h-[720px]">
        {/* Train Schedule */}
        <section className="flex min-h-0 min-w-0 flex-col overflow-hidden rounded-2xl border border-white/10 bg-white/[0.025]">
          <div className="flex items-center justify-between border-b border-white/10 px-5 py-4">
            <div>
              <h2 className="font-semibold text-white">Train Schedule</h2>
              <p className="mt-1 text-xs text-slate-500">
                Showing {filteredTrains.length} movements
              </p>
            </div>

            <div className="rounded-lg bg-blue-400/10 p-2 text-blue-300">
              <TrainFront size={18} />
            </div>
          </div>

          {loading ? (
            <div className="space-y-3 p-5">
              {[1, 2, 3, 4, 5].map((item) => (
                <div
                  key={item}
                  className="h-16 animate-pulse rounded-xl bg-white/[0.04]"
                />
              ))}
            </div>
          ) : (
            <div className="min-h-0 flex-1 overflow-auto">
              <table className="w-full min-w-[720px] text-left">
                <thead>
                  <tr className="border-b border-white/10 text-[11px] uppercase tracking-wider text-slate-500">
                    <th className="px-5 py-3">Train</th>
                    <th className="px-5 py-3">Corridor</th>
                    <th className="px-5 py-3">Type</th>
                    <th className="px-5 py-3">Date</th>
                    <th className="px-5 py-3">Time Window</th>
                  </tr>
                </thead>

                <tbody>
                  {filteredTrains.map((train, index) => (
                    <motion.tr
                      key={train.train_id}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{
                        delay: Math.min(index * 0.01, 0.3),
                      }}
                      className="border-b border-white/5 transition hover:bg-white/[0.03]"
                    >
                      <td className="px-5 py-4">
                        <div className="font-mono text-sm font-medium text-blue-300">
                          {train.train_id}
                        </div>
                        <div className="mt-1 text-xs text-slate-500">
                          #{train.train_number}
                        </div>
                      </td>

                      <td className="px-5 py-4">
                        <span className="rounded-lg bg-white/[0.05] px-2.5 py-1 text-xs font-medium text-slate-300">
                          {train.corridor_id}
                        </span>
                      </td>

                      <td className="px-5 py-4">
                        <TrainTypeBadge type={train.train_type} />
                      </td>

                      <td className="px-5 py-4 text-xs text-slate-400">
                        {train.date}
                      </td>

                      <td className="px-5 py-4">
                        <div className="flex items-center gap-2 text-xs text-slate-300">
                          <Clock3 size={14} className="text-slate-500" />
                          {train.start_time} – {train.end_time}
                        </div>
                      </td>
                    </motion.tr>
                  ))}
                </tbody>
              </table>

              {filteredTrains.length === 0 && (
                <div className="p-10 text-center text-sm text-slate-500">
                  No trains match the selected filters.
                </div>
              )}
            </div>
          )}
        </section>

        {/* Goods Forecast */}
        <section className="flex min-h-0 min-w-0 flex-col overflow-hidden rounded-2xl border border-white/10 bg-white/[0.025]">
          <div className="flex items-center justify-between border-b border-white/10 px-5 py-4">
            <div>
              <h2 className="font-semibold text-white">Goods Train Forecast</h2>
              <p className="mt-1 text-xs text-slate-500">
                Expected freight movements
              </p>
            </div>

            <div className="rounded-lg bg-amber-400/10 p-2 text-amber-300">
              <Package size={18} />
            </div>
          </div>

          <div className="min-h-0 flex-1 overflow-y-auto">
            <div className="space-y-3 p-4">
              {filteredForecasts.map((forecast, index) => (
                <motion.div
                  key={forecast.forecast_id}
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{
                    delay: Math.min(index * 0.015, 0.3),
                  }}
                  className="rounded-xl border border-white/10 bg-black/10 p-4 transition hover:border-white/15 hover:bg-white/[0.03]"
                >
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <p className="font-mono text-xs text-blue-300">
                        {forecast.forecast_id}
                      </p>

                      <p className="mt-1 text-sm font-medium text-white">
                        {forecast.corridor_id}
                      </p>
                    </div>

                    <div className="rounded-lg bg-amber-400/10 px-2.5 py-1.5 text-right">
                      <p className="text-lg font-bold text-amber-300">
                        {forecast.expected_goods_trains}
                      </p>
                      <p className="text-[9px] uppercase tracking-wider text-amber-400/70">
                        Expected
                      </p>
                    </div>
                  </div>

                  <div className="mt-4 flex items-center justify-between text-xs text-slate-500">
                    <span>{forecast.date}</span>

                    <span>
                      {forecast.start_time} – {forecast.end_time}
                    </span>
                  </div>

                  <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-white/5">
                    <div
                      className="h-full rounded-full bg-amber-400/70"
                      style={{
                        width: `${Math.min(
                          Number(forecast.expected_goods_trains) * 12,
                          100,
                        )}%`,
                      }}
                    />
                  </div>
                </motion.div>
              ))}

              {!loading && filteredForecasts.length === 0 && (
                <div className="py-10 text-center text-sm text-slate-500">
                  No forecast data available.
                </div>
              )}
            </div>
          </div>
        </section>
      </div>

      {/* Planning Intelligence */}
      <div className="rounded-2xl border border-blue-400/15 bg-blue-400/[0.04] p-5">
        <div className="flex items-start gap-4">
          <div className="rounded-xl bg-blue-400/10 p-3 text-blue-300">
            <TrendingUp size={20} />
          </div>

          <div>
            <h3 className="font-semibold text-white">
              Traffic-aware Block Planning
            </h3>

            <p className="mt-1 max-w-3xl text-sm leading-6 text-slate-400">
              Train timetable and goods-train forecasts provide traffic context
              for the optimization engine. Maintenance blocks can therefore be
              planned around operationally sensitive periods instead of treating
              maintenance requests independently.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

function KpiCard({ icon, label, value, description }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-2xl border border-white/10 bg-white/[0.025] p-5"
    >
      <div className="flex items-start justify-between">
        <div className="rounded-xl bg-blue-400/10 p-2.5 text-blue-300">
          {icon}
        </div>
      </div>

      <p className="mt-5 text-2xl font-bold text-white">
        {value.toLocaleString()}
      </p>

      <p className="mt-1 text-sm font-medium text-slate-300">{label}</p>

      <p className="mt-1 text-xs text-slate-500">{description}</p>
    </motion.div>
  );
}

function TrainTypeBadge({ type }) {
  const classes = {
    Goods: "bg-amber-400/10 text-amber-300",
    Express: "bg-blue-400/10 text-blue-300",
    Passenger: "bg-emerald-400/10 text-emerald-300",
    Special: "bg-purple-400/10 text-purple-300",
  };

  return (
    <span
      className={`rounded-full px-2.5 py-1 text-xs font-medium ${
        classes[type] || "bg-white/5 text-slate-300"
      }`}
    >
      {type}
    </span>
  );
}

export default TrainsForecast;
