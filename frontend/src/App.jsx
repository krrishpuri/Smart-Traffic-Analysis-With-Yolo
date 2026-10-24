
// import { useEffect, useState } from 'react'
// import {
//   Activity,
//   CarFront,
//   Gauge,
//   TriangleAlert,
//   Radio,
//   LayoutDashboard,
//   Video,
//   ChartNoAxesCombined,
//   Settings,
//   Wifi,
//   RefreshCw,
//   Bus,
//   Bike,
//   Truck,
//   ShieldCheck,
// } from 'lucide-react'

// import { getTrafficSummary, getHealth } from './services/api'
// import './App.css'

// const initialTraffic = {
//   vehicles_detected: 0,
//   cars: 0,
//   motorcycles: 0,
//   buses: 0,
//   trucks: 0,
//   density: 'LOW',
//   average_speed: null,
//   violations: 0,
// }

// function App() {
//   const [traffic, setTraffic] = useState(initialTraffic)
//   const [connected, setConnected] = useState(false)
//   const [loading, setLoading] = useState(true)
//   const [error, setError] = useState('')
//   const [lastUpdated, setLastUpdated] = useState(null)

//   const fetchTraffic = async () => {
//     try {
//       const [summary, health] = await Promise.all([
//         getTrafficSummary(),
//         getHealth(),
//       ])

//       setTraffic({ ...initialTraffic, ...summary })
//       setConnected(health.status === 'healthy')
//       setError('')
//       setLastUpdated(new Date())
//     } catch (err) {
//       setConnected(false)
//       setError(
//         err.response?.data?.detail ||
//           'Unable to connect to FastAPI. Check whether the backend is running.'
//       )
//     } finally {
//       setLoading(false)
//     }
//   }

//   useEffect(() => {
//     fetchTraffic()

//     // Refresh API data every 3 seconds.
//     const interval = setInterval(fetchTraffic, 3000)

//     return () => clearInterval(interval)
//   }, [])

//   const stats = [
//     {
//       title: 'Vehicles Detected',
//       value: traffic.vehicles_detected ?? 0,
//       detail: 'Unique tracked vehicles',
//       icon: CarFront,
//       color: 'text-cyan-400',
//     },
//     {
//       title: 'Traffic Density',
//       value: traffic.density ?? 'LOW',
//       detail: 'Current traffic level',
//       icon: Activity,
//       color: 'text-emerald-400',
//     },
//     {
//       title: 'Average Speed',
//       value:
//         traffic.average_speed == null
//           ? '--'
//           : `${Number(traffic.average_speed).toFixed(1)} km/h`,
//       detail: 'Estimated vehicle speed',
//       icon: Gauge,
//       color: 'text-violet-400',
//     },
//     {
//       title: 'Violations',
//       value: traffic.violations ?? 0,
//       detail: 'Reported traffic violations',
//       icon: TriangleAlert,
//       color: 'text-rose-400',
//     },
//   ]

//   const vehicleTypes = [
//     { name: 'Cars', value: traffic.cars, icon: CarFront },
//     { name: 'Motorcycles', value: traffic.motorcycles, icon: Bike },
//     { name: 'Buses', value: traffic.buses, icon: Bus },
//     { name: 'Trucks', value: traffic.trucks, icon: Truck },
//   ]

//   return (
//     <div className="min-h-screen bg-[#080d18] text-slate-200 md:flex">
//       {/* Sidebar */}
//       <aside className="border-b border-slate-800 p-5 md:min-h-screen md:w-64 md:shrink-0 md:border-b-0 md:border-r">
//         <div className="flex items-center gap-3">
//           <div className="rounded-xl bg-cyan-400/10 p-3 text-cyan-400">
//             <Activity size={25} />
//           </div>

//           <div>
//             <h1 className="font-bold text-white">TrafficAI</h1>
//             <p className="text-xs text-slate-500">
//               Intelligent Monitoring
//             </p>
//           </div>
//         </div>

//         <nav className="mt-8 flex gap-2 overflow-x-auto md:flex-col">
//           {[
//             { label: 'Overview', icon: LayoutDashboard },
//             { label: 'Live Monitoring', icon: Video },
//             { label: 'Analytics', icon: ChartNoAxesCombined },
//             { label: 'Violations', icon: TriangleAlert },
//             { label: 'Settings', icon: Settings },
//           ].map(({ label, icon: Icon }, index) => (
//             <button
//               type="button"
//               key={label}
//               onClick={() => {
//                 document
//                   .getElementById(
//                     ['overview', 'monitoring', 'analytics', 'violations', 'settings'][index]
//                   )
//                   ?.scrollIntoView({ behavior: 'smooth' })
//               }}
//               className={`flex shrink-0 items-center gap-3 rounded-lg px-4 py-3 text-sm transition ${
//                 index === 0
//                   ? 'bg-cyan-400/10 text-cyan-300'
//                   : 'text-slate-400 hover:bg-slate-800 hover:text-white'
//               }`}
//             >
//               <Icon size={18} />
//               {label}
//             </button>
//           ))}
//         </nav>

//         <div className="mt-8 rounded-xl border border-slate-800 p-4">
//           <div className="flex items-center gap-2 text-sm">
//             <Wifi
//               size={16}
//               className={connected ? 'text-emerald-400' : 'text-rose-400'}
//             />
//             <span>Backend connection</span>
//           </div>

//           <p
//             className={`mt-2 text-xs ${
//               connected ? 'text-emerald-400' : 'text-rose-400'
//             }`}
//           >
//             {connected ? 'Connected to FastAPI' : 'Disconnected'}
//           </p>

//           <p className="mt-2 text-xs text-slate-500">
//             {lastUpdated
//               ? `Updated ${lastUpdated.toLocaleTimeString()}`
//               : 'Waiting for API'}
//           </p>

//           <button
//             type="button"
//             onClick={fetchTraffic}
//             className="mt-4 flex w-full items-center justify-center gap-2 rounded-lg border border-slate-700 px-3 py-2 text-xs hover:bg-slate-800"
//           >
//             <RefreshCw size={14} />
//             Refresh data
//           </button>
//         </div>
//       </aside>

//       {/* Main content */}
//       <main id="overview" className="min-w-0 flex-1 p-5 md:p-8">
//         <header className="flex flex-wrap items-center justify-between gap-4">
//           <div>
//             <p className="text-sm text-slate-500">
//               Traffic Intelligence / Overview
//             </p>

//             <h2 className="mt-2 text-2xl font-bold text-white md:text-3xl">
//               Traffic Dashboard
//             </h2>

//             <p className="mt-2 text-sm text-slate-400">
//               Monitor vehicle movement and road conditions.
//             </p>
//           </div>

//           <div className="flex items-center gap-2 rounded-full border border-slate-700 px-3 py-2 text-sm">
//             <span
//               className={`h-2 w-2 rounded-full ${
//                 connected ? 'bg-emerald-400' : 'bg-rose-400'
//               }`}
//             />
//             {connected ? 'System Online' : 'System Offline'}
//           </div>
//         </header>

//         {error && (
//           <div
//             role="alert"
//             className="mt-6 rounded-xl border border-rose-500/30 bg-rose-500/10 p-4 text-sm text-rose-300"
//           >
//             {error}
//           </div>
//         )}

//         {/* Summary cards */}
//         <section className="mt-8 grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
//           {stats.map(({ title, value, detail, icon: Icon, color }) => (
//             <div
//               key={title}
//               className="rounded-2xl border border-slate-800 bg-[#101827] p-5"
//             >
//               <div className="flex items-center justify-between gap-3">
//                 <p className="text-sm text-slate-400">{title}</p>
//                 <Icon size={21} className={color} />
//               </div>

//               <p className="mt-5 text-3xl font-bold text-white">
//                 {loading ? '...' : value}
//               </p>

//               <p className="mt-2 text-xs text-slate-500">{detail}</p>
//             </div>
//           ))}
//         </section>

//         {/* Video and violations */}
//         <section className="mt-6 grid grid-cols-1 gap-5 xl:grid-cols-3">
//           <div
//             id="monitoring"
//             className="rounded-2xl border border-slate-800 bg-[#101827] p-5 xl:col-span-2"
//           >
//             <div className="flex items-center gap-2">
//               <Video size={19} className="text-cyan-400" />
//               <h3 className="font-semibold text-white">Live Traffic Feed</h3>
//             </div>

//             <div className="mt-5 flex min-h-64 flex-col items-center justify-center rounded-xl border border-dashed border-slate-700 bg-[#080d18] p-6 text-center">
//               <Radio size={42} className="text-slate-600" />

//               <p className="mt-4 font-medium text-slate-300">
//                 {connected
//                   ? 'Backend connected — video stream pending'
//                   : 'No video stream connected'}
//               </p>

//               <p className="mt-2 max-w-sm text-sm text-slate-500">
//                 The annotated YOLO video will appear here after we add a
//                 video-stream endpoint to FastAPI.
//               </p>
//             </div>
//           </div>

//           <div
//             id="violations"
//             className="rounded-2xl border border-slate-800 bg-[#101827] p-5"
//           >
//             <div className="flex items-center gap-2">
//               <TriangleAlert size={19} className="text-amber-400" />
//               <h3 className="font-semibold text-white">Traffic Violations</h3>
//             </div>

//             <div className="mt-5 rounded-xl border border-slate-800 p-4">
//               <p className="text-2xl font-bold text-white">
//                 {loading ? '...' : traffic.violations ?? 0}
//               </p>

//               <p className="mt-2 text-sm text-slate-400">
//                 Total reported violations
//               </p>
//             </div>

//             <div className="mt-4 rounded-xl bg-slate-800/50 p-4">
//               <div className="flex items-center gap-2">
//                 <ShieldCheck size={18} className="text-emerald-400" />
//                 <p className="text-sm text-slate-300">Monitoring status</p>
//               </div>

//               <p className="mt-2 text-xs text-slate-500">
//                 {connected
//                   ? 'Receiving API summary'
//                   : 'Waiting for backend connection'}
//               </p>
//             </div>
//           </div>
//         </section>

//         {/* Vehicle analytics */}
//         <section
//           id="analytics"
//           className="mt-6 rounded-2xl border border-slate-800 bg-[#101827] p-5"
//         >
//           <div className="flex items-center gap-2">
//             <ChartNoAxesCombined size={19} className="text-cyan-400" />
//             <h3 className="font-semibold text-white">Vehicle Analytics</h3>
//           </div>

//           <div className="mt-5 grid grid-cols-2 gap-4 md:grid-cols-4">
//             {vehicleTypes.map(({ name, value, icon: Icon }) => (
//               <div key={name} className="rounded-xl bg-[#080d18] p-4">
//                 <Icon size={20} className="text-cyan-400" />
//                 <p className="mt-3 text-sm text-slate-500">{name}</p>
//                 <p className="mt-2 text-2xl font-semibold text-white">
//                   {loading ? '...' : value ?? 0}
//                 </p>
//               </div>
//             ))}
//           </div>
//         </section>

//         <footer
//           id="settings"
//           className="mt-8 flex flex-wrap items-center justify-between gap-2 text-xs text-slate-600"
//         >
//           <span>Smart Traffic Analysis · Powered by YOLO</span>
//           <span>API polling interval: 3 seconds</span>
//         </footer>
//       </main>
//     </div>
//   )
// }

// export default App


import { useCallback, useEffect, useMemo, useState } from 'react'
import {
  Activity,
  Bike,
  Bus,
  CarFront,
  ChartNoAxesCombined,
  Gauge,
  LayoutDashboard,
  RefreshCw,
  Radio,
  Settings,
  ShieldCheck,
  TriangleAlert,
  Truck,
  Video,
  Wifi,
} from 'lucide-react'

import {
  getAvailableVideos,
  getHealth,
  getTrafficSummary,
  selectVideo,
} from './services/api'
import './App.css'

// Optional MJPEG/HLS-to-img stream from the backend, e.g. http://localhost:8000/video_feed
const VIDEO_URL = import.meta.env.VITE_VIDEO_STREAM_URL || ''
const POLL_MS = 3000

const buildStreamUrl = (filename) => {
  if (!VIDEO_URL || !filename) return ''
  const separator = VIDEO_URL.includes('?') ? '&' : '?'
  return `${VIDEO_URL}${separator}video=${encodeURIComponent(filename)}&session=${Date.now()}`
}

const initialTraffic = {
  vehicles_detected: 0,
  cars: 0,
  motorcycles: 0,
  buses: 0,
  trucks: 0,
  density: 'LOW',
  average_speed: null,
  violations: 0,
  violation_list: [],
}

const NAV_ITEMS = [
  { label: 'Overview', id: 'overview', icon: LayoutDashboard },
  { label: 'Live Monitoring', id: 'monitoring', icon: Video },
  { label: 'Analytics', id: 'analytics', icon: ChartNoAxesCombined },
  { label: 'Violations', id: 'violations', icon: TriangleAlert },
  { label: 'Settings', id: 'settings', icon: Settings },
]

const DENSITY_STYLES = {
  LOW: 'border-emerald-400/30 bg-emerald-400/10 text-emerald-300',
  MEDIUM: 'border-amber-400/30 bg-amber-400/10 text-amber-300',
  HIGH: 'border-rose-400/30 bg-rose-400/10 text-rose-300',
}

function Card({ id, className = '', children }) {
  return (
    <section
      id={id}
      className={`scroll-mt-6 rounded-2xl border border-white/5 bg-[#0f1729] p-5 shadow-lg shadow-black/20 ${className}`}
    >
      {children}
    </section>
  )
}

function CardTitle({ icon: Icon, iconClass, children, right }) {
  return (
    <div className="flex items-center justify-between gap-3">
      <div className="flex items-center gap-2">
        <Icon size={18} className={iconClass} />
        <h3 className="font-semibold text-white">{children}</h3>
      </div>
      {right}
    </div>
  )
}

function StatCard({ title, value, detail, icon: Icon, accent, loading }) {
  return (
    <div className="relative overflow-hidden rounded-2xl border border-white/5 bg-[#0f1729] p-5">
      <div className={`absolute inset-x-0 top-0 h-0.5 ${accent}`} />
      <div className="flex items-center justify-between gap-3">
        <p className="text-sm text-slate-400">{title}</p>
        <div className="rounded-lg bg-white/5 p-2">
          <Icon size={18} className="text-slate-300" />
        </div>
      </div>
      <p className="mt-4 text-3xl font-bold tabular-nums text-white">
        {loading ? '—' : value}
      </p>
      <p className="mt-2 text-xs text-slate-500">{detail}</p>
    </div>
  )
}

function App() {
  const [traffic, setTraffic] = useState(initialTraffic)
  const [connected, setConnected] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [lastUpdated, setLastUpdated] = useState(null)
  const [activeId, setActiveId] = useState('overview')
  const [streamFailed, setStreamFailed] = useState(false)
  const [videos, setVideos] = useState([])
  const [currentVideo, setCurrentVideo] = useState('')
  const [selectedVideo, setSelectedVideo] = useState('')
  const [videoLoading, setVideoLoading] = useState(true)
  const [videoSwitching, setVideoSwitching] = useState(false)
  const [videoError, setVideoError] = useState('')
  const [streamUrl, setStreamUrl] = useState('')

  const fetchTraffic = useCallback(async () => {
    try {
      const [summary, health] = await Promise.all([
        getTrafficSummary(),
        getHealth(),
      ])
      setTraffic({ ...initialTraffic, ...summary })
      setConnected(health?.status === 'healthy')
      setError('')
      setLastUpdated(new Date())
    } catch (err) {
      setConnected(false)
      setError(
        err?.response?.data?.detail ||
          err?.message ||
          'Unable to reach the FastAPI backend. Check that it is running.'
      )
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchTraffic()
    const id = setInterval(fetchTraffic, POLL_MS)
    return () => clearInterval(id)
  }, [fetchTraffic])

  useEffect(() => {
    let cancelled = false

    const loadVideos = async () => {
      try {
        const data = await getAvailableVideos()
        if (cancelled) return

        const availableVideos = Array.isArray(data?.videos) ? data.videos : []
        const activeVideo = data?.active_video || availableVideos[0]?.filename || ''
        setVideos(availableVideos)
        setCurrentVideo(activeVideo)
        setSelectedVideo(activeVideo)
        setStreamUrl(buildStreamUrl(activeVideo))
        setVideoError(
          availableVideos.length
            ? ''
            : 'No permitted video files are available in data/videos.'
        )
      } catch (err) {
        if (!cancelled) {
          setVideoError(
            err?.response?.data?.detail ||
              err?.message ||
              'Unable to load available video sources.'
          )
        }
      } finally {
        if (!cancelled) setVideoLoading(false)
      }
    }

    loadVideos()
    return () => {
      cancelled = true
    }
  }, [])

  const handleVideoSwitch = async () => {
    if (!selectedVideo || selectedVideo === currentVideo) return

    setVideoSwitching(true)
    setVideoError('')
    setStreamFailed(false)

    try {
      const result = await selectVideo(selectedVideo)
      const nextVideo = result?.filename || selectedVideo
      setCurrentVideo(nextVideo)
      setStreamUrl(buildStreamUrl(nextVideo))
      await fetchTraffic()
    } catch (err) {
      setVideoError(
        err?.response?.data?.detail ||
          err?.message ||
          'Unable to switch to the selected video.'
      )
      setSelectedVideo(currentVideo)
    } finally {
      setVideoSwitching(false)
    }
  }

  // Highlight the nav item for the section currently in view.
  useEffect(() => {
    const sections = NAV_ITEMS.map((n) => document.getElementById(n.id)).filter(Boolean)
    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries.find((e) => e.isIntersecting)
        if (visible) setActiveId(visible.target.id)
      },
      { rootMargin: '-40% 0px -50% 0px' }
    )
    sections.forEach((s) => observer.observe(s))
    return () => observer.disconnect()
  }, [])

  const vehicleTypes = useMemo(() => {
    const rows = [
      { name: 'Cars', value: traffic.cars ?? 0, icon: CarFront, bar: 'bg-cyan-400' },
      { name: 'Motorcycles', value: traffic.motorcycles ?? 0, icon: Bike, bar: 'bg-violet-400' },
      { name: 'Buses', value: traffic.buses ?? 0, icon: Bus, bar: 'bg-amber-400' },
      { name: 'Trucks', value: traffic.trucks ?? 0, icon: Truck, bar: 'bg-emerald-400' },
    ]
    const total = rows.reduce((sum, r) => sum + r.value, 0)
    return rows.map((r) => ({ ...r, percent: total ? Math.round((r.value / total) * 100) : 0 }))
  }, [traffic])

  const speedText =
    traffic.average_speed == null ? '--' : `${Number(traffic.average_speed).toFixed(1)} km/h`

  const densityKey = String(traffic.density ?? 'LOW').toUpperCase()
  const densityClass = DENSITY_STYLES[densityKey] ?? DENSITY_STYLES.LOW

  const violationList = Array.isArray(traffic.violation_list) ? traffic.violation_list : []

  const scrollTo = (id) => {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }

  return (
    <div className="min-h-screen bg-[#070c17] text-slate-200 md:flex">
      {/* Sidebar */}
      <aside className="border-b border-white/5 bg-[#0a1020] p-5 md:sticky md:top-0 md:h-screen md:w-64 md:shrink-0 md:border-b-0 md:border-r">
        <div className="flex items-center gap-3">
          <div className="rounded-xl bg-gradient-to-br from-cyan-400/20 to-cyan-400/5 p-2.5 text-cyan-300 ring-1 ring-cyan-400/20">
            <Activity size={22} />
          </div>
          <div>
            <h1 className="font-bold tracking-tight text-white">TrafficAI</h1>
            <p className="text-xs text-slate-500">Intelligent Monitoring</p>
          </div>
        </div>

        <nav className="dashboard-nav mt-8 flex gap-1.5 overflow-x-auto md:flex-col">
          {NAV_ITEMS.map(({ label, id, icon: Icon }) => {
            const active = activeId === id
            return (
              <button
                type="button"
                key={id}
                onClick={() => scrollTo(id)}
                className={`dashboard-nav-button flex shrink-0 items-center gap-3 rounded-lg px-3.5 py-2.5 text-sm transition ${
                  active
                    ? 'bg-cyan-400/10 text-cyan-300 ring-1 ring-cyan-400/20'
                    : 'text-slate-400 hover:bg-white/5 hover:text-white'
                }`}
              >
                <Icon size={17} />
                {label}
              </button>
            )
          })}
        </nav>

        <div className="mt-8 rounded-xl border border-white/5 bg-white/[0.02] p-4">
          <div className="flex items-center gap-2 text-sm">
            <Wifi size={15} className={connected ? 'text-emerald-400' : 'text-rose-400'} />
            <span>Backend</span>
            <span
              className={`ml-auto h-2 w-2 rounded-full ${
                connected ? 'bg-emerald-400 shadow-[0_0_8px_#34d399]' : 'bg-rose-400'
              }`}
            />
          </div>
          <p className={`mt-2 text-xs ${connected ? 'text-emerald-400' : 'text-rose-400'}`}>
            {connected ? 'Connected to FastAPI' : 'Disconnected'}
          </p>
          <p className="mt-1 text-xs text-slate-500">
            {lastUpdated ? `Updated ${lastUpdated.toLocaleTimeString()}` : 'Waiting for API'}
          </p>
          <button
            type="button"
            onClick={fetchTraffic}
            className="refresh-button mt-4 flex w-full items-center justify-center gap-2 rounded-lg border border-white/10 px-3 py-2 text-xs transition hover:bg-white/5"
          >
            <RefreshCw size={13} />
            Refresh data
          </button>
        </div>
      </aside>

      {/* Main */}
      <main className="dashboard-main min-w-0 flex-1 space-y-6 p-5 md:p-8">
        <header
          id="overview"
          className="dashboard-header scroll-mt-6 flex flex-wrap items-end justify-between gap-4"
        >
          <div>
            <p className="text-xs font-medium uppercase tracking-widest text-slate-500">
              Traffic Intelligence / Overview
            </p>
            <h2 className="mt-2 text-2xl font-bold tracking-tight text-white md:text-3xl">
              Traffic Dashboard
            </h2>
            <p className="mt-1 text-sm text-slate-400">
              Live vehicle movement, density and violations from the YOLO pipeline.
            </p>
          </div>

          <div className="flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.03] px-3.5 py-1.5 text-sm">
            <span
              className={`h-2 w-2 rounded-full ${
                connected ? 'animate-pulse bg-emerald-400' : 'bg-rose-400'
              }`}
            />
            {connected ? 'System Online' : 'System Offline'}
          </div>
        </header>

        {error && (
          <div
            role="alert"
            className="rounded-xl border border-rose-500/30 bg-rose-500/10 p-4 text-sm text-rose-300"
          >
            {error}
          </div>
        )}

        {/* Stat cards */}
        <div className="summary-grid grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <StatCard
            title="Vehicles Detected"
            value={traffic.vehicles_detected ?? 0}
            detail="Unique tracked vehicles"
            icon={CarFront}
            accent="bg-cyan-400"
            loading={loading}
          />
          <div className="relative overflow-hidden rounded-2xl border border-white/5 bg-[#0f1729] p-5">
            <div className="absolute inset-x-0 top-0 h-0.5 bg-emerald-400" />
            <div className="flex items-center justify-between gap-3">
              <p className="text-sm text-slate-400">Traffic Density</p>
              <div className="rounded-lg bg-white/5 p-2">
                <Activity size={18} className="text-slate-300" />
              </div>
            </div>
            <div className="mt-4">
              <span
                className={`inline-flex rounded-full border px-3 py-1 text-sm font-semibold ${densityClass}`}
              >
                {loading ? '—' : densityKey}
              </span>
            </div>
            <p className="mt-3 text-xs text-slate-500">Current traffic level</p>
          </div>
          <StatCard
            title="Average Speed"
            value={speedText}
            detail="Estimated vehicle speed"
            icon={Gauge}
            accent="bg-violet-400"
            loading={loading}
          />
          <StatCard
            title="Violations"
            value={traffic.violations ?? 0}
            detail="Reported traffic violations"
            icon={TriangleAlert}
            accent="bg-rose-400"
            loading={loading}
          />
        </div>

        {/* Feed + violations */}
        <div className="feed-layout grid grid-cols-1 gap-5 xl:grid-cols-3">
          <Card id="monitoring" className="monitoring-card xl:col-span-2">
            <CardTitle
              icon={Video}
              iconClass="text-cyan-400"
              right={
                <span
                  className={`rounded-full px-2.5 py-0.5 text-xs ${
                    connected && streamUrl && !streamFailed
                      ? 'bg-rose-500/15 text-rose-300'
                      : 'bg-white/5 text-slate-500'
                  }`}
                >
                  {connected && VIDEO_URL && !streamFailed ? '● LIVE' : 'OFFLINE'}
                </span>
              }
            >
              Live Traffic Feed
            </CardTitle>

            <div className="video-controls mt-5">
              <div className="video-select-group">
                <label htmlFor="video-source">Video source</label>
                <select
                  id="video-source"
                  value={selectedVideo}
                  onChange={(event) => setSelectedVideo(event.target.value)}
                  disabled={videoLoading || videoSwitching || videos.length === 0}
                >
                  {videos.length === 0 && <option value="">No videos available</option>}
                  {videos.map((video) => (
                    <option key={video.filename} value={video.filename}>
                      {video.label}
                    </option>
                  ))}
                </select>
              </div>
              <button
                type="button"
                className="video-switch-button"
                onClick={handleVideoSwitch}
                disabled={
                  videoLoading ||
                  videoSwitching ||
                  !selectedVideo ||
                  selectedVideo === currentVideo
                }
              >
                {videoSwitching ? 'Switching…' : 'Switch Video'}
              </button>
              <span className="video-current">
                Active: {currentVideo ? currentVideo.replace(/\.mp4$/i, '') : '—'}
              </span>
            </div>

            {videoError && <p className="video-error mt-3">{videoError}</p>}

            <div className="feed-frame mt-5 flex aspect-video w-full items-center justify-center overflow-hidden rounded-xl border border-dashed border-white/10 bg-[#070c17]">
              {connected && streamUrl && !streamFailed ? (
                <img
                  src={streamUrl}
                  alt="Annotated YOLO traffic feed"
                  className="h-full w-full object-contain"
                  onError={() => setStreamFailed(true)}
                />
              ) : (
                <div className="p-6 text-center">
                  <Radio size={40} className="mx-auto text-slate-600" />
                  <p className="mt-4 font-medium text-slate-300">
                    {connected
                      ? streamFailed
                        ? 'The selected video stream is unavailable'
                        : 'Video stream not configured'
                      : 'No video stream connected'}
                  </p>
                  <p className="mx-auto mt-2 max-w-sm text-sm text-slate-500">
                    {streamFailed
                      ? 'The stream failed to load. Check the backend video endpoint.'
                      : 'Set VITE_VIDEO_STREAM_URL to your FastAPI video endpoint to show the annotated feed.'}
                  </p>
                </div>
              )}
            </div>
          </Card>

          <Card id="violations">
            <CardTitle icon={TriangleAlert} iconClass="text-amber-400">
              Traffic Violations
            </CardTitle>

            <div className="mt-5 rounded-xl border border-white/5 bg-[#070c17] p-4">
              <p className="text-3xl font-bold tabular-nums text-white">
                {loading ? '—' : traffic.violations ?? 0}
              </p>
              <p className="mt-1 text-sm text-slate-400">Total reported violations</p>
            </div>

            <div className="mt-4 max-h-56 space-y-2 overflow-y-auto pr-1">
              {violationList.length === 0 ? (
                <div className="flex items-center gap-2 rounded-xl bg-emerald-400/5 p-4 text-sm text-slate-300">
                  <ShieldCheck size={17} className="text-emerald-400" />
                  {connected ? 'No violations recorded' : 'Waiting for backend connection'}
                </div>
              ) : (
                violationList.map((v, i) => (
                  <div
                    key={v.id ?? i}
                    className="rounded-xl border border-white/5 bg-[#070c17] p-3 text-sm"
                  >
                    <p className="font-medium text-rose-300">{v.type ?? 'Violation'}</p>
                    <p className="mt-1 text-xs text-slate-500">
                      {[v.vehicle_id && `Vehicle #${v.vehicle_id}`, v.time]
                        .filter(Boolean)
                        .join(' · ')}
                    </p>
                  </div>
                ))
              )}
            </div>
          </Card>
        </div>

        {/* Vehicle analytics */}
        <Card id="analytics">
          <CardTitle icon={ChartNoAxesCombined} iconClass="text-cyan-400">
            Vehicle Analytics
          </CardTitle>

          <div className="mt-5 grid grid-cols-2 gap-4 md:grid-cols-4">
            {vehicleTypes.map(({ name, value, percent, icon: Icon, bar }) => (
              <div key={name} className="rounded-xl bg-[#070c17] p-4">
                <div className="flex items-center justify-between">
                  <Icon size={19} className="text-slate-300" />
                  <span className="text-xs text-slate-500">{percent}%</span>
                </div>
                <p className="mt-3 text-sm text-slate-500">{name}</p>
                <p className="mt-1 text-2xl font-semibold tabular-nums text-white">
                  {loading ? '—' : value}
                </p>
                <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-white/5">
                  <div
                    className={`h-full rounded-full transition-all duration-500 ${bar}`}
                    style={{ width: `${percent}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </Card>

        <footer
          id="settings"
          className="scroll-mt-6 flex flex-wrap items-center justify-between gap-2 border-t border-white/5 pt-6 text-xs text-slate-600"
        >
          <span>Smart Traffic Analysis · Powered by YOLO</span>
          <span>API polling interval: {POLL_MS / 1000}s</span>
        </footer>
      </main>
    </div>
  )
}

export default App