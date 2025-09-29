import requests

from auth.exceptions import SuapAPIError, SuapAuthError


class SuapClient:
    """
    Cliente para interação com a API do SUAP do IFRN.

    Esta classe fornece métodos para autenticação e comunicação com os
    serviços do Sistema Unificado de Administração Pública (SUAP).

    Attributes:
        BASE_URL (str): URL base da API do SUAP
        token (Optional[str]): Token de acesso JWT após autenticação

    """

    BASE_URL = "https://suap.ifrn.edu.br/api"

    def authenticate(self, matricula: str, senha: str) -> str:
        """
        Autentica o usuário no SUAP e retorna o token de acesso.

        Este método realiza a autenticação usando as credenciais fornecidas
        e armazena o token JWT para uso em requisições subsequentes.

        Args:
            matricula (str): Matrícula do usuário
            senha (str): Senha do usuário no SUAP

        Returns:
            str: Token JWT de acesso para requisições autenticadas

        Raises:
            SuapAuthError: Quando as credenciais são inválidas (401)
            SuapAPIError: Quando há problemas de conexão ou outros erros da API

        Note:
            O token armazenado pode ser usado para requisições subsequentes
            que requerem autenticação. O token tem validade limitada.
        """
        url = f"{self.BASE_URL}/token/pair"

        try:
            response = requests.post(
                url,
                json={"username": matricula, "password": senha},
                headers={"Content-Type": "application/json"},
                timeout=10,
            )

            if response.status_code == 401:
                raise SuapAuthError("Matrícula ou senha inválidos.")

            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            raise SuapAPIError(f"Erro de conexão com o SUAP: {e}")

        self.token = response.json().get("access")
        return self.token
