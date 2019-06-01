# raspberry-mediaserver

# Post Install

https://gist.github.com/adann0/9eff3e831e514988579337dc11492570

# Disk Format & Mount

https://gist.github.com/adann0/4aad4526145044aceb40d8caf26524d1#disk-format

# Samba

## Installation

    $ sudo apt-get install samba samba-common-bin -y
    $ sudo smbpasswd -a <user>
    $ sudo cp /etc/samba/smb.conf /etc/samba/smb.conf.bak
    $ sudo nano /etc/samba/smb.conf

On modifie :

    #   wins support = no

En ca :

    wins support = yes

Tout en bas du fichier on ajoute :

    [Media]
    comment = Read Only Media Server Folder Share from RPi
    path = “/mnt/usb/mediaserver”
    create mask = 0710
    directory mask = 0710
    read only = yes
    browseable = yes
    public = yes
    guest ok = no

On sauvegarde puis :

    $ sudo reboot

Maintenant on peut accéder à Samba depuis le réseau local, uniquement en lecture, via :
smb://<ladresseiplocaleduraspberry>

## SSL avec Samba

    $ cd /etc/samba/tls
    $ sudo openssl req -newkey rsa:2048 -keyout myKey.pem -nodes -x509 -days 365 -out myCert.pem

    $ sudo chmod 600 myKey.pem
    $ sudo nano /etc/samba/smb.conf

On ajoute ça à la fin de notre config serveur :

    tls enabled  = yes
    tls keyfile  = tls/myKey.pem
    tls certfile = tls/myCert.pem
    tls cafile   =

Puis :

    $ sudo service smbd restart
    $ sudo reboot

smb://ip

# Plex

    $ sudo apt-get update && sudo apt-get upgrade -y
    $ wget https://downloads.plex.tv/plex-media-server-new/1.15.3.876-ad6e39743/debian/plexmediaserver_1.15.3.876-ad6e39743_armhf.deb
    $ sudo dpkg -i plexmediaserver_1.15.3.876-ad6e39743_armhf.deb

http://ip:32400/web

# Docker

(Potentiellement sur un second Raspberry, pour installer des apps supplémentaires comme Deluge ou autre le mieux est je pense de passer par Docker.)

    $ curl -sSL get.docker.com | sh
    $ sudo usermod -aG docker <user>
    $ sudo reboot

# NFS

(Si on a un deuxième Raspberry on devrait vouloir acceder aux données du disque dur connecté au premier Raspberry)

    node01$ sudo apt-get install nfs-common nfs-server -y
    node01$ sudo nano sudo nano /etc/exports
    
    /mnt/usb/mediaserver 192.168.0.x(rw,sync)

    node01$ sudo exportfs
    node01$ sudo udisks --unmount /dev/sda1
    node01$ sudo umount -l /data/brick1 ## if the disk is busy
    node01$ sudo udisks --detach /dev/sda
    node01$ sudo reboot
    
    node02$ sudo apt-get install nfs-common -y
    node02$ sudo mkdir -p /mnt/usb/mediaserver
    node02$ sudo chown -R <user>:<user> /mnt/usb/mediaserver
    node02$ sudo mount 192.168.x.x:/mnt/usb/mediaserver /mnt/usb/mediaserver
    
    node02$ sudo nano /etc/fstab
    
    192.168.x.x:/mnt/usb/mediaserver   /mnt/usb/mediaserver   nfs    rw  0  0

Si le automount ne fonctionne pas cette ligne résoud surement le problème :

    192.168.x.x:/mnt/usb/mediaserver   /mnt/usb/mediaserver   nfs    rw,noauto,x-systemd.automount  0  0

Alternative : GlusterFS (attention a la lenteur sur les petits fichiers en USB) https://gist.github.com/adann0/4aad4526145044aceb40d8caf26524d1#glusterfs

# HTTPS

    https://github.com/adann0/docker-nginx-letsencrypt
    https://github.com/adann0/openldap-armv7#openldap-certificates

# Docker Compose

    $ git clone https://github.com/adann0/raspberry-mediaserver.git &&
    cd raspberry-mediaserver
    
Il faut remplacer chaque valeur de example.com par le nom de domaine, mettre le mot de passe pour la base de donnée LDAP.

    $ mv nginx.conf /etc/nginx
    $ docker-compose up -d
