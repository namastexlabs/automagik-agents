"""Blackpearl API schemas.

This module defines the Pydantic models for Blackpearl API request and response validation.
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from enum import Enum

class StatusAprovacaoEnum(str, Enum):
    NOT_REGISTERED = "NOT_REGISTERED"
    REJECTED = "REJECTED"
    APPROVED = "APPROVED"
    PENDING_REVIEW = "PENDING_REVIEW"
    VERIFYING = "VERIFYING"

class StatusNegociacaoEnum(str, Enum):
    PROPOSTA = "0"
    ANALISE = "1"
    RENEGOCIACAO = "2"
    REPROVADO = "3"
    APROVADO = "4"

class StatusPedidoEnum(str, Enum):
    ABERTO = "0"
    VENDA = "10"
    SEPARAR_ESTOQUE = "20"
    FATURAR = "50"
    FATURADO = "60"
    ENTREGA = "70"

class FreteModalidadeEnum(str, Enum):
    CIF = "0"
    FOB = "1"
    TERCEIROS = "2"
    TRANSPORTE_PROPRIO_REMETENTE = "3"
    TRANSPORTE_PROPRIO_DESTINATARIO = "4"
    SEM_FRETE = "9"

class RegiaoEnum(str, Enum):
    AC = "AC"
    AL = "AL"
    AP = "AP"
    AM = "AM"
    BA = "BA"
    CE = "CE"
    DF = "DF"
    ES = "ES"
    GO = "GO"
    MA = "MA"
    MT = "MT"
    MS = "MS"
    MG = "MG"
    PA = "PA"
    PB = "PB"
    PR = "PR"
    PE = "PE"
    PI = "PI"
    RJ = "RJ"
    RN = "RN"
    RS = "RS"
    RO = "RO"
    RR = "RR"
    SC = "SC"
    SP = "SP"
    SE = "SE"
    TO = "TO"
    NORTE = "N"
    NORDESTE = "NE"
    CENTRO_OESTE = "CO"
    SUDESTE = "SU"
    SUL = "S"

class TimeEnum(str, Enum):
    INDEFINIDO = "Indefinido"
    REDRAGON = "Redragon"
    OUTRAS_MARCAS = "Outras Marcas"
    KALKAN_KEYTIME = "Kalkan/Keytime"

class TipoImagemEnum(str, Enum):
    OUTROS = "OUTROS"
    TECNICA = "TECNICA"
    MARKETING = "MARKETING"

class Marca(BaseModel):
    id: int = Field(..., description="Unique identifier")
    nome: str = Field(..., max_length=255)
    logo: Optional[str] = Field(None, description="Logo URL")
    site: Optional[str] = Field(None, max_length=200, description="Manufacturer website")

class FamiliaDeProduto(BaseModel):
    id: int = Field(..., description="Unique identifier")
    codigo: int = Field(..., description="Product family code in Omie")
    nomeFamilia: str = Field(..., max_length=255, description="Family name")

class Cliente(BaseModel):
    id: int = Field(..., description="Unique identifier")
    contatos: List[int] = Field(..., description="Contact IDs")
    vendedores: List[int] = Field(..., description="Salesperson IDs")
    telefone_comercial: str
    tipo_operacao: str
    numero_funcionarios: int
    razao_social: str = Field(..., max_length=255)
    nome_fantasia: str = Field(..., max_length=255)
    cnpj: str = Field(..., max_length=18)
    inscricao_estadual: str = Field(..., max_length=255)
    email: str = Field(..., max_length=500)
    endereco: str
    endereco_numero: Optional[str] = Field(None, max_length=16)
    endereco_complemento: Optional[str] = Field(None, max_length=255)
    bairro: str = Field(..., max_length=255)
    cidade: str = Field(..., max_length=255)
    estado: str = Field(..., max_length=2)
    cep: str = Field(..., max_length=9)
    codigo_cliente_omie: Optional[int] = Field(None, description="Omie client code")
    status_aprovacao: StatusAprovacaoEnum
    valor_limite_credito: int
    data_aprovacao: Optional[datetime]
    detalhes_aprovacao: Optional[str]
    data_registro: datetime
    ultima_atualizacao: Optional[datetime]

class Contato(BaseModel):
    id: int = Field(..., description="Unique identifier")
    nome: str
    telefone: str
    wpp_session_id: str
    ativo: bool
    data_registro: datetime
    status_aprovacao: StatusAprovacaoEnum
    data_aprovacao: Optional[datetime]
    detalhes_aprovacao: Optional[str]
    ultima_atualizacao: Optional[datetime]

class Vendedor(BaseModel):
    id: int = Field(..., description="Unique identifier")
    codigo: int = Field(..., description="Omie salesperson code")
    nome: str = Field(..., max_length=255)
    email: EmailStr = Field(..., max_length=254)
    telefone: Optional[str] = Field(None, max_length=20)
    regiao: Optional[str] = Field(None, max_length=64)
    regras: Optional[str]
    time: TimeEnum
    inativo: bool
    time_stan: bool

class Produto(BaseModel):
    id: int = Field(..., description="Unique identifier")
    marca: Marca
    familia: FamiliaDeProduto
    codigo_produto: int = Field(..., description="Product code in Omie")
    inativo: bool
    ean: Optional[str] = Field(None, max_length=64)
    codigo: Optional[str] = Field(None, max_length=64)
    descricao: Optional[str] = Field(None, max_length=255)
    descr_detalhada: Optional[str]
    unidade: Optional[str] = Field(None, max_length=32)
    valor_unitario: float
    peso_bruto: float
    peso_liq: float
    largura: float
    altura: float
    profundidade: float
    cfop: Optional[str] = Field(None, max_length=32)
    ncm: Optional[str] = Field(None, max_length=32)
    especificacoes: Optional[str]
    marketing_info: Optional[str]

class ItemDePedido(BaseModel):
    id: int = Field(..., description="Unique identifier")
    quantidade: int = Field(..., ge=0)
    valor_unitario_currency: str
    valor_unitario: str = Field(..., pattern=r'^-?\d{0,10}(?:\.\d{0,2})?$')
    desconto_currency: str
    desconto: str = Field(..., pattern=r'^-?\d{0,10}(?:\.\d{0,2})?$')
    porcentagem_desconto: float
    valor_total_currency: str
    valor_total: str = Field(..., pattern=r'^-?\d{0,10}(?:\.\d{0,2})?$')
    codigo_item_integracao: Optional[str] = Field(None, max_length=64)
    pedido: int
    produto: int

class PedidoDeVenda(BaseModel):
    id: int = Field(..., description="Unique identifier")
    status_negociacao: StatusNegociacaoEnum
    status_pedido: StatusPedidoEnum
    observacoes: Optional[str]
    codigo_pedido: int = Field(..., description="Order code in Omie")
    codigo_pedido_integracao: Optional[str] = Field(None, max_length=16)
    data_emissao: datetime
    data_aprovacao: Optional[datetime]
    frete_modalidade: FreteModalidadeEnum
    cancelado: bool
    cliente: int
    pagamento: Optional[int]
    transportadora: Optional[int]
    vendedor: List[int]

class RegraDeFrete(BaseModel):
    id: int = Field(..., description="Unique identifier")
    regiao: RegiaoEnum
    cidade: Optional[str] = Field(None, max_length=128)
    valor_minimo_comum_currency: str
    valor_minimo_comum: str = Field(..., pattern=r'^-?\d{0,10}(?:\.\d{0,2})?$')
    transportadora_comum: Optional[str] = Field(None, max_length=64)
    observacoes_comum: Optional[str]
    valor_minimo_autocare_currency: str
    valor_minimo_autocare: str = Field(..., pattern=r'^-?\d{0,10}(?:\.\d{0,2})?$')
    transportadora_autocare: Optional[str] = Field(None, max_length=64)
    observacoes_autocare: Optional[str]

class RegraDeNegocio(BaseModel):
    id: int = Field(..., description="Unique identifier")
    titulo: str = Field(..., max_length=64)
    regra: str
    ativo: bool 