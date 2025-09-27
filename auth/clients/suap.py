import requests


class SuapAPIError(Exception):
    """Erro genérico da API do SUAP."""

    pass


class SuapAuthError(SuapAPIError):
    """Erro de autenticação (ex: 401)."""

    pass


class SuapClient:
    BASE_URL = "https://suap.ifrn.edu.br/api"

    def authenticate(self, matricula: str, senha: str):
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
