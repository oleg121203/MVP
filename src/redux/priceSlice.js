import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Mock API call
const fetchPriceDataAPI = async () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        historicalPrices: [
          { date: '2023-01-01', price: 100 },
          { date: '2023-01-02', price: 105 },
          // ... more data
        ],
        forecast: [
          { date: '2023-01-08', predictedPrice: 110 },
          // ... more forecast data
        ]
      });
    }, 1000);
  });
};

export const fetchPriceData = createAsyncThunk(
  'price/fetchData',
  async () => {
    const data = await fetchPriceDataAPI();
    return data;
  }
);

const priceSlice = createSlice({
  name: 'price',
  initialState: {
    data: null,
    loading: false,
    error: null
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchPriceData.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchPriceData.fulfilled, (state, action) => {
        state.loading = false;
        state.data = action.payload;
      })
      .addCase(fetchPriceData.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  }
});

export default priceSlice.reducer;
