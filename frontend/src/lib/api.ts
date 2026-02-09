import axios from 'axios';
import type { Transaction, DashboardStats, Alert, TrendData } from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {'Content-Type': 'application/json'},
});

export const fraudAPI = {
  // Score transaction
  scoreTransaction: async (data: any) => {
    const response = await api.post<Transaction>('/api/v1/transactions/score', data);
    return response.data;
  },

  // Get recent transactions
  getRecentTransactions: async (limit: number = 50) => {
    const response = await api.get<Transaction[]>(`/api/v1/transactions/recent?limit=${limit}`);
    return response.data;
  },

  // Get transaction by ID
  getTransaction: async (id: string) => {
    const response = await api.get<Transaction>(`/api/v1/transactions/${id}`);
    return response.data;
  },

  // Get dashboard stats
  getDashboardStats: async () => {
    const response = await api.get<DashboardStats>('/api/v1/analytics/dashboard');
    return response.data;
  },

  // Get trends
  getTrends: async (days: number = 7) => {
    const response = await api.get<TrendData[]>(`/api/v1/analytics/trends?days=${days}`);
    return response.data;
  },

  // Get alerts
  getAlerts: async (resolved?: boolean, limit: number = 50) => {
    const params = new URLSearchParams();
    if (resolved !== undefined) params.append('resolved', String(resolved));
    params.append('limit', String(limit));
    const response = await api.get<Alert[]>(`/api/v1/analytics/alerts?${params}`);
    return response.data;
  },
};