"""Tests for the SimpleAgent tool registration functionality.

This module verifies that tools are properly registered with the agent
according to the documentation.
"""
import unittest
import os
import logging
from unittest.mock import patch, MagicMock

from src.agents.simple.simple_agent.agent import SimpleAgent
from src.agents.models.dependencies import SimpleAgentDependencies

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestSimpleAgentTools(unittest.TestCase):
    """Test cases for SimpleAgent tool registration."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = {
            "model": "openai:gpt-3.5-turbo",
            "enable_duckduckgo_search": "true",
            "tavily_api_key": "test-api-key",
            "agent_id": "test-agent"
        }
    
    @patch("src.agents.simple.simple_agent.agent.Agent")
    @patch("src.agents.simple.simple_agent.agent.DUCKDUCKGO_AVAILABLE", True)
    @patch("src.agents.simple.simple_agent.agent.TAVILY_AVAILABLE", True)
    @patch("src.agents.simple.simple_agent.agent.duckduckgo_search_tool")
    @patch("src.agents.simple.simple_agent.agent.tavily_search_tool")
    def test_search_tools_registration(self, mock_tavily, mock_ddg, mock_agent_class, *mocks):
        """Test that search tools are properly registered."""
        # Create mock tools
        mock_ddg_tool = MagicMock()
        mock_tavily_tool = MagicMock()
        mock_ddg.return_value = mock_ddg_tool
        mock_tavily.return_value = mock_tavily_tool
        
        # Create a mock agent instance
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        
        # Patch memory-related imports
        with patch("src.tools.memory_tools.prompt_helpers.register_memory_prompts") as mock_register_memory, \
             patch("src.tools.memory_tools.prompt_helpers.register_standard_prompts") as mock_register_standard, \
             patch("src.agents.simple.simple_agent.agent.get_agent") as mock_get_agent:
            
            # Initialize the agent
            agent = SimpleAgent(self.config)
            
            # Verify Agent was constructed with tools
            args, kwargs = mock_agent_class.call_args
            self.assertIn('tools', kwargs)
            tools = kwargs['tools']
            
            # Get the tools that should be in the list
            tool_count = 0
            
            # Should include DuckDuckGo tool
            self.assertIn(mock_ddg_tool, tools)
            tool_count += 1
            
            # Should include Tavily tool
            self.assertIn(mock_tavily_tool, tools)
            tool_count += 1
            
            # Should include memory tools (2)
            memory_tools_count = 2
            tool_count += memory_tools_count
            
            # Should include data tools (2)
            data_tools_count = 2
            tool_count += data_tools_count
            
            # Should include multimodal tools (1)
            multimodal_tools_count = 1
            tool_count += multimodal_tools_count
            
            # Verify total number of tools
            self.assertEqual(len(tools), tool_count)
    
    @patch("src.agents.simple.simple_agent.agent.Agent")
    @patch("src.agents.simple.simple_agent.agent.DUCKDUCKGO_AVAILABLE", False)
    @patch("src.agents.simple.simple_agent.agent.TAVILY_AVAILABLE", False)
    def test_no_search_tools_when_unavailable(self, mock_agent_class, *mocks):
        """Test that search tools are not registered when unavailable."""
        # Create a mock agent instance
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        
        # Patch memory-related imports
        with patch("src.tools.memory_tools.prompt_helpers.register_memory_prompts") as mock_register_memory, \
             patch("src.tools.memory_tools.prompt_helpers.register_standard_prompts") as mock_register_standard, \
             patch("src.agents.simple.simple_agent.agent.get_agent") as mock_get_agent:
            
            # Initialize the agent
            agent = SimpleAgent(self.config)
            
            # Verify Agent was constructed with tools
            args, kwargs = mock_agent_class.call_args
            self.assertIn('tools', kwargs)
            tools = kwargs['tools']
            
            # Calculate expected number of tools without search tools
            expected_tool_count = 5  # memory (2) + data (2) + multimodal (1)
            
            # Verify search tools were not included
            self.assertEqual(len(tools), expected_tool_count)
    
    @patch("src.agents.simple.simple_agent.agent.Agent")
    @patch("src.agents.simple.simple_agent.agent.DUCKDUCKGO_AVAILABLE", True)
    @patch("src.agents.simple.simple_agent.agent.TAVILY_AVAILABLE", True)
    @patch("src.agents.simple.simple_agent.agent.duckduckgo_search_tool")
    @patch("src.agents.simple.simple_agent.agent.tavily_search_tool")
    def test_tool_types(self, mock_tavily, mock_ddg, mock_agent_class, *mocks):
        """Test that all tools have the expected types."""
        # Create mock tools
        mock_ddg_tool = MagicMock()
        mock_tavily_tool = MagicMock()
        mock_ddg.return_value = mock_ddg_tool
        mock_tavily.return_value = mock_tavily_tool
        
        # Create a mock agent instance
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        
        # Patch memory-related imports
        with patch("src.tools.memory_tools.prompt_helpers.register_memory_prompts") as mock_register_memory, \
             patch("src.tools.memory_tools.prompt_helpers.register_standard_prompts") as mock_register_standard, \
             patch("src.agents.simple.simple_agent.agent.get_agent") as mock_get_agent:
            
            # Initialize the agent
            agent = SimpleAgent(self.config)
            
            # Verify Agent was constructed with tools
            args, kwargs = mock_agent_class.call_args
            self.assertIn('tools', kwargs)
            tools = kwargs['tools']
            
            # Check that all tools are callable
            for tool in tools:
                self.assertTrue(callable(tool))

if __name__ == "__main__":
    unittest.main() 