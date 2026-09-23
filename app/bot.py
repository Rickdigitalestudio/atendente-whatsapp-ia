"""Cérebro do atendente: regras (funciona sem chave) + IA (OpenAI/Gemini) quando há chave."""
import re
from datetime import datetime
from .config_loader import env

# ---------- detecção de intenção por regras (fallback + pré-roteamento) ----------

def detectar_intencao(texto: str) -> str:
    t = texto.lower()
    if re.search(r"\b(palestra|evento|motiva|conven[cç][aã]o|sipat|treinamento)\b", t):
        return "palestra"
    if re.search(r"\b(hor[aá]rio|abre|fecha|funciona|atende|quando|onde)\b", t):
        return "horario"
    if re.search(r"\b(pre[cç]o|valor|quanto|tabela|cota[cç][aã]o|plano|mensalidade|ades[aã]o|empresarial|cnpj|mei)\b", t):
        return "preco_plano"
    if re.search(r"\b(agend|marc|reuni[aã]o|visita|call|conversa|reserv|disponib|hor[aá]rio livre)\b", t):
        return "agendar"
    if re.search(r"\b(humano|atendente|pessoa|reclama| cancela|ouvidoria|gerente)\b", t):
        return "humano"
    if re.search(r"\b(urg[eê]ncia|emerg[eê]ncia|dor forte|samu|sangue|infarto)\b", t):
        return "urgencia"
    if re.search(r"\b(oi|ol[aá]|bom dia|boa tarde|boa noite|tudo bem)\b", t):
        return "saudacao"
    if re.search(r"\b(obrigad|valeu|tchau|ate mais|até mais)\b", t):
        return "despedida"
    return "geral"

def resposta_por_regras(texto: str, cfg: dict, contexto_agenda: str = "") -> str:
    inten = detectar_intencao(texto)
    nome = cfg["negocio"]["nome"]
    hor = cfg["horarios"]["texto_resumo"]
    regras = cfg["regras"]

    if inten == "saudacao":
        return cfg.get("boas_vindas") or (
            f"Olá! Aqui é do *{nome}* 👋\n"
            f"Posso te ajudar com *planos de saúde* ou *palestras*?\n"
            f"Me diz: é cotação ou evento?")
    if inten == "horario":
        return f"Nosso horário: {hor}\nQuer que eu já deixe uma reunião agendada?"
    if inten == "preco_plano":
        linhas = "\n".join(f"• *{p['nome']}*: {p['preco_referencia']}" for p in cfg["planos"])
        return (f"Valores de referência (a cotação exata depende de idade/cidade/operadora):\n{linhas}\n\n"
                f"Me passa: sua idade, cidade e se é individual, familiar ou CNPJ/MEI? Já monto sua cotação. 📋")
    if inten == "palestra":
        pal = cfg["palestras"]
        temas = ", ".join(pal["temas"])
        return (f"Palestras ({pal['formato']}, {pal['duracao']}):\n"
                f"Temas: {temas}.\nValor: {pal['preco_referencia']}\n\n"
                f"Me diz cidade, data prevista e público estimado que monto a proposta em 24h. 🎤")
    if inten == "agendar":
        extra = f"\n{contexto_agenda}" if contexto_agenda else ""
        return (f"Perfeito, vamos agendar! 📅\n"
                f"Me manda: *nome + melhor dia/horário + plano ou palestra*?\n"
                f"Ex: 'Ana, amanhã 15h, cotação familiar'{extra}")
    if inten == "humano":
        return ("Claro, vou te transferir para o especialista agora. 🙋\n"
                "Enquanto isso me deixa seu nome e telefone que já priorizo seu atendimento.")
    if inten == "urgencia":
        return (f"{regras['disclaimer_saude']}\nSe for plano e puder esperar, me diz sua cidade que já vejo a rede credenciada.")
    if inten == "despedida":
        return "Foi um prazer! Qualquer coisa é só chamar. Sucesso! 🚀"
    # geral
    return (f"Sou da equipe {nome}. Posso ajudar com:\n"
            f"1️⃣ Horário de atendimento\n2️⃣ Preço/cotação de planos\n3️⃣ Palestras\n4️⃣ Agendar reunião\n"
            f"É só me dizer o que precisa!")

# ---------- camada IA (usa se tiver chave, senão usa regras) ----------

SYSTEM_PROMPT_CACHE = None

def responder(texto: str, cfg: dict, historico: list | None = None, contexto_agenda: str = "") -> tuple[str, str]:
    """Retorna (resposta, motor_usado: regras|openai|gemini)."""
    global SYSTEM_PROMPT_CACHE
    historico = historico or []

    openai_key = env("OPENAI_API_KEY")
    gemini_key = env("GEMINI_API_KEY") or env("GOOGLE_API_KEY")

    # Sem chave -> regras (funciona de graça)
    if not openai_key and not gemini_key:
        return resposta_por_regras(texto, cfg, contexto_agenda), "regras"

    # Monta contexto para IA
    from .config_loader import load_system_prompt
    if SYSTEM_PROMPT_CACHE is None:
        SYSTEM_PROMPT_CACHE = load_system_prompt()
    dados = (f"DADOS: horários={cfg['horarios']['texto_resumo']}; "
             f"planos={cfg['planos']}; palestras={cfg['palestras']}; "
             f"agenda={contexto_agenda[:500] if contexto_agenda else 'livre'}")

    # Tenta OpenAI primeiro
    if openai_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai_key)
            msgs = [{"role": "system", "content": SYSTEM_PROMPT_CACHE + "\n" + dados}]
            for h in historico[-8:]:
                msgs.append(h)
            msgs.append({"role": "user", "content": texto})
            r = client.chat.completions.create(
                model=env("OPENAI_MODEL", "gpt-4o-mini"),
                messages=msgs, max_tokens=400, temperature=0.6)
            return r.choices[0].message.content.strip(), "openai"
        except Exception as e:
            print(f"[bot] OpenAI falhou ({e}), tentando fallback...")

    # Tenta Gemini
    if gemini_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel(
                env("GEMINI_MODEL", "gemini-1.5-flash"),
                system_instruction=SYSTEM_PROMPT_CACHE + "\n" + dados)
            chat_txt = "\n".join(f"{h['role']}: {h['content']}" for h in historico[-8:])
            resp = model.generate_content(f"{chat_txt}\nuser: {texto}")
            return resp.text.strip(), "gemini"
        except Exception as e:
            print(f"[bot] Gemini falhou ({e}), usando regras...")

    return resposta_por_regras(texto, cfg, contexto_agenda), "regras"

def deve_transferir_para_humano(texto: str) -> bool:
    return detectar_intencao(texto) == "humano"
