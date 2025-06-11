import { configureStore } from '@reduxjs/toolkit';
import priceReducer from './priceSlice';
import predictReducer from './predictSlice';

export default configureStore({
  reducer: {
    price: priceReducer,
    predict: predictReducer
  }
});
