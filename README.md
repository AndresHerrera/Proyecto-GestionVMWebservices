# Proyecto-GestionVMWebservices
Flask web service for handling virtual machines (VirtualBox )

git clone https://github.com/AndresHerrera/Proyecto-GestionVMWebservices.git

## Video (asciinema)

https://asciinema.org/a/RqNmrWZLqCgRKCx25mPD39Q8K

## Install

$python install.sh

## Run Web Service

$python prj-vmwebservice.py

## Usage  ( Complete command list ) :

$ curl -i http://localhost:5000/

## Extended list

<table style='width:100%'><tr><th>METHOD</th><th>URL</th><th>JSON Response</th></tr><tr><td colspan=3 align=center><b>GENERAL</b></td></tr><tr><td>GET</td><td>curl http://localhost:5000/</td><td>Avaliable services</td></tr><tr><td>GET</td><td>curl http://localhost:5000/vms/ostypes</td><td>List OS types supported for Virtual Box</td></tr><tr><td>GET</td><td>curl http://localhost:5000/vms</td><td>List VMS</td></tr><tr><td>GET</td><td>curl http://localhost:5000/vms/running</td><td>Running VMS</td></tr><tr><td>GET</td><td>curl http://localhost:5000/vms/info/vmname</td><td>Info for vmname VM</td></tr><tr><td>POST</td><td>curl -i -H "Content-Type: application/json" -X POST -d '{"name":"osweb", "disksize":"32738",  "cpunumber":"4" ,  "memory":"1024"   ,  "ram":"580"}' http://localhost:5000/vms	</td><td>Create a VM.</td></tr><tr><td>DELETE</td><td>curl -i -H "Content-Type: application/json" -X DELETE http://localhost:5000/vms/vmname</td><td>Delete a VM (vmname).</td></tr></table>


