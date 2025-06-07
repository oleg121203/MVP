module.exports = {
  darkMode: 'class',
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      colors: {
        'vent-primary': '#1E90FF',
        'vent-secondary': '#87CEFA',
        'vent-accent': '#4682B4',
        'vent-dark': '#1E3A8A',
        dark: {
          primary: '#1E40AF',
          secondary: '#1E3A8A',
          bg: '#0F172A',
          text: '#E5E7EB',
          card: '#1F2937',
          accent: '#3B82F6'
        }
      },
      backgroundImage: {
        'pipe-pattern': "url('/img/pipe-bg.svg')",
        'airflow-texture': "url('/img/airflow-pattern.svg')"
      },
      fontFamily: {
        sans: ['"Open Sans"', 'sans-serif'],
        technical: ['"Share Tech"', 'monospace']
      }
    }
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography')
  ]
}
