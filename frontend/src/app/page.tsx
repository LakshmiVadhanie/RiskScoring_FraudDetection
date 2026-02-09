'use client';

import { useQuery } from '@tanstack/react-query';
import { fraudAPI } from '@/lib/api';
import { StatsCards } from '@/components/StatsCards';
import { TransactionChart } from '@/components/TransactionChart';
import { RiskDistributionChart } from '@/components/RiskDistributionChart';
import { RecentTransactions } from '@/components/RecentTransactions';
import { AlertsPanel } from '@/components/AlertsPanel';
import { TestTransaction } from '@/components/TestTransaction';
import { Shield } from 'lucide-react';

export default function Dashboard() {
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: fraudAPI.getDashboardStats,
    refetchInterval: 5000,
  });

  const { data: trends } = useQuery({
    queryKey: ['trends'],
    queryFn: () => fraudAPI.getTrends(7),
    refetchInterval: 10000,
  });

  const { data: transactions } = useQuery({
    queryKey: ['recent-transactions'],
    queryFn: () => fraudAPI.getRecentTransactions(20),
    refetchInterval: 5000,
  });

  const { data: alerts } = useQuery({
    queryKey: ['alerts'],
    queryFn: () => fraudAPI.getAlerts(false, 10),
    refetchInterval: 5000,
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="bg-blue-600 p-2 rounded-lg">
                <Shield className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  Fraud Detection Platform
                </h1>
                <p className="text-sm text-gray-600">
                  Real-time risk scoring and monitoring
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <span className="flex h-3 w-3 relative">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
              </span>
              <span className="text-sm font-medium text-gray-700">Live</span>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Cards */}
        <StatsCards stats={stats} loading={statsLoading} />

        {/* Test Transaction */}
        <div className="mb-8">
          <TestTransaction />
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <TransactionChart data={trends} />
          <RiskDistributionChart data={stats?.risk_distribution} />
        </div>

        {/* Transactions and Alerts */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <RecentTransactions transactions={transactions} />
          </div>
          <div>
            <AlertsPanel alerts={alerts} />
          </div>
        </div>
      </main>
    </div>
  );
}