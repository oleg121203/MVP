import { configureStore } from '@reduxjs/toolkit';
import analyticsReducer from './analyticsSlice';
import predictiveModelsReducer from './predictiveModelsSlice';
import customReportsReducer from './customReportsSlice';

const store = configureStore({
  reducer: {
    analytics: analyticsReducer,
    predictiveModels: predictiveModelsReducer,
    customReports: customReportsReducer,
  },
});

export default store;
