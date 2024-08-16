/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./*"],
  theme: {
    extend: {

      w: {
        '24': '6rem',    // Añade un valor de ancho menor
        '32': '8rem',    // Puedes añadir otros valores personalizados si es necesario
        '48': '12rem',
        '64': '16rem',
        '80': '20rem',
        '96': '24rem',   // Valor mayor por defecto en Tailwind
        // Puedes añadir valores menores aquí
      }
    },
  },

  
  plugins: [],
}

