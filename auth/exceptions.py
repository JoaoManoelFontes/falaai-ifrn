class SuapAPIError(Exception):
    """
    Erro genérico da API do SUAP.

    Esta exceção é lançada quando ocorrem problemas gerais de comunicação
    ou processamento com a API do SUAP.
    """

    pass


class SuapAuthError(SuapAPIError):
    """
    Erro de autenticação específico do SUAP.

    Esta exceção é lançada quando as credenciais fornecidas são inválidas
    ou quando há problemas de autorização (ex: status 401).
    """

    pass
