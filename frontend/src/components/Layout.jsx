import { useState } from "react";
import { NavLink, Outlet } from "react-router-dom";
import {
  LayoutDashboard,
  Wrench,
  Route,
  CalendarClock,
  TrainFront,
  BrainCircuit,
  Menu,
  X,
  Activity,
  ChevronRight,
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

const navigation = [
  {
    name: "Dashboard",
    path: "/",
    icon: LayoutDashboard,
  },
  {
    name: "Maintenance",
    path: "/maintenance",
    icon: Wrench,
  },
  {
    name: "Corridors",
    path: "/corridors",
    icon: Route,
  },
  {
    name: "Block Planning",
    path: "/blocks",
    icon: CalendarClock,
  },
  {
    name: "Trains & Forecast",
    path: "/trains",
    icon: TrainFront,
  },
  {
    name: "AI Intelligence",
    path: "/ai-intelligence",
    icon: BrainCircuit,
  },
];

function Layout() {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <div className="min-h-screen bg-[#07111f] text-slate-100">
      {/* Desktop Sidebar */}
      <aside className="fixed inset-y-0 left-0 z-40 hidden w-64 border-r border-white/10 bg-[#0a1628]/95 backdrop-blur-xl lg:block">
        <div className="flex h-full flex-col">
          {/* Logo */}
          <div className="flex h-20 items-center gap-3 border-b border-white/10 px-6">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-500/15 ring-1 ring-blue-400/20">
              <TrainFront className="h-5 w-5 text-blue-400" />
            </div>

            <div>
              <h1 className="text-sm font-bold tracking-wide">
                RAIL<span className="text-blue-400">OPTIMA</span>
              </h1>
              <p className="text-[10px] uppercase tracking-[0.2em] text-slate-500">
                Block Intelligence
              </p>
            </div>
          </div>

          {/* Navigation */}
          <nav className="flex-1 space-y-1 px-3 py-6">
            <p className="mb-3 px-3 text-[10px] font-semibold uppercase tracking-[0.2em] text-slate-500">
              Operations
            </p>

            {navigation.map((item) => {
              const Icon = item.icon;

              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  className={({ isActive }) =>
                    `group flex items-center gap-3 rounded-xl px-3 py-3 text-sm transition-all duration-200 ${
                      isActive
                        ? "bg-blue-500/15 text-blue-300 ring-1 ring-blue-400/20"
                        : "text-slate-400 hover:bg-white/5 hover:text-slate-100"
                    }`
                  }
                  onClick={() => setMobileOpen(false)}
                >
                  <Icon className="h-4 w-4 shrink-0" />

                  <span className="flex-1">{item.name}</span>

                  <ChevronRight className="h-3.5 w-3.5 opacity-0 transition group-hover:opacity-50" />
                </NavLink>
              );
            })}
          </nav>

          {/* System Status */}
          <div className="m-4 rounded-2xl border border-emerald-400/10 bg-emerald-400/5 p-4">
            <div className="mb-2 flex items-center gap-2">
              <span className="relative flex h-2 w-2">
                <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-60" />
                <span className="relative inline-flex h-2 w-2 rounded-full bg-emerald-400" />
              </span>

              <span className="text-xs font-medium text-emerald-300">
                System Operational
              </span>
            </div>

            <p className="text-[11px] leading-relaxed text-slate-500">
              Optimization engine and railway data services are online.
            </p>
          </div>
        </div>
      </aside>

      {/* Mobile Sidebar */}
      <AnimatePresence>
        {mobileOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 z-40 bg-black/60 backdrop-blur-sm lg:hidden"
              onClick={() => setMobileOpen(false)}
            />

            <motion.aside
              initial={{ x: -280 }}
              animate={{ x: 0 }}
              exit={{ x: -280 }}
              transition={{ duration: 0.25 }}
              className="fixed inset-y-0 left-0 z-50 w-72 border-r border-white/10 bg-[#0a1628]"
            >
              <div className="flex h-full flex-col">
                <div className="flex h-20 items-center justify-between border-b border-white/10 px-5">
                  <div className="flex items-center gap-3">
                    <TrainFront className="h-6 w-6 text-blue-400" />
                    <span className="font-bold">
                      RAIL<span className="text-blue-400">OPTIMA</span>
                    </span>
                  </div>

                  <button
                    onClick={() => setMobileOpen(false)}
                    className="rounded-lg p-2 text-slate-400 hover:bg-white/5 hover:text-white"
                  >
                    <X className="h-5 w-5" />
                  </button>
                </div>

                <nav className="space-y-1 px-3 py-6">
                  {navigation.map((item) => {
                    const Icon = item.icon;

                    return (
                      <NavLink
                        key={item.path}
                        to={item.path}
                        onClick={() => setMobileOpen(false)}
                        className={({ isActive }) =>
                          `flex items-center gap-3 rounded-xl px-3 py-3 text-sm ${
                            isActive
                              ? "bg-blue-500/15 text-blue-300"
                              : "text-slate-400 hover:bg-white/5 hover:text-white"
                          }`
                        }
                      >
                        <Icon className="h-4 w-4" />
                        {item.name}
                      </NavLink>
                    );
                  })}
                </nav>
              </div>
            </motion.aside>
          </>
        )}
      </AnimatePresence>

      {/* Main Area */}
      <div className="lg:pl-64">
        {/* Top Header */}
        <header className="sticky top-0 z-30 flex h-20 items-center justify-between border-b border-white/10 bg-[#07111f]/80 px-4 backdrop-blur-xl sm:px-6 lg:px-8">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setMobileOpen(true)}
              className="rounded-xl border border-white/10 bg-white/5 p-2.5 text-slate-300 lg:hidden"
            >
              <Menu className="h-5 w-5" />
            </button>

            <div>
              <p className="hidden text-xs text-slate-500 sm:block">
                Railway Operations Control
              </p>

              <div className="flex items-center gap-2">
                <Activity className="h-4 w-4 text-blue-400" />
                <span className="text-sm font-semibold text-slate-200">
                  Intelligent Block Planning
                </span>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="hidden rounded-full border border-white/10 bg-white/5 px-3 py-1.5 text-xs text-slate-400 sm:block">
              AI Engine <span className="text-emerald-400">● Online</span>
            </div>

            <div className="flex h-9 w-9 items-center justify-center rounded-full bg-blue-500/15 text-xs font-bold text-blue-300 ring-1 ring-blue-400/20">
              RO
            </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="min-h-[calc(100vh-5rem)] p-4 sm:p-6 lg:p-8">
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.35 }}
          >
            <Outlet />
          </motion.div>
        </main>
      </div>
    </div>
  );
}

export default Layout;
