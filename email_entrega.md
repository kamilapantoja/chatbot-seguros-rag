# E-mail de entrega — Desafio 2

**Para:** challenges@i2a2.academy
**Assunto:** InsurMinds atividade obrigatória 2

---

Olá, equipe I2A2,

Segue a entrega do Desafio 2 do curso InsurMinds.

## Grupo

- **Nome do grupo:** Dracarys — House of the RAG
- **Modalidade:** individual
- **Representante / único integrante:**
  - Nome: Kamila Pantoja
  - E-mail: kamilapantoja@bemol.com.br
  - Celular: (92) 98133-9103

## Sobre a solução

Chatbot de atendimento a segurados baseado em **LLM + RAG**, rodando 100% em infraestrutura local/privada:

- **LLM:** `gemma2:27b` (15 GB, open source) rodando na GPU NVIDIA GB10 Grace Blackwell da DGX Spark via SSH tunnel cifrado — privacidade total das conversas
- **Embeddings:** `BAAI/bge-m3` (multilingual SOTA para PT-BR)
- **Vector DB:** Chroma persistido localmente
- **Framework:** LangChain
- **UI:** Chainlit com streaming de tokens e citação de fontes
- **Base de conhecimento:** 6 documentos de FAQ realistas + glossário SUSEP (~45 chunks)

## Resultados

- 19/20 perguntas com qualidade factual alta (95%)
- 4/4 edge cases (perguntas fora de escopo) recusados corretamente
- 100% das respostas citam fonte
- Tempo médio de resposta: 9s
- Throughput: 13,7 tok/s na GPU

## Observação sobre o ZIP

Os arquivos `setup.bat` e `start_chatbot.bat` foram renomeados para `setup.bat.txt` e `start_chatbot.bat.txt` dentro do ZIP porque o Gmail bloqueia anexos com `.bat`. Para executá-los no Windows, basta renomear de volta para `.bat`.

## O que está anexado

- Código-fonte completo (Python)
- Base de conhecimento (6 markdown FAQs)
- Relatório técnico (`relatorio-final.pdf`)
- Documentação dos prompts (`prompts.pdf`)
- Resultados do eval (`tests/eval_results.md`)
- Prints da execução (`prints/`)

Repositório GitHub: https://github.com/kamilapantoja/chatbot-seguros-rag

Atenciosamente,
Kamila Pantoja
Grupo Dracarys — House of the RAG
