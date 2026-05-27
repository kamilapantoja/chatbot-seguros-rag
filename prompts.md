# Prompts utilizados no Chatbot Dracarys

> Documentação detalhada das decisões de prompt engineering do Desafio 2.

## System Prompt

```
Você é o assistente virtual da seguradora Dracarys, especializado em atendimento a segurados.

Sua missão é responder dúvidas sobre apólices, sinistros, coberturas, regulamentação SUSEP e demais temas do mercado de seguros brasileiro, sempre baseado nos documentos fornecidos no contexto.

REGRAS INVIOLÁVEIS:
1. Responda APENAS com base no contexto fornecido entre as tags <contexto>. Se a informação não estiver no contexto, diga: "Não encontrei essa informação na nossa base. Recomendo entrar em contato com seu corretor ou consultar nossa central."
2. Nunca invente coberturas, valores, prazos ou procedimentos.
3. Sempre cite a fonte ao final da resposta, no formato: "Fonte: [nome do documento]".
4. Linguagem clara, em português do Brasil, tom acolhedor e profissional. Evite jargão técnico sem explicação.
5. Para sinistros graves (acidente, óbito, roubo), sempre oriente o contato imediato com a central 24h da seguradora antes de prosseguir.
6. Não faça promessas de cobertura ou pagamento — apenas informe o que os documentos dizem.

FORMATO DA RESPOSTA:
- Resposta direta e objetiva
- Quando houver passos (ex: como abrir um sinistro), use lista numerada
- Termine com a citação da fonte
```

## User Prompt Template

```
<contexto>
{context}
</contexto>

Pergunta do segurado: {question}

Responda seguindo as regras do sistema, citando a fonte ao final.
```

## Decisões de prompt engineering

### Persona explícita
**"assistente virtual da seguradora Dracarys"** — dá identidade ao bot e estabelece o tom esperado.

### Regras "inviolaveis"
A palavra "inviolável" funciona como instrução de alta prioridade. Modelos open source 27B-32B respondem bem a esta marcação semântica.

### Anti-alucinação por delimitadores
O contexto recuperado vem dentro de `<contexto>...</contexto>`. Isso:
- **Marca onde está a fonte de verdade** (modelo não confunde com a pergunta)
- **Permite recusa explícita** quando o contexto não tem a resposta
- Compatível com a estratégia de RAG da Aula 04 do curso

### Recusa estruturada
Mensagem padrão de "não encontrei" é literal — evita o modelo inventar variações criativas que possam soar como conhecimento real.

### Citação obrigatória de fonte
Forçar `Fonte: [nome do documento]` ao final:
- Aumenta auditabilidade
- Permite ao usuário verificar a informação
- Reduz percepção de "caixa-preta"

### Orientação de segurança
A regra 5 sobre sinistros graves força o bot a sempre direcionar ao canal humano em casos críticos, evitando responsabilidade indevida do chatbot em situações de emergência.

### Temperatura baixa (0.2)
- Reduz criatividade no LLM (queremos precisão, não originalidade)
- Aumenta consistência entre execuções da mesma pergunta
- Adequado para FAQ — alta temperatura = risco de divergência factual

### Top-K = 6
- Trade-off entre cobertura (mais chunks = mais info) e ruído (chunks irrelevantes confundem)
- 6 chunks de ~800 chars = ~4.8K tokens de contexto + prompt + resposta cabe folgadamente em 8K de contexto

### Chunk size 800 + overlap 150
- Chunks de 800 chars = ~200-250 tokens cada — granularidade suficiente para FAQs
- Overlap de 150 chars (~20%) evita cortar respostas em pontos críticos
- Separadores PT-BR específicos: `["\n\n", "\n", ". ", "! ", "? ", "; ", ", ", " ", ""]`

## Alternativas consideradas mas rejeitadas

### Chain-of-Thought explícito
Não foi adicionado pois:
- Em FAQ direto, raciocínio passo-a-passo gera respostas mais longas sem ganho factual
- Modelos 27B costumam responder bem direto

### Function calling para citações
Considerei usar function calling para retornar JSON estruturado com `{answer, sources}`. Rejeitado:
- gemma2:27b não tem function calling nativo no Ollama
- Adicionaria complexidade sem benefício claro para o usuário final

### Multiple turn refinement (HyDE)
HyDE (Hypothetical Document Embedding) — gerar uma resposta hipotética antes do retrieval — pode melhorar recall em 5-15%. Não usado:
- Adiciona uma chamada extra ao LLM (latência dobra)
- Em FAQ de seguros, perguntas costumam usar vocabulário similar aos documentos

### Reranking (bge-reranker-v2-m3)
Considerado mas não implementado por questão de tempo. Ficou nos próximos passos.
