import React from 'react';
import { Card, CardContent, Typography, Box, Chip } from '@mui/material';
import { useQuery } from 'react-query';
import { getInventoryStats } from '../../services/inventory';

const InventoryStats: React.FC = () => {
  const { data: stats } = useQuery('inventory-stats', getInventoryStats);

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Inventaire
        </Typography>

        <Box sx={{ mb: 2 }}>
          <Typography variant="subtitle2" color="text.secondary">
            Valeur Totale
          </Typography>
          <Typography variant="h4">
            {new Intl.NumberFormat('fr-FR', {
              style: 'currency',
              currency: 'XAF',
              maximumFractionDigits: 0
            }).format(stats?.valeur_totale || 0)}
          </Typography>
        </Box>

        <Box sx={{ display: 'flex', gap: 1 }}>
          <Chip
            label={`${stats?.alertes || 0} Alertes`}
            color="error"
            size="small"
          />
          <Chip
            label={`${stats?.mouvements_jour || 0} Mouvements`}
            color="info"
            size="small"
          />
        </Box>
      </CardContent>
    </Card>
  );
};

export default InventoryStats;