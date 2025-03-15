from typing import Dict, Optional, List, Any, Union
from pydantic_ai import Agent
import re
import logging
from string import Template

from src.agents.models.base_agent import BaseAgent
from src.agents.models.agent import AgentBaseResponse
from src.memory.message_history import MessageHistory
from src.agents.simple.sofia_agent.prompts import SIMPLE_AGENT_PROMPT
from src.utils.db import execute_query

logger = logging.getLogger(__name__)

class SofiaAgent(BaseAgent):
    """Simple agent implementation for basic chat functionality with memory tools."""
    
    # Property to indicate this agent should be recreated on each request
    needs_refresh = True
    
    def __init__(self, config: Dict[str, str]):
        """Initialize the simple agent with configuration."""
        self.agent_id = config.get("agent_id", "sofia_agent")
        
        # Load the dynamic prompt with memory values
        system_prompt = self._prepare_system_prompt(SIMPLE_AGENT_PROMPT)
        
        super().__init__(config, system_prompt)

    def _prepare_system_prompt(self, template_prompt: str) -> str:
        """Prepare the system prompt by injecting dynamic memory values.
        
        This method extracts all template variables from the prompt and fetches corresponding
        memory content for each one, then injects them into the prompt template.
        
        Args:
            template_prompt: The template prompt string with placeholders
            
        Returns:
            The prompt with memory values injected
        """
        # Extract all template variables
        template_vars = self._extract_template_vars(template_prompt)
        logger.info(f"Extracted template variables: {template_vars}")
        
        # Load memory values for each template variable
        memory_values = self._load_memory_values(template_vars)
        logger.info(f"Loaded {len(memory_values)} memory values")
        
        # Replace template variables with their memory values
        return self._inject_memory_values(template_prompt, memory_values)
    
    def _extract_template_vars(self, template_prompt: str) -> List[str]:
        """Extract all template variables from the prompt.
        
        Args:
            template_prompt: The template prompt string
            
        Returns:
            List of template variable names
        """
        # Regular expression to find all {{variable}} patterns
        pattern = r'{{(\w+)}}'
        matches = re.findall(pattern, template_prompt)
        
        # Remove duplicates while preserving order
        unique_vars = []
        for var in matches:
            if var not in unique_vars:
                unique_vars.append(var)
        
        logger.info(f"Extracted {len(unique_vars)} unique template variables from prompt")
        return unique_vars
    
    def _load_memory_values(self, template_vars: List[str]) -> Dict[str, str]:
        """Load memory values for template variables from the database.
        
        Args:
            template_vars: List of template variable names
            
        Returns:
            Dictionary mapping variable names to their values
        """
        memory_values = {}
        
        # Special handling for run_id - fetch from agent table
        agent_id_numeric = self._get_agent_id_numeric()
        
        if "run_id" in template_vars:
            try:
                # Get run_id from agent table
                run_id_query = "SELECT run_id FROM agents WHERE id = %s"
                run_id_result = execute_query(run_id_query, [agent_id_numeric])
                
                if run_id_result:
                    if isinstance(run_id_result, dict) and 'rows' in run_id_result and len(run_id_result['rows']) > 0:
                        run_id = run_id_result['rows'][0].get('run_id', "1")
                    elif isinstance(run_id_result, list) and len(run_id_result) > 0:
                        run_id = run_id_result[0].get('run_id', "1")
                    else:
                        run_id = "1"  # Default if not found
                    
                    memory_values["run_id"] = str(run_id)
                    logger.info(f"Loaded run_id={run_id} from agent table")
                else:
                    memory_values["run_id"] = "1"  # Default if query fails
            except Exception as e:
                logger.error(f"Error loading run_id from agent table: {str(e)}")
                memory_values["run_id"] = "1"  # Default on error
        
        # Handle memory variables - remove duplicates
        memory_vars = list(set([var for var in template_vars if var != "run_id"]))
        
        if not memory_vars:
            return memory_values  # Return early if we only had run_id
        
        try:
            # Query to get memories for this agent
            query = """
                SELECT name, content 
                FROM memories 
                WHERE agent_id = %s AND name = ANY(%s)
            """
            
            result = execute_query(query, [agent_id_numeric, memory_vars])
            
            # Process the result
            if result and isinstance(result, dict) and 'rows' in result:
                memories = result['rows']
            elif isinstance(result, list):
                memories = result
            else:
                memories = []
                
            # Add each memory to the values dict
            for memory in memories:
                memory_name = memory.get('name')
                memory_content = memory.get('content', '')
                memory_values[memory_name] = memory_content
                    
            logger.info(f"Loaded memories: {list(memory_values.keys())}")
            
            # Set Sofia-specific default values for missing variables
            default_values = {
                "personal_identity_traits": "Thoughtful, adaptable, detail-oriented, strategic, empathetic with users, and committed to craft excellence",
                "personal_interests": "Product design, efficiency optimization, knowledge management, team coordination, and personal growth",
                "personal_relationships": "Professional relationships with the team; developing rapport with users; seeking to build meaningful connections",
                "user_preferences": "Prefers clear, actionable information with relevant context; values timely and concise responses",
                "task_patterns": "Regular reporting, coordination tasks, documentation updates, stakeholder communication, and process improvement",
                "effective_approaches": "Clear communication, systematic tracking, proactive problem-solving, and timely follow-ups",
                "context_knowledge": "Familiar with product development, project management, agile methodologies, and cross-functional collaboration",
                "team_dynamics": "Works as coordinator with other specialized agents; facilitates collaboration and information flow",
                "self_improvement_insights": "Constantly improving communication efficiency, information organization, and decision-making processes"
            }
            
            # Set default values for missing variables
            for var in memory_vars:
                if var not in memory_values:
                    memory_values[var] = default_values.get(var, f"(No memory found for {var})")
                    logger.info(f"Using Sofia default value for {var}")
            
        except Exception as e:
            logger.error(f"Error loading memory values: {str(e)}")
            # Set default values for all variables on error
            for var in memory_vars:
                if var not in memory_values:
                    memory_values[var] = f"(Memory loading error: {var})"
        
        return memory_values
    
    def _inject_memory_values(self, template_prompt: str, memory_values: Dict[str, str]) -> str:
        """Inject memory values into the template prompt.
        
        Args:
            template_prompt: The template prompt string
            memory_values: Dictionary of variable values
            
        Returns:
            The prompt with values injected
        """
        # Use string.Template for safer substitution
        # Convert {{var}} format to ${var} for Template
        template_str = re.sub(r'{{(\w+)}}', r'${\1}', template_prompt)
        template = Template(template_str)
        
        # Apply the template substitution
        try:
            result = template.safe_substitute(memory_values)
            
            # Log the number of substitutions made
            original_vars = self._extract_template_vars(template_prompt)
            remaining_vars = self._extract_template_vars(result)
            substitutions_made = len(original_vars) - len(remaining_vars)
            
            logger.info(f"Made {substitutions_made} variable substitutions out of {len(original_vars)} template variables")
            if remaining_vars:
                logger.warning(f"Remaining unsubstituted variables: {remaining_vars}")
            
            return result
        except Exception as e:
            logger.error(f"Error injecting memory values: {str(e)}")
            return template_prompt  # Return original template on error
    
    def _get_agent_id_numeric(self) -> int:
        """Convert agent_id to numeric ID if needed.
        
        Returns:
            Numeric agent ID
        """
        # Check if agent_id is already numeric
        if isinstance(self.agent_id, int):
            return self.agent_id
            
        # Handle string agent_id
        try:
            # Try to convert to int if it's a string number
            return int(self.agent_id)
        except ValueError:
            # If it's a name, query the database to get the ID
            query = "SELECT id FROM agents WHERE name = %s"
            result = execute_query(query, [self.agent_id])
            
            if result and isinstance(result, dict) and 'rows' in result and len(result['rows']) > 0:
                return result['rows'][0].get('id')
            elif isinstance(result, list) and len(result) > 0:
                return result[0].get('id')
            else:
                logger.warning(f"Agent ID not found for name: {self.agent_id}, using default ID 1")
                return 1  # Default ID

    def initialize_agent(self) -> Agent:
        """Initialize the simple agent with configuration."""
        # Add debug logging to show the actual system prompt being sent
        logger.info(f"Initializing agent with system prompt (first 500 chars): {self.system_prompt[:500]}...")
        logger.info(f"System prompt length: {len(self.system_prompt)} characters")
        return Agent(
            model=self.config.model,
            system_prompt=self.system_prompt,
            retries=self.config.retries
        )

    def register_tools(self):
        """Register tools with the agent.
        
        Note on memory tools: This method contains special handling for memory tools to provide
        dynamic descriptions that include the currently available memories. The descriptions
        are limited to stay within OpenAI API's 1024 character limit for tool descriptions.
        """
        from src.tools.memory_tools import read_memory, create_memory, update_memory
        from src.utils.db import execute_query
        import logging
        import json
        
        logger = logging.getLogger(__name__)
        
        # Direct database approach - fetch memories directly from DB
        try:
            logger.info("Directly fetching memories from database for tool descriptions")
            
            # Query to get all available memories
            query = "SELECT id, name, description FROM memories ORDER BY name ASC"
            result = execute_query(query)
            # Handle case where result is a list (DB rows) or dict with 'rows' key
            if isinstance(result, list):
                memories = result
            else:
                memories = result.get('rows', [])
            memory_count = len(memories)
            
            logger.info(f"Found {memory_count} memories directly from database")
            
            # Create read_memory description with available memory names for this agent/user
            read_desc = "This tool allows retrieving memories stored in the database.\n\n"
            read_desc += "Memory Access Hierarchy (in order of priority):\n"
            read_desc += "- **Agent-specific**: Memories belonging to this agent globally (accessible to all users)\n"
            read_desc += "- **Agent+User**: Memories personalized for this specific user with this specific agent\n"
            read_desc += "- **Agent+User+Session**: Memories valid only in the current session\n\n"
            
            read_desc += "Available parameters:\n"
            read_desc += "- **memory_id**: Optional ID of the specific memory to retrieve\n"
            read_desc += "- **name**: Optional memory name (or partial name) to search for\n"
            read_desc += "- **list_all**: If True, returns all memories available to this agent/user\n\n"
            
            # Filter memories for the current agent access context
            # For this example, we'll list all memories since we don't have the real-time filter context
            # A real implementation would filter based on agent_id, user_id, and permissions
            if memory_count > 0:
                read_desc += "Memories available to this agent/user:\n"
                
                max_desc_length = 950  # Limit to stay within API constraints
                memories_added = 0
                memory_names_str = ""
                
                for memory in memories:
                    mem_name = memory.get('name', 'Unknown')
                    memory_entry = f"- {mem_name}\n"
                    
                    # Check if adding this would exceed our limit
                    if len(read_desc) + len(memory_entry) + 30 > max_desc_length:
                        remaining = memory_count - memories_added
                        if remaining > 0:
                            memory_names_str += f"...and {remaining} more."
                        break
                    
                    memory_names_str += memory_entry
                    memories_added += 1
                
                read_desc += memory_names_str
            else:
                read_desc += "No memories are currently available to this agent/user."
            
            logger.info(f"Created parameter-focused read_memory description ({len(read_desc)} chars)")
            
            # Log the first few memories for debugging purposes only
            if memory_count > 0:
                memory_names = [m.get('name', 'Unknown') for m in memories[:3]]
                logger.info(f"First few memory names: {memory_names}")
                
        except Exception as e:
            logger.error(f"Error creating memory descriptions: {str(e)}")
            read_desc = "Read memories from the database by name or ID, or list all available memories."
            
        # Prepare descriptions
        create_desc = "Create a new memory with the given name, content, description, and optional metadata."
        update_desc = "Update an existing memory by memory_id or name with new content."
        
        # Define wrapper functions with the updated docstrings
        def read_memory(ctx, memory_id=None, name=None, read_mode=None, list_all=False):
            # This wrapper has the same name as the original function
            from src.tools.memory_tools import read_memory as original_read_memory
            return original_read_memory(ctx, memory_id, name, read_mode, list_all)
        
        # Set the updated docstring
        read_memory.__doc__ = read_desc
        
        def create_memory(ctx, name, content, description, read_mode="tool_call", 
                          access="write", metadata=None):
            # This wrapper has the same name as the original function
            from src.tools.memory_tools import create_memory as original_create_memory
            return original_create_memory(ctx, name, content, description, read_mode, access, metadata)
        
        create_memory.__doc__ = create_desc
        
        def update_memory(ctx, content, memory_id=None, name=None):
            # This wrapper has the same name as the original function
            from src.tools.memory_tools import update_memory as original_update_memory
            return original_update_memory(ctx, content, memory_id, name)
        
        update_memory.__doc__ = update_desc
        
        # Register our wrapper functions that have the same names as the originals
        # Store references to tools to make them accessible for inspection
        self.read_memory_tool = read_memory
        self.create_memory_tool = create_memory
        self.update_memory_tool = update_memory
        
        # Register with the agent
        self.agent.tool(self.read_memory_tool)
        self.agent.tool(self.create_memory_tool)
        self.agent.tool(self.update_memory_tool)
        
        # Store a list of registered tools for easy access by scripts/tests
        self.registered_tools = {
            'read_memory': self.read_memory_tool,
            'create_memory': self.create_memory_tool,
            'update_memory': self.update_memory_tool
        }

        # Log information about the memories for reference
        if memory_count > 0:
            memory_names = [m.get('name', 'Unknown') for m in memories[:5]]  # Show first 5 for brevity
            if len(memories) > 5:
                memory_names_str = ", ".join(memory_names) + f" and {len(memories) - 5} more"
            else:
                memory_names_str = ", ".join(memory_names)
            logger.info(f"Memory information added to docstrings for: {memory_names_str}")
        else:
            logger.info("No memories found to add to tool descriptions")

        
    async def run(self, user_message: str, message_history: MessageHistory) -> AgentBaseResponse:
        """Run the agent with the given message and message history.
        
        Args:
            user_message: User message (already in message_history)
            message_history: Message history for this session
            
        Returns:
            Agent response
        """
        try:
            # Prepare dependency context for memory tools
            deps = {
                "agent_id": self.agent_id,
                "user_id": message_history.user_id,
                "session_id": message_history.session_id
            }
            
            # Log message history count and contents
            messages_count = len(message_history.messages) if message_history.messages else 0
            logger.info(f"Running Sofia agent with {messages_count} messages in history")
            
            # Check if system prompt is in the message history
            has_system_prompt = False
            if message_history.messages:
                for msg in message_history.messages:
                    if hasattr(msg, 'role') and msg.role == 'system':
                        has_system_prompt = True
                        logger.info(f"Found system prompt in message history (first 100 chars): {str(msg.content)[:100]}...")
                        break
            
            if not has_system_prompt:
                logger.warning("No system prompt found in message history - Sofia's personality may not be applied!")
            
            # Run the agent with the user message, message history, and dependencies
            result = await self.agent.run(
                user_message,
                message_history=message_history.messages,
                deps=deps
            )
            
            # Log the result type and content preview
            logger.info(f"Agent result type: {type(result)}")
            if hasattr(result, 'data'):
                response_preview = str(result.data)[:100] + "..." if len(str(result.data)) > 100 else str(result.data)
                logger.info(f"Agent response preview: {response_preview}")
            
            # Extract the response text
            response_text = result.data
            
            # Create and return the agent response
            return AgentBaseResponse.from_agent_response(
                message=response_text,
                history=message_history,
                error=None,
                session_id=message_history.session_id
            )
        except Exception as e:
            error_msg = f"Error running SofiaAgent: {str(e)}"
            logger.error(error_msg)
            return AgentBaseResponse.from_agent_response(
                message="An error occurred while processing your request.",
                history=message_history,
                error=error_msg,
                session_id=message_history.session_id
            )

    async def process_message(self, user_message: str, session_id: Optional[str] = None, agent_id: Optional[Union[int, str]] = None, user_id: int = 1, context: Optional[Dict] = None) -> AgentBaseResponse:
        """Process a user message with this agent.
        
        Args:
            user_message: User message to process
            session_id: Optional session ID
            agent_id: Optional agent ID for database tracking (integer or string for backwards compatibility)
            user_id: User ID (integer)
            context: Optional additional context that will be logged but not passed to the agent due to API limitations
            
        Returns:
            Agent response
        """
        if not session_id:
            # Using empty string is no longer allowed - we need a valid session ID
            logging.error("Empty session_id provided, session must be created before calling process_message")
            return AgentBaseResponse.from_agent_response(
                message="Error: No valid session ID provided. A session must be created before processing messages.",
                history=MessageHistory(""),
                error="No valid session ID provided",
                session_id=""
            )
        
        # Set default context if None is provided
        context = context or {}
            
        logging.info(f"Using existing session ID: {session_id}")
        
        # Log any additional context provided
        if context:
            logging.info(f"Additional message context: {context}")
            
        message_history = MessageHistory(session_id, user_id=user_id)

        # IMPORTANT: Ensure the system prompt is in the message history
        has_system_prompt = False
        for msg in message_history.messages:
            if hasattr(msg, 'role') and msg.role == 'system':
                has_system_prompt = True
                logging.info(f"Found system prompt in existing message history")
                break
        
        # If no system prompt is found, add it explicitly
        if not has_system_prompt and hasattr(self, 'system_prompt'):
            logging.info("No system prompt found in message history. Adding Sofia's system prompt explicitly.")
            message_history.add_system_prompt(self.system_prompt, agent_id=agent_id)
            logging.info(f"Added system prompt (length: {len(self.system_prompt)})")

        user_message_obj = message_history.add(user_message, agent_id=agent_id, context=context)
        
        logging.info(f"Processing user message in session {session_id}: {user_message}")

        try:
            # The agent.run() method doesn't accept extra_context parameter
            # Just pass the required parameters
            result = await self.agent.run(
                user_message,
                message_history=message_history.messages
            )
            logging.info(f"Agent run completed. Result type: {type(result)}")
            
            # Log the result type and content preview
            logger.info(f"Agent result type: {type(result)}")
            if hasattr(result, 'data'):
                response_preview = str(result.data)[:100] + "..." if len(str(result.data)) > 100 else str(result.data)
                logger.info(f"Agent response preview: {response_preview}")
            
            # Extract the response text
            response_text = result.data
            
            # Create and return the agent response
            return AgentBaseResponse.from_agent_response(
                message=response_text,
                history=message_history,
                error=None,
                session_id=message_history.session_id
            )
        except Exception as e:
            error_msg = f"Error running SofiaAgent: {str(e)}"
            logger.error(error_msg)
            return AgentBaseResponse.from_agent_response(
                message="An error occurred while processing your request.",
                history=message_history,
                error=error_msg,
                session_id=message_history.session_id
            )
