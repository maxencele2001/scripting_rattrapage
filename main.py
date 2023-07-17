import csv
import subprocess

vboxmanage_path = r'C:\Program Files\Oracle\VirtualBox\VBoxManage.exe'
iso_ubuntu_path = r'D:\Travail\scripting\ubuntu-22.04.2-desktop-amd64.iso'
def createVirtualMachine(name, ram, cpu, disk_size, i):
    subprocess.run([vboxmanage_path, 'createvm', '--name', name, '--register'])
    subprocess.run([vboxmanage_path, 'modifyvm', name, '--memory', str(ram)])
    subprocess.run([vboxmanage_path, 'modifyvm', name, '--cpus', str(cpu)])
    subprocess.run([vboxmanage_path, 'createhd', '--filename', f'{name}/{name}.vdi', '--size', str(disk_size)])
    subprocess.run([vboxmanage_path, 'storagectl', name, '--name', 'SATA Controller', '--add', 'sata'])
    subprocess.run([vboxmanage_path, 'storageattach', name, '--storagectl', 'SATA Controller', '--port', '0', '--device', '0', '--type', 'hdd', '--medium', f'{name}/{name}.vdi'])
    subprocess.run([vboxmanage_path, 'storageattach', name, '--storagectl', 'SATA Controller', '--port', '1', '--device', '0', '--type', 'dvddrive', '--medium', iso_ubuntu_path])
    # subprocess.run([vboxmanage_path, 'modifyvm', name, '--nic1', 'intnet', '--intnet1', 'internal_network'])
    # subprocess.run([vboxmanage_path, 'modifyvm', name, '--nicproperty1', f'ip=192.168.1.{i}']) ## tenter de se connecter en ssh
    subprocess.run([vboxmanage_path, 'startvm', name, '--type', 'headless'])

def main():
    with open('exo.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        i = 1
        for row in reader:
            createVirtualMachine(row['Nom'], int(row['RAM']), int(row['CPU']), int(row['TaillDisque']), i)
            i = i + 1

def removeVirtualMachines():
    result = subprocess.run([vboxmanage_path, 'list', 'vms'], capture_output=True, text=True)
    output = result.stdout
    for line in output.splitlines():
        vm_name = line.split(' ')[0].strip('\"') # c entoure de guillemet et ca fait buguer
        if (getHealthOne(vm_name) == 'running'):
            subprocess.run([vboxmanage_path, 'controlvm', vm_name, 'poweroff']) # faut eteindre avant sinon c lock
        subprocess.run([vboxmanage_path, 'unregistervm', '--delete-all', vm_name])

def getHealthAll():
    result = subprocess.run([vboxmanage_path, 'list', 'vms'], capture_output=True, text=True)
    output = result.stdout
    for line in output.splitlines():
        vm_name = line.split(' ')[0].strip('\"')
        vm_status = getHealthOne(vm_name)
        print(f"{vm_name}: {vm_status}")


def getHealthOne(vm_name):
    vm_status_result = subprocess.run([vboxmanage_path, 'showvminfo', '--machinereadable', vm_name], capture_output=True, text=True)
    vm_status_output = vm_status_result.stdout
    for status_line in vm_status_output.splitlines():
        if status_line.startswith('VMState='):
            return status_line.split('=')[1].strip('\"')
    return ''


def executeCowsay():
    result = subprocess.run([vboxmanage_path, 'list', 'vms'], capture_output=True, text=True)
    output = result.stdout
    for line in output.splitlines():
        vm_name = line.split(' ')[0].strip('\"')
        result = subprocess.run([vboxmanage_path, 'guestcontrol', vm_name,  "run"," cowsay 'Bon Week end'"], stdout=subprocess.PIPE, text=True)
        print(result)
        return
        print(f"{row['Nom']}: {output}")


# main()
# getHealthAll()
# removeVirtualMachines()
executeCowsay()



