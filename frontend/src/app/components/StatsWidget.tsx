"use client";

import { useEffect, useState } from 'react';
import { API_BASE_URL } from '@/lib/config';

type Stats = {
  total_users: number;
  average_age: number;
  min_age: number;
  max_age: number;
  eye_color_distribution: Record<string, number>;
  calculated_at: string;
};

export default function StatsWidget() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    let isMounted = true;
    async function load() {
      try {
        const res = await fetch(`${API_BASE_URL}/stats/latest`, { cache: 'no-store' });
        if (!res.ok) throw new Error(`Failed to fetch stats (${res.status})`);
        const data: Stats = await res.json();
        if (isMounted) setStats(data);
      } catch (e: any) {
        if (isMounted) setError(e.message || 'Failed to load stats');
      } finally {
        if (isMounted) setLoading(false);
      }
    }
    load();
    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <div className="mx-auto mt-8 max-w-3xl rounded-xl border border-white/20 bg-white/40 p-6 shadow-lg backdrop-blur">
      <h2 className="mb-4 text-xl font-semibold text-gray-800">Daily User Statistics</h2>
      {loading && <div className="text-gray-600">Loading...</div>}
      {error && <div className="text-red-600">{error}</div>}
      {!loading && !error && stats && (
        <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
          <StatCard label="Total Users" value={stats.total_users} />
          <StatCard label="Avg Age" value={stats.average_age} />
          <StatCard label="Min Age" value={stats.min_age} />
          <StatCard label="Max Age" value={stats.max_age} />
          <div className="col-span-2 md:col-span-4 mt-2">
            <h3 className="mb-2 text-sm font-medium text-gray-700">Eye Colors</h3>
            <div className="flex flex-wrap gap-2">
              {Object.entries(stats.eye_color_distribution).map(([color, count]) => (
                <span key={color} className="rounded-full bg-white/70 px-3 py-1 text-sm text-gray-800 shadow">
                  {color}: {count}
                </span>
              ))}
              {Object.keys(stats.eye_color_distribution).length === 0 && (
                <span className="text-gray-600">No data</span>
              )}
            </div>
          </div>
          <div className="col-span-2 md:col-span-4 mt-2 text-xs text-gray-600">
            Calculated at: {new Date(stats.calculated_at).toLocaleString()}
          </div>
        </div>
      )}
    </div>
  );
}

function StatCard({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded-lg bg-white/70 p-4 text-center shadow">
      <div className="text-sm text-gray-600">{label}</div>
      <div className="mt-1 text-2xl font-semibold text-gray-900">{value}</div>
    </div>
  );
}


