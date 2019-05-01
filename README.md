# Raspberry Pi 3b+ NFS Server

## Mount drives on Raspberry Pi
We are starting with an unformatted and unpartitioned SSD connected
to the RPi USB port.

1. Update your rig
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```
2. Raberry Pi online docs recommend installing exfat-fuse but,
   you wont need it if you are formatting fresh drives.
   ```bash
   sudo apt-get install exfat-fuse
   ```
3. find the device ```NAME```
   ```bash
   sudo lsblk -o UUID,NAME,FSTYPE,SIZE,MOUNTPOINT,LABEL,MODEL
   ```
   If it is the only hard drive connected it should be 'sda'.
   This means the device is located at ```/dev/sda```.  You can
   go check if you want.
4. It's easy to export this so we don't need to remember it.
   ```bash
   export DRIVE=/dev/sda
   ```
5. Lets Partition the drive
   ```bash
   sudo fdisk $DRIVE
   ```
6. You are now in the fdisk control space.
   * ```d``` will delete any prior partitions.
   * ```n``` creates new partitions (Defaults will produce a single
     partition spanning the entire drive).
   * ```w``` writes the changes and exits.
   * ```p``` displays the current partitions.
   * ```m``` for help/manual.
7. Time to give that new partition a filesystem.  ```1``` is added
   due to being the first partition on the drive.
   ```bash
   sudo mkfs -t vfat -I $DRIVE"1"
   ```
8. Create a mount point for the drive, generally in ```media``` or ```mnt```.
   ```bash
   export MOUNT="/mnt/SSD" && \ 
   sudo mkdir -p $MOUNT
   ```
9. Mount it. Note we mount partition1.
    ```bash
    sudo mount $DRIVE"1" $MOUNT -o umask=000
    ```
* https://thepihut.com/blogs/raspberry-pi-tutorials/17699796-formatting-and-mounting-a-usb-drive-from-a-terminal-window
* https://www.raspberrypi.org/documentation/configuration/external-storage.md


## Mount drive on reboot. Be gentle with fstab
Create an entry for the drive in ```/etc/fstab```
```bash
export UUID=$(sudo blkid $DRIVE | awk '{print substr($2,7,9)}') && \  
sudo echo "UUID=$UUID $MOUNT vfat defaults,auto,umask=000,users,rw   0      0" | sudo tee -a /etc/fstab
```
Restart after this step to verify that the fstab setting is correct.
```bash
sudo reboot
```  
If your RPi does not boot, don't worry you just need to correct it using
the section below.


## EXT4 Support for Mac OSX
If something goes wrong when editing the fstab file in the previous step,
your RPi will not boot.  We gotta correct this as easy as possible.
You could wipe the entire card and reload the raspian image, but lets
just comment out the bad fstab line instead.

* Virtual Box Ubuntu VM
* USB 3.0 Expansion Pack for Virtual Box

On Mac Machine: 
1. Unmount MMC card from Mac machine
2. Fire up ubuntu inside virtual box
3. Go to Devices>USB to enable your MMC card in Ubuntu
4. ```rootfs``` drive partition is what we want
5. find your jacked fstab file and sudo edit it.
6. Comment out the botched fstab entry

https://inderpreetsingh.com/2014/11/02/ext4-repair-on-mac-osx/

## NFS Server on Raspberry Pi
Now, the drive is partitioned, imaged, and set to mount on start.
It is time to install the NFS server and configure it.

1. Pre-reqs
   ```bash
   sudo apt-get install nfs-kernel-server portmap nfs-common
   ```
2. Make NFS folder and give lenient permissions for local network
   ```bash
   mkdir -p $MOUNT/nfs && \ 
   sudo chmod -R 777 $MOUNT/nfs
   ```
3. Add shared folder to ```/etc/exports```
   ```bash
   sudo echo -e "$MOUNT/nfs\t*(rw,sync,no_subtree_check,insecure,all_squash)" >> /etc/exports
   ```
4. Reset exports
   ```bash
   sudo exportfs -a
   ```
5. And restart nfs service
   ```bash
   sudo systemctl restart nfs-kernel-server
   ```

## Quick connect NFS Client
1. install nfs utils
   ```bash
   sudo apt install nfs-utils
   ```
2. Create local mount directory
   ```bash
   export LOCAL_MOUNT_DIR=/mnt/nfs1 && \ 
   sudo mkdir -p $LOCAL_MOUNT_DIR
3. Use the mount.nfs tool
   ```bash
   export NFS_IP=nfs1.local && \ 
   export NFS_MOUNT_DIR=/mnt/SSD/nfs && \ 
   sudo mount.nfs $NFS_IP:$NFS_MOUNT_DIR $LOCAL_MOUNT_DIR
   ```