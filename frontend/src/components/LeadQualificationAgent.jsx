import React, { useState, useEffect } from 'react';
import { Bot, CheckCircle, Clock, AlertCircle, TrendingUp, User, Mail, Phone } from 'lucide-react';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import TerminalWindow from './TerminalWindow';

const LeadQualificationAgent = ({ leadData, onQualificationComplete }) => {
  const [isQualifying, setIsQualifying] = useState(false);
  const [qualificationResult, setQualificationResult] = useState(null);
  const [agentStatus, setAgentStatus] = useState('idle');
  const [taskId, setTaskId] = useState(null);

  useEffect(() => {
    if (leadData && Object.keys(leadData).length > 0) {
      qualifyLead();
    }
  }, [leadData]);

  const qualifyLead = async () => {
    setIsQualifying(true);
    setAgentStatus('running');
    
    const backendUrl = process.env.REACT_APP_BACKEND_URL || "http://localhost:8001";
    
    try {
      // Submit lead qualification task to Sales Agent
      const response = await fetch(`${backendUrl}/api/agents/sales/qualify-lead`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(leadData)
      });

      if (response.ok) {
        const result = await response.json();
        setTaskId(result.data?.task_id);
        
        // Poll for results (in a real implementation, you'd use WebSockets or Server-Sent Events)
        setTimeout(() => {
          // Mock result for demonstration
          const mockResult = {
            lead_id: `lead_${Date.now()}`,
            qualified: leadData.budget && leadData.budget !== 'under_5k',
            score: Math.random() * 4 + 6, // 6-10 range
            analysis: {
              ai_analysis: `Based on the provided information, this lead shows ${leadData.budget && leadData.budget !== 'under_5k' ? 'strong' : 'moderate'} potential for conversion. The business requirements align well with our service offerings.`,
              market_insights: `The ${leadData.industry || 'general'} industry is experiencing significant digital transformation trends, creating opportunities for growth.`,
              strategy_proposal: `Recommended approach: Start with a consultation to understand specific needs, then propose a phased implementation of digital solutions.`
            },
            response_template: `Thank you ${leadData.name || 'for your interest'}! Our AI analysis indicates you would benefit from our digital transformation services. I'd like to schedule a consultation to discuss your specific needs.`,
            recommendations: [
              {
                service: "Digital Ecosystem Development",
                price_range: "AED 8,999-19,999/month",
                fit_reason: "Comprehensive solution for your digital transformation needs",
                expected_roi: "200-300% ROI within 6 months",
                timeline: "4-6 weeks implementation"
              }
            ]
          };
          
          setQualificationResult(mockResult);
          setAgentStatus('completed');
          setIsQualifying(false);
          
          if (onQualificationComplete) {
            onQualificationComplete(mockResult);
          }
        }, 3000); // 3 second delay to simulate processing
        
      } else {
        throw new Error('Failed to qualify lead');
      }
    } catch (error) {
      console.error('Lead qualification error:', error);
      setAgentStatus('error');
      setIsQualifying(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'running': return 'text-blue-400 bg-blue-400/20 border-blue-400/40';
      case 'completed': return 'text-green-400 bg-green-400/20 border-green-400/40';
      case 'error': return 'text-red-400 bg-red-400/20 border-red-400/40';
      default: return 'text-matrix-green bg-matrix-green/20 border-matrix-green/40';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'running': return <Clock className="w-4 h-4 animate-spin" />;
      case 'completed': return <CheckCircle className="w-4 h-4" />;
      case 'error': return <AlertCircle className="w-4 h-4" />;
      default: return <Bot className="w-4 h-4" />;
    }
  };

  return (
    <div className="space-y-6">
      {/* Agent Status Header */}
      <Card className="modern-card">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Bot className="w-8 h-8 text-matrix-cyan animate-pulse-glow" />
              <div>
                <CardTitle className="text-matrix-green font-heading">AI Sales Agent</CardTitle>
                <CardDescription className="text-matrix-green/60">Intelligent lead qualification in progress</CardDescription>
              </div>
            </div>
            <Badge className={`${getStatusColor(agentStatus)} font-mono text-xs`}>
              {getStatusIcon(agentStatus)}
              <span className="ml-1">{agentStatus.toUpperCase()}</span>
            </Badge>
          </div>
        </CardHeader>
        {taskId && (
          <CardContent>
            <div className="text-sm text-matrix-green/70 font-mono">
              Task ID: {taskId}
            </div>
          </CardContent>
        )}
      </Card>

      {/* Processing Animation */}
      {isQualifying && (
        <TerminalWindow title="AI_SALES_AGENT.log" className="animate-fadeInUp">
          <div className="space-y-2 text-sm font-mono">
            <div className="text-matrix-green animate-glow">
              &gt; Initializing lead qualification process...
            </div>
            <div className="text-matrix-cyan animate-glow" style={{animationDelay: '0.5s'}}>
              &gt; Analyzing business requirements and budget alignment...
            </div>
            <div className="text-matrix-green animate-glow" style={{animationDelay: '1s'}}>
              &gt; Evaluating market fit and growth potential...
            </div>
            <div className="text-matrix-cyan animate-glow" style={{animationDelay: '1.5s'}}>
              &gt; Generating personalized recommendations...
            </div>
            <div className="text-matrix-green animate-glow" style={{animationDelay: '2s'}}>
              &gt; Calculating ROI projections and implementation timeline...
            </div>
            <div className="text-matrix-bright-cyan animate-glow" style={{animationDelay: '2.5s'}}>
              &gt; Finalizing qualification report...
            </div>
          </div>
        </TerminalWindow>
      )}

      {/* Qualification Results */}
      {qualificationResult && (
        <div className="space-y-6 animate-fadeInUp">
          {/* Lead Score */}
          <Card className="modern-card hover-glow">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-matrix-green flex items-center">
                  <TrendingUp className="w-5 h-5 mr-2" />
                  Lead Qualification Score
                </CardTitle>
                <div className="text-right">
                  <div className="text-3xl font-bold text-matrix-bright-cyan">
                    {qualificationResult.score.toFixed(1)}/10
                  </div>
                  <Badge className={qualificationResult.qualified ? 
                    'bg-green-400/20 text-green-400 border-green-400/40' : 
                    'bg-yellow-400/20 text-yellow-400 border-yellow-400/40'
                  }>
                    {qualificationResult.qualified ? 'QUALIFIED' : 'NEEDS NURTURING'}
                  </Badge>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-matrix-green/80 text-sm">
                {qualificationResult.analysis.ai_analysis}
              </p>
            </CardContent>
          </Card>

          {/* Service Recommendations */}
          <Card className="modern-card hover-glow">
            <CardHeader>
              <CardTitle className="text-matrix-green">AI-Recommended Services</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {qualificationResult.recommendations.map((rec, index) => (
                  <div key={index} className="border border-matrix-green/20 rounded-lg p-4 hover:border-matrix-green/40 transition-colors">
                    <div className="flex items-start justify-between mb-2">
                      <h4 className="font-semibold text-matrix-green">{rec.service}</h4>
                      <Badge variant="outline" className="text-matrix-cyan border-matrix-cyan/40">
                        {rec.price_range}
                      </Badge>
                    </div>
                    <p className="text-sm text-matrix-green/70 mb-3">{rec.fit_reason}</p>
                    <div className="grid grid-cols-2 gap-4 text-xs">
                      <div>
                        <span className="text-matrix-green/60">Expected ROI:</span>
                        <div className="text-matrix-bright-cyan font-mono">{rec.expected_roi}</div>
                      </div>
                      <div>
                        <span className="text-matrix-green/60">Timeline:</span>
                        <div className="text-matrix-bright-cyan font-mono">{rec.timeline}</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* AI-Generated Response */}
          <TerminalWindow title="AI_RESPONSE_TEMPLATE.txt">
            <div className="text-matrix-green/80 font-mono text-sm leading-relaxed">
              {qualificationResult.response_template}
            </div>
          </TerminalWindow>

          {/* Action Buttons */}
          <div className="flex space-x-4">
            <Button className="btn-matrix hover-lift font-heading">
              <Mail className="w-4 h-4 mr-2" />
              Send AI Response
            </Button>
            <Button variant="outline" className="border-matrix-green text-matrix-green hover:bg-matrix-green/10">
              <Phone className="w-4 h-4 mr-2" />
              Schedule Call
            </Button>
            <Button variant="outline" className="border-matrix-green text-matrix-green hover:bg-matrix-green/10">
              <User className="w-4 h-4 mr-2" />
              Add to CRM
            </Button>
          </div>
        </div>
      )}
    </div>
  );
};

export default LeadQualificationAgent;