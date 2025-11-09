# 🔧 Configuración de Variables de Entorno

## 1. Crear archivo .env

Copia `.env.example` a `.env` en la carpeta `ms-blockchain`:

```bash
cd ms-blockchain
copy .env.example .env
```

## 2. Configurar credenciales

Edita el archivo `.env` con tus credenciales reales:

```env
# Polygon Amoy Configuration
INFURA_PROJECT_ID=tu_project_id_de_infura
PRIVATE_KEY=tu_private_key_de_metamask

# Pinata IPFS Configuration  
PINATA_API_KEY=tu_api_key_de_pinata
PINATA_SECRET_API_KEY=tu_secret_key_de_pinata

# Contract Address (se configurará después del deploy)
CONTRACT_ADDRESS=
```

## 3. Obtener credenciales

### Infura:
1. Ve a https://infura.io
2. Crea un proyecto Polygon
3. Copia el Project ID

### Pinata:
1. Ve a https://pinata.cloud
2. Crea cuenta y ve a API Keys
3. Crea nueva API key con permisos de Pin

### MetaMask:
1. Exporta tu private key de MetaMask
2. Asegúrate de tener MATIC en Polygon Amoy testnet

## 4. Instalar dependencias

```bash
cd ms-blockchain
npm install dotenv
```