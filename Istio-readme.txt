Istio

El despliegue se realiza en una máquina Ubuntu usando minikube.

1) Instalar Docker
# Clave y repo oficial de Docker
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) \
signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/ubuntu \
$(. /etc/os-release; echo "$VERSION_CODENAME") stable" \
| sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable --now docker

# Usar Docker sin sudo
sudo usermod -aG docker $USER
newgrp docker
docker run --rm hello-world


2) Instalar kubectl, Minikube, Helm, istioctl
sudo snap install kubectl --classic
kubectl version --client

curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
minikube version

curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
helm version --short

curl -L https://istio.io/downloadIstio | sh -
cd istio-*
export PATH="$PWD/bin:$PATH"
echo 'export PATH="$PATH:'"$PWD"'/bin"' >> ~/.bashrc
source ~/.bashrc
istioctl version --remote=false


3) Levantar Kubernetes con Minikube (Docker driver)
minikube start --driver=docker --cpus=4 --memory=8192


4) Instalar Istio (perfil “demo” para laboratorio)
istioctl install --set profile=demo -y
cd ~/Downloads/istio-1.27.0/	#O ingresar a la carpeta donde se descargó el istio
kubectl apply -f samples/addons/kiali.yaml


5) Generar las imágenes de los microservicios
cd ~ #O ingresar a la carpeta del repositorio
minikube image build -t ms-bodega:latest ./ms-bodega
#repetir el comando anterior con los otros 5 microservicios


6) Desplegar los microservicios en istio
cd ~	#O ingresar a la carpeta del repositorio, donde está el archivo istio.yaml
kubectl apply -f istio.yaml


7) Verificar microservicios
#Si todo sale bien, al ejecutar los siguientes comandos deben salir los pods del istio y de los microservicios
kubectl get pods -n istio-system
kubectl get pods -n service-mesh


8) Hacer port forwarding para visualizar kiali
kubectl port-forward svc/kiali -n istio-system 20001:20001
# Navega a:
# http://localhost:20001
