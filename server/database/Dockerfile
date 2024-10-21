# Usa un'immagine di base di Node.js
FROM node:14

# Imposta la directory di lavoro nell'immagine Docker
WORKDIR /usr/src/app

# Copia package.json e package-lock.json (se esiste) per installare le dipendenze
COPY package*.json ./

# Installa le dipendenze dell'applicazione
RUN npm install

# Copia il resto dell'applicazione nel container
COPY . .

# Copia i dati JSON nel container
COPY ./data /usr/src/app/database/data

# Espone la porta 3030 per il server
EXPOSE 3030

# Comando per avviare l'applicazione Node.js
CMD ["npm", "start"]
