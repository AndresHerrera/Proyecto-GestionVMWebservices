#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#
# El siguiente Web Service  permite gestionar maquinas virtuales de VirtualBox
# Basado en los ejemplos de curso Fundamentos de Sistemas Distribuidos
# DS-Fall 2007 -  Docente : John Sanabria - john.sanabria@correounivalle.edu.co   
#
# Alumnos:  Fabio Andres Herrera - fabio.herrera@correounivalle.edu.co
#                  Mario Castillo - mario.castillo@correounivalle.edu.co
#
#
#
# Librerias requeridas para correr aplicaciones basadas en Flask
import os
from flask import Flask, jsonify, make_response,  request, abort
import subprocess 

app = Flask(__name__)


# curl http://localhost:5000
@app.route('/')
@app.route('/index.htm')
@app.route('/index.html')
def index():
    request_host=request.host
    output = "<html><head><style>table,th,td{border:1px solid black;border-collapse:collapse;}</style></head><body>" 
    output += "<h2>VM WebService</h2>"
    output +="<h3>By:<br>Andres Herrera - fabio.herrera@correounivalle.edu.co"
    output +="<br>Mario Castillo - mario.castillo@correounivalle.edu.co</h3>"
    output +="<h3>Usage:</h3>"
    output +="<table style='width:100%'><tr><th>METHOD</th><th>URL</th><th>JSON Response</th></tr>"
    output +="<tr><td colspan=3 align=center><b>GENERAL</b></td></tr>"
    output +="<tr><td>GET</td><td>curl http://"+request_host+"/</td><td>Avaliable services</td></tr>"
    output +="<tr><td>GET</td><td>curl http://"+request_host+"/vms/ostypes</td><td>List OS types supported for Virtual Box</td></tr>"
    output +="<tr><td>GET</td><td>curl http://"+request_host+"/vms</td><td>List VMS</td></tr>"
    output +="<tr><td>GET</td><td>curl http://"+request_host+"/vms/running</td><td>Running VMS</td></tr>"
    output +="<tr><td>GET</td><td>curl http://"+request_host+"/vms/info/vmname</td><td>Info for vmname VM</td></tr>"
    output +="<tr><td>POST</td><td>curl -i -H \"Content-Type: application/json\" -X POST -d \'{\"name\":\"osweb\", \"disksize\":\"32738\",  \"cpunumber\":\"4\" ,  \"memory\":\"1024\"   ,  \"ram\":\"580\"}\' http://"+request_host+"/vms	</td><td>Create a VM.</td></tr>"
    output +="<tr><td>DELETE</td><td>curl -i -H \"Content-Type: application/json\" -X DELETE http://"+request_host+"/vms/vmname</td><td>Delete a VM (vmname).</td></tr>"
    output +="</table>"
    output +="</body></html>"
    return output

# Lista de sistemas operativos soportados por VirtualBox
#curl http://localhost:5000/vms/ostypes
#command vboxmanage list ostypes | grep ^ID | tr -s ' '  | cut -d ':' -f 2
@app.route('/vms/ostypes',methods = ['GET'])
def ostypes():
    vboxm =  subprocess.Popen(['vboxmanage', 'list' , 'ostypes'], stdout = subprocess.PIPE) 
    grep = subprocess.Popen(['grep','^ID'], stdin = vboxm.stdout, stdout = subprocess.PIPE)
    tr = subprocess.Popen(['tr','-s', ' '], stdin = grep.stdout, stdout = subprocess.PIPE)
    output = subprocess.check_output(['cut','-d', ':', '-f', '2'], stdin = tr.stdout)
    list = output.split('\n')
    return jsonify({'ostypes':  filter(None,  list ) }) , 201 

# Lista de maquinas asociadas 
#curl http://localhost:5000/vms
#command vboxmanage list vms | cut -d ' ' -f 1 | tr -d '"'
@app.route('/vms',methods = ['GET'])
def listvms():
    vboxm = subprocess.Popen(['vboxmanage','list','vms'], stdout = subprocess.PIPE)
    tr = subprocess.Popen(['tr','-d','"'], stdin = vboxm.stdout,  stdout = subprocess.PIPE)
    output = subprocess.check_output(['cut','-d', ' ', '-f', '1'], stdin = tr.stdout)
    list = output.split('\n')
    return jsonify({'vms':  filter(None,  list ) }) , 201 

# Muestra  maquinas que se encuentran en ejecucion 
# curl http://localhost:5000/vms/running
# command vboxmanage list runningvms | cut -d ' ' -f 1 | tr -d '"'
@app.route('/vms/running',methods = ['GET'])
def runninglistvms():
    vboxm = subprocess.Popen(['vboxmanage','list','runningvms'], stdout = subprocess.PIPE)
    tr = subprocess.Popen(['tr','-d','"'], stdin = vboxm.stdout,  stdout = subprocess.PIPE)
    output = subprocess.check_output(['cut','-d', ' ', '-f', '1'], stdin = tr.stdout)
    list = output.split('\n')
    return jsonify({'running-vms': filter(None,  list ) }) , 201 

# info de una maquina virtual 
# numero de cpus
# vboxmanage showvminfo web | grep 'Number of CPUs' | cut -d ': ' -f 2
# tamano de ram 
#count network interfaces
#vboxmanage showvminfo db | grep '^NIC' | grep -v disabled | grep MAC | tr -s ' ' | wc -l

#mac de las interfaces de red
#vboxmanage showvminfo db | grep '^NIC' | grep -v disabled | grep MAC | tr -s ' ' | cut -d ':' -f 3 | cut -d ',' -f 1 | cut -d ' ' -f 2
#tipo de interfase de red
#vboxmanage showvminfo db | grep '^NIC' | grep -v disabled | grep MAC | tr -s ' ' | cut -d ':' -f 4
# numero de interfases de red
# si es nat , bridge .. etc
@app.route('/vms/info/<vmname>', methods = ['GET'])
def vminfo(vmname):
    #numero de cpus
    vboxm = subprocess.Popen(['vboxmanage','showvminfo',str(vmname)], stdout = subprocess.PIPE)
    grep = subprocess.Popen(['grep','Number of CPUs'], stdin = vboxm.stdout, stdout = subprocess.PIPE)
    tr = subprocess.Popen(['tr', '-s', ' '], stdin = grep.stdout, stdout = subprocess.PIPE)
    cpunum = subprocess.check_output(['cut','-d', ':', '-f', '2'], stdin = tr.stdout)
    #ram 
    vboxmram = subprocess.Popen(['vboxmanage','showvminfo',str(vmname)], stdout = subprocess.PIPE)
    grepram = subprocess.Popen(['grep','Memory size'], stdin = vboxmram.stdout, stdout = subprocess.PIPE)
    trram = subprocess.Popen(['tr', '-s', ' '], stdin = grepram.stdout, stdout = subprocess.PIPE)
    vramsize = subprocess.check_output(['cut','-d', ':', '-f', '2'], stdin = trram.stdout)
    #count network interfaces
    vboxmcnt= subprocess.Popen(['vboxmanage','showvminfo',str(vmname)], stdout = subprocess.PIPE)
    grepcnt = subprocess.Popen(['grep','^NIC'], stdin = vboxmcnt.stdout, stdout = subprocess.PIPE)
    grepdis = subprocess.Popen(['grep','-v', 'disabled'], stdin = grepcnt.stdout, stdout = subprocess.PIPE)
    grepmac = subprocess.Popen(['grep','MAC'], stdin = grepdis.stdout, stdout = subprocess.PIPE)
    trcnt = subprocess.Popen(['tr', '-s', ' '], stdin = grepmac.stdout, stdout = subprocess.PIPE)
    cntinet = subprocess.check_output(['wc','-l'], stdin = trcnt.stdout)
    #mac interfaces de red
    vboxmmac= subprocess.Popen(['vboxmanage','showvminfo',str(vmname)], stdout = subprocess.PIPE)
    grepni = subprocess.Popen(['grep','^NIC'], stdin = vboxmmac.stdout, stdout = subprocess.PIPE)
    grepmacs = subprocess.Popen(['grep','-v', 'disabled'], stdin = grepni.stdout, stdout = subprocess.PIPE)
    grepmacmac = subprocess.Popen(['grep','MAC'], stdin = grepmacs.stdout, stdout = subprocess.PIPE)
    trcmac = subprocess.Popen(['tr', '-s', ' '], stdin = grepmacmac.stdout, stdout = subprocess.PIPE)
    cu1 = subprocess.Popen(['cut', '-d', ':', '-f', '3'], stdin = trcmac.stdout, stdout = subprocess.PIPE)
    cu2 = subprocess.Popen(['cut', '-d', ',', '-f', '1'], stdin = cu1.stdout, stdout = subprocess.PIPE)
    cu3 = subprocess.check_output(['cut', '-d', ' ', '-f', '2'], stdin = cu2.stdout)
    listmacs = cu3.split('\n')
    #network interfaces type
    vboxmtyp= subprocess.Popen(['vboxmanage','showvminfo',str(vmname)], stdout = subprocess.PIPE)
    grepnit = subprocess.Popen(['grep','^NIC'], stdin = vboxmtyp.stdout, stdout = subprocess.PIPE)
    grepf= subprocess.Popen(['grep','-v', 'disabled'], stdin = grepnit.stdout, stdout = subprocess.PIPE)
    grepm = subprocess.Popen(['grep','MAC'], stdin = grepf.stdout, stdout = subprocess.PIPE)
    trtyp = subprocess.Popen(['tr', '-s', ' '], stdin = grepm.stdout, stdout = subprocess.PIPE)
    cuc1 = subprocess.check_output(['cut', '-d', ':', '-f', '4'], stdin = trtyp.stdout)
    listiftype =  cuc1.split('\n')
    
    merged = {'mac': filter(None,  listmacs) ,  'type':filter(None,  listiftype) }
    
    return jsonify({'cpus-number': cpunum.strip(),'name':vmname , 'ram': vramsize.strip() , 'network-interfaces-count': cntinet.strip() ,   'network-interfaces':  merged }) , 201 

#Create VM
#curl -i -H "Content-Type: application/json" -X POST -d '{"name":"Docker", "disk-size":"32738",  "cpu-number":"2" ,  "memory":"1024"   ,  "ram":"124"    }' http://localhost:5000/vms	
#curl -i -H "Content-Type: application/json" -X POST -d '{"name":"osweb", "disksize":"32738",  "cpunumber":"4" ,  "memory":"1024"   ,  "ram":"580"    }' http://localhost:5000/vms	

@app.route('/vms', methods=['POST'])
def create_vms():
    namevm= request.json['name']
    dsvm= request.json['disksize']
    cpuvm= request.json['cpunumber']
    memvm= request.json['memory']
    ramvm= request.json['ram']
    
    FNULL = open(os.devnull,  'w')
    reatevm = subprocess.call(['./utils-createvm.sh', str(namevm), str(dsvm), str(cpuvm),str(memvm), str(ramvm)],  stdout=FNULL ,  stderr=subprocess.STDOUT)
    if reatevm==1:
        msg="VM Created"
    else:
        msg="Error: VM not created "
    return jsonify({'vm-mensaje': msg }), 201

#Delete VM    
#curl -i -H "Content-Type: application/json" -X DELETE http://localhost:5000/vms/Docker	

@app.route('/vms/<vmname>', methods=['DELETE'])    
def delete_vms(vmname):
    try:
        deletevm = subprocess.check_output(['vboxmanage', 'unregistervm', '-delete', str(vmname)])
        msg="VM "+vmname+" Deleted " 
    except Exception:
        msg="Error: VM "+vmname+" Could not delete from vmlist " 
    return jsonify({'vm-mensaje': msg }), 201
    
    
if __name__ == '__main__':
        app.run(debug = True, host='0.0.0.0')
