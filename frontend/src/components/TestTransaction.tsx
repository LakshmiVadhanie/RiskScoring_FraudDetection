'use client';

import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { fraudAPI } from '@/lib/api';
import { Send, Loader2 } from 'lucide-react';

export function TestTransaction() {
  const queryClient = useQueryClient();
  const [amount, setAmount] = useState('250');
  
  const mutation = useMutation({
    mutationFn: fraudAPI.scoreTransaction,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['recent-transactions'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard-stats'] });
      queryClient.invalidateQueries({ queryKey: ['alerts'] });
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const testData = {
      user_id: `USER_${Math.floor(Math.random() * 10000)}`,
      merchant_id: `MERCHANT_${Math.floor(Math.random() * 1000)}`,
      amount: parseFloat(amount),
      currency: 'USD',
      country: 'US',
      device_id: `DEVICE_${Math.floor(Math.random() * 5000)}`,
      ip_address: `192.168.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}`,
      transaction_type: 'purchase',
      channel: Math.random() > 0.5 ? 'mobile' : 'web',
    };
    mutation.mutate(testData);
  };

  return (
    <div className="card bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Test Transaction</h3>
      <form onSubmit={handleSubmit} className="flex items-end gap-4">
        <div className="flex-1">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Transaction Amount ($)
          </label>
          <input
            type="number"
            step="0.01"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Enter amount"
          />
        </div>
        <button
          type="submit"
          disabled={mutation.isPending}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 transition-colors"
        >
          {mutation.isPending ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              Processing...
            </>
          ) : (
            <>
              <Send className="w-4 h-4" />
              Score Transaction
            </>
          )}
        </button>
      </form>
      {mutation.isSuccess && (
        <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
          <p className="text-sm font-medium text-green-900">
            Transaction scored successfully!
          </p>
          <p className="text-xs text-green-700 mt-1">
            Risk Score: {(mutation.data.risk_score * 100).toFixed(1)}% | 
            Decision: {mutation.data.decision}
          </p>
        </div>
      )}
    </div>
  );
}