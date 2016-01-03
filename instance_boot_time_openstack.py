import time
from keystoneclient.auth.identity import v2
from keystoneclient import session
from keystoneclient.v2_0 import client as clientKeystone
from novaclient import client as clientNova

# Variables
AUTH_URL = 'http://devconsole.nubomedia.eu:5000/v2.0'
myuserid = "admin"
mypassword = "mypassword"
mytenantname = "admin"
nova_api_version = 2
key_name = "your-key-name"

kvm_image = "54b3df5b-ce74-4f7c-b2eb-6cb1d97c605a"
kvm_instance_name = "KVM_tests_"+str(time.time())
kvm_flavor = "f4881c75-78b0-4766-bf12-6c09bf862f90"

docker_image = "83bd37e5-2b1e-49ef-8898-1b1d3d9af0c2"
docker_instance_name = "Docker_tests_"+str(time.time())
docker_flavor = "ea071529-6bed-4299-a463-7e182d5b119f"

def check_boot_time ( instance_name ) :
   # Check the time needed to boot a instance
   status = "PENDING"
   start_time = time.time();
   instances = nova.servers.list()
   for instance in instances:
      if instance.name == instance_name :
         instanceId=instance.id
         while status != "ACTIVE" : 
            run_time = time.time()
            status = instance.status
            print instance.status
   nova.servers.delete(instanceId)
   return run_time-start_time

# Authentication with Keystone
auth = v2.Password(auth_url=AUTH_URL,
                   username=myuserid,
                   password=mypassword,
                   tenant_name=mytenantname)

sess = session.Session(auth=auth)
keystone = clientKeystone.Client(session=sess)
print sess

# Authentication with Nova using the previously created session on Keystone
nova = clientNova.Client(nova_api_version,session=sess)

# prints a list with all users
tenants = keystone.tenants.list()
print tenants

# prints a list with all flavors
flavors = nova.flavors.list()
print flavors

# print the list of all running instances
servers = nova.servers.list()
print servers

# prints the list of all keypairs
keypairs = nova.keypairs.list()
print keypairs

# prints the list with all images
images = nova.images.list()
print images

# Start a kvm instance
nova.servers.create(kvm_instance_name,
                    kvm_image,
                    kvm_flavor,
                    meta=None,
                    files=None,
                    reservation_id=None,
                    min_count=None,
                    max_count=None,
                    security_groups=None,
                    userdata=None,
                    key_name=key_name,
                    availability_zone=None,
                    block_device_mapping=None,
                    block_device_mapping_v2=None,
                    nics=None,
                    scheduler_hints=None,
                    config_drive=None,
                    disk_config=None)

# Check the boot time of one instance with KVM hypervisor
print "KVM spawning time:" , check_boot_time(kvm_instance_name)

# Porneste o instanta de tip Docker
nova.servers.create(docker_instance_name,
                    docker_image,
                    docker_flavor,
                    meta=None,
                    files=None,
                    reservation_id=None,
                    min_count=None,
                    max_count=None,
                    security_groups=None,
                    userdata=None,
                    key_name=key_name,
                    availability_zone=None,
                    block_device_mapping=None,
                    block_device_mapping_v2=None,
                    nics=None,
                    scheduler_hints=None,
                    config_drive=None,
                    disk_config=None)

# Check the boot time of one instance with docker hypervisor
print "Docker spawning time:" , check_boot_time(docker_instance_name)