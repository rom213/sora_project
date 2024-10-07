
module.exports = {
  apps: [
    {
      name: "flask-app",
      script: '/home/bitnami/.local/bin/gunicorn',
      args: "--worker-class eventlet -w 1 -b 0.0.0.0:3000 app:app",
      interpreter: "none",
      env: {
        FLASK_ENV: "production",
        FLASK_DEBUG: "1",
        SECRET_KEY: "tu_clave_secreta",
        MYSQL_HOST: "localhost",
        MYSQL_USER: "root",
        MYSQL_PASSWORD: "B=HNBaII:aV9",
        MYSQL_DB: "chat",
      },
    },
  ],
};
