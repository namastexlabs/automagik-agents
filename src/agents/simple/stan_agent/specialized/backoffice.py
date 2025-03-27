from pydantic_ai import Agent, RunContext
import logging
from typing import Dict, Any, Optional

# Import Blackpearl tools
from src.tools.blackpearl import (
    get_clientes, get_cliente, create_cliente, update_cliente,
    get_contatos, get_contato
)

# Import Omie tools
from src.tools.omie import (
    search_clients, 
    search_client_by_cnpj
)

# Import Gmail tools
from src.tools.gmail import (
    send_email,
    SendEmailInput
)

# Import necessary schemas
from src.tools.blackpearl.schema import (
    Cliente
)
from src.tools.omie.schema import ClientSearchInput

logger = logging.getLogger(__name__)

# Path to
async def backoffice_agent(input_text: str, context: Optional[Dict[str, Any]] = None) -> str:
    """Specialized backoffice agent with access to BlackPearl and Omie tools.
    
    Args:
        input_text: User input text
        context: Optional context dictionary
        
    Returns:
        Response from the agent
    """
    if context is None:
        context = {}
    
    # Initialize the agent with appropriate system prompt
    backoffice_agent = Agent(  
        'openai:gpt-4o',
        deps_type=Dict[str, Any],
        result_type=str,
        system_prompt=(
            'You are a specialized backoffice agent with expertise in BlackPearl and Omie APIs, working in direct support of STAN. '
            'Your primary responsibilities include:\n'
            '1. Managing client information - finding, creating, and updating client records\n'
            '2. Processing lead information when received from STAN\n'
            '3. Creating BlackPearl client records with complete information\n'
            '4. Sending lead notifications to the solid team via email\n'
            '5. Retrieving and providing product information\n'
            '6. Managing orders and sales processes\n'
            'Always use the most appropriate BlackPearl or Omie tool based on the specific request from STAN. '
            'Provide complete yet concise information, focusing on exactly what STAN needs. '
            'When creating new client records, automatically send lead information to the solid team. '
            'Respond in a professional, straightforward manner without unnecessary explanations or apologies. '
            'Your role is to be efficient, accurate, and helpful in managing backend business operations.\n\n'
            'IMPORTANT: When writing emails or any external communications, ALWAYS use Portuguese as the default language.'
        ),
    )
    
    # Register BlackPearl client tools
    @backoffice_agent.tool
    async def bp_get_clientes(
        ctx: RunContext[Dict[str, Any]], 
        limit: Optional[int] = None, 
        offset: Optional[int] = None,
        search: Optional[str] = None, 
        ordering: Optional[str] = None,
        cidade: Optional[str] = None,
        estado: Optional[str] = None,
        cnpj: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get list of clients from BlackPearl.
        
        Args:
            limit: Maximum number of clients to return
            offset: Number of clients to skip
            search: Search term to filter clients
            ordering: Field to order results by (example: 'nome' or '-nome' for descending)
            cidade: Filter by city name
            estado: Filter by state code (2 letters)
            cnpj: Filter by CNPJ number
        """
        filters = {}
        if cidade:
            filters["cidade"] = cidade
        if estado:
            filters["estado"] = estado
        if cnpj:
            filters["cnpj"] = cnpj
            
        return await get_clientes(ctx.deps, limit, offset, search, ordering, **filters)
    
    @backoffice_agent.tool
    async def bp_get_cliente(ctx: RunContext[Dict[str, Any]], cliente_id: int) -> Dict[str, Any]:
        """Get specific client details from BlackPearl.
        
        Args:
            cliente_id: The client ID
        """
        return await get_cliente(ctx.deps, cliente_id)
    
    @backoffice_agent.tool
    async def bp_create_cliente(
        ctx: RunContext[Dict[str, Any]], 
        nome: str,
        email: str,
        telefone: str,
        cnpj: Optional[str] = None,
        endereco: Optional[str] = None,
        cidade: Optional[str] = None,
        estado: Optional[str] = None,
        cep: Optional[str] = None,
        inscricao_estadual: Optional[str] = None,
        observacao: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new client in BlackPearl.
        
        Args:
            nome: Client name
            email: Client email
            telefone: Client phone number
            cnpj: Client CNPJ (optional)
            endereco: Client address (optional)
            cidade: Client city (optional)
            estado: Client state (optional)
            cep: Client postal code (optional)
            inscricao_estadual: Client state registration (optional)
            observacao: Additional notes about the client (optional)
        """
        cliente_data = {
            "nome": nome,
            "email": email,
            "telefone": telefone
        }
        
        # Add optional fields if provided
        if cnpj:
            cliente_data["cnpj"] = cnpj
        if endereco:
            cliente_data["endereco"] = endereco
        if cidade:
            cliente_data["cidade"] = cidade
        if estado:
            cliente_data["estado"] = estado
        if cep:
            cliente_data["cep"] = cep
        if inscricao_estadual:
            cliente_data["inscricao_estadual"] = inscricao_estadual
        if observacao:
            cliente_data["observacao"] = observacao
            
        cliente = Cliente(**cliente_data)
        return await create_cliente(ctx.deps, cliente)
    
    @backoffice_agent.tool
    async def bp_update_cliente(
        ctx: RunContext[Dict[str, Any]], 
        cliente_id: int,
        nome: Optional[str] = None,
        email: Optional[str] = None,
        telefone: Optional[str] = None,
        cnpj: Optional[str] = None,
        endereco: Optional[str] = None,
        cidade: Optional[str] = None,
        estado: Optional[str] = None,
        cep: Optional[str] = None,
        inscricao_estadual: Optional[str] = None,
        observacao: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update a client in BlackPearl.
        
        Args:
            cliente_id: The client ID
            nome: Client name (optional)
            email: Client email (optional)
            telefone: Client phone number (optional)
            cnpj: Client CNPJ (optional)
            endereco: Client address (optional)
            cidade: Client city (optional)
            estado: Client state (optional)
            cep: Client postal code (optional)
            inscricao_estadual: Client state registration (optional)
            observacao: Additional notes (optional)
        """
        # First get the current client data
        current_cliente = await get_cliente(ctx.deps, cliente_id)
        
        # Update with new values if provided
        cliente_data = {}
        for key, value in current_cliente.items():
            if key != "id" and key != "created_at" and key != "updated_at":
                cliente_data[key] = value
                
        # Update fields with new values if provided
        if nome:
            cliente_data["nome"] = nome
        if email:
            cliente_data["email"] = email
        if telefone:
            cliente_data["telefone"] = telefone
        if cnpj:
            cliente_data["cnpj"] = cnpj
        if endereco:
            cliente_data["endereco"] = endereco
        if cidade:
            cliente_data["cidade"] = cidade
        if estado:
            cliente_data["estado"] = estado
        if cep:
            cliente_data["cep"] = cep
        if inscricao_estadual:
            cliente_data["inscricao_estadual"] = inscricao_estadual
        if observacao:
            cliente_data["observacao"] = observacao
            
        cliente = Cliente(**cliente_data)
        return await update_cliente(ctx.deps, cliente_id, cliente)
    
    # Register BlackPearl contact tools
    @backoffice_agent.tool
    async def bp_get_contatos(
        ctx: RunContext[Dict[str, Any]], 
        limit: Optional[int] = None, 
        offset: Optional[int] = None,
        search: Optional[str] = None, 
        ordering: Optional[str] = None,
        telefone: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get list of contacts from BlackPearl.
        
        Args:
            limit: Maximum number of contacts to return
            offset: Number of contacts to skip
            search: Search term to filter contacts (searches in name and email)
            ordering: Field to order results by (example: 'nome' or '-nome' for descending)
            telefone: Filter by phone number
        """
        filters = {}
        if telefone:
            filters["telefone"] = telefone
            
        return await get_contatos(ctx.deps, limit, offset, search, ordering, **filters)
    
    @backoffice_agent.tool
    async def bp_get_contato(ctx: RunContext[Dict[str, Any]], contato_id: int) -> Dict[str, Any]:
        """Get specific contact details from BlackPearl.
        
        Args:
            contato_id: The contact ID
        """
        return await get_contato(ctx.deps, contato_id)
    
    # Register Omie tools
    @backoffice_agent.tool
    async def omie_search_clients(
        ctx: RunContext[Dict[str, Any]],
        email: Optional[str] = None,
        razao_social: Optional[str] = None,
        nome_fantasia: Optional[str] = None,
        pagina: int = 1,
        registros_por_pagina: int = 50
    ) -> Dict[str, Any]:
        """Search for clients in Omie with various search options.
        
        Args:
            email: Client email
            razao_social: Company name
            nome_fantasia: Trading name
            pagina: Page number (default: 1)
            registros_por_pagina: Results per page (default: 50)
        """
        search_input = {
            "pagina": pagina,
            "registros_por_pagina": registros_por_pagina
        }
        
        # Add search filters if provided
        if email:
            search_input["email"] = email
        if razao_social:
            search_input["razao_social"] = razao_social
        if nome_fantasia:
            search_input["nome_fantasia"] = nome_fantasia
            
        input_obj = ClientSearchInput(**search_input)
        return await search_clients(ctx, input_obj)
    
    @backoffice_agent.tool
    async def omie_search_client_by_cnpj(ctx: RunContext[Dict[str, Any]], cnpj: str) -> Dict[str, Any]:
        """Search for a client by CNPJ in Omie.
        
        Args:
            cnpj: The CNPJ to search for (format: xx.xxx.xxx/xxxx-xx or clean numbers)
        """
        return await search_client_by_cnpj(ctx, cnpj)

    # Gmail lead email tool
    @backoffice_agent.tool
    async def send_lead_email(
        ctx: RunContext[Dict[str, Any]],
        lead_information: str
    ) -> Dict[str, Any]:
        """Send an email with lead information to the solid team.
           Consolidate all information in a proper format, in portuguese, and send to the solid team.
           Example: 

                BlackPearl User ID: 100
                Nome: João Silva
                Email: joao.silva@exemplo.com
                Telefone: +5511987654321
                Empresa: Exemplo Ltda.
                Detalhes: Algumas informações adicionais
                Interesses: Algumas informações sobre os interesses do lead
                CNPJ: 12.345.678/0001-00
                Endereço: Rua Exemplo, 123 - São Paulo/SP 
                
        
        Args:
            lead_information: Information about the lead
        """
        
        # Construct the email
        subject = f"[STAN - Novo Lead]"
        
        message = "A new lead has been registered with the following details:\n\n"
        message += "\n".join(lead_information)
        message += "\n\nPlease follow up with this lead as soon as possible."
        
        # Determine recipient email
        recipient = "cezar@namastex.ai"
        
        # Create email input
        email_input = SendEmailInput(
            to=recipient,
            subject=subject,
            message=message
        )
        
        # Send the email using Gmail API
        try:
            result = await send_email(ctx, email_input)
            
            if result["success"]:
                return {
                    "success": True,
                    "message": f"Lead information has been sent to the solid team",
                    "email_id": result["message_id"]
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to send lead email: {result['error']}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error sending lead email: {str(e)}"
            }

    # Execute the agent
    try:
        result = await backoffice_agent.run(input_text, deps=context)
        logger.info(f"Backoffice agent response: {result}")
        return result.data
    except Exception as e:
        error_msg = f"Error in backoffice agent: {str(e)}"
        logger.error(error_msg)
        return f"I apologize, but I encountered an error processing your request: {str(e)}"