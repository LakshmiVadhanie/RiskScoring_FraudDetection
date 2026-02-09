import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

interface Props {
  data?: Record<string, number>;
}

const COLORS = {
  MINIMAL: '#10b981',
  LOW: '#3b82f6',
  MEDIUM: '#f59e0b',
  HIGH: '#ef4444',
  CRITICAL: '#7f1d1d',
};

export function RiskDistributionChart({ data }: Props) {
  const chartData = data
    ? Object.entries(data).map(([name, value]) => ({ name, value }))
    : [];

  return (
    <div className="card">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Risk Distribution</h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[entry.name as keyof typeof COLORS]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}