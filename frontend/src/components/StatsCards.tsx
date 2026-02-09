import { TrendingUp, AlertTriangle, DollarSign, Activity } from 'lucide-react';
import type { DashboardStats } from '@/types';

interface Props {
  stats?: DashboardStats;
  loading: boolean;
}

export function StatsCards({ stats, loading }: Props) {
  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="stat-card animate-pulse">
            <div className="h-20 bg-gray-200 rounded"></div>
          </div>
        ))}
      </div>
    );
  }

  const cards = [
    {
      title: 'Total Transactions',
      value: stats?.total_transactions?.toLocaleString() || '0',
      icon: TrendingUp,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
    },
    {
      title: 'Fraud Detected',
      value: stats?.fraud_detected?.toLocaleString() || '0',
      subtitle: `${((stats?.fraud_rate || 0) * 100).toFixed(2)}% rate`,
      icon: AlertTriangle,
      color: 'text-red-600',
      bgColor: 'bg-red-100',
    },
    {
      title: 'Amount Processed',
      value: `$${(stats?.total_amount_processed || 0).toLocaleString(undefined, { maximumFractionDigits: 0 })}`,
      icon: DollarSign,
      color: 'text-green-600',
      bgColor: 'bg-green-100',
    },
    {
      title: 'Avg Risk Score',
      value: ((stats?.average_risk_score || 0) * 100).toFixed(1),
      subtitle: '/ 100',
      icon: Activity,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100',
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      {cards.map((card) => {
        const Icon = card.icon;
        return (
          <div key={card.title} className="stat-card hover:shadow-xl transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">{card.title}</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">
                  {card.value}
                </p>
                {card.subtitle && (
                  <p className="text-sm text-gray-500 mt-1">{card.subtitle}</p>
                )}
              </div>
              <div className={`${card.bgColor} p-3 rounded-lg`}>
                <Icon className={`w-6 h-6 ${card.color}`} />
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}