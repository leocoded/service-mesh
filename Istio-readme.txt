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
minikube start --driver=docker --cpus=4 --memory=10240 #Modificar el valor de memoria según necesidades


4) Instalar Istio (perfil “demo” para laboratorio)
istioctl install --set profile=demo -y
cd ~/Downloads/istio-1.27.0/	#O ingresar a la carpeta donde se descargó el istio


5)Instalar los addons de istio (Kiali, Grafana, Prometheus, Loki, Jaeger)
kubectl apply -f samples/addons


6) Generar las imágenes de los microservicios
cd ~/arquitectura/repo/service-mesh #O ingresar a la carpeta del repositorio
minikube image build -t ms-bodega:latest ./ms-bodega
minikube image build -t ms-lote:latest ./ms-lote
minikube image build -t ms-orden-compra:latest ./ms-orden-compra
minikube image build -t ms-producto:latest ./ms-producto
minikube image build -t ms-proveedor:latest ./ms-proveedor
minikube image build -t ms-proyeccion-demanda:latest ./ms-proyeccion-demanda


7) Desplegar los microservicios en istio
cd ~/arquitectura/repo/service-mesh #O ingresar a la carpeta del repositorio
kubectl apply -f istio.yaml


8) Verificar microservicios
#Si todo sale bien, al ejecutar los siguientes comandos deben salir los pods del istio y de los microservicios
kubectl get pods -n istio-system
kubectl get pods -n service-mesh


9) Hacer port forwarding para visualizar los addons
cd ~/arquitectura/repo/service-mesh #O ingresar a la carpeta del repositorio
./istio-port-forward.sh


10) Instalar promtail
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm install promtail grafana/promtail -n istio-system


11) Configurar telemetría para modificar el sampling de eventos de tráfico
istioctl install -f ./tracing.yaml --skip-confirmation
kubectl apply -f ./telemetry.yaml
helm upgrade --install promtail grafana/promtail \
  --namespace istio-system \
  -f promtail-values.yaml


12) Activar el tunner de minikube
minikube tunnel #bloquea la terminal
kubectl get svc -n istio-system istio-ingressgateway # Para ver el puerto usado para los requests


13) Hacer port forwarding para visualizar Jaeger
kubectl port-forward pod/<nombre-jaeger-pod> -n istio-system 16686:16686


14) Activar el mTLS estricto
kubectl apply -f peerauth-strict.yaml


15) Desplegar pod con tcpdump para visualizar tráfico
kubectl apply -f tcpdump.yaml
kubectl exec -it tcpdump -n istio-system -- sh
tcpdump -i any -A -s 0 port 8003