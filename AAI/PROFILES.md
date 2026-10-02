
## Three GA4GH AAI Profiles

General Ecosystem

```mermaid
graph LR
  User --> Broker
  User --> RP
  RP --> Broker
  RP --> Clearinghouse
  Clearinghouse --> AuthorizationServer
  Clearinghouse --> Broker
```

### Approach 1: All AuthZ through RP

```mermaid
sequenceDiagram
  User->>Broker
  User->>RP
  RP->>Broker
  RP->>Clearinghouse
  Clearinghouse->>AuthorizationServer
  Clearinghouse->>Broker
```


### Approach 2: Task-Specific AuthZ through RP



### Approach 3: No AuthZ through RP

## Three GA4GH AAI Profiles

General Ecosystem

```mermaid
graph LR
  User --> Broker
  User --> RP
  RP --> Broker
  RP --> Clearinghouse
  Clearinghouse --> AuthorizationServer
  Clearinghouse --> Broker
```

### Approach 1: All AuthZ through RP

```mermaid
sequenceDiagram
  User->>RP: Log in
  RP->>Broker: Request authentication
  Broker->>RP: Authenticate

  RP->>Broker: Request passport
  Broker->>RP: Passport with ALL user's visas
  RP->>Clearinghouse: Passport with ALL user's visas
  Clearinghouse->>RP: Data
```


### Approach 2: Task-Specific AuthZ through RP

```mermaid
sequenceDiagram
  User->>RP: Log in
  RP->>Broker: Request authentication
  Broker->>RP: Authenticate

  RP->>Broker: Request passport
  Broker->>RP: Passport with ALL user's visas
  RP->>Clearinghouse: Passport with ALL user's visas
  Clearinghouse->>RP: Data
```

### Approach 3: No AuthZ through RP

```mermaid
sequenceDiagram
  User->>RP: Log in
  RP->>Broker: Request authentication
  Broker->>RP: Authenticate

  RP->>Clearinghouse: Request data
  Clearinghouse->>RP: Data
```
