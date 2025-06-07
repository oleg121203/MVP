## Theme System Guide

### Basic Usage
```jsx
<ThemeProvider>
  <App />
</ThemeProvider>

function Component() {
  const { darkMode, toggleTheme } = useTheme();
  return (
    <div className={darkMode ? 'dark' : 'light'}>
      <button onClick={toggleTheme}>Toggle</button>
    </div>
  );
}
```

### Theme Variables
- `darkMode`: boolean
- `toggleTheme`: function

### Styling
Use Tailwind's `dark:` prefix:
```html
<div class="bg-white dark:bg-gray-800">
```
