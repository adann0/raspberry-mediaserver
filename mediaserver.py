#!/usr/bin/env python3

"""
Simple script Python ayant pour but de faciliter la "maintenance" du Serveur :
  - Reboot Propre
  - Arret des Services
ToDo : Si il y avait 50 services ça ferait un peu lourd une varriable par commande ?
Faire peut être un dictionnaire favorisant la recursivité d'une fonction action(a)
"""

import sys
import subprocess

arg = ["start", "stop", "restart", "reboot", "status"] #liste avec tout les arg

"""
Fonction chargée de repérer si la commande comporte une erreur
"""

def false_arg() :
  if (len(sys.argv) < 2) or (len(sys.argv) == 2 and sys.argv[1] not in arg) : 
    return(True)
  return(False)

"""
Execute une commande passé en argument et retourne le code erreur/sortie
Print sur stdout la commande si out=True, pour status()
"""

def exec(cmd, out=False) :
  print("$ " + cmd)
  p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
  output = p.communicate()[0]
  if out :
    print(output.decode("utf-8").encode("utf-8"))
  return(p.returncode)

"""
Lance les services qui ne le sont pas au démarrage du système
"""

def start() :
  deluge = "docker start deluge"
  if exec(deluge) != 0 :
    print("start: can't start deluge")

"""
Arrete tous les services
"""

def stop() :
  deluge = "docker stop deluge"
  plex = "sudo systemctl stop plexmediaserver.service"
  samba = "sudo service smbd stop"
  if exec(deluge) != 0 :
    print("stop: can't stop deluge")
  if exec(plex) != 0 :
    print("stop: can't stop plex")
  if exec(samba) != 0 :
    print("stop: can't stop samba")
  return()

"""
Restart tous les services
"""

def restart() :
  deluge = "docker restart deluge"
  plex = "sudo systemctl restart plexmediaserver.service"
  samba = "sudo service smbd restart"
  if exec(deluge) != 0 :
    print("restart: can't stop deluge")
  if exec(plex) != 0 :
    print("restart: can't stop plex")
  if exec(samba) != 0 :
    print("restart: can't stop samba")
  return()  

"""
Donne des infos sur les services
"""

def status() :
  deluge = "docker logs deluge"
  plex = "sudo systemctl status plexmediaserver.service"
  samba = "sudo service smbd status"
  if exec(deluge, out=True) != 0 :
    print("status: can't get deluge")
  if exec(plex, out=True) != 0 :
    print("status: can't get plex")
  if exec(samba, out=True) != 0 :
    print("status: can't get samba")
  return()
  
"""
Ejecte le disque dur
"""  

def eject() :
  umount = "sudo udisks --unmount /dev/sda1"
  detach = "sudo udisks --detach /dev/sda"
  if exec(umount) != 0 :
    print("eject: can't umount")
    sys.exit(2)
  if exec(detach) != 0 :
    print("eject: can't detach")
    sys.exit(3)
  return()
  
"""
Reboot
"""
  
def reboot() :
  if exec("sudo reboot") != 0 :
    print("reboot: can't reboot")
    sys.exit(10)
  return()

if __name__ == "__main__" : 
  if false_arg() :
    print("USAGE: mediaserver {" + "|".join(arg) + "}")
    sys.exit(1)
  elif sys.argv[1] == "reboot" :
    stop()
    eject()
    reboot()
  elif sys.argv[1] == "stop" :
    stop()
  elif sys.argv[1] == "start" :
    start()
  elif sys.argv[1] == "restart" :
    restart()
  elif sys.argv[1] == "status" :
    status()
