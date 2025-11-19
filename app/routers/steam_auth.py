import re
import httpx
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from urllib.parse import urlencode

from app.db.session import SessionLocal, engine
from app.models.user import User
from app.core.config import settings
from app.utils.jwt_handler import create_access_token

router = APIRouter()

# URL base para a API da Steam
STEAM_OPENID_URL = "https://steamcommunity.com/openid/login"
STEAM_PLAYER_SUMMARY_URL = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"

# Regex para extrair o SteamID da URL de resposta
STEAM_ID_REGEX = re.compile(r"https://steamcommunity.com/openid/id/(\d+)")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/login")
def steam_login(request: Request):
    """
    Endpoint para iniciar o login com a Steam.
    Redireciona o usuário para a página de login da Steam.
    """
    
    # O 'return_to' DEVE ser a URL do seu backend (API).
    # Em testes locais, é o seu uvicorn na porta 8000.
    api_base_url = "http://localhost:8000" 
    
    # IMPORTANTE: Se você for colocar isso em produção.
    # você precisará mudar "http://localhost:8000".
    # para a sua URL pública, ex: "https://api.seujogo.com".

    # Esta é a URL para ONDE a Steam deve enviar o usuário de volta.
    return_to_url = f"{api_base_url}/api/auth/steam/callback"
    
    params = {
        "openid.ns": "http://specs.openid.net/auth/2.0",
        "openid.mode": "checkid_setup",
        "openid.return_to": return_to_url,
        "openid.realm": api_base_url, # O realm deve bater com o domínio do 'return_to'.
        "openid.identity": "http://specs.openid.net/auth/2.0/identifier_select",
        "openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select",
    }
    
    steam_redirect_url = f"{STEAM_OPENID_URL}?{urlencode(params)}"
    return RedirectResponse(steam_redirect_url)

@router.get("/callback", include_in_schema=False)
async def steam_callback(request: Request, db: Session = Depends(get_db)):
    """
    Endpoint de callback. A Steam redireciona o usuário para cá.
    Verifica a autenticidade da resposta e cria/log o usuário.
    """
    
    # 1. Copiar todos os parâmetros recebidos
    params = dict(request.query_params)
    
    # 2. Mudar 'openid.mode' para 'check_authentication' para verificar
    params["openid.mode"] = "check_authentication"

    # 3. Fazer a requisição de verificação de volta para a Steam
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(STEAM_OPENID_URL, data=params)
            response.raise_for_status()
        except httpx.HTTPStatusError:
            raise HTTPException(status_code=500, detail="Falha ao verificar com a Steam")

    # 4. Analisar a resposta da Steam
    if "is_valid:true" not in response.text:
        raise HTTPException(status_code=401, detail="Login Steam inválido ou falhou a verificação")

    # 5. Extrair o SteamID
    match = STEAM_ID_REGEX.search(params.get("openid.claimed_id", ""))
    if not match:
        raise HTTPException(status_code=500, detail="Não foi possível extrair o SteamID")
        
    steam_id_64 = match.group(1)

    # 6. Lógica de Usuário: Encontrar ou Criar
    user = db.query(User).filter(User.steam_id == steam_id_64).first()

    if not user:
        # Usuário NOVO: Precisamos criar a conta
        if not settings.STEAM_API_KEY:
            raise HTTPException(status_code=500, detail="STEAM_API_KEY não configurada no servidor para buscar perfil.")

        # Buscar o nome do perfil público do usuário na Steam
        async with httpx.AsyncClient() as client:
            try:
                summary_resp = await client.get(
                    f"{STEAM_PLAYER_SUMMARY_URL}?key={settings.STEAM_API_KEY}&steamids={steam_id_64}"
                )
                summary_data = summary_resp.json()
                player_name = summary_data["response"]["players"][0]["personaname"]
            except Exception:
                player_name = f"steam_user_{steam_id_64}" # Nome fallback

        # Criar novo usuário (lembre-se do Passo 1: email e password são nulos)
        user = User(
            name=player_name,
            steam_id=steam_id_64,
            email=None, # Permitido por causa da nossa mudança no model
            password_hash=None # Permitido por causa da nossa mudança no model
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # 7. Criar o nosso próprio Token JWT para o usuário
    # Usando a função que você já tem em app/utils/jwt_handler.py
    access_token = create_access_token(subject=str(user.id))

    # 8. Redirecionar o usuário de volta para o Frontend com o token
    # O frontend deve pegar esse token da URL e salvar.
    frontend_login_success_url = f"{settings.FRONTEND_URL or 'http://localhost:3000'}/login-success?token={access_token}"
    
    return RedirectResponse(frontend_login_success_url)