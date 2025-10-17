import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  Activity, 
  Users, 
  TrendingUp, 
  Bot, 
  Play, 
  Pause, 
  RotateCcw,
  Eye,
  CheckCircle,
  AlertCircle,
  Clock,
  Zap
} from 'lucide-react';
import MobileMatrixOptimizer from '../components/MobileMatrixOptimizer';
import TerminalWindow from '../components/TerminalWindow';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';

const AgentDashboard = () => {
  const [agentStatus, setAgentStatus] = useState({});
  const [orchestratorMetrics, setOrchestratorMetrics] = useState({});
  const [taskHistory, setTaskHistory] = useState([]);
  const [salesPipeline, setSalesPipeline] = useState({});
  const [loading, setLoading] = useState(true);
  const [selectedAgent, setSelectedAgent] = useState(null);

  useEffect(() => {
    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || "http://localhost:8001";
      
      // Fetch agent status
      const agentResponse = await fetch(`${backendUrl}/api/agents/status`);
      if (agentResponse.ok) {
        const agentData = await agentResponse.json();
        setAgentStatus(agentData.data || {});
      }

      // Fetch orchestrator metrics
      const metricsResponse = await fetch(`${backendUrl}/api/agents/metrics`);
      if (metricsResponse.ok) {
        const metricsData = await metricsResponse.json();
        setOrchestratorMetrics(metricsData.data || {});
      }

      // Fetch task history
      const historyResponse = await fetch(`${backendUrl}/api/agents/tasks/history?limit=10`);
      if (historyResponse.ok) {
        const historyData = await historyResponse.json();
        setTaskHistory(historyData.data?.tasks || []);
      }

      setLoading(false);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      setLoading(false);
    }
  };

  const handleAgentAction = async (agentId, action) => {
    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || "http://localhost:8001";
      const response = await fetch(`${backendUrl}/api/agents/${agentId}/${action}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });

      if (response.ok) {
        // Refresh data after action
        fetchDashboardData();
      }
    } catch (error) {
      console.error(`Error ${action} agent:`, error);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'running': return 'text-green-400 bg-green-400/20 border-green-400/40';
      case 'idle': return 'text-blue-400 bg-blue-400/20 border-blue-400/40';
      case 'paused': return 'text-yellow-400 bg-yellow-400/20 border-yellow-400/40';
      case 'error': return 'text-red-400 bg-red-400/20 border-red-400/40';
      default: return 'text-matrix-green bg-matrix-green/20 border-matrix-green/40';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'running': return <CheckCircle className="w-4 h-4" />;
      case 'idle': return <Clock className="w-4 h-4" />;
      case 'paused': return <Pause className="w-4 h-4" />;
      case 'error': return <AlertCircle className="w-4 h-4" />;
      default: return <Activity className="w-4 h-4" />;
    }
  };

  if (loading) {
    return (
      <MobileMatrixOptimizer className="min-h-screen bg-black text-matrix-green flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin w-12 h-12 border-2 border-matrix-green border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-matrix-green/80">Loading Agent Dashboard...</p>
        </div>
      </MobileMatrixOptimizer>
    );
  }

  const agents = agentStatus.agents || {};
  const metrics = orchestratorMetrics || {};

  return (
    <MobileMatrixOptimizer className="min-h-screen bg-black text-matrix-green relative overflow-hidden">
      {/* Background */}
      <div className="fixed inset-0 z-0 bg-matrix-gradient-dark" />
      
      {/* Header */}
      <div className="relative z-10 pt-24 pb-8 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <Badge className="bg-gradient-to-r from-matrix-green/20 to-matrix-cyan/20 text-matrix-green border-matrix-green/40 font-body animate-scaleIn mb-4">
              🤖 AI Agent Command Center
            </Badge>
            
            <h1 className="text-4xl lg:text-6xl font-bold font-heading leading-tight animate-fadeInUp">
              <span className="matrix-text-bright animate-glow">
                AGENT_DASHBOARD
              </span>
            </h1>
            
            <p className="text-xl text-matrix-green/80 font-body mt-4 animate-fadeInUp" style={{animationDelay: '0.2s'}}>
              Monitor and control your AI-powered business automation agents
            </p>
          </div>

          {/* Orchestrator Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <Card className="modern-card hover-lift">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-matrix-green">Active Agents</CardTitle>
                <Bot className="h-4 w-4 text-matrix-cyan" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-matrix-bright-cyan">{metrics.active_agents || 0}</div>
                <p className="text-xs text-matrix-green/60">AI agents online</p>
              </CardContent>
            </Card>

            <Card className="modern-card hover-lift">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-matrix-green">Total Tasks</CardTitle>
                <Activity className="h-4 w-4 text-matrix-cyan" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-matrix-bright-cyan">{metrics.total_tasks || 0}</div>
                <p className="text-xs text-matrix-green/60">Tasks processed</p>
              </CardContent>
            </Card>

            <Card className="modern-card hover-lift">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-matrix-green">Success Rate</CardTitle>
                <TrendingUp className="h-4 w-4 text-matrix-cyan" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-matrix-bright-cyan">{Math.round(metrics.success_rate || 0)}%</div>
                <p className="text-xs text-matrix-green/60">Task success rate</p>
              </CardContent>
            </Card>

            <Card className="modern-card hover-lift">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-matrix-green">Uptime</CardTitle>
                <Zap className="h-4 w-4 text-matrix-cyan" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-matrix-bright-cyan">
                  {Math.round((metrics.uptime_seconds || 0) / 3600)}h
                </div>
                <p className="text-xs text-matrix-green/60">System uptime</p>
              </CardContent>
            </Card>
          </div>

          {/* Agents Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
            {Object.entries(agents).map(([agentId, agent]) => (
              <Card key={agentId} className="modern-card hover-glow">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <Bot className="w-8 h-8 text-matrix-cyan animate-pulse-glow" />
                      <div>
                        <CardTitle className="text-matrix-green font-heading">{agent.name}</CardTitle>
                        <CardDescription className="text-matrix-green/60">{agent.description}</CardDescription>
                      </div>
                    </div>
                    <Badge className={`${getStatusColor(agent.status)} font-mono text-xs`}>
                      {getStatusIcon(agent.status)}
                      <span className="ml-1">{agent.status?.toUpperCase()}</span>
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {/* Agent Metrics */}
                    <div className="grid grid-cols-3 gap-4">
                      <div className="text-center">
                        <div className="text-lg font-bold text-matrix-bright-cyan">{agent.metrics?.tasks_completed || 0}</div>
                        <div className="text-xs text-matrix-green/60">Completed</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-bold text-matrix-bright-cyan">{agent.metrics?.tasks_failed || 0}</div>
                        <div className="text-xs text-matrix-green/60">Failed</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-bold text-matrix-bright-cyan">{Math.round((agent.metrics?.success_rate || 0) * 100)}%</div>
                        <div className="text-xs text-matrix-green/60">Success</div>
                      </div>
                    </div>

                    {/* Agent Capabilities */}
                    <div>
                      <h4 className="text-sm font-semibold text-matrix-green mb-2">Capabilities</h4>
                      <div className="flex flex-wrap gap-2">
                        {(agent.capabilities || []).map((capability, index) => (
                          <Badge key={index} variant="outline" className="text-xs font-mono border-matrix-green/40 text-matrix-green">
                            {capability.replace(/_/g, ' ')}
                          </Badge>
                        ))}
                      </div>
                    </div>

                    {/* Agent Controls */}
                    <div className="flex space-x-2 pt-2">
                      <Button 
                        size="sm" 
                        variant="outline"
                        className="border-matrix-green text-matrix-green hover:bg-matrix-green/10"
                        onClick={() => handleAgentAction(agentId, 'pause')}
                        disabled={agent.status === 'paused'}
                      >
                        <Pause className="w-3 h-3 mr-1" />
                        Pause
                      </Button>
                      <Button 
                        size="sm" 
                        variant="outline"
                        className="border-matrix-green text-matrix-green hover:bg-matrix-green/10"
                        onClick={() => handleAgentAction(agentId, 'resume')}
                        disabled={agent.status !== 'paused'}
                      >
                        <Play className="w-3 h-3 mr-1" />
                        Resume
                      </Button>
                      <Button 
                        size="sm" 
                        variant="outline"
                        className="border-matrix-green text-matrix-green hover:bg-matrix-green/10"
                        onClick={() => handleAgentAction(agentId, 'reset')}
                      >
                        <RotateCcw className="w-3 h-3 mr-1" />
                        Reset
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Task History */}
          <TerminalWindow title="TASK_EXECUTION_LOG.txt" className="mb-8">
            <div className="space-y-2 max-h-64 overflow-y-auto">
              {taskHistory.length > 0 ? (
                taskHistory.map((task, index) => (
                  <div key={index} className="flex items-center justify-between text-sm font-mono">
                    <span className="text-matrix-green/80">
                      {new Date(task.started_at).toLocaleTimeString()} - {task.task?.type || 'unknown'}
                    </span>
                    <Badge className={task.result ? 'bg-green-400/20 text-green-400' : 'bg-red-400/20 text-red-400'}>
                      {task.result ? 'SUCCESS' : 'PENDING'}
                    </Badge>
                  </div>
                ))
              ) : (
                <div className="text-matrix-green/60 text-center py-4">
                  No task history available
                </div>
              )}
            </div>
          </TerminalWindow>

          {/* Quick Actions */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Link to="/ai-solver">
              <Card className="modern-card hover-lift cursor-pointer">
                <CardHeader>
                  <CardTitle className="text-matrix-green flex items-center">
                    <Bot className="w-5 h-5 mr-2" />
                    AI Problem Solver
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-matrix-green/70 text-sm">Launch AI-powered business problem analysis</p>
                </CardContent>
              </Card>
            </Link>

            <Link to="/services">
              <Card className="modern-card hover-lift cursor-pointer">
                <CardHeader>
                  <CardTitle className="text-matrix-green flex items-center">
                    <Users className="w-5 h-5 mr-2" />
                    Service Catalog
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-matrix-green/70 text-sm">Browse available AI-powered services</p>
                </CardContent>
              </Card>
            </Link>

            <Link to="/contact">
              <Card className="modern-card hover-lift cursor-pointer">
                <CardHeader>
                  <CardTitle className="text-matrix-green flex items-center">
                    <Eye className="w-5 h-5 mr-2" />
                    Support Console
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-matrix-green/70 text-sm">Connect with our technical support team</p>
                </CardContent>
              </Card>
            </Link>
          </div>
        </div>
      </div>
    </MobileMatrixOptimizer>
  );
};

export default AgentDashboard;