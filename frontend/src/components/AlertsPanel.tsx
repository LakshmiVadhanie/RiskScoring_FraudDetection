import { AlertTriangle, CheckCircle } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';
import type { Alert } from '@/types';

interface Props {
  alerts?: Alert[];
}

export function AlertsPanel({ alerts }: Props) {
  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Active Alerts</h3>
        <span className="px-2 py-1 text-xs font-semibold bg-red-100 text-red-800 rounded-full">
          {alerts?.length || 0}
        </span>
      </div>
      <div className="space-y-3">
        {alerts?.map((alert) => (
          <div 
            key={alert.id} 
            className="p-3 border border-red-200 rounded-lg bg-red-50 hover:bg-red-100 transition-colors"
          >
            <div className="flex items-start">
              <AlertTriangle className="w-5 h-5 text-red-600 mt-0.5 mr-3 flex-shrink-0" />
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900">{alert.message}</p>
                <p className="text-xs text-gray-600 mt-1">
                  {formatDistanceToNow(new Date(alert.created_at), { addSuffix: true })}
                </p>
                <div className="mt-2">
                  <span className="inline-block px-2 py-1 text-xs font-semibold bg-white text-red-800 rounded">
                    {alert.severity}
                  </span>
                </div>
              </div>
            </div>
          </div>
        ))}
        {(!alerts || alerts.length === 0) && (
          <div className="text-center py-8">
            <CheckCircle className="w-12 h-12 text-green-500 mx-auto mb-2" />
            <p className="text-sm text-gray-600">No active alerts</p>
          </div>
        )}
      </div>
    </div>
  );
}