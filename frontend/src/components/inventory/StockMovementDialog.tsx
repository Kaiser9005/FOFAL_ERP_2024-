import React from 'react';
import { useForm, Controller } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Grid,
  TextField,
  MenuItem,
  Button
} from '@mui/material';
import { useMutation, useQueryClient } from 'react-query';
import { createMovement } from '../../services/inventory';
import { LoadingButton } from '@mui/lab';

const schema = yup.object({
  type: yup.string().required('Le type de mouvement est requis'),
  quantity: yup.number()
    .required('La quantité est requise')
    .positive('La quantité doit être positive'),
  reference: yup.string()
}).required();

interface StockMovementDialogProps {
  open: boolean;
  onClose: () => void;
  productId: string | null;
}

const StockMovementDialog: React.FC<StockMovementDialogProps> = ({
  open,
  onClose,
  productId
}) => {
  const queryClient = useQueryClient();

  const { control, handleSubmit, formState: { errors } } = useForm({
    resolver: yupResolver(schema),
    defaultValues: {
      type: '',
      quantity: '',
      reference: ''
    }
  });

  const mutation = useMutation(createMovement, {
    onSuccess: () => {
      queryClient.invalidateQueries('stocks');
      queryClient.invalidateQueries('recent-movements');
      onClose();
    }
  });

  const onSubmit = (data: any) => {
    if (productId) {
      mutation.mutate({
        productId,
        ...data
      });
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <form onSubmit={handleSubmit(onSubmit)}>
        <DialogTitle>Nouveau Mouvement de Stock</DialogTitle>
        
        <DialogContent>
          <Grid container spacing={3} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <Controller
                name="type"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    select
                    label="Type de Mouvement"
                    fullWidth
                    error={!!errors.type}
                    helperText={errors.type?.message}
                  >
                    <MenuItem value="ENTREE">Entrée</MenuItem>
                    <MenuItem value="SORTIE">Sortie</MenuItem>
                    <MenuItem value="TRANSFERT">Transfert</MenuItem>
                  </TextField>
                )}
              />
            </Grid>

            <Grid item xs={12}>
              <Controller
                name="quantity"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Quantité"
                    type="number"
                    fullWidth
                    error={!!errors.quantity}
                    helperText={errors.quantity?.message}
                  />
                )}
              />
            </Grid>

            <Grid item xs={12}>
              <Controller
                name="reference"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Référence"
                    fullWidth
                    error={!!errors.reference}
                    helperText={errors.reference?.message}
                  />
                )}
              />
            </Grid>
          </Grid>
        </DialogContent>

        <DialogActions>
          <Button onClick={onClose}>
            Annuler
          </Button>
          <LoadingButton
            variant="contained"
            type="submit"
            loading={mutation.isLoading}
          >
            Enregistrer
          </LoadingButton>
        </DialogActions>
      </form>
    </Dialog>
  );
};

export default StockMovementDialog;