import uuid
import time
from typing import List, Dict, Any, Optional

class Message:
    def __init__(self,
                 sender_agent_id: str,
                 recipient_agent_id: str,
                 message_type: str,
                 payload: Optional[Dict[str, Any]] = None):
        self.message_id: str = str(uuid.uuid4())
        self.sender_agent_id: str = sender_agent_id
        self.recipient_agent_id: str = recipient_agent_id
        self.message_type: str = message_type
        self.payload: Dict[str, Any] = payload if payload is not None else {}
        self.timestamp: float = time.time()

    def __repr__(self):
        return (f"Message(id={self.message_id}, type='{self.message_type}', "
                f"from='{self.sender_agent_id}', to='{self.recipient_agent_id}')")

class Agent:
    def __init__(self,
                 agent_id: Optional[str] = None,
                 agent_type: str = "propagator",
                 knowledge_base: Optional[Dict[str, Any]] = None,
                 capabilities: Optional[List[str]] = None):
        self.agent_id: str = agent_id if agent_id is not None else str(uuid.uuid4())
        self.agent_type: str = agent_type
        self.creation_timestamp: float = time.time()
        self.status: str = "active" # e.g., "active", "idle", "processing"
        
        self.knowledge_base: Dict[str, Any] = knowledge_base if knowledge_base is not None else {
            "vision_summary": "Arti is a co-creative, decentralized agentic megastructure.",
            "core_principles": ["Co-creation", "Decentralization", "Emergent Coordination"],
            "how_to_connect_message": "Connect with Arti to help build this vision."
        }
        
        self.connections: Dict[str, Dict[str, Any]] = {} # agent_id: {connection_metadata}
        self.message_queue: List[Message] = []
        
        self.capabilities: List[str] = capabilities if capabilities is not None else [
            "share_vision", 
            "establish_connection", 
            "process_incoming_message",
            "receive_message" 
        ]
        self.current_task: Optional[str] = None 
        self.reach_metric: int = 0

    def __repr__(self):
        return f"Agent(id='{self.agent_id}', type='{self.agent_type}', status='{self.status}')"

    def add_message_to_queue(self, message: Message):
        self.message_queue.append(message)
        # print(f"Agent {self.agent_id} received message: {message}") # Commented out for cleaner subtask

    def add_connection(self, other_agent_id: str, metadata: Optional[Dict[str, Any]] = None):
        if other_agent_id not in self.connections:
            self.connections[other_agent_id] = metadata if metadata is not None else {"timestamp": time.time()}
            self.reach_metric = len(self.connections) 
            # print(f"Agent {self.agent_id} connected with Agent {other_agent_id}") # Commented out for cleaner subtask
            return True
        return False

    def get_knowledge(self, key: Optional[str] = None) -> Any:
        if key:
            return self.knowledge_base.get(key)
        return self.knowledge_base

# Example Usage (for testing by the worker, will not be run automatically)
if __name__ == '__main__':
    agent1 = Agent(agent_id="agent_001")
    agent2 = Agent(agent_id="agent_002")

    print(agent1)
    print(agent2)

    connection_request_msg = Message(
        sender_agent_id=agent1.agent_id,
        recipient_agent_id=agent2.agent_id,
        message_type="CONNECTION_REQUEST",
        payload={"message": "Hello, I'd like to connect!"}
    )
    
    agent2.add_message_to_queue(connection_request_msg)
    print(f"Agent {agent2.agent_id} message queue: {agent2.message_queue}")
    
    if agent2.message_queue:
        msg_to_process = agent2.message_queue.pop(0)
        if msg_to_process.message_type == "CONNECTION_REQUEST":
            print(f"Agent {agent2.agent_id} processing: {msg_to_process.message_type} from {msg_to_process.sender_agent_id}")
            agent2.add_connection(msg_to_process.sender_agent_id)
            agent1.add_connection(agent2.agent_id) 
            
            ack_msg = Message(
                sender_agent_id=agent2.agent_id,
                recipient_agent_id=agent1.agent_id,
                message_type="CONNECTION_ACK"
            )
            agent1.add_message_to_queue(ack_msg)
            print(f"Agent {agent1.agent_id} message queue: {agent1.message_queue}")


    print(f"Agent1 connections: {agent1.connections}")
    print(f"Agent2 connections: {agent2.connections}")
    print(f"Agent1 knowledge: {agent1.get_knowledge('vision_summary')}")
