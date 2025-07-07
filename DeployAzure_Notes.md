# 🚀 Deploy Flask + Docker no Azure App Service usando ACR e GitHub Actions

## ✅ 1. Pré-requisitos
✔️ Conta no Azure
✔️ Resource Group criado
✔️ Azure Container Registry (ACR) criado
✔️ Storage Account (opcional, se for usado pela aplicação)
✔️ Repositório GitHub com:
✔️ Código Flask
✔️ Dockerfile

## 🔐 2. Criar o Service Principal (SP) para CI/CD

2.1 Criar o Service Principal com permissão no Resource Group

No terminal ou Cloud Shell do Azure:

```bash
az ad sp create-for-rbac \
  --name "<sp-name>" \
  --role contributor \
  --scopes /subscriptions/<subscription-id>/resourceGroups/<resource-group> \
  --sdk-auth
```
📥 Guarde o JSON gerado, por exemplo:

```json
{
  "clientId": "...",
  "clientSecret": "...",
  "subscriptionId": "...",
  "tenantId": "...",
  ...
}

```

2.2 Criar o Secret no GitHub

1.Acesse seu repositório no GitHub → Settings → Secrets and Variables → Actions
2.Clique em New repository secret
3.Nomeie como: `AZURE_CREDENTIALS`
4.Cole o JSON inteiro gerado no passo anterior

## ⚙️ 3. Criar Azure App Service e Service Plan

3.1 Criar o App Service Plan:

Execute o seguinte comando no terminal para registrar o provedor de recursos Microsoft.Web:

```bash
az provider register --namespace Microsoft.Web
```
✔️ Verificar o Status depois
Você pode verificar se foi registrado corretamente com:

```bash
az provider show --namespace Microsoft.Web --query "registrationState"
```

```bash
az appservice plan create \
  --name <app-service-plan-name> \
  --resource-group <resource-group> \
  --location <region> \
  --is-linux \
  --sku B1
```

3.2 Criar o Web App (App Service)

```bash
az webapp create \
  --resource-group <resource-group> \
  --plan <app-service-plan-name> \
  --name <app-service-name> \
  --deployment-container-image-name <acr-name>.azurecr.io/<image-name>:latest
```

## 🔑 4. Dar Permissão do App Service ao ACR

```bash
az webapp config container set \
  --name <app-service-name> \
  --resource-group <resource-group> \
  --docker-registry-server-url https://<acr-name>.azurecr.io \
  --docker-registry-server-user <acr-username> \
  --docker-registry-server-password <acr-password>
```

📌 Para pegar usuário e senha do ACR:

```bash
az acr credential show --name <acr-name>
```

## 📦 5. Dockerfile da Aplicação Flask

```dockerfile
FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -e .

EXPOSE 5000

ENV FLASK_APP = application.py

CMD ["python", "application.py"]
```

## 🔧 6. Criar o Workflow do GitHub Actions


## 🚀 7. Realizar o Deploy

## 🔍 8. Verificar o Deploy
Ver logs da aplicação:

```bash
az webapp log tail --name <app-service-name> --resource-group <resource-group>
```