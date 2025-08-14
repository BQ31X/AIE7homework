sequenceDiagram
    autonumber
    participant U as User
    participant C as Simple Agent Client
    participant A as A2A Client
    participant S as Agent Node Server (10000)
    participant X as GeneralAgentExecutor
    participant G as LangGraph Agent
    participant T as Tools (web/arxiv/rag)

    U->>C: Enter query
    C->>A: Resolve Agent Card
    A->>S: GET /.well-known/agent-card.json
    S-->>A: AgentCard JSON
    C->>A: send_message (JSON-RPC)
    A->>S: POST /
    S->>X: handle request
    X->>G: stream (query, context_id)
    G->>T: optional tool calls
    T-->>G: results
    G-->>X: final answer
    X-->>S: task completed + artifacts
    S-->>A: JSON-RPC response
    A-->>C: result JSON
    C-->>U: print response
