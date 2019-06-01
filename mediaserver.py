#!/usr/bin/env python3

"""
Simple script Python ayant pour but de faciliter la "maintenance" du Serveur :
  - Reboot Propre
  - Arret des Services
"""

import sys
import subprocess

arg = ["reboot", "stop"] #liste avec tout les arg

"""
Fonction chargée de repérer si la commande comporte une erreur
"""

def false_arg() :
  if (len(sys.argv) < 2) or (len(sys.argv) == 2 and sys.argv[1] not in arg) : 
    return(False)
  return(True)

"""
Execute une commande passé en argument et retourne le code erreur/sortie
"""

def exec(cmd) :
  p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
  output = p.communicate()[0]
  return(p.returncode)

"""
Arrete tous les services
"""

def stop() :
  deluge = "docker stop deluge"
  plex = "sudo systemctl stop plexmediaserver.service"
  samba = "sudo service smbd stop"
  if exec(deluge) != 0 :
    print("stop: can't stop deluge")
    sys.exit(4)
  if exec(plex) != 0 :
    print("stop: can't stop plex")
    sys.exit(5)
  if exec(samba) != 0 :
    print("stop: can't stop samba")
    sys.exit(6)
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
  elif sys.argv[2] == "stop" :
    stop()
