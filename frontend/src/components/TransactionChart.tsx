import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import type { TrendData } from '@/types';

interface Props {
  data?: TrendData[];
}

export function TransactionChart({ data }: Props) {
  return (
    <div className="card">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Transaction Trends</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data || []}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis 
            dataKey="date" 
            stroke="#6b7280"
            style={{ fontSize: '12px' }}
          />
          <YAxis stroke="#6b7280" style={{ fontSize: '12px' }} />
          <Tooltip 
            contentStyle={{
              backgroundColor: '#fff',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
              padding: '12px'
            }}
          />
          <Legend />
          <Line 
            type="monotone" 
            dataKey="total" 
            stroke="#3b82f6" 
            strokeWidth={2}
            name="Total Transactions"
            dot={{ fill: '#3b82f6', r: 4 }}
          />
          <Line 
            type="monotone" 
            dataKey="fraud" 
            stroke="#ef4444" 
            strokeWidth={2}
            name="Fraud Detected"
            dot={{ fill: '#ef4444', r: 4 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}