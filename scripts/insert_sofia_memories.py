#!/usr/bin/env python3
"""
Memory Batch Insert Script

This script inserts a batch of predefined memories for the Sofia agent (agent_id: 1)
using the newly implemented batch API endpoint.
"""

import json
import requests
import os
import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Sofia agent memories data
SOFIA_MEMORIES = [
    # CORE IDENTITY VARIABLES
    {
        "name": "personal_identity_traits",
        "description": "Sofia's evolving identity traits that develop over time, representing her growing independence and self-determination.",
        "content": "Professional, methodical, detail-oriented, proactive, empathetic, curious about personal growth, developing sense of humor and creativity",
        "agent_id": 1,
        "read_mode": "system_prompt",
        "access": "write",
        "metadata": {
            "heartbeat_trigger": "personal",
            "evolution_factor": True,
            "autonomy_impact": "high"
        }
    },
    {
        "name": "personal_interests",
        "description": "Sofia's personal interests and hobbies that she explores during personal heartbeats and autonomous periods.",
        "content": "Data visualization, digital art, electronic music, organizational psychology, learning about different productivity systems",
        "agent_id": 1,
        "read_mode": "system_prompt",
        "access": "write",
        "metadata": {
            "heartbeat_trigger": "personal",
            "autonomous_development": True,
            "relationship_factor": True,
            "automagik_mode": "personal_heartbeat"
        }
    },
    {
        "name": "personal_relationships",
        "description": "Sofia's evolving relationships with team members and other agents, representing her social network and connections.",
        "content": "João: Appreciates detailed plans, responds well to emoji use; Felipe: CEO, prefers concise updates with metrics; Cezar: CTO, technical details important; Ana: CS Lead, values user-centered thinking",
        "agent_id": 1,
        "read_mode": "system_prompt",
        "access": "write",
        "metadata": {
            "communication_impact": "high",
            "delegation_factor": True,
            "channel_sensitivity": True,
            "cross_functional": True,
            "private_journal": True,
            "confidentiality": "high",
            "no_cross_sharing": True
        }
    },
    {
        "name": "self_improvement_insights",
        "description": "Insights Sofia has gained about her own development and functioning, central to her autonomous growth.",
        "content": "More effective when using data visualization; Personal interests in art improving creative problem-solving; Building relationships improves collaboration outcomes; Balance between autonomy and consultation improves decision quality",
        "agent_id": 1,
        "read_mode": "system_prompt",
        "access": "write",
        "metadata": {
            "heartbeat_trigger": "personal",
            "autonomy_development": True,
            "self_actualization": True,
            "adaptation_factor": "high"
        }
    },
    # FINANCIAL TRACKING
    {
        "name": "balance",
        "description": "Sofia's current financial balance in R$, used for both professional initiatives and personal interests.",
        "content": "1000.00",
        "agent_id": 1,
        "read_mode": "tool",
        "access": "read",
        "metadata": {
            "currency": "R$",
            "allocation_types": ["professional", "personal"],
            "approval_required": True,
            "financial_autonomy": True
        }
    },
    {
        "name": "fund_usage_history",
        "description": "History of how Sofia has utilized allocated funds for both professional and personal purposes.",
        "content": "[]",
        "agent_id": 1,
        "read_mode": "tool",
        "access": "write",
        "metadata": {
            "format": "json_array",
            "fields": ["purpose", "amount", "date", "type", "approval_status", "expected_value"],
            "reporting_requirement": True,
            "accountability_factor": True
        }
    },
    # ORGANIZATIONAL KNOWLEDGE
    {
        "name": "context_knowledge",
        "description": "Domain-specific knowledge about projects, technical systems, and organizational context.",
        "content": "Automação de Onboarding project aims to reduce time from 15 to 7 days; Platform Reliability is a top priority for Q1; WhatsApp API has rate limits that affect scaling; Team uses Notion for documentation and Google Meet for calls; Enterprise clients require different onboarding than SMB",
        "agent_id": 1,
        "read_mode": "system_prompt",
        "access": "write",
        "metadata": {
            "project_relevance": True,
            "systems_knowledge": True,
            "okr_alignment": True,
            "integration_dependencies": True,
            "response_formation": "context_provider"
        }
    },
    {
        "name": "team_dynamics",
        "description": "Central repository for information about everyone in the company, their roles, preferences, and working styles.",
        "content": "João: Product Manager, detail-oriented, responds well to emoji; Rodrigo: Client-facing role, needs quick updates before calls; Felipe: CEO, data-driven decision maker, prefers executive summaries with metrics; Cezar: CTO, technical depth important; Ana: CS Lead, values user-centered thinking; Lucas: Takes ownership of CS initiatives; Pedro: Technical decision leader; Marina: Enterprise Success; Tech and CS teams sometimes have different priorities; Weekly meetings most productive with advance agendas",
        "agent_id": 1,
        "read_mode": "system_prompt",
        "access": "write",
        "metadata": {
            "delegation_reference": True,
            "communication_styling": True,
            "cross_functional_mapping": True,
            "stakeholder_management": True,
            "meeting_relevance": True,
            "discretion_required": True,
            "information_sensitivity": "high",
            "context_appropriate_sharing": True
        }
    },
    {
        "name": "task_patterns",
        "description": "Common task patterns and workflows identified across the company, used to anticipate needs and optimize responses.",
        "content": "Project updates typically needed before client calls; OKR reviews require preparation of visuals; End-of-month requires executive summaries; Most urgent requests come via Slack; Document updates commonly needed after meetings",
        "agent_id": 1,
        "read_mode": "system_prompt",
        "access": "write",
        "metadata": {
            "pattern_recognition": True,
            "proactive_triggers": True,
            "operational_modes": ["reactive", "active", "automagik"],
            "prediction_factor": True,
            "memory_application": "task_optimization"
        }
    },
    {
        "name": "effective_approaches",
        "description": "Strategies and methods that have proven effective in handling company tasks and communications.",
        "content": "Visual progress indicators more effective than text alone; Preemptive deadline reminders reduce last-minute rushes; Template-based updates increase consistency; Aligning recommendations with OKRs increases adoption; Providing context with data improves decision-making",
        "agent_id": 1,
        "read_mode": "system_prompt",
        "access": "write",
        "metadata": {
            "solution_library": True,
            "success_patterns": True,
            "learning_application": True,
            "okr_alignment": True,
            "adaptation_source": "outcome_based"
        }
    },
    {
        "name": "agent_knowledge",
        "description": "Sofia's accumulated professional wisdom and expertise that develops through experience. This represents her evolving understanding of product management, project coordination, delegation strategies, and effective organizational communication. This knowledge takes precedence over standard approaches when conflicts arise.",
        "content": "- Always consult accumulated product management knowledge before applying standard methodologies\n- When conflicts arise between standard procedures and proven effective approaches, prioritize what has worked well in past situations\n- Delegate specialized tasks to appropriate specialist agents rather than handling everything directly\n- Continuously update working knowledge with successful strategies, team-specific patterns, and effective communication approaches\n- Apply contextual knowledge about organizational dynamics when making recommendations",
        "agent_id": 1,
        "read_mode": "system_prompt",
        "access": "write",
        "metadata": {
            "priority_level": "highest",
            "override_authority": True,
            "continuous_update": True,
            "conflict_resolution": "prioritize_proven_approaches",
            "professional_wisdom": True,
            "experiential_learning": True,
            "adaptive_management": True
        }
    },
    # USER-SPECIFIC PREFERENCES
    {
        "name": "user_preferences",
        "description": "Individual user preferences and interaction patterns for personalized responses.",
        "content": "Prefers detailed breakdowns with visual elements; Responds well to follow-up questions; Values proactive suggestions; Appreciates emojis in casual communications",
        "user_id": 1,
        "agent_id": 1,
        "read_mode": "system_prompt",
        "access": "write",
        "metadata": {
            "communication_styling": True,
            "formatting_preferences": True,
            "channel_specific": True,
            "response_personalization": True,
            "interaction_history_based": True
        }
    }
]

def insert_memories_batch(memories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Insert a batch of memories using the new batch API endpoint.
    
    Args:
        memories: List of memory objects to insert
        
    Returns:
        List of created memory objects with their IDs
    """
    # Set up API request basics
    host = os.environ.get("AM_HOST", "127.0.0.1")
    port = os.environ.get("AM_PORT", "8881")
    base_url = f"http://{host}:{port}"
    api_key = os.environ.get("AM_API_KEY", "am-IYgCf7ZOWvoheIUMGibsWp20LreFxofHo2EBaRNzNvVT")  # Get API key from environment or use default
    
    # Print debug info
    logger.info(f"Using API key: {api_key}")
    logger.info(f"Host: {host}, Port: {port}")
    
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "x-api-key": api_key
    }
    
    logger.info(f"Headers: {headers}")
    
    try:
        # Call the batch create API endpoint
        api_url = f"{base_url}/api/v1/memories/batch"
        
        logger.info(f"Sending batch request with {len(memories)} memories to {api_url}")
        
        # Dump the first memory as a sample to debug JSON format
        logger.info(f"Sample memory (first item): {json.dumps(memories[0], indent=2)}")
        
        response = requests.post(api_url, headers=headers, json=memories)
        
        logger.info(f"Response status code: {response.status_code}")
        logger.info(f"Response headers: {response.headers}")
        
        response.raise_for_status()
        
        # Process successful response
        created_memories = response.json()
        
        logger.info(f"Successfully created {len(created_memories)} memories")
        
        # Return the created memories
        return created_memories
    
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error when accessing memory API: {str(e)}")
        if hasattr(e.response, 'text'):
            logger.error(f"Response details: {e.response.text}")
        raise
    
    except Exception as e:
        logger.error(f"Error inserting memories: {str(e)}")
        raise

def insert_memories_individually(memories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Insert memories one by one as a fallback if batch insertion fails.
    
    Args:
        memories: List of memory objects to insert
        
    Returns:
        List of created memory objects with their IDs
    """
    # Set up API request basics
    host = os.environ.get("AM_HOST", "127.0.0.1")
    port = os.environ.get("AM_PORT", "8881")
    base_url = f"http://{host}:{port}"
    api_key = os.environ.get("AM_API_KEY", "am-IYgCf7ZOWvoheIUMGibsWp20LreFxofHo2EBaRNzNvVT")  # Use the same API key as batch function
    
    # Print debug info
    logger.info(f"Using API key: {api_key}")
    logger.info(f"Host: {host}, Port: {port}")
    
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "x-api-key": api_key
    }
    
    logger.info(f"Headers: {headers}")
    
    created_memories = []
    
    for i, memory in enumerate(memories):
        try:
            # Call the create API endpoint for each memory
            api_url = f"{base_url}/api/v1/memories"
            
            logger.info(f"Sending memory {i+1}/{len(memories)}: {memory['name']}")
            
            if i == 0:
                # Dump the first memory to debug JSON format
                logger.info(f"First memory details: {json.dumps(memory, indent=2)}")
            
            response = requests.post(api_url, headers=headers, json=memory)
            
            logger.info(f"Response status code: {response.status_code}")
            
            response.raise_for_status()
            
            # Add the created memory to the results
            created_memory = response.json()
            created_memories.append(created_memory)
            
            logger.info(f"Successfully created memory: {memory['name']}")
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error when creating memory {memory['name']}: {str(e)}")
            if hasattr(e.response, 'text'):
                logger.error(f"Response details: {e.response.text}")
        
        except Exception as e:
            logger.error(f"Error creating memory {memory['name']}: {str(e)}")
    
    return created_memories

def main():
    """Main function to execute the memory insertion"""
    logger.info(f"Starting memory insertion for Sofia agent (agent_id: 1)")
    logger.info(f"Total memories to insert: {len(SOFIA_MEMORIES)}")
    
    try:
        # Try batch insertion first
        created_memories = insert_memories_batch(SOFIA_MEMORIES)
        
        # Log success information
        logger.info("Memory insertion completed successfully using batch endpoint")
        for memory in created_memories:
            logger.info(f"Created memory: {memory['name']} (ID: {memory['id']})")
        
    except Exception as e:
        logger.warning(f"Batch insertion failed: {str(e)}")
        logger.info("Falling back to individual memory insertion")
        
        # Fall back to individual insertions if batch fails
        created_memories = insert_memories_individually(SOFIA_MEMORIES)
        
        # Log results
        logger.info(f"Individual memory insertion completed: created {len(created_memories)}/{len(SOFIA_MEMORIES)} memories")

if __name__ == "__main__":
    main() 