"""
Base Agent Class - Foundation for all AI agents in the platform
"""
import uuid
import asyncio
import logging
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from enum import Enum
import json

class AgentStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    ERROR = "error"
    COMPLETED = "completed"

class AgentCapability(Enum):
    LEAD_QUALIFICATION = "lead_qualification"
    CAMPAIGN_MANAGEMENT = "campaign_management"
    CONTENT_CREATION = "content_creation"
    DATA_ANALYSIS = "data_analysis"
    WORKFLOW_AUTOMATION = "workflow_automation"
    CLIENT_COMMUNICATION = "client_communication"

class BaseAgent(ABC):
    """
    Base class for all AI agents in the NOWHERE platform
    Provides core functionality: logging, memory access, event handling
    """
    
    def __init__(self, agent_id: str = None, name: str = "", description: str = ""):
        self.agent_id = agent_id or str(uuid.uuid4())
        self.name = name
        self.description = description
        self.status = AgentStatus.IDLE
        self.created_at = datetime.now(timezone.utc)
        self.last_activity = datetime.now(timezone.utc)
        
        # Agent configuration
        self.config = {}
        self.capabilities = []
        self.memory = {}
        self.context = {}
        
        # Logging setup
        self.logger = logging.getLogger(f"agent.{self.name.lower().replace(' ', '_')}")
        
        # Event handlers
        self.event_handlers = {}
        
        # Performance tracking
        self.metrics = {
            "tasks_completed": 0,
            "tasks_failed": 0,
            "total_runtime": 0,
            "success_rate": 0.0
        }
        
    @abstractmethod
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a task - must be implemented by each agent
        """
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[AgentCapability]:
        """
        Return list of agent capabilities
        """
        pass
    
    async def execute(self, task: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Main execution method with logging, error handling, and metrics
        """
        task_id = task.get('id', str(uuid.uuid4()))
        self.status = AgentStatus.RUNNING
        start_time = datetime.now(timezone.utc)
        
        try:
            self.logger.info(f"Starting task {task_id}: {task.get('type', 'unknown')}")
            
            # Update context
            if context:
                self.context.update(context)
            
            # Store task in memory
            self._store_task_memory(task_id, task)
            
            # Process the task
            result = await self.process_task(task)
            
            # Update metrics
            self.metrics["tasks_completed"] += 1
            self.status = AgentStatus.COMPLETED
            
            # Calculate success rate
            total_tasks = self.metrics["tasks_completed"] + self.metrics["tasks_failed"]
            self.metrics["success_rate"] = self.metrics["tasks_completed"] / total_tasks if total_tasks > 0 else 0
            
            # Store result in memory
            self._store_result_memory(task_id, result)
            
            self.logger.info(f"Task {task_id} completed successfully")
            
            return {
                "success": True,
                "task_id": task_id,
                "agent_id": self.agent_id,
                "result": result,
                "execution_time": (datetime.now(timezone.utc) - start_time).total_seconds(),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Task {task_id} failed: {str(e)}")
            self.metrics["tasks_failed"] += 1
            self.status = AgentStatus.ERROR
            
            return {
                "success": False,
                "task_id": task_id,
                "agent_id": self.agent_id,
                "error": str(e),
                "execution_time": (datetime.now(timezone.utc) - start_time).total_seconds(),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        finally:
            self.last_activity = datetime.now(timezone.utc)
            if self.status == AgentStatus.RUNNING:
                self.status = AgentStatus.IDLE
    
    def _store_task_memory(self, task_id: str, task: Dict[str, Any]):
        """Store task information in agent memory"""
        if 'tasks' not in self.memory:
            self.memory['tasks'] = {}
        
        self.memory['tasks'][task_id] = {
            'task': task,
            'started_at': datetime.now(timezone.utc).isoformat()
        }
    
    def _store_result_memory(self, task_id: str, result: Dict[str, Any]):
        """Store task result in agent memory"""
        if 'tasks' in self.memory and task_id in self.memory['tasks']:
            self.memory['tasks'][task_id]['result'] = result
            self.memory['tasks'][task_id]['completed_at'] = datetime.now(timezone.utc).isoformat()
    
    async def get_memory(self, key: str = None) -> Dict[str, Any]:
        """Retrieve agent memory"""
        if key:
            return self.memory.get(key, {})
        return self.memory
    
    async def update_memory(self, key: str, value: Any):
        """Update agent memory"""
        self.memory[key] = value
        self.logger.debug(f"Memory updated: {key}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status and metrics"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "capabilities": [cap.value for cap in self.get_capabilities()],
            "metrics": self.metrics,
            "last_activity": self.last_activity.isoformat(),
            "uptime": (datetime.now(timezone.utc) - self.created_at).total_seconds()
        }
    
    async def pause(self):
        """Pause agent execution"""
        self.status = AgentStatus.PAUSED
        self.logger.info(f"Agent {self.name} paused")
    
    async def resume(self):
        """Resume agent execution"""
        self.status = AgentStatus.IDLE
        self.logger.info(f"Agent {self.name} resumed")
    
    async def reset(self):
        """Reset agent state"""
        self.status = AgentStatus.IDLE
        self.memory.clear()
        self.context.clear()
        self.metrics = {
            "tasks_completed": 0,
            "tasks_failed": 0,
            "total_runtime": 0,
            "success_rate": 0.0
        }
        self.logger.info(f"Agent {self.name} reset")
    
    def add_event_handler(self, event_type: str, handler):
        """Add event handler for agent"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
    
    async def emit_event(self, event_type: str, data: Dict[str, Any]):
        """Emit event to handlers"""
        if event_type in self.event_handlers:
            for handler in self.event_handlers[event_type]:
                try:
                    await handler(data)
                except Exception as e:
                    self.logger.error(f"Event handler error: {e}")
    
    def configure(self, config: Dict[str, Any]):
        """Update agent configuration"""
        self.config.update(config)
        self.logger.info(f"Agent {self.name} configured with: {list(config.keys())}")
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.agent_id}, name={self.name}, status={self.status.value})>"