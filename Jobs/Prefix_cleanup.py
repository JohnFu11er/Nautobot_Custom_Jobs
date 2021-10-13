from nautobot.extras.jobs import *
from nautobot.extras.models import Status
from nautobot.ipam.models import IPAddress, Prefix
import ipaddress



class PrefixCleanup(Job):

    class Meta:
        name = "Prefix Cleanup"
        description = "Creates a prefix for any IP address that does not have a prefix in the database."
        commit_default = False
    
    def run(self, data, commit):
        STATUS_ACTIVE = Status.objects.get(slug="active")
        prefixes_to_add = []
        all_nautobot_prefixes= [str(_.network) for _ in Prefix.objects.all()]
        
        
        def create_prefix(network:str):
            '''
            - Logs that a prefix does not exist
            - Creates and saves the prefix
            - Logs that the prefix was created
            '''
            self.log_failure(f"Prefix {network} not in Nautobot database")
            
            new_prefix = Prefix(
                prefix=network,
                is_pool=False,
                status= STATUS_ACTIVE
            )

            new_prefix.validated_save()
            self.log_success(f"Prefix {network} created in Nautobot database")

        
        # Loop through all IPs in Nautobot.
        # If the IPs network address is not in the list of all Nautobot
        # prefixes, append the network address to a list for later use
        for ip in IPAddress.objects.all():
            prefix = str(ipaddress.ip_network(ip, strict=False).network_address)
            if prefix not in all_nautobot_prefixes:
                prefixes_to_add.append(prefix)
        
        # If the prefix_to_add list has anything in it, then run the
        # create_prefix function for each missing prefix
        if prefixes_to_add:
            for missing_prefix in set(prefixes_to_add):
                create_prefix(missing_prefix)
        else:
            self.log_success("There are no IPs in the database that are not associated with a prefix")