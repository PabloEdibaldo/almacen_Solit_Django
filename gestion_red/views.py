import subprocess
from django.http import JsonResponse
from django.views import View
import ast
import json
from .serializers import Router_serializer,Redes_ipb4_serializers,Monitoreo_serializer,NapCaja_serializer,OltDevice_serializer
from rest_framework import viewsets
from rest_framework.response import Response 
from . models import Router, RedesIpv4,Monitoreo,NapCaja,OltDevice
import requests
from clientes.models import Clientes
from django.views.decorators.csrf import csrf_exempt
import requests
import base64
#--------------------------------------------------------------------------------------PPP----------------------------------------------------------------------------------------------------------
class Datos_Clientes_PPP_View(View):     
    
    def guardarClientes(self, data):
        data_dict = json.loads(data)
        pppoe_clients = data_dict.get("PPPoE", [])
        for client in pppoe_clients:
            comment = client.get("=comment", "")
            name = client.get("=name", "")
            if comment and name:
                # Verificar si ya existe un cliente con el mismo comentario
                if not Clientes.objects.filter(nombres_apellidos=comment,name = name).exists():
                    cliente = Clientes(nombres_apellidos=comment,name=name)
                    cliente.save()           
    def get(self, request):
        try:
            router_ip = request.GET.get('router_ip', None)
            if router_ip is None:
                raise ValueError("La IP del router no se proporcionó en los parámetros de la solicitud.")
            ruta = "gestion_red/ApiRos.py"

            # Peticion a la API
            consulta1 = subprocess.run(["python3", ruta, router_ip, 'solit', 'Pa238388$', '/ppp/active/print'], capture_output=True)
            salida_estandar1 = consulta1.stdout.decode('utf-8')
            data_dict1 = ast.literal_eval(salida_estandar1)
            result1 = {}
            for ip, info in data_dict1.items():
                result1[ip] = {'resultado': []}
                for entry in info['resultado']:
                    item_dict = {}
                    for item in entry[1]:
                        if item.startswith('='):
                            item_dict[item] = entry[1][item]
                    # Agregar el campo "Activo" a cada objeto con un valor predeterminado (True en este ejemplo)
                    item_dict['Activo'] = 'activo'
                    result1[ip]['resultado'].append(item_dict)

            resultado_filtrado = {'PPPoE': [item for item in result1[router_ip]['resultado'] if '=comment' in item]}
            self.guardarClientes(json.dumps(resultado_filtrado))
          
           
        except Exception as e:
            resultado_filtrado = {'error': str(e)}
        return JsonResponse(resultado_filtrado)

#/ppp/profile/print
#---------------------------------------------------------------------------------------DHCP---------------------------------------------------------------------------------------------------------
class Datos_ClientesView(View):
    def guardarClientes(self, data):
        data_dict = json.loads(data)
        pppoe_clients = data_dict.get("DHCP", [])
        for client in pppoe_clients:
            comment = client.get("=comment", "")
            if comment:
                # Verificar si ya existe un cliente con el mismo comentario
                if not Clientes.objects.filter(nombres_apellidos=comment).exists():
                    cliente = Clientes(nombres_apellidos=comment)
                    cliente.save()
                    
    def get(self,request,*args,**kwargs):
        try:
            # Obtener la IP del router desde los parámetros de la solicitud
            router_ip = request.GET.get('router_ip', None)
            if router_ip is None:
                raise ValueError("La IP del router no se proporcionó en los parámetros de la solicitud.")
            ruta = "gestion_red/ApiRos.py"
            # Peticion a la API
            consulta1 = subprocess.run(["python3", ruta, router_ip, 'solit', 'Pa238388$', '/ip/dhcp-server/lease/print'], capture_output=True)
            salida_estandar1 = consulta1.stdout.decode('utf-8')
            data_dict1 = ast.literal_eval(salida_estandar1)
            
            result1 = {}
            for ip, info in data_dict1.items():
                result1[ip] = {'resultado': []}
                for entry in info['resultado']:
                    item_dict = {}
                    for item in entry[1]:
                        if item.startswith('='):
                            item_dict[item] = entry[1][item]
                    result1[ip]['resultado'].append(item_dict)

            resultado_filtrado = {'DHCP': [item for item in result1[router_ip]['resultado'] if '=comment' in item]}
            self.guardarClientes(json.dumps(resultado_filtrado))
            return JsonResponse(resultado_filtrado)

        except Exception as e:
            return JsonResponse({'error': str(e)})

class Datos_RouterView(View):

    def get(self,request,*args,**kwargs):
        try:
            ruta = "gestion_red/ApiRos.py"
            router_ip = request.GET.get('router_ip', None)
            if router_ip is None:
                raise ValueError("La IP del router no se proporcionó en los parámetros de la solicitud.")
            result = {}
            consulta1 = subprocess.run(["python3", ruta, router_ip, 'solit', 'Pa238388$', '/system/resource/print'], capture_output=True)
            salida_estandar1 = consulta1.stdout.decode('utf-8')
            data_dict = ast.literal_eval(salida_estandar1)
        # Procesar el diccionario para obtener el formato deseado

            campos_interesantes = [
                "=uptime", "=version", "=build-time", "=factory-software",
                "=free-memory", "=total-memory", "=cpu", "=cpu-count",
                "=cpu-load", "=free-hdd-space", "=total-hdd-space",
                "=write-sect-since-reboot", "=write-sect-total",
                "=bad-blocks", "=architecture-name", "=board-name",
                "=platform"
            ]
            for ip, info in data_dict.items():
                result[ip] = {}
                for campo in campos_interesantes:
                    if campo in info['resultado'][0][1]:
                        result[ip][campo] = info['resultado'][0][1][campo]
            # Eliminar la IP del resultado final
            result = next(iter(result.values()))
            # Convertir el resultado a una cadena JSON con formato indentado
            respuesta_json = json.dumps(result, indent=4)
            # Devolver la respuesta JSON al cliente
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({'error': str(e)})

class RouterView(viewsets.ModelViewSet):
    serializer_class = Router_serializer
    queryset = Router.objects.all()


    def update(self, request, pk=None):
        router = self.get_object()
        serializer = self.serializer_class(router, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class Redes_ipb4View(viewsets.ModelViewSet):
    serializer_class = Redes_ipb4_serializers
    queryset = RedesIpv4.objects.all()
#------------------------------------------------------------API SMARTOLT--------------------------------------------------------------------
class ZonasView(View):
    def get(self,request,*args,**kwargs):
        url = "https://solit.smartolt.com/api/system/get_zones"
        headers = {
            'X-Token': 'cb9d8a2f53970330be6bb1bcef1f4d0b'
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            return JsonResponse(data)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
        


    @csrf_exempt
    def post(self,request,*args,**kwargs):
        data = json.loads(request.body)
        url = "https://solit.smartolt.com/api/system/add_zone"
        payload={'zone': data}
        files=[]
        headers = {'X-Token': 'cb9d8a2f53970330be6bb1bcef1f4d0b'}
        try:

            response = requests.request("POST", url, headers=headers, data=payload, files=files)
            response.raise_for_status()
            api_data = response.json()

            # Aquí puedes guardar los datos en tu modelo o base de datos
            # Por ejemplo, si tienes un modelo Zona:
            # nueva_zona = Zona(nombre=api_data['nombre'])
            # nueva_zona.save()

            return JsonResponse(api_data)
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": str(e)},status = 500)

class ProfilesView(View):
    def get(self,request,*args,**kwargs):
        url = "https://solit.smartolt.com/api/system/get_speed_profiles"
        headers = {
            'X-Token': 'cb9d8a2f53970330be6bb1bcef1f4d0b'
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return JsonResponse(data)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
   
class MonitoreoView(viewsets.ModelViewSet):
    serializer_class = Monitoreo_serializer
    queryset = Monitoreo.objects.all()

class NapCajaView(viewsets.ModelViewSet):
    serializer_class = NapCaja_serializer
    queryset = NapCaja.objects.all()
       
class OltDeviceView(viewsets.ModelViewSet):
    serializer_class = OltDevice_serializer
    queryset = OltDevice.objects.all()
    
class obtenerClientesSmartOLT(View):
    
    def getOlts(self,request,*args,**kwargs):
        url = "https://solit.smartolt.com/api/system/get_olts"
        headers = {'X-Token': 'cb9d8a2f53970330be6bb1bcef1f4d0b'}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            if data.get('status') and data.get('response_code') == 'success':
                 for olt_data in data.get('response', []):
                # Verificamos si el OLT ya existe en la base de datos
                    olt_id = olt_data.get('id')
                    olt, created = OltDevice.objects.get_or_create(id=olt_id)
                    # Actualizamos los campos del modelo con los datos de la API
                    olt.name = olt_data.get('name')
                    olt.olt_hardware_version = olt_data.get('olt_hardware_version')
                    olt.ip = olt_data.get('ip')
                    olt.telnet_port = olt_data.get('telnet_port')
                    olt.snmp_port = olt_data.get('snmp_port')
                    # Guardamos el objeto OltDevice
                    olt.save()
                    
            return JsonResponse(data)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
        
        
    def get(self,request,*args,**kwargs):
        # Hacer la primera solicitud para obtener la lista de OLTs
        url_olts = "https://solit.smartolt.com/api/system/get_olts"
        headers = {'X-Token': 'cb9d8a2f53970330be6bb1bcef1f4d0b'}  # Asegúrate de reemplazar 'tu_token_aqui' con tu token real
        
        try: 
            response_olts = requests.get(url_olts,headers=headers)
            data_olts = response_olts.json()
            
            if data_olts.get('status') and data_olts.get('response_code') == 'success':
                # Extraer las IDs de los OLTs
                olt_ids = [olt['id'] for olt in data_olts.get('response', [])]
                 # Hacer la segunda solicitud para cada ID de OLT
                url_onus = "https://solit.smartolt.com/api/onu/get_all_onus_details?olt_id={}"
                onus_data = {}
                
                for olt_id in olt_ids:
                    url_olt_onus = url_onus.format(olt_id)
                    response_onus = requests.get(url_olt_onus, headers=headers)
                    data_onus = response_onus.json()
                    
                        # Añadir los datos de ONU al diccionario
                    onus_data[olt_id] = data_onus
                return JsonResponse({'onus_data': onus_data})
            else:
                return JsonResponse({'error': 'Error en la respuesta de la API de OLTs'})
        except Exception as e:
            return JsonResponse({'error': f"Error al realizar la petición a la API de OLTs: {str(e)}"})

class ObtenerVLANs(View):
    def get(self, request, *args, **kwargs):
        url_olts = "https://solit.smartolt.com/api/system/get_olts"
        headers = {'X-Token': 'cb9d8a2f53970330be6bb1bcef1f4d0b'}  # Asegúrate de reemplazar 'tu_token_aqui' con tu token real

        try:
            response_olts = requests.get(url_olts, headers=headers)
            data_olts = response_olts.json()
            if data_olts.get('status') and data_olts.get('response_code') == 'success':
                # Extraer las IDs de los OLTs
                olt_ids = [olt['id'] for olt in data_olts.get('response', [])]
                # Lista para almacenar los resultados de cada solicitud
                all_onus_response_list = []
                # Hacer la segunda solicitud para cada ID de OLT
                url_onus = "https://solit.smartolt.com/api/olt/get_vlans/{}"
                for olt_id in olt_ids:
                    url_olt_onus = url_onus.format(olt_id)
                    response_onus = requests.get(url_olt_onus, headers=headers)
                    data_onus = response_onus.json()
                    if data_onus.get('status') and data_onus.get('response_code') == 'success':
                        onus_response_list = data_onus.get('response', [])
                        all_onus_response_list.extend(onus_response_list)
                # Devolver la lista completa de resultados fuera del bucle
                return JsonResponse({"vlans": all_onus_response_list})
            else:
                return JsonResponse({'error': 'Error en la respuesta de la API de OLTs'})

        except Exception as e:
            return JsonResponse({'error': f"Error al realizar la petición a la API de OLTs: {str(e)}"})

class GetONUfullStatus(View):
    def get(self,request):
        ip = request.GET.get('ip')
        try:
            url_olts = f"https://solit.smartolt.com/api/onu/get_onu_full_status_info/{ip}"
            headers = {'X-Token': 'cb9d8a2f53970330be6bb1bcef1f4d0b'}  
            payload={}
            response = requests.request("GET", url_olts, headers=headers, data=payload)
            print(response)
            
            if response.status_code ==200:
                return JsonResponse(response.json())
            else:
                return JsonResponse({'error': f"Error en la solicitud: {response.status_code}"}, status=500)
                     
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
        
class GetRoutingCofig(View):
    def get(self,request):
        ip = request.GET.get('ip')
        try:
            url_olts = f"https://solit.smartolt.com/api/onu/get_running_config/{ip}"
            headers = {'X-Token': 'cb9d8a2f53970330be6bb1bcef1f4d0b'}  
            payload={}
            response = requests.request("GET", url_olts, headers=headers, data=payload)
            print(response)
            
            if response.status_code ==200:
                return JsonResponse(response.json())
            else:
                return JsonResponse({'error': f"Error en la solicitud: {response.status_code}"}, status=500)
                     
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
                
class getTrafficGrap(View):
    def get(self, request):
        ip = request.GET.get('ip')
        try:
            base_url = "https://solit.smartolt.com/api/onu/get_onu_traffic_graph/"
            headers = {'X-Token': 'cb9d8a2f53970330be6bb1bcef1f4d0b'}  
            
            # Lista de tiempos
            tiempos = ["hourly", "daily", "weekly", "monthly", "yearly"]
            
            # Diccionario para almacenar imágenes codificadas en base64 por tiempo
            resultados = {}

            for tiempo in tiempos:
                # Corrección en la construcción de la URL
                url = f"{base_url}{ip}/{tiempo}"
                print("bg", url)
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    # Verificar si la respuesta contiene datos antes de codificar en base64
                    if response.content:
                        # Codificar en base64 y almacenar la cadena resultante
                        resultados[tiempo] = base64.b64encode(response.content).decode('utf-8')
                    else:
                        resultados[tiempo] = None
                else:
                    # Imprimir el contenido de la respuesta en caso de un error
                    print(response.content.decode('utf-8'))
                    return JsonResponse({'error': f"Error en la solicitud para tiempo {tiempo}: {response.status_code}"}, status=500)

            # Devolver las imágenes codificadas en base64 como respuesta JSON
            return JsonResponse(resultados)

        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
class getSignalGraph(View):
    def get(self, request):
        ip = request.GET.get('ip')
        try:
            base_url = "https://solit.smartolt.com/api/onu/get_onu_signal_graph/"
            headers = {'X-Token': 'cb9d8a2f53970330be6bb1bcef1f4d0b'}  
            
            # Lista de tiempos
            tiempos = ["hourly", "daily", "weekly", "monthly", "yearly"]
            
            # Diccionario para almacenar imágenes codificadas en base64 por tiempo
            resultados = {}

            for tiempo in tiempos:
                # Corrección en la construcción de la URL
                url = f"{base_url}{ip}/{tiempo}"
              
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    # Verificar si la respuesta contiene datos antes de codificar en base64
                    if response.content:
                        # Codificar en base64 y almacenar la cadena resultante
                        resultados[tiempo] = base64.b64encode(response.content).decode('utf-8')
                    else:
                        resultados[tiempo] = None
                else:
                    # Imprimir el contenido de la respuesta en caso de un error
                    print(response.content.decode('utf-8'))
                    return JsonResponse({'error': f"Error en la solicitud para tiempo {tiempo}: {response.status_code}"}, status=500)

            # Devolver las imágenes codificadas en base64 como respuesta JSON
            return JsonResponse(resultados)

        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)