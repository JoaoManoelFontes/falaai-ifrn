# Fala ai - IFRN
## Projeto Integrador de ADS

### Theme
**Plataforma de Ideias e Desafios de Inovação Institucional**

**Visão Geral:** Alunos e servidores frequentemente têm ideias excelentes para melhorar o campus, otimizar processos ou resolver problemas, mas não existe um canal estruturado para que essas ideias sejam ouvidas, debatidas e potencialmente implementadas.

**Objetivo Principal:** Desenvolver uma plataforma de inovação aberta (crowdsourcing) onde a comunidade acadêmica possa submeter, discutir e votar em ideias para a melhoria da instituição. O sistema deve fomentar uma cultura de participação e criatividade.


### Authors
- [João Manoel](https://github.com/JoaoManoelFontes)
- [Rangel Alves](https://github.com/alvesrangellws)
- [Gabriel Enzo](https://github.com/GabrielEnzoVidaldeAlmeida)

### Links
- [Documento de requisitos](https://docs.google.com/document/d/1kUMdEQq1YbdbOy7oYL5Tuzy3-a1d2wKjgbikccEweNM/edit?tab=t.0)
- [Protótipo Figma](https://www.figma.com/design/wPmHzmHzOV7PLDN9mbkKWJ/PI---FalaAi?node-id=0-1&p=f&t=sL055wXmvqTFE9CW-0)
- [Design Sistem Excalidraw](https://excalidraw.com/#room=68512b34a237307a7263,y6DvKL7TMZjF9vpuOX3iGg)


### Stack
- Python (>= 3.13)
- Git e Gitflow
- Docker e Docker Compose
- Postgres
- Django
- Ruf Formatter
- Tailwind
- Node (>=22.14)

### Recomended VSCode Extensions
- **Ruff** - Linting e formatação
- **Python** - Suporte básico ao Python
- **Pylance** - IntelliSense avançado
- **Django** - Suporte ao framework Django
- **Jinja** - Suporte a templates

### Lint commands
O `settings.json` do projeto já configura o linting e formating do Ruff por padrão.

- `Ctrl+Shift+P` > "Ruff: Fix all auto-fixable problems"
- `Ctrl+Shift+P` > "Format Document" (para formatar o arquivo atual)
- O código será formatado automaticamente ao salvar

### Tailwind css build
- Rode `npm install` para instalar as dependencias do tailwind com o node
- Rode `npm run dev` para realizar o build do tailwind nos arquivos estáticos e usá-los no sistema
- Em produção, rode `npm run build` para fazer o build sem hot reload do tailwind


### Run project
- Copie as variáveis de ambiente que estão em `.env.example` para um arquivo `.env` e modifique conforme necessário
- Rode `docker-compose up -d` para iniciar o banco
- Rode `npm run dev` em um terminal separado para realizar o build do tailwind nos arquivos estáticos e usá-los no sistema
- Rode `python manage.py migrate` se preciso para atualizar o banco
- Rode `python manage.py runserver` para iniciar o servidor
- Acesse o site em http://localhost:8000