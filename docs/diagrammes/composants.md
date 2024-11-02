# Diagramme des Composants FOFAL ERP

```mermaid
graph TB
    subgraph Frontend
        UI[Interface Utilisateur React]
        Store[State Management]
        API_Client[API Client]
    end

    subgraph Backend
        API[FastAPI Backend]
        Auth[Authentication Service]
        
        subgraph Core_Modules
            Finance[Module Finance]
            Inventory[Module Inventaire]
            Production[Module Production]
            HR[Module RH]
            Project[Module Projets]
            Accounting[Module Comptabilité]
            Management[Module Contrôle de Gestion]
        end
        
        subgraph Services
            TaskQueue[Celery Task Queue]
            Cache[Redis Cache]
            FileStorage[Stockage Fichiers]
            Notifications[Service Notifications]
        end
    end

    subgraph Database
        PostgreSQL[(PostgreSQL)]
        Backup[Système Backup]
    end

    subgraph External_Services
        Weather[API Météo]
        IoT[Capteurs IoT]
        SMS[Service SMS]
        Email[Service Email]
    end

    UI --> API_Client
    API_Client --> API
    Store --> UI

    API --> Auth
    Auth --> PostgreSQL
    
    Finance --> PostgreSQL
    Inventory --> PostgreSQL
    Production --> PostgreSQL
    HR --> PostgreSQL
    Project --> PostgreSQL
    Accounting --> PostgreSQL
    Management --> PostgreSQL

    API --> Core_Modules
    Core_Modules --> Services

    TaskQueue --> External_Services
    Cache --> API
    PostgreSQL --> Backup

    Production --> Weather
    Production --> IoT
    Notifications --> SMS
    Notifications --> Email
```

## Légende des Interactions

### Frontend → Backend
- Requêtes HTTP/HTTPS
- WebSocket pour les mises à jour en temps réel
- JWT pour l'authentification

### Backend → Base de données
- Connexions poolées
- Transactions ACID
- Migrations automatisées

### Services → Services Externes
- API REST
- MQTT pour IoT
- SMTP pour emails
- API SMS

### Flux de Données Principaux

1. **Circuit Production**
   ```
   Capteurs IoT → Production → PostgreSQL → Management → Rapports
   ```

2. **Circuit Finance**
   ```
   Transactions → Finance → Accounting → PostgreSQL → Rapports
   ```

3. **Circuit Inventaire**
   ```
   Production → Inventory → Notifications → Email/SMS
   ```

4. **Circuit RH**
   ```
   HR → Finance → PostgreSQL → Rapports
   ```

## Notes Techniques

1. **Scalabilité**
   - Composants stateless
   - Cache distribué
   - Load balancing possible

2. **Haute Disponibilité**
   - Réplication PostgreSQL
   - Failover automatique
   - Monitoring continu

3. **Sécurité**
   - Authentification multi-facteurs
   - Encryption des données
   - Audit logs
