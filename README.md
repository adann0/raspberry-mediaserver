# raspberry-mediaserver

# Post Install

https://gist.github.com/adann0/9eff3e831e514988579337dc11492570

# Disk Format & Mount

https://gist.github.com/adann0/4aad4526145044aceb40d8caf26524d1#disk-format

# Samba

## Installation

    $ sudo apt-get install samba samba-common-bin -y
    $ sudo smbpasswd -a nqqb
    $ sudo cp /etc/samba/smb.conf /etc/samba/smb.conf.bak
    $ sudo nano /etc/samba/smb.conf

On modifie :

    #   wins support = no

En ca :

    wins support = yes

Tout en bas du fichier on ajoute :

    [Media Server]
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



