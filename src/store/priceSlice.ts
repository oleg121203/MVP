import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface PriceState {
  data: any[];
  loading: boolean;
  error: string | null;
}

const initialState: PriceState = {
  data: [],
  loading: false,
  error: null,
};

const priceSlice = createSlice({
  name: 'price',
  initialState,
  reducers: {
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setPriceData: (state, action: PayloadAction<any[]>) => {
      state.data = action.payload;
      state.loading = false;
      state.error = null;
    },
    setError: (state, action: PayloadAction<string>) => {
      state.error = action.payload;
      state.loading = false;
    },
    clearError: (state) => {
      state.error = null;
    },
  },
});

export const { setLoading, setPriceData, setError, clearError } = priceSlice.actions;

const priceReducer = priceSlice.reducer;
export { priceReducer };
export default priceReducer;