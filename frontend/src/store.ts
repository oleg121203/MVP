import { configureStore } from '@reduxjs/toolkit';

export const store = configureStore({
  reducer: {}, // Add reducers as needed; currently empty for mock setup
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
