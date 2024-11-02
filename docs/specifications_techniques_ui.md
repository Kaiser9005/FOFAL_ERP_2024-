# Spécifications Techniques de l'Interface Utilisateur

## 1. Technologies Frontend

### 1.1 Stack Technique
```yaml
Framework Principal:
  - React 18.x
  - TypeScript 5.x

État Global:
  - Redux Toolkit
  - React Query (pour la gestion du cache)

Routage:
  - React Router 6.x

Styles:
  - TailwindCSS
  - SCSS Modules
  - CSS-in-JS (styled-components)

Composants UI:
  - Material-UI (MUI)
  - React Icons
  - Custom Components

Graphiques:
  - Chart.js
  - React-ChartJS-2
  - D3.js (pour visualisations complexes)

Formulaires:
  - React Hook Form
  - Yup (validation)

Internationalisation:
  - i18next
  - react-i18next

Tests:
  - Jest
  - React Testing Library
  - Cypress
```

## 2. Architecture Frontend

### 2.1 Structure des Dossiers
```
src/
├── assets/
│   ├── images/
│   ├── icons/
│   └── styles/
├── components/
│   ├── common/
│   ├── forms/
│   ├── layout/
│   └── modules/
├── config/
├── hooks/
├── interfaces/
├── modules/
│   ├── finance/
│   ├── inventory/
│   ├── production/
│   ├── hr/
│   └── projects/
├── services/
├── store/
├── utils/
└── views/
```

### 2.2 Composants Réutilisables

#### DataTable
```typescript
interface DataTableProps<T> {
  data: T[];
  columns: Column[];
  pagination?: PaginationConfig;
  sorting?: SortingConfig;
  filtering?: FilterConfig;
  actions?: ActionConfig[];
  onRowClick?: (row: T) => void;
}

// Exemple d'utilisation
<DataTable
  data={inventoryItems}
  columns={[
    { field: 'code', header: 'Code' },
    { field: 'name', header: 'Nom' },
    { field: 'quantity', header: 'Quantité' },
    { field: 'value', header: 'Valeur', format: 'currency' }
  ]}
  pagination={{
    pageSize: 10,
    totalItems: 100
  }}
/>
```

#### StatCard
```typescript
interface StatCardProps {
  title: string;
  value: number | string;
  variation?: {
    value: number;
    type: 'increase' | 'decrease';
  };
  icon?: IconType;
  format?: 'number' | 'currency' | 'percentage';
}

// Exemple d'utilisation
<StatCard
  title="Chiffre d'affaires"
  value={500000000}
  variation={{ value: 15, type: 'increase' }}
  format="currency"
/>
```

#### ChartComponent
```typescript
interface ChartProps {
  type: 'line' | 'bar' | 'pie' | 'radar';
  data: ChartData;
  options?: ChartOptions;
  height?: number;
  width?: number;
}

// Exemple d'utilisation
<ChartComponent
  type="line"
  data={{
    labels: ['Jan', 'Fév', 'Mar'],
    datasets: [{
      label: 'Ventes',
      data: [65, 59, 80]
    }]
  }}
/>
```

## 3. Intégration API

### 3.1 Service de Base
```typescript
class ApiService {
  private baseUrl: string;
  private headers: Headers;

  constructor() {
    this.baseUrl = process.env.REACT_APP_API_URL;
    this.headers = new Headers({
      'Content-Type': 'application/json'
    });
  }

  async get<T>(endpoint: string): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      headers: this.headers
    });
    return response.json();
  }

  // Autres méthodes HTTP...
}
```

### 3.2 Services Spécifiques
```typescript
class InventoryService extends ApiService {
  async getStock(): Promise<StockItem[]> {
    return this.get('/inventory/stock');
  }

  async updateStock(item: StockItem): Promise<void> {
    return this.put(`/inventory/stock/${item.id}`, item);
  }
}
```

## 4. Gestion de l'État

### 4.1 Store Redux
```typescript
interface RootState {
  auth: AuthState;
  inventory: InventoryState;
  finance: FinanceState;
  production: ProductionState;
  hr: HRState;
}

// Slice Exemple (Finance)
const financeSlice = createSlice({
  name: 'finance',
  initialState,
  reducers: {
    setTransactions: (state, action) => {
      state.transactions = action.payload;
    },
    updateDashboardStats: (state, action) => {
      state.dashboardStats = action.payload;
    }
  }
});
```

### 4.2 React Query Hooks
```typescript
function useInventoryStock() {
  return useQuery('inventory-stock', () => 
    inventoryService.getStock(), {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 30 * 60 * 1000 // 30 minutes
    }
  );
}
```

## 5. Composants Spécifiques aux Modules

### 5.1 Module Finance
```typescript
// Dashboard Finance
interface FinanceDashboardProps {
  period: DateRange;
  currency: string;
}

// Composant Transaction
interface TransactionListProps {
  transactions: Transaction[];
  onTransactionClick: (id: string) => void;
  filters: TransactionFilters;
}
```

### 5.2 Module Inventaire
```typescript
// Tableau de Stock
interface StockTableProps {
  items: StockItem[];
  onItemUpdate: (item: StockItem) => void;
  onItemDelete: (id: string) => void;
}

// Formulaire d'Article
interface ItemFormProps {
  item?: StockItem;
  onSubmit: (data: StockItem) => void;
  categories: Category[];
}
```

## 6. Optimisations

### 6.1 Performance
```typescript
// Mémoisation des composants lourds
const MemoizedDataGrid = React.memo(DataGrid);

// Virtualisation des listes longues
import { VirtualizedList } from 'react-virtualized';

// Chargement différé des modules
const FinanceModule = React.lazy(() => 
  import('./modules/finance/FinanceModule')
);
```

### 6.2 Mise en Cache
```typescript
// Configuration du cache React Query
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,
      cacheTime: 30 * 60 * 1000,
      retry: 1,
      refetchOnWindowFocus: false
    }
  }
});
```

## 7. Tests

### 7.1 Tests Unitaires
```typescript
describe('StatCard', () => {
  it('affiche correctement la variation positive', () => {
    render(
      <StatCard
        title="CA"
        value={1000000}
        variation={{ value: 15, type: 'increase' }}
      />
    );
    expect(screen.getByText('+15%')).toBeInTheDocument();
  });
});
```

### 7.2 Tests E2E
```typescript
describe('Module Inventaire', () => {
  it('permet d\'ajouter un nouvel article', () => {
    cy.visit('/inventory');
    cy.get('[data-testid="add-item-btn"]').click();
    cy.get('[data-testid="item-form"]').within(() => {
      cy.get('input[name="name"]').type('Nouvel Article');
      cy.get('input[name="quantity"]').type('100');
      cy.get('button[type="submit"]').click();
    });
    cy.contains('Article ajouté avec succès');
  });
});
```

## 8. Sécurité

### 8.1 Protection des Routes
```typescript
const PrivateRoute: React.FC<PrivateRouteProps> = ({
  component: Component,
  roles,
  ...rest
}) => {
  const { user } = useAuth();
  
  return (
    <Route
      {...rest}
      render={props => {
        if (!user) {
          return <Redirect to="/login" />;
        }

        if (roles && !roles.includes(user.role)) {
          return <Redirect to="/unauthorized" />;
        }

        return <Component {...props} />;
      }}
    />
  );
};
```

### 8.2 Intercepteurs HTTP
```typescript
const authInterceptor = (config: AxiosRequestConfig) => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
};

axios.interceptors.request.use(authInterceptor);
```

## 9. Internationalisation

### 9.1 Configuration i18n
```typescript
i18n.use(initReactI18next).init({
  resources: {
    fr: {
      translation: {
        inventory: {
          title: 'Gestion de l\'Inventaire',
          stock: 'Stock total',
          value: 'Valeur du stock'
        }
      }
    }
  },
  lng: 'fr',
  fallbackLng: 'fr'
});
```

## 10. Documentation

### 10.1 Storybook
```typescript
// Button.stories.tsx
export default {
  title: 'Components/Button',
  component: Button
} as ComponentMeta<typeof Button>;

const Template: ComponentStory<typeof Button> = (args) => 
  <Button {...args} />;

export const Primary = Template.bind({});
Primary.args = {
  variant: 'primary',
  label: 'Button Primary'
};
