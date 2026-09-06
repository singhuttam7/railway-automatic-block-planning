import { useEffect, useMemo, useState } from "react";
import { motion } from "framer-motion";
import {
  Route,
  MapPin,
  Ruler,
  Search,
  RefreshCw,
  Activity,
  ArrowRight,
} from "lucide-react";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

function Corridors() {
  const [corridors, setCorridors] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchCorridors = () => {
    setLoading(true);
    setError(null);

    fetch(`${API_URL}/api/corridors/`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Unable to load corridor data");
        }
        return response.json();
      })
      .then((data) => setCorridors(data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchCorridors();
  }, []);

  const filteredCorridors = useMemo(() => {
    return corridors.filter((corridor) => {
      const value = search.toLowerCase();

      return (
        corridor.corridor_id?.toLowerCase().includes(value) ||
        corridor.corridor_name?.toLowerCase().includes(value)
      );
    });
  }, [corridors, search]);

  const totalLength = corridors.reduce(
    (sum, corridor) =>
      sum + Number(corridor.end_km || 0) - Number(corridor.start_km || 0),
    0,
  );

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
              <Route className="h-4 w-4 text-blue-400" />
              <span className="text-xs font-medium uppercase tracking-[0.18em] text-blue-400">
                Railway Network
              </span>
            </div>

            <h1 className="text-2xl font-bold tracking-tight text-white sm:text-3xl">
              Corridor Management
            </h1>

            <p className="mt-2 max-w-2xl text-sm text-slate-400">
              Monitor railway corridors and their geographic maintenance
              planning boundaries.
            </p>
          </div>

          <button
            onClick={fetchCorridors}
            className="flex w-fit items-center gap-2 rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-sm text-slate-300 transition hover:border-blue-400/20 hover:bg-blue-400/10 hover:text-white"
          >
            <RefreshCw className="h-4 w-4" />
            Refresh
          </button>
        </div>
      </motion.div>

      {/* Summary */}
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          className="rounded-2xl border border-white/10 bg-white/[0.035] p-5"
        >
          <div className="flex items-center justify-between">
            <p className="text-xs text-slate-500">Active Corridors</p>
            <Route className="h-4 w-4 text-blue-400" />
          </div>

          <p className="mt-3 text-3xl font-bold text-white">
            {corridors.length}
          </p>

          <p className="mt-2 text-xs text-slate-500">
            Network corridors available for planning
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.08 }}
          className="rounded-2xl border border-white/10 bg-white/[0.035] p-5"
        >
          <div className="flex items-center justify-between">
            <p className="text-xs text-slate-500">Network Coverage</p>
            <Ruler className="h-4 w-4 text-cyan-400" />
          </div>

          <p className="mt-3 text-3xl font-bold text-white">
            {totalLength.toFixed(0)}
            <span className="ml-1 text-base font-medium text-slate-500">
              km
            </span>
          </p>

          <p className="mt-2 text-xs text-slate-500">
            Combined corridor planning distance
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.16 }}
          className="rounded-2xl border border-emerald-400/10 bg-emerald-400/[0.035] p-5 sm:col-span-2 xl:col-span-1"
        >
          <div className="flex items-center justify-between">
            <p className="text-xs text-slate-500">Planning Status</p>
            <Activity className="h-4 w-4 text-emerald-400" />
          </div>

          <p className="mt-3 text-xl font-bold text-emerald-400">
            Optimization Ready
          </p>

          <p className="mt-2 text-xs text-slate-500">
            Corridor data is available to the block optimization engine.
          </p>
        </motion.div>
      </div>

      {/* Search */}
      <div className="rounded-2xl border border-white/10 bg-white/[0.035] p-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" />

          <input
            type="text"
            placeholder="Search corridor..."
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            className="w-full rounded-xl border border-white/10 bg-black/10 py-2.5 pl-10 pr-4 text-sm text-white outline-none transition placeholder:text-slate-600 focus:border-blue-400/30 focus:ring-2 focus:ring-blue-400/10"
          />
        </div>
      </div>

      {/* Corridor cards */}
      {loading ? (
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {[1, 2, 3, 4, 5].map((item) => (
            <div
              key={item}
              className="h-56 animate-pulse rounded-2xl bg-white/5"
            />
          ))}
        </div>
      ) : error ? (
        <div className="rounded-2xl border border-red-400/20 bg-red-400/5 p-10 text-center">
          <Activity className="mx-auto h-8 w-8 text-red-400" />
          <p className="mt-3 text-sm text-slate-300">{error}</p>
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {filteredCorridors.map((corridor, index) => {
            const start = Number(corridor.start_km);
            const end = Number(corridor.end_km);
            const length = end - start;

            return (
              <motion.div
                key={corridor.corridor_id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: Math.min(index * 0.08, 0.4) }}
                whileHover={{ y: -4 }}
                className="group overflow-hidden rounded-2xl border border-white/10 bg-white/[0.035] transition-colors duration-300 hover:border-blue-400/20 hover:bg-white/[0.05]"
              >
                {/* Card header */}
                <div className="flex items-start justify-between border-b border-white/10 p-5">
                  <div className="flex items-center gap-3">
                    <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-500/10 ring-1 ring-blue-400/10">
                      <Route className="h-5 w-5 text-blue-400" />
                    </div>

                    <div>
                      <p className="font-mono text-xs text-blue-300">
                        {corridor.corridor_id}
                      </p>

                      <h2 className="mt-1 font-semibold text-white">
                        {corridor.corridor_name || "Railway Corridor"}
                      </h2>
                    </div>
                  </div>

                  <span className="rounded-full border border-emerald-400/20 bg-emerald-400/10 px-2.5 py-1 text-[10px] font-medium text-emerald-300">
                    ACTIVE
                  </span>
                </div>

                {/* Route visualization */}
                <div className="p-5">
                  <div className="relative py-5">
                    <div className="absolute left-3 right-3 top-1/2 h-px bg-white/10" />

                    <div className="relative flex items-center justify-between">
                      <div className="flex flex-col items-start gap-2">
                        <div className="flex h-7 w-7 items-center justify-center rounded-full bg-blue-500/15 ring-4 ring-[#0d192a]">
                          <MapPin className="h-3.5 w-3.5 text-blue-400" />
                        </div>

                        <div>
                          <p className="text-[10px] uppercase tracking-wider text-slate-600">
                            Start
                          </p>
                          <p className="font-mono text-xs text-slate-300">
                            KM {start}
                          </p>
                        </div>
                      </div>

                      <div className="z-10 rounded-full border border-white/10 bg-[#0d192a] px-3 py-1.5">
                        <span className="font-mono text-[10px] text-slate-500">
                          {length} KM
                        </span>
                      </div>

                      <div className="flex flex-col items-end gap-2">
                        <div className="flex h-7 w-7 items-center justify-center rounded-full bg-cyan-500/15 ring-4 ring-[#0d192a]">
                          <MapPin className="h-3.5 w-3.5 text-cyan-400" />
                        </div>

                        <div className="text-right">
                          <p className="text-[10px] uppercase tracking-wider text-slate-600">
                            End
                          </p>
                          <p className="font-mono text-xs text-slate-300">
                            KM {end}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="mt-4 flex items-center justify-between border-t border-white/5 pt-4">
                    <div>
                      <p className="text-[10px] uppercase tracking-wider text-slate-600">
                        Planning Segment
                      </p>

                      <p className="mt-1 text-xs text-slate-400">
                        KM {start} → KM {end}
                      </p>
                    </div>

                    <ArrowRight className="h-4 w-4 text-slate-600 transition group-hover:translate-x-1 group-hover:text-blue-400" />
                  </div>
                </div>
              </motion.div>
            );
          })}
        </div>
      )}

      {!loading && !error && filteredCorridors.length === 0 && (
        <div className="rounded-2xl border border-white/10 bg-white/[0.035] p-10 text-center">
          <Search className="mx-auto h-8 w-8 text-slate-600" />
          <p className="mt-3 text-sm text-slate-400">
            No corridors match your search.
          </p>
        </div>
      )}
    </div>
  );
}

export default Corridors;
