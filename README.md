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
    $ sudo reboot

smb://ip

# Plex

    $ cd && 
    wget https://downloads.plex.tv/plex-media-server-new/1.15.3.876-ad6e39743/debian/plexmediaserver_1.15.3.876-ad6e39743_armhf.deb &&
    sudo dpkg -i plexmediaserver_1.15.3.876-ad6e39743_armhf.deb &&
    rm plexmediaserver_1.15.3.876-ad6e39743_armhf.deb

# Deluge

    $ sudo apt-get install deluge &&
    sudo service deluged start &&
    sudo service deluge-web start

