from nautobot.extras.jobs import *
from nautobot.ipam.models import Interface
from nautobot.dcim.models import Cable

# Developed by: John Fuller
# Developed on: 10/27/2021

# Created expressly for proof of concept purposes.  Use at your own risk.

class BasicCable(Job):

    class Meta:
        name = "Basic Cable Script"
        description = "Proof of concept for connecting cables via a script"
        commit_default = False
    
    def run(self, data, commit):
        ''' Creates a new Cable based on the parameters:
            - 'termination_a' : this is the interface ogject for
                end of your cable
            - 'termination_b' : this is the interface object for
                the opposite end of the cable
            - 'status' : is defaulted here to the 'Cable' classes
                'STATUS_CONNECTED' variable
        '''
        
        # There is an assumption that the two interface objects below
        # already exist in your database.  If they do not, this script
        # will fail:
        new_cable = Cable(
            termination_a= Interface.objects.get(
                device__name="Core_Router_1",
                name="GigabitEthernet2"
                ),

            termination_b= Interface.objects.get(
                device__name="Distro_Router_1",
                name="GigabitEthernet1"
                ),
            
            status= Cable.STATUS_CONNECTED
        )

        # Use the internal 'validated_save()' to verify
        # that the newly created cable has the minimum
        # values set for this database object type
        new_cable.validated_save()
