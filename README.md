# SMART-FRIDGE - _Kreative Köpfe_ 

__SMART-FRIDGE__ macht jeden Kühlschrank smart. __SMART-FRIDGE__ unterstützt deine
Nachhaltigkeit, indem es die Lebensmittel in deinem Kühlschrank verwaltet und einen
Alarm auslöst, wenn das MHD (Mindest-Haltbarkeits-Datum) erreicht wird. 
Mit einer Kamera können Artikel einfach erfasst werden, dazu ist ein EAN-Code Scanner
in der App integriert, dieser ermöglicht das Erfassen der Artikel. Daten für bereits
bekannte Lebensmittel werden automatisch bei Einbuchen von Artikel ausgefüllt.
___
## Technisches
___
### SSH Verbindung
### Server Seite (Raspberry PI)
#### Step 1 SSH Server aktivieren

Auf dem Raspberry PI ein Terminal öffnen und die Konfiguration öffnen:

```sh
sudo raspi-config
```
!!! Das Standard Passwort für den User __PI__ ist __raspberry__

Aus dem Menü den Menüpunkt __Interface Options__ wählen und in dem Untermenü
__SSH Enable/disable__ wähle, im folgenden Dialog die Auswahl mit __Ja__ bestätigen.
Anschliessend die Konfiguration mit __Finish__ schliessen.  

Nun ist erst die Clientseite für die Verbindung einzurichten.


### Client Seite (Windows, macOS, ...)
#### Step 1 __Schlüsselpaar erzeugen__

Mit ssh-keygen aus der Kommandozeile ein neues Schlüsselpaar erstellen.
```bash
ssh-keygen -t rsa -b 4096
```
Es werden im Pfad __\<USER-HOME\>/.ssh/__ zwei Dateien angelegt: 
> id_rsa  
> id_rsa.pub. 

Die erste Datei ist der private Schlüssel, dieser bleibt auf dem Client, von dem 
aus wir uns auf den SSH-Server verbinden wollen. 
Dieser Schlüssel ist private und sollte nicht in falsche Hände geraten!

Die zweite Datei ist der öffentliche Schlüssel und muss nun im zweiten 
Schritt auf den Server kopiert werden. 
Der Server erwartet den öffentlichen Schlüssel eines Benutzers in der 
Datei ~/.ssh/authorized_keys.

#### Step 2 Public Key auf den Raspberry PI kopieren

Mit SCP ist der Public Key auf den Raspberry Pi zu kopieren.

```sh
scp </USER-HOME>/.ssh/id_rsa.pub pi@SERVER:/home/pi/.ssh/
````

#### Step 3 

SSH Config Datei anpasssen. Die Datei </USER-HOME>/.ssh/config
öffnen, wenn sie nicht existiert eine neue Datei anlegen.
In die config Datei die folgenden Einträge einfügen.

```sh
Host raspi
    HostName <RASPBERRY IP>
    IdentityFile ~/.ssh/id_rsa
    User pi
    StrictHostKeyChecking accept-new
    ServerAliveInterval 1200
    ServerAliveCountMax 5
```

### Server Seite (Raspberry PI)

Der kopierte Public Key wird mit der folgenden Anweisung in die 
Datei __authorized_keys__ kopiert. 

```sh
cat id_rsa.pub >> /home/pi/.ssh/authorized_keys
```
Die Datei __id_rsa.pub__ kann jetzt gelöscht werden. 

### Verbindungs Test

Im Terminal den folgenden Befehl eingeben:

```sh
ssh raspi
```

Wenn alles funktioniert erscheint jetzt die Remoteverbindung 
zum Raspberry PI.

```sh
pi@raspberrypi:~ $
```

