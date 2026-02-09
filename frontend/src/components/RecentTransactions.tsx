import { formatDistanceToNow } from 'date-fns';
import { ExternalLink } from 'lucide-react';
import type { Transaction } from '@/types';

interface Props {
  transactions?: Transaction[];
}

const getRiskColor = (level: string) => {
  const colors = {
    MINIMAL: 'bg-green-100 text-green-800',
    LOW: 'bg-blue-100 text-blue-800',
    MEDIUM: 'bg-yellow-100 text-yellow-800',
    HIGH: 'bg-orange-100 text-orange-800',
    CRITICAL: 'bg-red-100 text-red-800',
  };
  return colors[level as keyof typeof colors] || colors.MEDIUM;
};

const getDecisionColor = (decision: string) => {
  const colors = {
    APPROVE: 'bg-green-100 text-green-800',
    REVIEW: 'bg-yellow-100 text-yellow-800',
    BLOCK: 'bg-red-100 text-red-800',
  };
  return colors[decision as keyof typeof colors] || colors.REVIEW;
};

export function RecentTransactions({ transactions }: Props) {
  return (
    <div className="card">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Transactions</h3>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">User</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Amount</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Risk</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Decision</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Time</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {transactions?.map((txn) => (
              <tr key={txn.id} className="hover:bg-gray-50">
                <td className="px-4 py-3 whitespace-nowrap text-sm font-mono text-gray-900">
                  {txn.id.slice(0, 8)}...
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-900">
                  {txn.user_id}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">
                  ${txn.amount.toLocaleString()}
                </td>
                <td className="px-4 py-3 whitespace-nowrap">
                  <span className={`px-2 py-1 text-xs font-semibold rounded-full ${getRiskColor(txn.risk_level)}`}>
                    {txn.risk_level}
                  </span>
                  <span className="ml-2 text-xs text-gray-600">
                    {(txn.risk_score * 100).toFixed(0)}%
                  </span>
                </td>
                <td className="px-4 py-3 whitespace-nowrap">
                  <span className={`px-2 py-1 text-xs font-semibold rounded-full ${getDecisionColor(txn.decision)}`}>
                    {txn.decision}
                  </span>
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-600">
                  {formatDistanceToNow(new Date(txn.created_at), { addSuffix: true })}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}