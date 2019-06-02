# raspberry-mediaserver

# Post Install

https://gist.github.com/adann0/9eff3e831e514988579337dc11492570

# Locales

https://www.skyminds.net/linux-cannot-set-default-locale/

# Disk Format & Mount

https://gist.github.com/adann0/4aad4526145044aceb40d8caf26524d1#disk-format

# Three

    $ mkdir -p /mnt/usb/mediaserver/Deposit/.backup &&
    mkdir -p /mnt/usb/mediaserver/Deposit/.downloading &&
    mkdir -p /mnt/usb/mediaserver/Films &&
    mkdir -p /mnt/usb/mediaserver/Series

# Samba

## Installation

    $ sudo apt-get install samba samba-common-bin -y
    $ sudo smbpasswd -a <user>
    $ sudo cp /etc/samba/smb.conf /etc/samba/smb.conf.bak &&
    sudo nano /etc/samba/smb.conf

On modifie :

    #   wins support = no

En ca :

    wins support = yes

Tout en bas du fichier on ajoute :

    [Media]
    comment = Shared
    path = "/mnt/usb/mediaserver"
    create mask = 0710
    directory mask = 0710
    read only = yes
    browseable = yes
    public = yes
    guest ok = no
    write list = <user>

On sauvegarde puis :

    $ sudo reboot

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
    $ sudo udisks --unmount /dev/sda1
    $ sudo udisks --detach /dev/sda
    $ sudo reboot

smb://ip

# Plex

    $ cd && 
    wget https://downloads.plex.tv/plex-media-server-new/1.15.3.876-ad6e39743/debian/plexmediaserver_1.15.3.876-ad6e39743_armhf.deb &&
    sudo dpkg -i plexmediaserver_1.15.3.876-ad6e39743_armhf.deb &&
    rm plexmediaserver_1.15.3.876-ad6e39743_armhf.deb

http://ip:32400/web/index.html

# Deluge

    $ sudo apt-get install deluge deluged deluge-console deluge-web
    $ deluged 
    $ deluge-console
    > config -s allow_remote True 
    > exit
    $ sudo pkill deluged 
    $ deluged
    
    $ sudo nano /etc/rc.local

Avant “exit 0” on met :

    # Start Deluge on boot:
    sudo -u <user> /usr/bin/python /usr/bin/deluged
    sudo -u <user> /usr/bin/python /usr/bin/deluge-web

Reboot une dernière fois :

    $ sudo udisks --unmount /dev/sda1
    $ sudo udisks --detach /dev/sda
    $ sudo reboot
    
# Darkstat

    $ sudo apt install darkstat
    $ sudo nano /etc/darkstat/init.cfg
    
    START_DARKSTAT=yes
    BINDIP="-b x.x.x.x"
    
    $ sudo service darkstat restart
    
http://ip:666
    
# Bonus

## Increase SWAP

    $ sudo nano /etc/dphys-swapfile
    
    CONF_SWAPFILE=2048
    
    $ sudo /etc/init.d/dphys-swapfile restart

## Fuites de mémoire avec Plex

Embetant d'avoir un service qui utilise beaucoup de mémoire alors que personne ne l'utilise :

    $ sudo nano /lib/systemd/system/plexmediaserver.service

    MemoryMax=350M

    $ sudo systemctl daemon-reload
    $ sudo systemctl restart plexmediaserver

A ajuster en fonction des besoins mais aucune perte de performance au niveau de Plex sur un Raspberry avec ce setting pour le moment.
