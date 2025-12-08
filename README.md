# Gerador de Ficha de Personagem - D&D 5ª Edição

Aplicação web simples, rápida e 100% em português para gerar fichas de personagem completas para **Dungeons & Dragons 5ª Edição**.

Com poucos cliques você escolhe raça, classe, antecedente e rola (ou define) os atributos — o sistema já calcula automaticamente:
- Modificadores de atributos
- Bônus raciais
- Proficiências e perícias
- Pontos de vida iniciais
- Classe de armadura inicial
- Ataques, magias e habilidades de nível 1
- Equipamento inicial

Perfeito para mestres que precisam criar NPCs em segundos ou jogadores que querem agilizar a criação!

## Funcionalidades atuais
- Rolagem automática 4d6-drop-lowest ou atribuição manual de valores
- Suporte completo às raças e classes do Player’s Handbook
- Cálculo automático de todos os bônus e modificadores
- Interface limpa e totalmente em português (PT-BR)
- Exportação da ficha em PDF (em desenvolvimento)
- Envio da ficha por e-mail (opcional)
- Salvamento local da ficha gerada

## Tecnologias utilizadas
- Python 3.8+
- Django 4.x (framework principal)
- SQLite (banco de dados em desenvolvimento)
- Bootstrap 5 + HTML/CSS/JavaScript
- python-decouple (variáveis de ambiente)
- WeasyPrint / ReportLab (futuro - geração de PDF)

## Pré-requisitos
- Python 3.8 ou superior
- pip
- virtualenv (recomendado)

## Como rodar o projeto localmente

```bash
# 1. Clone o repositório
git clone https://github.com/LucasRocha4/Gerar_Ficha_RPG.git
cd Gerar_Ficha_RPG

# 2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/Mac
# ou
venv\Scripts\activate           # Windows

# 3. Instale as dependências
pip install -r requirements.txt
# (Se ainda não existir requirements.txt: pip install django python-decouple)

# 4. Execute as migrações
python manage.py migrate

# 5. Crie um superusuário (opcional, para acessar o admin)
python manage.py createsuperuser

# 6. Inicie o servidor
python manage.py runserver
Acesse no navegador: http://127.0.0.1:8000
Admin Django: http://127.0.0.1:8000/admin
Configuração de Envio de E-mail (Gmail)
A aplicação permite enviar a ficha por e-mail. As credenciais são carregadas via variáveis de ambiente por segurança.

Crie um arquivo .env na raiz do projeto (mesmo nível do manage.py):

envEMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu_email@gmail.com
EMAIL_HOST_PASSWORD=sua_senha_de_app_16_digitos
DEFAULT_FROM_EMAIL=seu_email@gmail.com

Como gerar a senha de app do Google (obrigatório desde 2022):
Acesse: https://myaccount.google.com/security
Ative a Verificação em duas etapas
Vá em “Senhas de app” → selecione “Mail” → “Outro” → digite “Django RPG”
Copie a senha de 16 caracteres gerada e cole no campo EMAIL_HOST_PASSWORD

Instale a biblioteca de variáveis de ambiente (se ainda não tiver):

Bashpip install python-decouple
Pronto! O envio de e-mails funcionará normalmente.
Nunca commite o arquivo .env — ele já está ignorado no .gitignore
Contribuição
Issues e Pull Requests são super bem-vindos!
Ideias para o futuro:

Exportação completa em PDF (WeasyPrint ou ReportLab)
Suporte a multiclasse e níveis acima do 1
Integração com API oficial do D&D Beyond
Suporte a livros adicionais (Xanathar, Tasha’s, etc.)
Sistema de login e salvamento de personagens
Modo offline (PWA)

Licença
MIT License – sinta-se à vontade para usar, modificar e distribuir livremente.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/d40fba3b-1d3f-4e07-a03d-528dd37273ac" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/41390baf-23d4-48bf-858d-398f0242ea48" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/fdc09212-3cda-49cc-b531-2258840a4b6f" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/fdc24c7b-6843-41a9-9694-d1a4b444f2b7" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/aaf8a630-3d9e-491b-997f-8525a111c08a" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/3150b6ea-325c-404a-a484-8e2746403102" />

